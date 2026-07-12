from __future__ import annotations

import argparse
import shlex
import sys
from pathlib import Path
from typing import Sequence, TextIO

from .answers import path_safe_model_name
from .harnesses import (
    SUPPORTED_HARNESSES,
    find_missing_cli_binaries,
    render_missing_cli_binaries,
    select_harnesses,
)
from .litellm import check_litellm_proxy, render_litellm_unavailable
from .paths import default_repo_root, display_path
from .progress import (
    BenchmarkRunCancelledError,
    TextualUnavailableError,
    preview_textual_progress,
    run_matrix_with_textual_progress,
)
from .results_importer import ImportResult, import_run_records
from .runs import (
    MatrixRunResult,
    RunPlan,
    build_run_plans,
    default_run_id,
    run_matrix,
)
from .tasks import SelectionError, Task, discover_tasks, select_tasks


DEFAULT_TIMEOUT_SECONDS = 600
DEFAULT_RESULTS_DB = "results.sqlite"
DEFAULT_MODEL = "openai/gpt-5.4"


def render_list(tasks: Sequence[Task]) -> str:
    lines = ["SBench benchmark orchestrator", "", "Supported harnesses:"]
    lines.extend(f"- {harness}" for harness in SUPPORTED_HARNESSES)
    lines.extend(["", "Discovered tasks:"])
    if tasks:
        lines.extend(f"- {task.id} [{task.track}]" for task in tasks)
    else:
        lines.append("- none")
    return "\n".join(lines) + "\n"


def render_dry_run(
    repo_root: Path,
    *,
    plans: Sequence[RunPlan],
    model: str,
    timeout_seconds: int,
) -> str:
    lines = [
        "SBench dry run",
        f"repo_root: {repo_root}",
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
                f"  track: {plan.track}",
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


def render_import_result(repo_root: Path, database_path: Path, result: ImportResult) -> str:
    lines = [
        "SBench results import complete",
        f"database: {display_path(database_path, repo_root)}",
        f"executions_imported: {result.execution_count}",
        f"warnings: {result.warning_count}",
    ]
    return "\n".join(lines) + "\n"


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def should_show_progress(output: TextIO) -> bool:
    return bool(getattr(output, "isatty", lambda: False)())


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
    parser.add_argument(
        "--model",
        help=f"Model name to record and pass to harness command planning. Defaults to {DEFAULT_MODEL}.",
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
        "--capture-json-events",
        action="store_true",
        help="Write stdout to events.jsonl when it is valid JSON Lines output.",
    )
    parser.add_argument(
        "--results-db",
        type=Path,
        default=Path(DEFAULT_RESULTS_DB),
        help=f"SQLite database path for --import-results. Defaults to {DEFAULT_RESULTS_DB} under repo root.",
    )

    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--list", action="store_true", help="List discovered tasks and supported harnesses.")
    mode.add_argument("--dry-run", action="store_true", help="Print the planned matrix without running agents.")
    mode.add_argument("--run", action="store_true", help="Run the selected harness/task matrix.")
    mode.add_argument(
        "--import-results",
        action="store_true",
        help="Import existing orchestrator run artifacts into SQLite.",
    )
    mode.add_argument(
        "--progress-preview",
        action="store_true",
        help="Preview the Textual progress UI with simulated task updates.",
    )
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

    if args.progress_preview:
        try:
            preview_textual_progress()
        except TextualUnavailableError as error:
            error_output.write(f"{error}\n")
            return 2
        return 0

    if args.import_results:
        database_path = args.results_db
        if not database_path.is_absolute():
            database_path = repo_root / database_path
        import_result = import_run_records(repo_root, database_path)
        output.write(render_import_result(repo_root, database_path, import_result))
        return 0

    model = args.model or DEFAULT_MODEL

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
        model=model,
        timeout_seconds=args.timeout,
        run_id=actual_run_id,
    )
    if args.dry_run:
        output.write(
            render_dry_run(
                repo_root,
                plans=plans,
                model=model,
                timeout_seconds=args.timeout,
            )
        )
        return 0

    missing = find_missing_cli_binaries(selected_harnesses)
    if missing:
        error_output.write(render_missing_cli_binaries(missing))
        return 2

    if "bdi" in selected_harnesses:
        litellm_health = check_litellm_proxy(repo_root=repo_root)
        if not litellm_health.available:
            error_output.write(render_litellm_unavailable(litellm_health))
            return 2

    if should_show_progress(output):
        try:
            matrix_result = run_matrix_with_textual_progress(
                repo_root,
                plans,
                model=model,
                timeout_seconds=args.timeout,
                stop_on_first_failure=args.stop_on_first_failure,
                run_id=actual_run_id,
                capture_json_events=args.capture_json_events,
            )
        except TextualUnavailableError as error:
            error_output.write(f"{error}\n")
            matrix_result = run_matrix(
                repo_root,
                plans,
                model=model,
                timeout_seconds=args.timeout,
                stop_on_first_failure=args.stop_on_first_failure,
                run_id=actual_run_id,
                capture_json_events=args.capture_json_events,
            )
        except BenchmarkRunCancelledError as error:
            error_output.write(f"{error}\n")
            return 130
    else:
        matrix_result = run_matrix(
            repo_root,
            plans,
            model=model,
            timeout_seconds=args.timeout,
            stop_on_first_failure=args.stop_on_first_failure,
            run_id=actual_run_id,
            capture_json_events=args.capture_json_events,
        )
    output.write(render_matrix_result(repo_root, matrix_result))
    return 0 if all(result.status == "success" for result in matrix_result.results) else 1
