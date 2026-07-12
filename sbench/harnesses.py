from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from .paths import display_path
from .tasks import SelectionError, split_requested_values


SUPPORTED_HARNESSES = ("bdi", "codex", "opencode")
CLI_BINARY_BY_HARNESS = {"bdi": "uv", "codex": "codex", "opencode": "opencode"}
DEFAULT_REASONING_EFFORT = "medium"
STANDARD_TASK_PROMPT = (
    "You are working in the provided folder. Read task.md and the other local "
    "files, then complete the requested work. Create the requested `answer/` "
    "folder and put all requested deliverables there."
)


@dataclass(frozen=True)
class HarnessInvocation:
    command: tuple[str, ...]
    settings: dict[str, object]
    working_dir: Path | None = None


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


def command_model_name(harness: str, model: str) -> str:
    if harness == "bdi":
        for prefix in ("openai/", "openai-codex/"):
            if model.startswith(prefix):
                return f"chatgpt/{model.removeprefix(prefix)}"
    if harness == "codex":
        for prefix in ("openai/", "openai-codex/"):
            if model.startswith(prefix):
                return model.removeprefix(prefix)
    return model


def build_command_shape(
    harness: str,
    *,
    model: str,
    timeout_seconds: int,
    task_dir: Path,
    repo_root: Path,
) -> tuple[str, ...]:
    return build_harness_invocation(
        harness,
        model=model,
        timeout_seconds=timeout_seconds,
        task_dir=task_dir,
        repo_root=repo_root,
    ).command


def build_harness_invocation(
    harness: str,
    *,
    model: str,
    timeout_seconds: int | float,
    task_dir: Path,
    repo_root: Path,
) -> HarnessInvocation:
    task_dir_arg = display_path(task_dir, repo_root)
    command_model = command_model_name(harness, model)

    if harness == "codex":
        return HarnessInvocation(
            command=(
                "codex",
                "exec",
                "-m",
                command_model,
                "--cd",
                task_dir_arg,
                "--sandbox",
                "workspace-write",
                "--config",
                'approval_policy="never"',
                "--config",
                f'model_reasoning_effort="{DEFAULT_REASONING_EFFORT}"',
                "--skip-git-repo-check",
                "--ephemeral",
                "--json",
                STANDARD_TASK_PROMPT,
            ),
            settings={
                "approval_policy": "never",
                "binary": "codex",
                "command_model": command_model,
                "json_events": True,
                "reasoning_effort": DEFAULT_REASONING_EFFORT,
                "sandbox": "workspace-write",
                "task_directory_scope": task_dir_arg,
            },
            working_dir=repo_root,
        )

    if harness == "opencode":
        return HarnessInvocation(
            command=(
                "opencode",
                "run",
                "-m",
                command_model,
                "--variant",
                DEFAULT_REASONING_EFFORT,
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
                "command_model": command_model,
                "format": "json",
                "reasoning_effort": DEFAULT_REASONING_EFFORT,
                "task_directory_scope": task_dir_arg,
                "writable_scope": "task_directory_only",
            },
            working_dir=repo_root,
        )

    if harness == "bdi":
        return HarnessInvocation(
            command=(
                "uv",
                "run",
                "sbench-bdi",
                "--sbench-root",
                str(repo_root),
                "--tasks",
                task_dir.name,
                "--model",
                command_model,
                "--command-timeout-seconds",
                str(int(timeout_seconds)),
                "--quiet",
            ),
            settings={
                "binary": "uv",
                "command_model": command_model,
                "command_timeout_seconds": int(timeout_seconds),
                "delegation": "SBench BDI runner",
                "reasoning_effort": DEFAULT_REASONING_EFFORT,
                "runner": "sbench-bdi",
                "task_directory_scope": task_dir_arg,
            },
            working_dir=repo_root,
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
