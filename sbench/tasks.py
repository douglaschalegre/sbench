from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


TASK_TRACK_BY_ID = {
    "vendor_selection": "smoke",
    "travel_reimbursement_audit": "smoke",
    "incident_staffing_plan": "smoke",
    "clinic_rollout_plan": "long_context",
    "community_workshop_replan": "replanning",
    "grant_closeout_recovery": "recovery",
    "shelter_restock_scope": "distractor_goal",
}
UNREGISTERED_TRACK = "unregistered"


class SelectionError(ValueError):
    """Raised when a requested task or harness is not available."""


@dataclass(frozen=True)
class Task:
    id: str
    path: Path
    track: str


def discover_tasks(repo_root: Path) -> list[Task]:
    tasks_root = repo_root / "tasks"
    if not tasks_root.is_dir():
        return []

    tasks: list[Task] = []
    for child in sorted(tasks_root.iterdir(), key=lambda path: path.name):
        if child.is_dir() and (child / "task.md").is_file():
            tasks.append(Task(id=child.name, path=child, track=task_track(child.name)))
    return tasks


def task_track(task_id: str) -> str:
    return TASK_TRACK_BY_ID.get(task_id, UNREGISTERED_TRACK)


def split_requested_values(values: Sequence[str] | None) -> list[str]:
    requested: list[str] = []
    for value in values or ():
        for item in value.split(","):
            stripped = item.strip()
            if stripped:
                requested.append(stripped)
    return requested


def select_tasks(
    discovered_tasks: Sequence[Task], requested_values: Sequence[str] | None
) -> list[Task]:
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
