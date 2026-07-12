from __future__ import annotations

import asyncio
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from sbench.bdi import config as bdi_config
from sbench.bdi import tools as bdi_tools
from sbench.bdi import toy
def make_sbench_root(tmp_path: Path, task_id: str = "task-a") -> Path:
    sbench_root = tmp_path / "sbench"
    task_path = sbench_root / "tasks" / task_id
    task_path.mkdir(parents=True)
    (task_path / "task.md").write_text(f"# {task_id}\n", encoding="utf-8")
    return sbench_root


def test_parse_config_accepts_the_migrated_runner_options(tmp_path: Path) -> None:
    sbench_root = tmp_path / "sbench"

    config = bdi_config.parse_config(
        [
            "--sbench-root",
            str(sbench_root),
            "--tasks",
            "task-a",
            "--model",
            "gpt-test",
            "--command-timeout-seconds",
            "12",
            "--quiet",
        ]
    )

    assert config == bdi_config.RunConfig(
        task_id="task-a",
        model_name="gpt-test",
        sbench_root=sbench_root,
        command_timeout_seconds=12,
        verbose=False,
    )


def test_get_task_path_resolves_selected_task(tmp_path: Path) -> None:
    sbench_root = make_sbench_root(tmp_path)

    task_path = bdi_config.get_task_path(
        bdi_config.RunConfig(task_id="task-a", sbench_root=sbench_root)
    )

    assert task_path == sbench_root / "tasks" / "task-a"


def test_get_task_path_rejects_missing_task_file(tmp_path: Path) -> None:
    config = bdi_config.RunConfig(
        task_id="missing-task",
        sbench_root=tmp_path / "sbench",
    )

    with pytest.raises(bdi_config.RunnerConfigError, match="SBench task file not found"):
        bdi_config.get_task_path(config)


def test_run_command_uses_task_cwd_and_clamps_timeout(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    captured = {}

    def fake_run(command, *, shell, cwd, capture_output, text, timeout):
        captured.update(
            command=command,
            shell=shell,
            cwd=cwd,
            capture_output=capture_output,
            text=text,
            timeout=timeout,
        )
        return SimpleNamespace(stdout="ok\n", stderr="", returncode=0)

    monkeypatch.setattr(bdi_tools.subprocess, "run", fake_run)

    result = bdi_tools.run_command(
        tmp_path / "task-a",
        "pwd",
        timeout_seconds=999,
        max_timeout_seconds=17,
    )

    assert result == "ok"
    assert captured == {
        "command": "pwd",
        "shell": True,
        "cwd": str(tmp_path / "task-a"),
        "capture_output": True,
        "text": True,
        "timeout": 17,
    }


def test_create_agent_scopes_run_tool_and_usage_tracker(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    captured = {}

    class FakeBDI:
        def __init__(self, *args, **kwargs):
            captured["args"] = args
            captured["kwargs"] = kwargs

        def tool_plain(self, func):
            captured["tool"] = func
            return func

    def fake_run_command(task_path, command, *, timeout_seconds, max_timeout_seconds):
        captured["run_command"] = {
            "task_path": task_path,
            "command": command,
            "timeout_seconds": timeout_seconds,
            "max_timeout_seconds": max_timeout_seconds,
        }
        return "ran"

    monkeypatch.setattr(toy, "BDI", FakeBDI)
    monkeypatch.setattr(toy, "run_command", fake_run_command)
    task_path = tmp_path / "tasks" / "task-a"
    usage_tracker = object()
    config = bdi_config.RunConfig(
        task_id="task-a",
        command_timeout_seconds=9,
        verbose=False,
    )

    agent = toy.create_agent("model", task_path, config, usage_tracker)
    result = captured["tool"]("ls", timeout_seconds=99)

    assert isinstance(agent, FakeBDI)
    assert captured["args"] == ("model",)
    assert captured["kwargs"]["verbose"] is False
    assert captured["kwargs"]["usage_tracker"] is usage_tracker
    assert captured["kwargs"]["emit_run_events_to_stdout"] is True
    assert captured["kwargs"]["stream_model_requests"] is True
    assert captured["kwargs"]["mcp_servers"] == []
    assert "Do not read hidden SBench evaluation files" in captured["kwargs"]["desires"][0]
    assert result == "ran"
    assert captured["run_command"] == {
        "task_path": task_path,
        "command": "ls",
        "timeout_seconds": 99,
        "max_timeout_seconds": 9,
    }


def test_run_task_emits_usage_metadata(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    task_path = tmp_path / "tasks" / "task-a"
    task_path.mkdir(parents=True)
    config = bdi_config.RunConfig(
        task_id="task-a",
        model_name="gpt-test",
        verbose=False,
    )

    class FakeRunMCPServers:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return None

    class FakeAgent:
        def __init__(self, usage_tracker):
            self.usage_tracker = usage_tracker
            self.beliefs = SimpleNamespace(beliefs={"task": "done"})
            self.desires = [
                SimpleNamespace(
                    id="desire_1", status=SimpleNamespace(value="achieved")
                )
            ]
            self.active_intention = None
            self.cycle_count = 1

        def run_mcp_servers(self):
            return FakeRunMCPServers()

        async def bdi_cycle(self):
            self.usage_tracker.record_usage(
                SimpleNamespace(
                    requests=2,
                    tool_calls=1,
                    input_tokens=100,
                    cache_read_tokens=60,
                    output_tokens=20,
                )
            )
            return "terminal"

    def fake_create_agent(model, selected_task_path, run_config, usage_tracker=None):
        assert model == "model"
        assert selected_task_path.name == "task-a"
        assert run_config is config
        assert usage_tracker is not None
        return FakeAgent(usage_tracker)

    monkeypatch.setattr(toy, "create_agent", fake_create_agent)
    monkeypatch.setattr(toy, "CYCLE_SLEEP_SECONDS", 0)

    outcome = asyncio.run(toy.run_task("model", task_path, config))

    assert outcome == "achieved"
    output_lines = capsys.readouterr().out.splitlines()
    metadata = json.loads(next(line for line in reversed(output_lines) if line.startswith("{")))
    assert metadata["type"].split(".")[-2:] == ["run", "completed"]
    assert metadata["model"] == "gpt-test"
    assert metadata["task"] == "task-a"
    assert metadata["outcome"] == "achieved"
    assert metadata["cycles"] == {"run": 1, "max": toy.MAX_CYCLES}
    assert metadata["usage"]["requests"] == 2
    assert metadata["usage"]["tool_calls"] == 1
    assert metadata["usage"]["input_tokens"] == 100
    assert metadata["usage"]["cached_input_tokens"] == 60
    assert metadata["usage"]["output_tokens"] == 20
    assert metadata["usage"]["total_tokens"] == 120
    assert metadata["cost"]["estimated"] is False


def test_sync_main_is_backed_by_the_new_package_runner() -> None:
    assert callable(toy.sync_main)


def test_main_returns_config_error_for_missing_sbench_root(tmp_path: Path) -> None:
    exit_code = asyncio.run(
        toy.main(
            ["--sbench-root", str(tmp_path / "missing"), "--tasks", "task-a"]
        )
    )

    assert exit_code == toy.EXIT_CONFIG_ERROR
