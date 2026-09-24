from __future__ import annotations

import json
import re
import subprocess
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

from .answers import (
    AnswerArchivePlan,
    AnswerArchiveResult,
    archive_answer_files,
    clean_answer_dir,
    path_safe_model_name,
    plan_answer_archive,
)
from .harnesses import build_harness_invocation
from .paths import display_path
from .scratch import ScratchCleanupResult, capture_task_snapshot, restore_task_snapshot
from .tasks import Task


ANSI_COLOR_RE = re.compile(r"\x1b\[[0-9;:]*m")


@dataclass(frozen=True)
class RunPlan:
    task_id: str
    track: str
    harness: str
    task_dir: Path
    working_dir: Path
    archive_dir: Path
    command: tuple[str, ...]
    settings: dict[str, object] = field(default_factory=dict)


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


@dataclass(frozen=True)
class RunProgress:
    total: int
    completed: int
    succeeded: int
    failed_or_incomplete: int
    current_plan: RunPlan | None
    last_result: RunExecutionResult | None


def execute_run_plan(
    repo_root: Path,
    plan: RunPlan,
    *,
    model: str,
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
    task = Task(id=plan.task_id, path=plan.task_dir, track=plan.track)
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

    if plan.harness == "bdi":
        stdout_text = ANSI_COLOR_RE.sub("", stdout_text)
        stderr_text = ANSI_COLOR_RE.sub("", stderr_text)

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
        track=plan.track,
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
    timeout_seconds: float,
    stop_on_first_failure: bool = False,
    run_id: str | None = None,
    capture_json_events: bool = False,
    progress_callback: Callable[[RunProgress], None] | None = None,
) -> MatrixRunResult:
    actual_run_id = run_id or default_run_id()
    run_root = repo_root / "runs" / actual_run_id
    run_root.mkdir(parents=True, exist_ok=True)
    results: list[RunExecutionResult] = []
    stopped_after_failure = False
    succeeded = 0
    failed_or_incomplete = 0
    last_result: RunExecutionResult | None = None

    def report_progress(current_plan: RunPlan | None) -> None:
        if progress_callback is None:
            return
        progress_callback(
            RunProgress(
                total=len(plans),
                completed=len(results),
                succeeded=succeeded,
                failed_or_incomplete=failed_or_incomplete,
                current_plan=current_plan,
                last_result=last_result,
            )
        )

    for plan in plans:
        report_progress(plan)
        result = execute_run_plan(
            repo_root,
            plan,
            model=model,
            timeout_seconds=timeout_seconds,
            run_root=run_root,
            capture_json_events=capture_json_events,
        )
        results.append(result)
        last_result = result
        if result.status == "success":
            succeeded += 1
        else:
            failed_or_incomplete += 1
        if stop_on_first_failure and result.status != "success":
            stopped_after_failure = True
            break
    report_progress(None)

    summary_path = run_root / "summary.json"
    matrix_result = MatrixRunResult(
        run_id=actual_run_id,
        run_root=run_root,
        summary_path=summary_path,
        results=tuple(results),
        stopped_after_failure=stopped_after_failure,
    )
    _write_json(
        summary_path,
        matrix_result_to_dict(
            matrix_result,
            repo_root,
            plans,
            model,
            timeout_seconds,
            stop_on_first_failure,
        ),
    )
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
    timeout_seconds: float,
    stop_on_first_failure: bool,
) -> dict[str, object]:
    status_counts: dict[str, int] = {}
    track_counts: dict[str, int] = {}
    for result in matrix_result.results:
        status_counts[result.status] = status_counts.get(result.status, 0) + 1
        track_counts[result.track] = track_counts.get(result.track, 0) + 1

    planned_track_counts: dict[str, int] = {}
    for plan in planned:
        planned_track_counts[plan.track] = planned_track_counts.get(plan.track, 0) + 1

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
        "track_counts": track_counts,
        "planned_track_counts": planned_track_counts,
    }


def build_run_plans(
    repo_root: Path,
    *,
    tasks: Sequence[Task],
    harnesses: Sequence[str],
    model: str,
    timeout_seconds: int,
    run_id: str | None = None,
) -> list[RunPlan]:
    plans: list[RunPlan] = []

    for task in tasks:
        for harness in harnesses:
            archive_plan = plan_answer_archive(repo_root, task, model=model, harness=harness)
            invocation = build_harness_invocation(
                harness,
                model=model,
                timeout_seconds=timeout_seconds,
                task_dir=task.path,
                repo_root=repo_root,
            )
            plans.append(
                RunPlan(
                    task_id=task.id,
                    track=task.track,
                    harness=harness,
                    task_dir=task.path,
                    working_dir=invocation.working_dir or task.path,
                    archive_dir=archive_plan.archive_dir,
                    command=invocation.command,
                    settings=invocation.settings,
                )
            )

    return plans
