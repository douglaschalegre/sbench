from __future__ import annotations

from pathlib import Path


def default_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def display_path(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)
