from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path
from threading import Thread
from time import monotonic, sleep
from typing import Sequence

from .runs import MatrixRunResult, RunPlan, RunProgress, run_matrix

try:
    from rich.console import Group
    from rich.text import Text
except ImportError:
    Group = None
    Text = None


CONTENT_WIDTH = 68
PANEL_WIDTH = CONTENT_WIDTH + 2
ANIMATION_INTERVAL_SECONDS = 0.03
PREVIEW_STEP_SECONDS = 1.2
PREVIEW_HOLD_SECONDS = 2
CANCELLED_RESULT = "cancelled"
TEXTUAL_UNAVAILABLE_MESSAGE = (
    "Textual is required for the interactive progress UI. Use `uv run sbench ...`, "
    "activate the project virtualenv, or install Textual into the Python interpreter "
    "running this command."
)

TEXT_STYLE = "#e5e7eb"
TITLE_STYLE = "bold #f5f5f4"
SUCCESS_STYLE = "#22c55e"
FAILURE_STYLE = "#ef4444"
ACTIVE_BAR_STYLE = "#0178d4"
COMPLETE_BAR_STYLE = "#4ebf71"
EMPTY_BAR_STYLE = "#303030"

GRADIENT_STOPS = (
    (234, 88, 12),
    (249, 115, 22),
    (251, 146, 60),
    (253, 186, 116),
    (255, 237, 213),
    (253, 186, 116),
    (251, 146, 60),
    (249, 115, 22),
)

PREVIEW_TASKS = (
    ("vendor_selection", "codex", "success"),
    ("travel_reimbursement_audit", "opencode", "failed"),
    ("clinic_rollout_plan", "bdi", "success"),
    ("grant_closeout_recovery", "codex", "incomplete"),
)


class TextualUnavailableError(RuntimeError):
    """Raised when the interactive progress UI cannot be loaded."""


class BenchmarkRunCancelledError(RuntimeError):
    """Raised when the interactive progress UI cancels a benchmark run."""


@dataclass(frozen=True)
class _ProgressDisplay:
    total: int
    current_task: str | None
    completed: int = 0
    succeeded: int = 0
    failed_or_incomplete: int = 0
    last_task: str | None = None
    last_status: str | None = None


_ProgressWorker = Callable[[Callable[[_ProgressDisplay], None]], object]


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
            current_task=_plan_label(planned[0] if planned else None),
        ),
        worker=run_benchmark,
        require_result=True,
    )
    if not isinstance(result, MatrixRunResult):
        raise RuntimeError("benchmark run did not produce a result")
    return result


def preview_textual_progress() -> None:
    def run_preview(update: Callable[[_ProgressDisplay], None]) -> None:
        succeeded = 0
        failed_or_incomplete = 0
        total = len(PREVIEW_TASKS)

        for completed, task in enumerate(PREVIEW_TASKS, start=1):
            task_id, harness, status = task
            sleep(PREVIEW_STEP_SECONDS)
            if status == "success":
                succeeded += 1
            else:
                failed_or_incomplete += 1
            next_task = PREVIEW_TASKS[completed] if completed < total else None
            update(
                _ProgressDisplay(
                    total=total,
                    completed=completed,
                    succeeded=succeeded,
                    failed_or_incomplete=failed_or_incomplete,
                    current_task=_preview_label(next_task),
                    last_task=f"{task_id} {harness}",
                    last_status=status,
                )
            )
        sleep(PREVIEW_HOLD_SECONDS)

    _run_progress_app(
        title="SBench Progress Preview",
        initial_progress=_ProgressDisplay(
            total=len(PREVIEW_TASKS),
            current_task=_preview_label(PREVIEW_TASKS[0]),
        ),
        worker=run_preview,
        require_result=False,
    )


def _run_progress_app(
    *,
    title: str,
    initial_progress: _ProgressDisplay,
    worker: _ProgressWorker,
    require_result: bool,
) -> object:
    App, ComposeResult, Static = _load_textual_dependencies()
    result: object = None
    run_error: BaseException | None = None

    class BenchmarkProgressApp(App):
        CSS = f"""
        Screen {{
            align: center middle;
        }}

        #panel {{
            width: {PANEL_WIDTH};
            height: auto;
        }}
        """

        def compose(self) -> ComposeResult:
            yield Static(id="panel")

        def action_quit(self) -> None:
            self.exit(CANCELLED_RESULT)

        def on_mount(self) -> None:
            self._started_at = monotonic()
            self._border_frame = 0
            self._progress = initial_progress
            self.set_interval(ANIMATION_INTERVAL_SECONDS, self._advance_animation)
            self._render_panel()
            Thread(target=self._run_worker, name="sbench-progress", daemon=True).start()

        def _advance_animation(self) -> None:
            self._border_frame += 1
            self._render_panel()

        def _render_panel(self) -> None:
            elapsed = _format_elapsed(monotonic() - self._started_at)
            self.query_one("#panel", Static).update(
                _render_panel(title, self._progress, elapsed, self._border_frame)
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
            self.call_from_thread(self._set_progress, progress)

        def _set_progress(self, progress: _ProgressDisplay) -> None:
            self._progress = progress
            self._render_panel()

    app_result = BenchmarkProgressApp().run()
    if run_error is not None:
        raise run_error
    if require_result and app_result == CANCELLED_RESULT:
        raise BenchmarkRunCancelledError("Benchmark run cancelled.")
    if require_result and result is None:
        raise BenchmarkRunCancelledError("Benchmark run cancelled.")
    return result


def _load_textual_dependencies() -> tuple[object, object, object]:
    if Group is None or Text is None:
        raise TextualUnavailableError(TEXTUAL_UNAVAILABLE_MESSAGE)
    try:
        from textual.app import App, ComposeResult
        from textual.widgets import Static
    except ImportError as error:
        raise TextualUnavailableError(TEXTUAL_UNAVAILABLE_MESSAGE) from error
    return App, ComposeResult, Static


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


def _render_panel(
    title: str, progress: _ProgressDisplay, elapsed: str, frame: int
) -> object:
    assert Group is not None and Text is not None
    content_lines = [
        _fit_text(Text(title, style=TITLE_STYLE), align="center"),
        Text(""),
        _progress_line(progress, elapsed),
        _status_line("Success: ", str(progress.succeeded)),
        _status_line("Failed_or_incomplete: ", str(progress.failed_or_incomplete)),
        _status_line(
            "Last executed task: ",
            progress.last_task or "-",
            _last_status_style(progress.last_status),
        ),
        _status_line("Current task: ", progress.current_task or "-"),
    ]
    content_height = len(content_lines)
    perimeter = (PANEL_WIDTH * 2) + (content_height * 2)
    bottom_start = PANEL_WIDTH + content_height
    left_start = bottom_start + PANEL_WIDTH

    top = _border_text(
        "╭" + ("─" * CONTENT_WIDTH) + "╮", range(PANEL_WIDTH), perimeter, frame
    )
    body = []
    for row, content in enumerate(content_lines):
        line = Text()
        line.append(
            "│",
            style=_border_style(left_start + content_height - row - 1, perimeter, frame),
        )
        line.append_text(_fit_text(content))
        line.append("│", style=_border_style(PANEL_WIDTH + row, perimeter, frame))
        body.append(line)
    bottom = _border_text(
        "╰" + ("─" * CONTENT_WIDTH) + "╯",
        range(bottom_start + PANEL_WIDTH - 1, bottom_start - 1, -1),
        perimeter,
        frame,
    )
    return Group(top, *body, bottom)


def _fit_text(content: object, *, align: str = "left") -> object:
    text = content.copy()
    if text.cell_len > CONTENT_WIDTH:
        text.truncate(CONTENT_WIDTH, overflow="ellipsis")
    remaining = CONTENT_WIDTH - text.cell_len
    if remaining <= 0:
        return text
    if align == "center":
        left = remaining // 2
        return Text(" " * left) + text + Text(" " * (remaining - left))
    text.append(" " * remaining)
    return text


def _status_line(prefix: str, value: str, style: str = TEXT_STYLE) -> object:
    return Text.assemble((prefix, TEXT_STYLE), (value, style))


def _progress_line(progress: _ProgressDisplay, elapsed: str) -> object:
    total = max(progress.total, 1)
    ratio = min(1.0, max(0.0, progress.completed / total))
    percent = f"{round(ratio * 100):>3}%"
    elapsed_label = f"Elapsed: {elapsed}"
    bar_width = max(12, CONTENT_WIDTH - len(percent) - len(elapsed_label) - 6)
    filled = min(bar_width, round(bar_width * ratio))
    empty = bar_width - filled
    bar_style = (
        COMPLETE_BAR_STYLE if progress.completed >= progress.total else ACTIVE_BAR_STYLE
    )

    line = Text()
    line.append("━" * filled, style=bar_style)
    if empty:
        line.append(
            "╺" if filled else "━", style=bar_style if filled else EMPTY_BAR_STYLE
        )
        line.append("━" * (empty - 1), style=EMPTY_BAR_STYLE)
    line.append(f"  {percent}  {elapsed_label}", style=TEXT_STYLE)
    return line


def _border_text(
    chars: str, positions: Iterable[int], perimeter: int, frame: int
) -> object:
    text = Text()
    for char, position in zip(chars, positions):
        text.append(char, style=_border_style(position, perimeter, frame))
    return text


def _border_style(position: int, perimeter: int, frame: int) -> str:
    return f"bold {_gradient_color((position - frame) / perimeter)}"


def _gradient_color(position: float) -> str:
    scaled = (position % 1.0) * len(GRADIENT_STOPS)
    index = int(scaled)
    mix = scaled - index
    start = GRADIENT_STOPS[index]
    end = GRADIENT_STOPS[(index + 1) % len(GRADIENT_STOPS)]
    channels = (round(a + (b - a) * mix) for a, b in zip(start, end))
    return "#" + "".join(f"{channel:02x}" for channel in channels)


def _last_status_style(status: str | None) -> str:
    if status is None:
        return TEXT_STYLE
    if status == "success":
        return SUCCESS_STYLE
    return FAILURE_STYLE


def _preview_label(task: tuple[str, str, str] | None) -> str | None:
    if task is None:
        return None
    return f"{task[0]} {task[1]}"


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
