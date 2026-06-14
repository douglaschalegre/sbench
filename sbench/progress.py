from __future__ import annotations

from pathlib import Path
from threading import Thread
from time import monotonic
from typing import Sequence

from .runs import MatrixRunResult, RunPlan, RunProgress, run_matrix


class TextualUnavailableError(RuntimeError):
    """Raised when the interactive progress UI cannot be loaded."""


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

    planned = tuple(plans)
    matrix_result: MatrixRunResult | None = None
    run_error: BaseException | None = None

    def plan_label(plan: RunPlan | None) -> str:
        if plan is None:
            return "-"
        return f"{plan.task_id} {plan.harness}"

    def format_elapsed(seconds: float) -> str:
        elapsed = int(seconds)
        hours, remainder = divmod(elapsed, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours:
            return f"{hours}:{minutes:02}:{seconds:02}"
        return f"{minutes}:{seconds:02}"

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
            margin-bottom: 1;
        }

        #progress {
            width: 1fr;
        }

        #elapsed {
            width: auto;
            margin-left: 2;
        }
        """

        def compose(self) -> ComposeResult:
            with Vertical(id="panel"):
                yield Static("SBench Benchmark Progress", id="title")
                with Horizontal(id="progress-row"):
                    yield ProgressBar(
                        total=max(len(planned), 1),
                        show_eta=False,
                        id="progress",
                    )
                    yield Label("Elapsed: 0:00", id="elapsed")
                yield Label("Success: 0", id="success")
                yield Label("Failed_or_incomplete: 0", id="failed")
                yield Label("Last executed task: -", id="last")
                yield Label(
                    f"Current task: {plan_label(planned[0] if planned else None)}",
                    id="current",
                )

        def on_mount(self) -> None:
            self._started_at = monotonic()
            self.set_interval(1, self._render_elapsed)
            self._render_elapsed()
            worker = Thread(target=self._run_benchmark, name="sbench-progress", daemon=True)
            worker.start()

        def _render_elapsed(self) -> None:
            self.query_one("#elapsed", Label).update(
                f"Elapsed: {format_elapsed(monotonic() - self._started_at)}"
            )

        def _run_benchmark(self) -> None:
            nonlocal matrix_result, run_error
            try:
                matrix_result = run_matrix(
                    repo_root,
                    planned,
                    model=model,
                    timeout_seconds=timeout_seconds,
                    stop_on_first_failure=stop_on_first_failure,
                    run_id=run_id,
                    capture_json_events=capture_json_events,
                    progress_callback=self._queue_progress_update,
                )
            except BaseException as error:
                run_error = error
            finally:
                self.call_from_thread(self.exit)

        def _queue_progress_update(self, progress: RunProgress) -> None:
            self.call_from_thread(self._render_progress, progress)

        def _render_progress(self, progress: RunProgress) -> None:
            progress_bar = self.query_one("#progress", ProgressBar)
            progress_bar.update(total=max(progress.total, 1), progress=progress.completed)
            self.query_one("#success", Label).update(f"Success: {progress.succeeded}")
            self.query_one("#failed", Label).update(
                f"Failed_or_incomplete: {progress.failed_or_incomplete}"
            )

            if progress.last_result is None:
                self.query_one("#last", Label).update("Last executed task: -")
            else:
                last_label = f"{progress.last_result.task_id} {progress.last_result.harness}"
                color = "green" if progress.last_result.status == "success" else "red"
                self.query_one("#last", Label).update(
                    f"Last executed task: [{color}]{escape(last_label)}[/]"
                )

            current_label = escape(plan_label(progress.current_plan))
            self.query_one("#current", Label).update(f"Current task: {current_label}")

    BenchmarkProgressApp().run()
    if run_error is not None:
        raise run_error
    if matrix_result is None:
        raise RuntimeError("benchmark run did not produce a result")
    return matrix_result
