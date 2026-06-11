from __future__ import annotations

import argparse
import json
import re
import shutil
import shlex
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Sequence, TextIO


SUPPORTED_HARNESSES = ("bdi", "codex", "opencode")
CLI_BINARY_BY_HARNESS = {"codex": "codex", "opencode": "opencode"}
DEFAULT_TRACK = "smoke"
DEFAULT_TIMEOUT_SECONDS = 600
STANDARD_TASK_PROMPT = (
    "You are working in the provided folder. Read task.md and the other local "
    "files, then complete the requested work. Create the requested `answer/` "
    "folder and put all requested deliverables there."
)


class SelectionError(ValueError):
    """Raised when a requested task or harness is not available."""


class ArchiveError(RuntimeError):
    """Raised when answer archiving would overwrite existing results."""


@dataclass(frozen=True)
class Task:
    id: str
    path: Path


@dataclass(frozen=True)
class AnswerArchivePlan:
    task_id: str
    harness: str
    display_model: str
    model_path: str
    run_id: str
    source_dir: Path
    archive_dir: Path


@dataclass(frozen=True)
class AnswerArchiveResult:
    status: str
    archive_dir: Path
    archived_paths: tuple[Path, ...]
    incomplete_reason: str | None = None


@dataclass(frozen=True)
class RunPlan:
    task_id: str
    harness: str
    task_dir: Path
    working_dir: Path
    archive_dir: Path
    command: tuple[str, ...]
    settings: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class HarnessInvocation:
    command: tuple[str, ...]
    settings: dict[str, object]
    working_dir: Path | None = None


@dataclass(frozen=True)
class TaskSnapshot:
    root: Path
    files: dict[str, bytes]
    directories: frozenset[str]


@dataclass(frozen=True)
class ScratchCleanupResult:
    policy: str
    record_dir: Path
    created_paths: tuple[str, ...]
    modified_paths: tuple[str, ...]
    deleted_paths: tuple[str, ...]


@dataclass(frozen=True)
class RunExecutionResult:
    task_id: str
    harness: str
    model: str
    model_path: str
    track: str
    status: str
    command: tuple[str, ...]
    settings: dict[str, object]
    working_dir: Path
    start_time: str
    end_time: str
    elapsed_seconds: float
    timeout_seconds: float
    timed_out: bool
    exit_code: int | None
    archive_dir: Path
    archived_paths: tuple[Path, ...]
    incomplete_reason: str | None
    stdout_log_path: Path
    stderr_log_path: Path
    json_event_log_path: Path | None
    metadata_path: Path
    scratch_cleanup: ScratchCleanupResult


@dataclass(frozen=True)
class MatrixRunResult:
    run_id: str
    run_root: Path
    summary_path: Path
    results: tuple[RunExecutionResult, ...]
    stopped_after_failure: bool


def default_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_bdi_repo() -> Path:
    return default_repo_root().parent / "pydantic-ai-bdi"


def discover_tasks(repo_root: Path) -> list[Task]:
    tasks_root = repo_root / "tasks"
    if not tasks_root.is_dir():
        return []

    tasks: list[Task] = []
    for child in sorted(tasks_root.iterdir(), key=lambda path: path.name):
        if child.is_dir() and (child / "task.md").is_file():
            tasks.append(Task(id=child.name, path=child))
    return tasks


def split_requested_values(values: Sequence[str] | None) -> list[str]:
    requested: list[str] = []
    for value in values or ():
        for item in value.split(","):
            stripped = item.strip()
            if stripped:
                requested.append(stripped)
    return requested


def select_harnesses(requested_values: Sequence[str] | None) -> list[str]:
    requested = split_requested_values(requested_values)
    if not requested:
        return list(SUPPORTED_HARNESSES)

    unsupported = sorted(set(requested) - set(SUPPORTED_HARNESSES))
    if unsupported:
        supported = ", ".join(SUPPORTED_HARNESSES)
        raise SelectionError(
            f"unsupported harness: {', '.join(unsupported)}; supported harnesses: {supported}"
        )

    selected: list[str] = []
    for harness in requested:
        if harness not in selected:
            selected.append(harness)
    return selected


def select_tasks(discovered_tasks: Sequence[Task], requested_values: Sequence[str] | None) -> list[Task]:
    requested = split_requested_values(requested_values)
    if not requested:
        return list(discovered_tasks)

    task_by_id = {task.id: task for task in discovered_tasks}
    missing = [task_id for task_id in requested if task_id not in task_by_id]
    if missing:
        available = ", ".join(sorted(task_by_id)) or "none"
        raise SelectionError(
            f"unknown task: {', '.join(missing)}; discovered tasks: {available}"
        )

    selected: list[Task] = []
    for task_id in requested:
        task = task_by_id[task_id]
        if task not in selected:
            selected.append(task)
    return selected


def path_safe_model_name(model: str) -> str:
    safe = model.strip().replace("/", "__")
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", safe)
    safe = safe.strip(".-")
    return safe or "model"


def next_run_id(repo_root: Path, task_id: str, model_path: str, harness: str) -> str:
    archive_parent = repo_root / "answers" / task_id / model_path / harness
    max_run = 0
    if archive_parent.is_dir():
        for child in archive_parent.iterdir():
            if not child.is_dir():
                continue
            match = re.fullmatch(r"r(\d+)", child.name)
            if match:
                max_run = max(max_run, int(match.group(1)))
    return f"r{max_run + 1}"


def plan_answer_archive(repo_root: Path, task: Task, *, model: str, harness: str) -> AnswerArchivePlan:
    model_path = path_safe_model_name(model)
    run_id = next_run_id(repo_root, task.id, model_path, harness)
    return AnswerArchivePlan(
        task_id=task.id,
        harness=harness,
        display_model=model,
        model_path=model_path,
        run_id=run_id,
        source_dir=task.path / "answer",
        archive_dir=repo_root / "answers" / task.id / model_path / harness / run_id,
    )


def clean_answer_dir(task: Task) -> Path:
    answer_dir = task.path / "answer"
    if answer_dir.is_dir():
        shutil.rmtree(answer_dir)
    elif answer_dir.exists():
        answer_dir.unlink()
    answer_dir.mkdir(parents=True, exist_ok=False)
    return answer_dir


def archive_answer_files(plan: AnswerArchivePlan, *, overwrite: bool = False) -> AnswerArchiveResult:
    if not plan.source_dir.is_dir():
        return AnswerArchiveResult(
            status="incomplete",
            archive_dir=plan.archive_dir,
            archived_paths=(),
            incomplete_reason="missing answer directory",
        )

    source_entries = sorted(plan.source_dir.iterdir(), key=lambda path: path.name)
    if not source_entries:
        return AnswerArchiveResult(
            status="incomplete",
            archive_dir=plan.archive_dir,
            archived_paths=(),
            incomplete_reason="empty answer directory",
        )

    if plan.archive_dir.exists():
        if not overwrite:
            raise ArchiveError(f"answer archive already exists: {plan.archive_dir}")
        if plan.archive_dir.is_dir():
            shutil.rmtree(plan.archive_dir)
        else:
            plan.archive_dir.unlink()

    plan.archive_dir.mkdir(parents=True, exist_ok=False)
    archived_paths: list[Path] = []

    for source_entry in source_entries:
        destination = plan.archive_dir / source_entry.name
        if source_entry.is_dir():
            shutil.copytree(source_entry, destination)
            archived_paths.extend(path for path in sorted(destination.rglob("*")) if path.is_file())
        else:
            shutil.copy2(source_entry, destination)
            archived_paths.append(destination)

    return AnswerArchiveResult(
        status="success",
        archive_dir=plan.archive_dir,
        archived_paths=tuple(archived_paths),
    )


def capture_task_snapshot(task: Task) -> TaskSnapshot:
    files: dict[str, bytes] = {}
    directories: set[str] = set()

    for path in sorted(task.path.rglob("*")):
        relative = path.relative_to(task.path)
        if _is_answer_relative_path(relative):
            continue
        relative_text = relative.as_posix()
        if path.is_dir():
            directories.add(relative_text)
        elif path.is_file():
            files[relative_text] = path.read_bytes()

    return TaskSnapshot(root=task.path, files=files, directories=frozenset(directories))


def restore_task_snapshot(snapshot: TaskSnapshot, scratch_record_dir: Path) -> ScratchCleanupResult:
    scratch_record_dir.mkdir(parents=True, exist_ok=True)
    current_files: dict[str, Path] = {}

    for path in sorted(snapshot.root.rglob("*")):
        relative = path.relative_to(snapshot.root)
        if _is_answer_relative_path(relative) or not path.is_file():
            continue
        current_files[relative.as_posix()] = path

    created_paths: list[str] = []
    modified_paths: list[str] = []
    deleted_paths: list[str] = []

    for relative_text, path in sorted(current_files.items()):
        if relative_text not in snapshot.files:
            _copy_scratch_file(path, scratch_record_dir / "created" / relative_text)
            path.unlink()
            created_paths.append(relative_text)
            continue

        original_bytes = snapshot.files[relative_text]
        current_bytes = path.read_bytes()
        if current_bytes != original_bytes:
            _copy_scratch_file(path, scratch_record_dir / "modified" / relative_text)
            path.write_bytes(original_bytes)
            modified_paths.append(relative_text)

    for relative_text, original_bytes in sorted(snapshot.files.items()):
        destination = snapshot.root / relative_text
        if destination.exists():
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(original_bytes)
        deleted_paths.append(relative_text)

    _remove_new_empty_directories(snapshot)

    return ScratchCleanupResult(
        policy="restore_task_files_outside_answer_after_each_run",
        record_dir=scratch_record_dir,
        created_paths=tuple(created_paths),
        modified_paths=tuple(modified_paths),
        deleted_paths=tuple(deleted_paths),
    )


def _is_answer_relative_path(relative: Path) -> bool:
    return bool(relative.parts) and relative.parts[0] == "answer"


def _copy_scratch_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def _remove_new_empty_directories(snapshot: TaskSnapshot) -> None:
    for path in sorted(snapshot.root.rglob("*"), reverse=True):
        if not path.is_dir():
            continue
        relative = path.relative_to(snapshot.root)
        if _is_answer_relative_path(relative):
            continue
        if relative.as_posix() in snapshot.directories:
            continue
        try:
            path.rmdir()
        except OSError:
            pass


def execute_run_plan(
    repo_root: Path,
    plan: RunPlan,
    *,
    model: str,
    track: str,
    timeout_seconds: float,
    run_root: Path,
    capture_json_events: bool = False,
) -> RunExecutionResult:
    record_dir = run_root / "entries" / plan.task_id / plan.harness / plan.archive_dir.name
    record_dir.mkdir(parents=True, exist_ok=True)
    stdout_log_path = record_dir / "stdout.log"
    stderr_log_path = record_dir / "stderr.log"
    metadata_path = record_dir / "metadata.json"
    json_event_log_path = record_dir / "events.jsonl"
    scratch_record_dir = record_dir / "scratch"
    task = Task(id=plan.task_id, path=plan.task_dir)
    model_path = path_safe_model_name(model)

    clean_answer_dir(task)
    snapshot = capture_task_snapshot(task)

    start = datetime.now(timezone.utc)
    start_monotonic = time.monotonic()
    stdout_text = ""
    stderr_text = ""
    exit_code: int | None = None
    timed_out = False

    try:
        completed = subprocess.run(
            plan.command,
            cwd=plan.working_dir,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
        stdout_text = completed.stdout
        stderr_text = completed.stderr
        exit_code = completed.returncode
    except subprocess.TimeoutExpired as error:
        timed_out = True
        stdout_text = _normalize_process_output(error.stdout)
        stderr_text = _normalize_process_output(error.stderr)
    except FileNotFoundError as error:
        stderr_text = f"missing executable: {error.filename}\n"

    end = datetime.now(timezone.utc)
    elapsed_seconds = round(time.monotonic() - start_monotonic, 3)
    stdout_log_path.write_text(stdout_text, encoding="utf-8")
    stderr_log_path.write_text(stderr_text, encoding="utf-8")

    actual_json_event_log_path: Path | None = None
    if capture_json_events and _looks_like_json_events(stdout_text):
        json_event_log_path.write_text(stdout_text, encoding="utf-8")
        actual_json_event_log_path = json_event_log_path

    archive_plan = AnswerArchivePlan(
        task_id=plan.task_id,
        harness=plan.harness,
        display_model=model,
        model_path=model_path,
        run_id=plan.archive_dir.name,
        source_dir=plan.task_dir / "answer",
        archive_dir=plan.archive_dir,
    )
    archive_result = archive_answer_files(archive_plan)
    scratch_cleanup = restore_task_snapshot(snapshot, scratch_record_dir)
    clean_answer_dir(task)

    status = _run_status(
        timed_out=timed_out,
        exit_code=exit_code,
        archive_result=archive_result,
    )

    result = RunExecutionResult(
        task_id=plan.task_id,
        harness=plan.harness,
        model=model,
        model_path=model_path,
        track=track,
        status=status,
        command=plan.command,
        settings=plan.settings,
        working_dir=plan.working_dir,
        start_time=_format_timestamp(start),
        end_time=_format_timestamp(end),
        elapsed_seconds=elapsed_seconds,
        timeout_seconds=timeout_seconds,
        timed_out=timed_out,
        exit_code=exit_code,
        archive_dir=plan.archive_dir,
        archived_paths=archive_result.archived_paths,
        incomplete_reason=archive_result.incomplete_reason,
        stdout_log_path=stdout_log_path,
        stderr_log_path=stderr_log_path,
        json_event_log_path=actual_json_event_log_path,
        metadata_path=metadata_path,
        scratch_cleanup=scratch_cleanup,
    )
    _write_json(metadata_path, run_result_to_dict(result, repo_root))
    return result


def run_matrix(
    repo_root: Path,
    plans: Sequence[RunPlan],
    *,
    model: str,
    track: str,
    timeout_seconds: float,
    stop_on_first_failure: bool = False,
    run_id: str | None = None,
    capture_json_events: bool = False,
) -> MatrixRunResult:
    actual_run_id = run_id or default_run_id()
    run_root = repo_root / "runs" / actual_run_id
    run_root.mkdir(parents=True, exist_ok=True)
    results: list[RunExecutionResult] = []
    stopped_after_failure = False

    for plan in plans:
        result = execute_run_plan(
            repo_root,
            plan,
            model=model,
            track=track,
            timeout_seconds=timeout_seconds,
            run_root=run_root,
            capture_json_events=capture_json_events,
        )
        results.append(result)
        if stop_on_first_failure and result.status != "success":
            stopped_after_failure = True
            break

    summary_path = run_root / "summary.json"
    matrix_result = MatrixRunResult(
        run_id=actual_run_id,
        run_root=run_root,
        summary_path=summary_path,
        results=tuple(results),
        stopped_after_failure=stopped_after_failure,
    )
    _write_json(summary_path, matrix_result_to_dict(matrix_result, repo_root, plans, model, track, timeout_seconds, stop_on_first_failure))
    return matrix_result


def default_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _normalize_process_output(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def _looks_like_json_events(output: str) -> bool:
    lines = [line for line in output.splitlines() if line.strip()]
    if not lines:
        return False
    for line in lines:
        try:
            json.loads(line)
        except json.JSONDecodeError:
            return False
    return True


def _run_status(*, timed_out: bool, exit_code: int | None, archive_result: AnswerArchiveResult) -> str:
    if timed_out:
        return "timed_out"
    if exit_code not in (0, None):
        return "failed"
    if exit_code is None:
        return "failed"
    if archive_result.status != "success":
        return "incomplete"
    return "success"


def _format_timestamp(value: datetime) -> str:
    return value.isoformat(timespec="seconds").replace("+00:00", "Z")


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_result_to_dict(result: RunExecutionResult, repo_root: Path) -> dict[str, object]:
    return {
        "archive_path": display_path(result.archive_dir, repo_root),
        "archived_paths": [display_path(path, repo_root) for path in result.archived_paths],
        "command": list(result.command),
        "elapsed_seconds": result.elapsed_seconds,
        "end_time": result.end_time,
        "exit_code": result.exit_code,
        "harness": result.harness,
        "incomplete_reason": result.incomplete_reason,
        "json_event_log_path": display_path(result.json_event_log_path, repo_root)
        if result.json_event_log_path
        else None,
        "metadata_path": display_path(result.metadata_path, repo_root),
        "model": result.model,
        "model_path": result.model_path,
        "scratch_cleanup": {
            "created_paths": list(result.scratch_cleanup.created_paths),
            "deleted_paths": list(result.scratch_cleanup.deleted_paths),
            "modified_paths": list(result.scratch_cleanup.modified_paths),
            "policy": result.scratch_cleanup.policy,
            "record_dir": display_path(result.scratch_cleanup.record_dir, repo_root),
        },
        "settings": result.settings,
        "start_time": result.start_time,
        "status": result.status,
        "stderr_log_path": display_path(result.stderr_log_path, repo_root),
        "stdout_log_path": display_path(result.stdout_log_path, repo_root),
        "task_id": result.task_id,
        "timed_out": result.timed_out,
        "timeout_seconds": result.timeout_seconds,
        "track": result.track,
        "working_dir": display_path(result.working_dir, repo_root),
    }


def matrix_result_to_dict(
    matrix_result: MatrixRunResult,
    repo_root: Path,
    planned: Sequence[RunPlan],
    model: str,
    track: str,
    timeout_seconds: float,
    stop_on_first_failure: bool,
) -> dict[str, object]:
    status_counts: dict[str, int] = {}
    for result in matrix_result.results:
        status_counts[result.status] = status_counts.get(result.status, 0) + 1

    return {
        "model": model,
        "model_path": path_safe_model_name(model),
        "results": [run_result_to_dict(result, repo_root) for result in matrix_result.results],
        "run_id": matrix_result.run_id,
        "run_root": display_path(matrix_result.run_root, repo_root),
        "status_counts": status_counts,
        "stop_on_first_failure": stop_on_first_failure,
        "stopped_after_failure": matrix_result.stopped_after_failure,
        "summary_path": display_path(matrix_result.summary_path, repo_root),
        "timeout_seconds": timeout_seconds,
        "total_attempted": len(matrix_result.results),
        "total_planned": len(planned),
        "track": track,
    }


def build_command_shape(
    harness: str,
    *,
    model: str,
    track: str,
    timeout_seconds: int,
    task_dir: Path,
    repo_root: Path,
    bdi_repo: Path | None = None,
) -> tuple[str, ...]:
    return build_harness_invocation(
        harness,
        model=model,
        track=track,
        timeout_seconds=timeout_seconds,
        task_dir=task_dir,
        repo_root=repo_root,
        bdi_repo=bdi_repo,
    ).command


def build_harness_invocation(
    harness: str,
    *,
    model: str,
    track: str,
    timeout_seconds: int | float,
    task_dir: Path,
    repo_root: Path,
    bdi_repo: Path | None = None,
    bdi_output_dir: Path | None = None,
) -> HarnessInvocation:
    task_dir_arg = display_path(task_dir, repo_root)

    if harness == "codex":
        return HarnessInvocation(
            command=(
                "codex",
                "exec",
                "--model",
                model,
                "--cd",
                task_dir_arg,
                "--sandbox",
                "workspace-write",
                "--config",
                'approval_policy="never"',
                "--skip-git-repo-check",
                "--ephemeral",
                "--json",
                STANDARD_TASK_PROMPT,
            ),
            settings={
                "approval_policy": "never",
                "binary": "codex",
                "json_events": True,
                "sandbox": "workspace-write",
                "task_directory_scope": task_dir_arg,
            },
        )

    if harness == "opencode":
        return HarnessInvocation(
            command=(
                "opencode",
                "run",
                "--model",
                model,
                "--dir",
                task_dir_arg,
                "--format",
                "json",
                "--dangerously-skip-permissions",
                STANDARD_TASK_PROMPT,
            ),
            settings={
                "auto_approve_permissions": True,
                "binary": "opencode",
                "format": "json",
                "task_directory_scope": task_dir_arg,
                "writable_scope": "task_directory_only",
            },
        )

    if harness == "bdi":
        actual_bdi_repo = (bdi_repo or default_bdi_repo()).resolve()
        toy_runner = actual_bdi_repo / "toy.py"
        output_dir = bdi_output_dir or repo_root / "runs" / "<run-id>" / "bdi" / task_dir.name
        return HarnessInvocation(
            command=(
                sys.executable,
                str(toy_runner),
                "--sbench-root",
                str(repo_root),
                "--tasks",
                task_dir.name,
                "--model",
                model,
                "--output-dir",
                str(output_dir),
                "--command-timeout-seconds",
                str(int(timeout_seconds)),
                "--quiet",
            ),
            settings={
                "bdi_repo": str(actual_bdi_repo),
                "command_timeout_seconds": int(timeout_seconds),
                "delegation": "pydantic-ai-bdi toy runner",
                "output_dir": str(output_dir),
                "task_directory_scope": task_dir_arg,
                "toy_runner": str(toy_runner),
            },
            working_dir=actual_bdi_repo,
        )

    raise SelectionError(f"unsupported harness: {harness}")


def find_missing_cli_binaries(
    harnesses: Sequence[str],
    *,
    which: Callable[[str], str | None] | None = None,
) -> dict[str, str]:
    resolver = which or shutil.which
    missing: dict[str, str] = {}
    for harness in harnesses:
        binary = CLI_BINARY_BY_HARNESS.get(harness)
        if binary and resolver(binary) is None:
            missing[harness] = binary
    return missing


def render_missing_cli_binaries(missing: dict[str, str]) -> str:
    lines = ["Missing required CLI binaries:"]
    for harness, binary in sorted(missing.items()):
        lines.append(f"- {harness}: {binary}")
    return "\n".join(lines) + "\n"


def find_missing_repository_paths(harnesses: Sequence[str], *, bdi_repo: Path) -> dict[str, str]:
    if "bdi" not in harnesses:
        return {}
    toy_runner = bdi_repo / "toy.py"
    if bdi_repo.is_dir() and toy_runner.is_file():
        return {}
    return {"bdi": str(bdi_repo)}


def render_missing_repository_paths(missing: dict[str, str]) -> str:
    lines = ["Missing required repository paths:"]
    for harness, path in sorted(missing.items()):
        lines.append(f"- {harness}: {path}")
    return "\n".join(lines) + "\n"


def build_run_plans(
    repo_root: Path,
    *,
    tasks: Sequence[Task],
    harnesses: Sequence[str],
    model: str,
    track: str,
    timeout_seconds: int,
    bdi_repo: Path | None = None,
    run_id: str | None = None,
) -> list[RunPlan]:
    plans: list[RunPlan] = []

    for task in tasks:
        for harness in harnesses:
            archive_plan = plan_answer_archive(repo_root, task, model=model, harness=harness)
            bdi_output_dir = None
            if harness == "bdi":
                bdi_output_dir = repo_root / "runs" / (run_id or "<run-id>") / "bdi" / task.id
            invocation = build_harness_invocation(
                harness,
                model=model,
                track=track,
                timeout_seconds=timeout_seconds,
                task_dir=task.path,
                repo_root=repo_root,
                bdi_repo=bdi_repo,
                bdi_output_dir=bdi_output_dir,
            )
            plans.append(
                RunPlan(
                    task_id=task.id,
                    harness=harness,
                    task_dir=task.path,
                    working_dir=invocation.working_dir or task.path,
                    archive_dir=archive_plan.archive_dir,
                    command=invocation.command,
                    settings=invocation.settings,
                )
            )

    return plans


def display_path(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def render_list(tasks: Sequence[Task]) -> str:
    lines = ["SBench benchmark orchestrator", "", "Supported harnesses:"]
    lines.extend(f"- {harness}" for harness in SUPPORTED_HARNESSES)
    lines.extend(["", "Discovered tasks:"])
    if tasks:
        lines.extend(f"- {task.id}" for task in tasks)
    else:
        lines.append("- none")
    return "\n".join(lines) + "\n"


def render_dry_run(
    repo_root: Path,
    *,
    plans: Sequence[RunPlan],
    model: str,
    track: str,
    timeout_seconds: int,
) -> str:
    lines = [
        "SBench dry run",
        f"repo_root: {repo_root}",
        f"track: {track}",
        f"model: {model}",
        f"model_path: {path_safe_model_name(model)}",
        f"timeout_seconds: {timeout_seconds}",
        f"matrix_entries: {len(plans)}",
        "",
    ]

    for plan in plans:
        lines.extend(
            [
                f"- task: {plan.task_id}",
                f"  harness: {plan.harness}",
                f"  task_dir: {display_path(plan.task_dir, repo_root)}",
                f"  archive: {display_path(plan.archive_dir, repo_root)}",
                f"  command: {shlex.join(plan.command)}",
            ]
        )

    return "\n".join(lines) + "\n"


def render_matrix_result(repo_root: Path, matrix_result: MatrixRunResult) -> str:
    failed_count = sum(1 for result in matrix_result.results if result.status != "success")
    lines = [
        "SBench run complete",
        f"run_id: {matrix_result.run_id}",
        f"summary: {display_path(matrix_result.summary_path, repo_root)}",
        f"attempted: {len(matrix_result.results)}",
        f"failed_or_incomplete: {failed_count}",
    ]
    return "\n".join(lines) + "\n"


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m sbench",
        description="Run or inspect SBench benchmark harness/task matrices.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=default_repo_root(),
        help="SBench repository root. Defaults to the current package root.",
    )
    parser.add_argument(
        "--task",
        action="append",
        help="Task ID to include. May be repeated or comma-separated. Defaults to all discovered tasks.",
    )
    parser.add_argument(
        "--harness",
        action="append",
        help="Harness to include: bdi, codex, or opencode. May be repeated or comma-separated. Defaults to all harnesses.",
    )
    parser.add_argument("--model", help="Model name to record and pass to harness command planning.")
    parser.add_argument(
        "--track",
        default=DEFAULT_TRACK,
        help=f"Benchmark track label to record. Defaults to {DEFAULT_TRACK}.",
    )
    parser.add_argument(
        "--timeout",
        type=positive_int,
        default=DEFAULT_TIMEOUT_SECONDS,
        metavar="SECONDS",
        help=f"Per-task timeout in seconds. Defaults to {DEFAULT_TIMEOUT_SECONDS}.",
    )
    parser.add_argument(
        "--stop-on-first-failure",
        action="store_true",
        help="Stop the batch after the first failed, timed-out, or incomplete run.",
    )
    parser.add_argument("--run-id", help="Optional run record ID. Defaults to a UTC timestamp.")
    parser.add_argument(
        "--bdi-repo",
        type=Path,
        default=default_bdi_repo(),
        help="Path to the pydantic-ai-bdi repository for BDI harness runs.",
    )
    parser.add_argument(
        "--capture-json-events",
        action="store_true",
        help="Write stdout to events.jsonl when it is valid JSON Lines output.",
    )

    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--list", action="store_true", help="List discovered tasks and supported harnesses.")
    mode.add_argument("--dry-run", action="store_true", help="Print the planned matrix without running agents.")
    mode.add_argument("--run", action="store_true", help="Run the selected harness/task matrix.")
    return parser


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    return build_parser().parse_args(argv)


def main(
    argv: Sequence[str] | None = None,
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    output = stdout or sys.stdout
    error_output = stderr or sys.stderr
    repo_root = args.repo_root.resolve()
    discovered_tasks = discover_tasks(repo_root)

    if args.list:
        output.write(render_list(discovered_tasks))
        return 0

    if (args.dry_run or args.run) and not args.model:
        parser.error("--model is required with --dry-run or --run")

    try:
        selected_tasks = select_tasks(discovered_tasks, args.task)
        selected_harnesses = select_harnesses(args.harness)
    except SelectionError as error:
        parser.error(str(error))

    actual_run_id = args.run_id or (default_run_id() if args.run else None)
    plans = build_run_plans(
        repo_root,
        tasks=selected_tasks,
        harnesses=selected_harnesses,
        model=args.model,
        track=args.track,
        timeout_seconds=args.timeout,
        bdi_repo=args.bdi_repo.resolve(),
        run_id=actual_run_id,
    )
    if args.dry_run:
        output.write(
            render_dry_run(
                repo_root,
                plans=plans,
                model=args.model,
                track=args.track,
                timeout_seconds=args.timeout,
            )
        )
        return 0

    missing_repositories = find_missing_repository_paths(
        selected_harnesses,
        bdi_repo=args.bdi_repo.resolve(),
    )
    if missing_repositories:
        error_output.write(render_missing_repository_paths(missing_repositories))
        return 2

    missing = find_missing_cli_binaries(selected_harnesses)
    if missing:
        error_output.write(render_missing_cli_binaries(missing))
        return 2

    matrix_result = run_matrix(
        repo_root,
        plans,
        model=args.model,
        track=args.track,
        timeout_seconds=args.timeout,
        stop_on_first_failure=args.stop_on_first_failure,
        run_id=actual_run_id,
        capture_json_events=args.capture_json_events,
    )
    output.write(render_matrix_result(repo_root, matrix_result))
    return 0 if all(result.status == "success" for result in matrix_result.results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
