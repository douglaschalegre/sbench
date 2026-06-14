from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from threading import Thread
from time import monotonic, sleep
from typing import Sequence

from .runs import MatrixRunResult, RunPlan, RunProgress, run_matrix


class TextualUnavailableError(RuntimeError):
    """Raised when the interactive progress UI cannot be loaded."""


class BenchmarkRunCancelledError(RuntimeError):
    """Raised when the interactive progress UI cancels a benchmark run."""


@dataclass(frozen=True)
class _ProgressDisplay:
    total: int
    completed: int
    succeeded: int
    failed_or_incomplete: int
    current_task: str | None
    last_task: str | None
    last_status: str | None


def run_matrix_with_textual_progress(
    repo_root: Path,
    plans: Sequence[RunPlan],
    *,
    model: str,
    timeout_seconds: float,
    stop_on_first_failure: bool = False,
    run_id: str | None = None,
    capture_json_events: bool = False,
) -> MatrixRunResult:
    planned = tuple(plans)

    def run_benchmark(update: Callable[[_ProgressDisplay], None]) -> MatrixRunResult:
        return run_matrix(
            repo_root,
            planned,
            model=model,
            timeout_seconds=timeout_seconds,
            stop_on_first_failure=stop_on_first_failure,
            run_id=run_id,
            capture_json_events=capture_json_events,
            progress_callback=lambda progress: update(_progress_from_run(progress)),
        )

    result = _run_progress_app(
        title="SBench Benchmark Progress",
        initial_progress=_ProgressDisplay(
            total=len(planned),
            completed=0,
            succeeded=0,
            failed_or_incomplete=0,
            current_task=_plan_label(planned[0] if planned else None),
            last_task=None,
            last_status=None,
        ),
        worker=run_benchmark,
        require_result=True,
    )
    if not isinstance(result, MatrixRunResult):
        raise RuntimeError("benchmark run did not produce a result")
    return result


def preview_textual_progress() -> None:
    preview_tasks = (
        ("vendor_selection", "codex", "success"),
        ("travel_reimbursement_audit", "opencode", "failed"),
        ("clinic_rollout_plan", "bdi", "success"),
        ("grant_closeout_recovery", "codex", "incomplete"),
    )

    def run_preview(update: Callable[[_ProgressDisplay], None]) -> None:
        succeeded = 0
        failed_or_incomplete = 0
        total = len(preview_tasks)
        for completed, (task_id, harness, status) in enumerate(preview_tasks, start=1):
            sleep(1.2)
            if status == "success":
                succeeded += 1
            else:
                failed_or_incomplete += 1

            next_task = preview_tasks[completed] if completed < total else None
            update(
                _ProgressDisplay(
                    total=total,
                    completed=completed,
                    succeeded=succeeded,
                    failed_or_incomplete=failed_or_incomplete,
                    current_task=f"{next_task[0]} {next_task[1]}" if next_task else None,
                    last_task=f"{task_id} {harness}",
                    last_status=status,
                )
            )
        sleep(2)

    _run_progress_app(
        title="SBench Progress Preview",
        initial_progress=_ProgressDisplay(
            total=len(preview_tasks),
            completed=0,
            succeeded=0,
            failed_or_incomplete=0,
            current_task=f"{preview_tasks[0][0]} {preview_tasks[0][1]}",
            last_task=None,
            last_status=None,
        ),
        worker=run_preview,
        require_result=False,
    )


def _run_progress_app(
    *,
    title: str,
    initial_progress: _ProgressDisplay,
    worker: Callable[[Callable[[_ProgressDisplay], None]], object],
    require_result: bool,
) -> object:
    try:
        from rich.markup import escape
        from textual.app import App, ComposeResult
        from textual.containers import Horizontal, Vertical
        from textual.widgets import Label, ProgressBar, Static
    except ImportError as error:
        raise TextualUnavailableError(
            "Textual is required for the interactive progress UI. Use `uv run sbench ...`, "
            "activate the project virtualenv, or install Textual into the Python interpreter "
            "running this command."
        ) from error

    result: object = None
    run_error: BaseException | None = None
    cancelled_result = "cancelled"
    border_colors = (
        "#f97316",
        "#fb923c",
        "#fdba74",
        "#fb923c",
        "#f97316",
        "#ea580c",
    )

    class BenchmarkProgressApp(App):
        CSS = """
        Screen {
            align: center middle;
        }

        #panel {
            width: 80%;
            max-width: 100;
            height: auto;
            border: round $accent;
            padding: 1 2;
        }

        #title {
            text-style: bold;
            margin-bottom: 1;
        }

        #progress-row {
            height: auto;
            margin-bottom: 1;
        }

        #progress {
            height: auto;
            width: 1fr;
        }

        #elapsed {
            height: auto;
            width: auto;
            margin-left: 2;
        }
        """

        def compose(self) -> ComposeResult:
            with Vertical(id="panel"):
                yield Static(title, id="title")
                with Horizontal(id="progress-row"):
                    yield ProgressBar(
                        total=max(initial_progress.total, 1),
                        show_eta=False,
                        id="progress",
                    )
                    yield Label("Elapsed: 0:00", id="elapsed")
                yield Label("Success: 0", id="success")
                yield Label("Failed_or_incomplete: 0", id="failed")
                yield Label("Last executed task: -", id="last")
                yield Label("Current task: -", id="current")

        def action_quit(self) -> None:
            self.exit(cancelled_result)

        def on_mount(self) -> None:
            self._started_at = monotonic()
            self._border_frame = 0
            self.set_interval(0.3, self._animate_border)
            self.set_interval(1, self._render_elapsed)
            self._animate_border()
            self._render_elapsed()
            self._render_progress(initial_progress)
            Thread(target=self._run_worker, name="sbench-progress", daemon=True).start()

        def _animate_border(self) -> None:
            color = border_colors[self._border_frame % len(border_colors)]
            self.query_one("#panel", Vertical).styles.border = ("round", color)
            self._border_frame += 1

        def _render_elapsed(self) -> None:
            self.query_one("#elapsed", Label).update(
                f"Elapsed: {_format_elapsed(monotonic() - self._started_at)}"
            )

        def _run_worker(self) -> None:
            nonlocal result, run_error
            try:
                result = worker(self._queue_progress_update)
            except BaseException as error:
                run_error = error
            finally:
                self.call_from_thread(self.exit)

        def _queue_progress_update(self, progress: _ProgressDisplay) -> None:
            self.call_from_thread(self._render_progress, progress)

        def _render_progress(self, progress: _ProgressDisplay) -> None:
            progress_bar = self.query_one("#progress", ProgressBar)
            progress_bar.update(
                total=max(progress.total, 1), progress=progress.completed
            )
            self.query_one("#success", Label).update(f"Success: {progress.succeeded}")
            self.query_one("#failed", Label).update(
                f"Failed_or_incomplete: {progress.failed_or_incomplete}"
            )

            if progress.last_task is None:
                self.query_one("#last", Label).update("Last executed task: -")
            else:
                color = "green" if progress.last_status == "success" else "red"
                self.query_one("#last", Label).update(
                    f"Last executed task: [{color}]{escape(progress.last_task)}[/]"
                )

            current_task = escape(progress.current_task or "-")
            self.query_one("#current", Label).update(f"Current task: {current_task}")

    app_result = BenchmarkProgressApp().run()
    if run_error is not None:
        raise run_error
    if require_result and app_result == cancelled_result:
        raise BenchmarkRunCancelledError("Benchmark run cancelled.")
    if require_result and result is None:
        raise BenchmarkRunCancelledError("Benchmark run cancelled.")
    return result


def _progress_from_run(progress: RunProgress) -> _ProgressDisplay:
    last_task = None
    last_status = None
    if progress.last_result is not None:
        last_task = f"{progress.last_result.task_id} {progress.last_result.harness}"
        last_status = progress.last_result.status
    return _ProgressDisplay(
        total=progress.total,
        completed=progress.completed,
        succeeded=progress.succeeded,
        failed_or_incomplete=progress.failed_or_incomplete,
        current_task=_plan_label(progress.current_plan),
        last_task=last_task,
        last_status=last_status,
    )


def _plan_label(plan: RunPlan | None) -> str | None:
    if plan is None:
        return None
    return f"{plan.task_id} {plan.harness}"


def _format_elapsed(seconds: float) -> str:
    elapsed = int(seconds)
    hours, remainder = divmod(elapsed, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02}:{seconds:02}"
    return f"{minutes}:{seconds:02}"
