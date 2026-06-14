from __future__ import annotations

from pathlib import Path


def default_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_bdi_repo() -> Path:
    return default_repo_root().parent / "pydantic-ai-bdi"


def display_path(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)
