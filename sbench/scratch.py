from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from .tasks import Task


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
