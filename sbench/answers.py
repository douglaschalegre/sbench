from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from .tasks import Task


class ArchiveError(RuntimeError):
    """Raised when answer archiving would overwrite existing results."""


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


def path_safe_model_name(model: str) -> str:
    safe = model.strip().replace("/", "__")
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", safe)
    safe = safe.strip(".-")
    return safe or "model"


def next_run_id(repo_root: Path, task_id: str, model_path: str, harness: str) -> str:
    archive_parent = repo_root / "answers" / task_id / model_path / harness
    max_run = 0
    empty_runs: list[int] = []
    if archive_parent.is_dir():
        for child in archive_parent.iterdir():
            if not child.is_dir():
                continue
            match = re.fullmatch(r"r(\d+)", child.name)
            if match:
                run_number = int(match.group(1))
                if _contains_files(child):
                    max_run = max(max_run, run_number)
                elif run_number > 0:
                    empty_runs.append(run_number)
    if empty_runs:
        return f"r{min(empty_runs)}"
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
    if not source_entries or not _contains_files(plan.source_dir):
        return AnswerArchiveResult(
            status="incomplete",
            archive_dir=plan.archive_dir,
            archived_paths=(),
            incomplete_reason="empty answer directory",
        )

    if plan.archive_dir.exists():
        if not overwrite and (
            not plan.archive_dir.is_dir() or _contains_files(plan.archive_dir)
        ):
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


def _contains_files(directory: Path) -> bool:
    return any(path.is_file() for path in directory.rglob("*"))
