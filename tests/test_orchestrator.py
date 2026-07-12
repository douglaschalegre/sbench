from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock
from pathlib import Path

from sbench import cli, orchestrator


class OrchestratorTest(unittest.TestCase):
    def make_repo(self) -> tempfile.TemporaryDirectory[str]:
        temp_dir = tempfile.TemporaryDirectory()
        repo_root = Path(temp_dir.name)
        (repo_root / "tasks" / "vendor_selection").mkdir(parents=True)
        (repo_root / "tasks" / "vendor_selection" / "task.md").write_text(
            "task", encoding="utf-8"
        )
        (repo_root / "tasks" / "travel_reimbursement_audit").mkdir(parents=True)
        (repo_root / "tasks" / "travel_reimbursement_audit" / "task.md").write_text(
            "task", encoding="utf-8"
        )
        (repo_root / "tasks" / "clinic_rollout_plan").mkdir(parents=True)
        (repo_root / "tasks" / "clinic_rollout_plan" / "task.md").write_text(
            "task", encoding="utf-8"
        )
        (repo_root / "tasks" / "not_a_task").mkdir(parents=True)
        return temp_dir

    def make_plan(
        self,
        repo_root: Path,
        *,
        task_id: str = "vendor_selection",
        harness: str = "codex",
        model: str = "gpt-5.2",
        command: tuple[str, ...],
        settings: dict[str, object] | None = None,
    ) -> orchestrator.RunPlan:
        task = orchestrator.select_tasks(
            orchestrator.discover_tasks(repo_root), [task_id]
        )[0]
        archive_plan = orchestrator.plan_answer_archive(
            repo_root, task, model=model, harness=harness
        )
        return orchestrator.RunPlan(
            task_id=task.id,
            track=task.track,
            harness=harness,
            task_dir=task.path,
            working_dir=task.path,
            archive_dir=archive_plan.archive_dir,
            command=command,
            settings=settings or {},
        )

    def test_discovers_task_directories_with_task_markdown_only(self) -> None:
        with self.make_repo() as repo:
            tasks = orchestrator.discover_tasks(Path(repo))

        self.assertEqual(
            [task.id for task in tasks],
            ["clinic_rollout_plan", "travel_reimbursement_audit", "vendor_selection"],
        )
        self.assertEqual(
            {task.id: task.track for task in tasks},
            {
                "clinic_rollout_plan": "long_context",
                "travel_reimbursement_audit": "smoke",
                "vendor_selection": "smoke",
            },
        )

    def test_harness_selection_defaults_to_supported_harnesses(self) -> None:
        self.assertEqual(
            orchestrator.select_harnesses(None),
            ["bdi", "codex", "opencode"],
        )

    def test_harness_selection_accepts_repeated_and_comma_separated_values(
        self,
    ) -> None:
        self.assertEqual(
            orchestrator.select_harnesses(["codex,opencode", "codex"]),
            ["codex", "opencode"],
        )

    def test_harness_selection_rejects_unknown_harnesses(self) -> None:
        with self.assertRaises(orchestrator.SelectionError):
            orchestrator.select_harnesses(["codex", "unknown"])

    def test_task_selection_accepts_discovered_task_ids(self) -> None:
        with self.make_repo() as repo:
            tasks = orchestrator.discover_tasks(Path(repo))
            selected = orchestrator.select_tasks(tasks, ["vendor_selection"])

        self.assertEqual([task.id for task in selected], ["vendor_selection"])

    def test_task_selection_rejects_unknown_task_ids(self) -> None:
        with self.make_repo() as repo:
            tasks = orchestrator.discover_tasks(Path(repo))
            with self.assertRaises(orchestrator.SelectionError):
                orchestrator.select_tasks(tasks, ["missing_task"])

    def test_parse_args_accepts_orchestrator_options(self) -> None:
        args = orchestrator.parse_args(
            [
                "--dry-run",
                "--model",
                "gpt-5.4",
                "--timeout",
                "120",
                "--task",
                "vendor_selection",
                "--harness",
                "codex",
            ]
        )

        self.assertTrue(args.dry_run)
        self.assertEqual(args.model, "gpt-5.4")
        self.assertEqual(args.timeout, 120)
        self.assertEqual(args.task, ["vendor_selection"])
        self.assertEqual(args.harness, ["codex"])

    def test_parse_args_accepts_progress_preview_without_model(self) -> None:
        args = orchestrator.parse_args(["--progress-preview"])

        self.assertTrue(args.progress_preview)
        self.assertIsNone(args.model)

    def test_parse_args_accepts_import_results_without_model(self) -> None:
        args = orchestrator.parse_args(
            ["--import-results", "--results-db", "custom.sqlite"]
        )

        self.assertTrue(args.import_results)
        self.assertIsNone(args.model)
        self.assertEqual(args.results_db, Path("custom.sqlite"))

    def test_progress_ui_is_enabled_for_tty_output_only(self) -> None:
        class TtyOutput(io.StringIO):
            def isatty(self) -> bool:
                return True

        self.assertFalse(cli.should_show_progress(io.StringIO()))
        self.assertTrue(cli.should_show_progress(TtyOutput()))

    def test_list_mode_prints_tasks_and_harnesses_without_planning_commands(
        self,
    ) -> None:
        with self.make_repo() as repo:
            output = io.StringIO()
            exit_code = orchestrator.main(
                ["--repo-root", repo, "--list"], stdout=output
            )

        rendered = output.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("Supported harnesses:", rendered)
        self.assertIn("- bdi", rendered)
        self.assertIn("- codex", rendered)
        self.assertIn("- opencode", rendered)
        self.assertIn("- vendor_selection [smoke]", rendered)
        self.assertIn("- travel_reimbursement_audit [smoke]", rendered)
        self.assertIn("- clinic_rollout_plan [long_context]", rendered)
        self.assertNotIn("command:", rendered)

    def test_progress_preview_runs_without_model_or_run_artifacts(self) -> None:
        with self.make_repo() as repo:
            output = io.StringIO()
            stderr = io.StringIO()
            with mock.patch.object(cli, "preview_textual_progress") as preview:
                exit_code = orchestrator.main(
                    ["--repo-root", repo, "--progress-preview"],
                    stdout=output,
                    stderr=stderr,
                )

            self.assertEqual(exit_code, 0)
            preview.assert_called_once_with()
            self.assertEqual(output.getvalue(), "")
            self.assertEqual(stderr.getvalue(), "")
            self.assertFalse((Path(repo) / "runs").exists())

    def test_import_results_runs_importer_without_model_or_harness_planning(
        self,
    ) -> None:
        with self.make_repo() as repo:
            output = io.StringIO()
            with mock.patch.object(
                cli,
                "import_run_records",
                return_value=cli.ImportResult(execution_count=3, warning_count=1),
            ) as importer:
                exit_code = orchestrator.main(
                    [
                        "--repo-root",
                        repo,
                        "--import-results",
                        "--results-db",
                        "custom.sqlite",
                    ],
                    stdout=output,
                )

            database_path = Path(repo).resolve() / "custom.sqlite"
            self.assertEqual(exit_code, 0)
            importer.assert_called_once_with(Path(repo).resolve(), database_path)
            rendered = output.getvalue()
            self.assertIn("SBench results import complete", rendered)
            self.assertIn("database: custom.sqlite", rendered)
            self.assertIn("executions_imported: 3", rendered)
            self.assertIn("warnings: 1", rendered)

    def test_dry_run_prints_selected_matrix_commands_and_archive_destinations(
        self,
    ) -> None:
        with self.make_repo() as repo:
            repo_root = Path(repo)
            (
                repo_root / "answers" / "vendor_selection" / "gpt-5.2" / "codex" / "r1"
            ).mkdir(parents=True)
            (
                repo_root
                / "answers"
                / "vendor_selection"
                / "gpt-5.2"
                / "codex"
                / "r1"
                / "result.md"
            ).write_text("existing result", encoding="utf-8")
            output = io.StringIO()
            exit_code = orchestrator.main(
                [
                    "--repo-root",
                    repo,
                    "--dry-run",
                    "--model",
                    "gpt-5.2",
                    "--timeout",
                    "300",
                    "--task",
                    "vendor_selection",
                    "--harness",
                    "codex,opencode",
                ],
                stdout=output,
            )

        rendered = output.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("SBench dry run", rendered)
        self.assertIn("  track: smoke", rendered)
        self.assertIn("model: gpt-5.2", rendered)
        self.assertIn("timeout_seconds: 300", rendered)
        self.assertIn("matrix_entries: 2", rendered)
        self.assertIn("archive: answers/vendor_selection/gpt-5.2/codex/r2", rendered)
        self.assertIn("archive: answers/vendor_selection/gpt-5.2/opencode/r1", rendered)
        self.assertIn("command: codex exec", rendered)
        self.assertIn("command: opencode run", rendered)
        self.assertIn(orchestrator.STANDARD_TASK_PROMPT, rendered)

    def test_codex_and_opencode_command_shapes_include_standard_prompt(self) -> None:
        with self.make_repo() as repo:
            repo_root = Path(repo)
            task = orchestrator.discover_tasks(repo_root)[0]

            codex = orchestrator.build_command_shape(
                "codex",
                model="gpt-5.2",
                timeout_seconds=600,
                task_dir=task.path,
                repo_root=repo_root,
            )
            opencode = orchestrator.build_command_shape(
                "opencode",
                model="gpt-5.2",
                timeout_seconds=600,
                task_dir=task.path,
                repo_root=repo_root,
            )

        self.assertEqual(codex[-1], orchestrator.STANDARD_TASK_PROMPT)
        self.assertEqual(opencode[-1], orchestrator.STANDARD_TASK_PROMPT)

    def test_codex_invocation_uses_task_scoped_noninteractive_command_and_settings(
        self,
    ) -> None:
        with self.make_repo() as repo:
            repo_root = Path(repo)
            task = orchestrator.select_tasks(
                orchestrator.discover_tasks(repo_root), ["vendor_selection"]
            )[0]

            invocation = orchestrator.build_harness_invocation(
                "codex",
                model="openai/gpt-5.2",
                timeout_seconds=600,
                task_dir=task.path,
                repo_root=repo_root,
            )

        self.assertEqual(invocation.command[0:2], ("codex", "exec"))
        self.assertIn("-m", invocation.command)
        self.assertIn("gpt-5.2", invocation.command)
        self.assertNotIn("openai/gpt-5.2", invocation.command)
        self.assertIn("--cd", invocation.command)
        self.assertEqual(
            invocation.command[invocation.command.index("--cd") + 1],
            "tasks/vendor_selection",
        )
        self.assertIn("--sandbox", invocation.command)
        self.assertIn("workspace-write", invocation.command)
        self.assertIn("--config", invocation.command)
        self.assertIn('approval_policy="never"', invocation.command)
        self.assertIn('model_reasoning_effort="medium"', invocation.command)
        self.assertIn("--ephemeral", invocation.command)
        self.assertIn("--json", invocation.command)
        self.assertNotIn("--add-dir", invocation.command)
        self.assertNotIn("evaluation", invocation.command)
        self.assertNotIn(".prd", invocation.command)
        self.assertEqual(invocation.working_dir, repo_root)
        self.assertEqual(invocation.settings["approval_policy"], "never")
        self.assertEqual(invocation.settings["command_model"], "gpt-5.2")
        self.assertEqual(invocation.settings["reasoning_effort"], "medium")
        self.assertEqual(invocation.settings["sandbox"], "workspace-write")
        self.assertEqual(
            invocation.settings["task_directory_scope"], "tasks/vendor_selection"
        )

    def test_opencode_invocation_uses_task_scoped_json_autoapproved_command_and_settings(
        self,
    ) -> None:
        with self.make_repo() as repo:
            repo_root = Path(repo)
            task = orchestrator.select_tasks(
                orchestrator.discover_tasks(repo_root), ["vendor_selection"]
            )[0]

            invocation = orchestrator.build_harness_invocation(
                "opencode",
                model="openai/gpt-5.2",
                timeout_seconds=600,
                task_dir=task.path,
                repo_root=repo_root,
            )

        self.assertEqual(invocation.command[0:2], ("opencode", "run"))
        self.assertIn("-m", invocation.command)
        self.assertIn("openai/gpt-5.2", invocation.command)
        self.assertIn("--variant", invocation.command)
        self.assertEqual(
            invocation.command[invocation.command.index("--variant") + 1], "medium"
        )
        self.assertIn("--dir", invocation.command)
        self.assertEqual(
            invocation.command[invocation.command.index("--dir") + 1],
            "tasks/vendor_selection",
        )
        self.assertIn("--format", invocation.command)
        self.assertIn("json", invocation.command)
        self.assertIn("--dangerously-skip-permissions", invocation.command)
        self.assertNotIn("--add-dir", invocation.command)
        self.assertNotIn("evaluation", invocation.command)
        self.assertNotIn(".prd", invocation.command)
        self.assertEqual(invocation.working_dir, repo_root)
        self.assertTrue(invocation.settings["auto_approve_permissions"])
        self.assertEqual(invocation.settings["command_model"], "openai/gpt-5.2")
        self.assertEqual(invocation.settings["format"], "json")
        self.assertEqual(invocation.settings["reasoning_effort"], "medium")
        self.assertEqual(invocation.settings["writable_scope"], "task_directory_only")
        self.assertEqual(
            invocation.settings["task_directory_scope"], "tasks/vendor_selection"
        )

    def test_missing_cli_binary_detection_reports_selected_agent_binaries(self) -> None:
        missing = orchestrator.find_missing_cli_binaries(
            ["bdi", "codex", "opencode"],
            which=lambda binary: (
                "/bin/" + binary if binary in {"opencode", "uv"} else None
            ),
        )

        self.assertEqual(missing, {"codex": "codex"})

    def test_run_mode_preflight_reports_missing_cli_before_running(self) -> None:
        with self.make_repo() as repo:
            stdout = io.StringIO()
            stderr = io.StringIO()
            with mock.patch.object(
                cli,
                "find_missing_cli_binaries",
                return_value={"codex": "codex"},
            ):
                exit_code = orchestrator.main(
                    [
                        "--repo-root",
                        repo,
                        "--run",
                        "--model",
                        "gpt-5.2",
                        "--harness",
                        "codex",
                    ],
                    stdout=stdout,
                    stderr=stderr,
                )

            self.assertEqual(exit_code, 2)
            self.assertIn("Missing required CLI binaries", stderr.getvalue())
            self.assertFalse((Path(repo) / "runs").exists())

    def test_run_mode_reports_interactive_progress_cancellation_without_traceback(
        self,
    ) -> None:
        class TtyOutput(io.StringIO):
            def isatty(self) -> bool:
                return True

        with self.make_repo() as repo:
            stdout = TtyOutput()
            stderr = io.StringIO()
            with (
                mock.patch.object(cli, "find_missing_cli_binaries", return_value={}),
                mock.patch.object(
                    cli,
                    "run_matrix_with_textual_progress",
                    side_effect=cli.BenchmarkRunCancelledError(
                        "Benchmark run cancelled."
                    ),
                ),
            ):
                exit_code = orchestrator.main(
                    [
                        "--repo-root",
                        repo,
                        "--run",
                        "--model",
                        "gpt-5.2",
                        "--harness",
                        "codex",
                    ],
                    stdout=stdout,
                    stderr=stderr,
                )

            self.assertEqual(exit_code, 130)
            self.assertEqual(stdout.getvalue(), "")
            self.assertEqual(stderr.getvalue(), "Benchmark run cancelled.\n")

    def test_bdi_invocation_uses_the_internal_runner_and_task(self) -> None:
        with self.make_repo() as repo:
            repo_root = Path(repo)
            task = orchestrator.select_tasks(
                orchestrator.discover_tasks(repo_root), ["vendor_selection"]
            )[0]

            invocation = orchestrator.build_harness_invocation(
                "bdi",
                model="openai/gpt-5.2",
                timeout_seconds=600,
                task_dir=task.path,
                repo_root=repo_root,
            )

        self.assertEqual(invocation.command[0:3], ("uv", "run", "sbench-bdi"))
        self.assertIn("--sbench-root", invocation.command)
        self.assertIn(str(repo_root), invocation.command)
        self.assertIn("--tasks", invocation.command)
        self.assertIn("vendor_selection", invocation.command)
        self.assertIn("--model", invocation.command)
        self.assertIn("chatgpt/gpt-5.2", invocation.command)
        self.assertNotIn("openai/gpt-5.2", invocation.command)
        self.assertNotIn("--output-dir", invocation.command)
        self.assertIn("--command-timeout-seconds", invocation.command)
        self.assertIn("600", invocation.command)
        self.assertIn("--quiet", invocation.command)
        self.assertEqual(invocation.working_dir, repo_root)
        self.assertEqual(invocation.settings["binary"], "uv")
        self.assertEqual(invocation.settings["reasoning_effort"], "medium")
        self.assertEqual(
            invocation.settings["command_model"], "chatgpt/gpt-5.2"
        )
        self.assertEqual(invocation.settings["runner"], "sbench-bdi")
        self.assertEqual(
            invocation.settings["task_directory_scope"], "tasks/vendor_selection"
        )

    def test_bdi_run_plan_uses_sbench_working_dir_and_canonical_archive_destination(
        self,
    ) -> None:
        with self.make_repo() as repo:
            repo_root = Path(repo)
            task = orchestrator.select_tasks(
                orchestrator.discover_tasks(repo_root), ["vendor_selection"]
            )

            plans = orchestrator.build_run_plans(
                repo_root,
                tasks=task,
                harnesses=["bdi"],
                model="gpt-5.2",
                timeout_seconds=600,
                run_id="bdi-run",
            )
            plan = plans[0]

        self.assertEqual(plan.working_dir, repo_root)
        self.assertEqual(
            plan.archive_dir,
            repo_root / "answers" / "vendor_selection" / "gpt-5.2" / "bdi" / "r1",
        )
        self.assertNotIn("output_dir", plan.settings)

    def test_bdi_run_mode_requires_litellm_proxy_before_running(self) -> None:
        with self.make_repo() as repo:
            stdout = io.StringIO()
            stderr = io.StringIO()
            unavailable = SimpleNamespace(
                available=False,
                url="http://localhost:4000/health/liveliness",
                detail="connection refused",
            )
            with (
                mock.patch.object(cli, "find_missing_cli_binaries", return_value={}),
                mock.patch.object(cli, "check_litellm_proxy", return_value=unavailable),
                mock.patch.object(cli, "run_matrix") as run_matrix,
            ):
                exit_code = orchestrator.main(
                    [
                        "--repo-root",
                        repo,
                        "--run",
                        "--model",
                        "gpt-5.2",
                        "--harness",
                        "bdi",
                    ],
                    stdout=stdout,
                    stderr=stderr,
                )

            self.assertEqual(exit_code, 2)
            self.assertIn("LiteLLM proxy is not available", stderr.getvalue())
            self.assertIn("make litellm", stderr.getvalue())
            run_matrix.assert_not_called()

    def test_archive_plan_selects_r1_when_no_canonical_runs_exist(self) -> None:
        with self.make_repo() as repo:
            repo_root = Path(repo)
            task = orchestrator.select_tasks(
                orchestrator.discover_tasks(repo_root), ["vendor_selection"]
            )[0]
            plan = orchestrator.plan_answer_archive(
                repo_root, task, model="gpt-5.2", harness="codex"
            )

        self.assertEqual(plan.run_id, "r1")
        self.assertEqual(plan.model_path, "gpt-5.2")
        self.assertEqual(plan.display_model, "gpt-5.2")
        self.assertEqual(
            plan.archive_dir,
            Path(repo) / "answers" / "vendor_selection" / "gpt-5.2" / "codex" / "r1",
        )

    def test_archive_plan_selects_next_canonical_run_per_scope(self) -> None:
        with self.make_repo() as repo:
            repo_root = Path(repo)
            task = orchestrator.select_tasks(
                orchestrator.discover_tasks(repo_root), ["vendor_selection"]
            )[0]
            (
                repo_root / "answers" / "vendor_selection" / "gpt-5.2" / "codex" / "r1"
            ).mkdir(parents=True)
            (
                repo_root
                / "answers"
                / "vendor_selection"
                / "gpt-5.2"
                / "codex"
                / "r1"
                / "result.md"
            ).write_text("r1", encoding="utf-8")
            (
                repo_root / "answers" / "vendor_selection" / "gpt-5.2" / "codex" / "r2"
            ).mkdir()
            (
                repo_root
                / "answers"
                / "vendor_selection"
                / "gpt-5.2"
                / "codex"
                / "r2"
                / "result.md"
            ).write_text("r2", encoding="utf-8")
            (
                repo_root
                / "answers"
                / "vendor_selection"
                / "gpt-5.2"
                / "opencode"
                / "r7"
            ).mkdir(parents=True)
            (
                repo_root
                / "answers"
                / "travel_reimbursement_audit"
                / "gpt-5.2"
                / "codex"
                / "r8"
            ).mkdir(parents=True)

            plan = orchestrator.plan_answer_archive(
                repo_root, task, model="gpt-5.2", harness="codex"
            )

        self.assertEqual(plan.run_id, "r3")

    def test_archive_plan_reuses_lowest_empty_canonical_run(self) -> None:
        with self.make_repo() as repo:
            repo_root = Path(repo)
            task = orchestrator.select_tasks(
                orchestrator.discover_tasks(repo_root), ["vendor_selection"]
            )[0]
            archive_parent = (
                repo_root / "answers" / "vendor_selection" / "gpt-5.2" / "codex"
            )
            (archive_parent / "r1" / "empty-nested-directory").mkdir(parents=True)
            (archive_parent / "r2").mkdir()
            (archive_parent / "r2" / "result.md").write_text("r2", encoding="utf-8")

            plan = orchestrator.plan_answer_archive(
                repo_root, task, model="gpt-5.2", harness="codex"
            )

        self.assertEqual(plan.run_id, "r1")

    def test_archive_plan_normalizes_model_path_without_losing_display_model(
        self,
    ) -> None:
        with self.make_repo() as repo:
            repo_root = Path(repo)
            task = orchestrator.select_tasks(
                orchestrator.discover_tasks(repo_root), ["vendor_selection"]
            )[0]
            plan = orchestrator.plan_answer_archive(
                repo_root,
                task,
                model="openai/gpt 5.5",
                harness="opencode",
            )

        self.assertEqual(plan.display_model, "openai/gpt 5.5")
        self.assertEqual(plan.model_path, "openai__gpt-5.5")
        self.assertIn("openai__gpt-5.5", str(plan.archive_dir))

    def test_command_model_name_uses_each_harness_provider_alias(self) -> None:
        self.assertEqual(
            orchestrator.command_model_name("codex", "openai/gpt-5.2"), "gpt-5.2"
        )
        self.assertEqual(
            orchestrator.command_model_name("bdi", "openai-codex/gpt-5.2"),
            "chatgpt/gpt-5.2",
        )
        self.assertEqual(
            orchestrator.command_model_name("opencode", "openai/gpt-5.2"),
            "openai/gpt-5.2",
        )

    def test_legacy_direct_answer_files_do_not_affect_canonical_run_selection(
        self,
    ) -> None:
        with self.make_repo() as repo:
            repo_root = Path(repo)
            legacy_dir = (
                repo_root / "answers" / "vendor_selection" / "gpt-5.2" / "codex"
            )
            legacy_dir.mkdir(parents=True)
            (legacy_dir / "vendor_screen.md").write_text("legacy", encoding="utf-8")
            task = orchestrator.select_tasks(
                orchestrator.discover_tasks(repo_root), ["vendor_selection"]
            )[0]

            plan = orchestrator.plan_answer_archive(
                repo_root, task, model="gpt-5.2", harness="codex"
            )

            self.assertEqual(plan.run_id, "r1")
            self.assertTrue((legacy_dir / "vendor_screen.md").is_file())

    def test_clean_answer_dir_removes_previous_outputs_and_recreates_directory(
        self,
    ) -> None:
        with self.make_repo() as repo:
            repo_root = Path(repo)
            task = orchestrator.select_tasks(
                orchestrator.discover_tasks(repo_root), ["vendor_selection"]
            )[0]
            answer_dir = task.path / "answer"
            answer_dir.mkdir()
            (answer_dir / "old.md").write_text("old", encoding="utf-8")

            cleaned = orchestrator.clean_answer_dir(task)

            self.assertEqual(cleaned, answer_dir)
            self.assertTrue(answer_dir.is_dir())
            self.assertEqual(list(answer_dir.iterdir()), [])

    def test_archive_answer_files_copies_outputs_to_canonical_destination(self) -> None:
        with self.make_repo() as repo:
            repo_root = Path(repo)
            task = orchestrator.select_tasks(
                orchestrator.discover_tasks(repo_root), ["vendor_selection"]
            )[0]
            answer_dir = task.path / "answer"
            answer_dir.mkdir()
            (answer_dir / "source_resolution.md").write_text("source", encoding="utf-8")
            (answer_dir / "nested").mkdir()
            (answer_dir / "nested" / "notes.md").write_text("notes", encoding="utf-8")
            plan = orchestrator.plan_answer_archive(
                repo_root, task, model="gpt-5.2", harness="codex"
            )

            result = orchestrator.archive_answer_files(plan)

            self.assertEqual(result.status, "success")
            self.assertIsNone(result.incomplete_reason)
            self.assertTrue((plan.archive_dir / "source_resolution.md").is_file())
            self.assertTrue((plan.archive_dir / "nested" / "notes.md").is_file())
            self.assertEqual(
                (plan.archive_dir / "source_resolution.md").read_text(encoding="utf-8"),
                "source",
            )

    def test_archive_answer_files_reuses_empty_canonical_destination(self) -> None:
        with self.make_repo() as repo:
            repo_root = Path(repo)
            task = orchestrator.select_tasks(
                orchestrator.discover_tasks(repo_root), ["vendor_selection"]
            )[0]
            answer_dir = task.path / "answer"
            answer_dir.mkdir()
            (answer_dir / "source_resolution.md").write_text("source", encoding="utf-8")
            plan = orchestrator.plan_answer_archive(
                repo_root, task, model="gpt-5.2", harness="codex"
            )
            (plan.archive_dir / "empty-nested-directory").mkdir(parents=True)

            result = orchestrator.archive_answer_files(plan)

            self.assertEqual(result.status, "success")
            self.assertEqual(
                (plan.archive_dir / "source_resolution.md").read_text(encoding="utf-8"),
                "source",
            )

    def test_archive_answer_files_records_missing_or_empty_answers_as_incomplete(
        self,
    ) -> None:
        with self.make_repo() as repo:
            repo_root = Path(repo)
            task = orchestrator.select_tasks(
                orchestrator.discover_tasks(repo_root), ["vendor_selection"]
            )[0]
            missing_plan = orchestrator.plan_answer_archive(
                repo_root, task, model="gpt-5.2", harness="codex"
            )

            missing_result = orchestrator.archive_answer_files(missing_plan)
            (task.path / "answer").mkdir()
            empty_plan = orchestrator.plan_answer_archive(
                repo_root, task, model="gpt-5.2", harness="codex"
            )
            empty_result = orchestrator.archive_answer_files(empty_plan)

            self.assertEqual(missing_result.status, "incomplete")
            self.assertEqual(
                missing_result.incomplete_reason, "missing answer directory"
            )
            self.assertEqual(empty_result.status, "incomplete")
            self.assertEqual(empty_result.incomplete_reason, "empty answer directory")
            self.assertFalse(missing_plan.archive_dir.exists())
            self.assertFalse(empty_plan.archive_dir.exists())

    def test_archive_answer_files_refuses_to_overwrite_existing_run_by_default(
        self,
    ) -> None:
        with self.make_repo() as repo:
            repo_root = Path(repo)
            task = orchestrator.select_tasks(
                orchestrator.discover_tasks(repo_root), ["vendor_selection"]
            )[0]
            answer_dir = task.path / "answer"
            answer_dir.mkdir()
            (answer_dir / "source_resolution.md").write_text("source", encoding="utf-8")
            plan = orchestrator.plan_answer_archive(
                repo_root, task, model="gpt-5.2", harness="codex"
            )
            plan.archive_dir.mkdir(parents=True)
            (plan.archive_dir / "existing.md").write_text("existing", encoding="utf-8")

            with self.assertRaises(orchestrator.ArchiveError):
                orchestrator.archive_answer_files(plan)

            self.assertEqual(
                (plan.archive_dir / "existing.md").read_text(encoding="utf-8"),
                "existing",
            )

    def test_run_matrix_records_success_logs_metadata_summary_and_archives_answers(
        self,
    ) -> None:
        command = (
            sys.executable,
            "-c",
            "from pathlib import Path; Path('answer/out.md').write_text('ok'); print('done')",
        )
        with self.make_repo() as repo:
            repo_root = Path(repo)
            plan = self.make_plan(repo_root, command=command)

            matrix = orchestrator.run_matrix(
                repo_root,
                [plan],
                model="gpt-5.2",
                timeout_seconds=5,
                run_id="success-run",
            )
            result = matrix.results[0]
            metadata = json.loads(result.metadata_path.read_text(encoding="utf-8"))
            summary = json.loads(matrix.summary_path.read_text(encoding="utf-8"))

            self.assertEqual(result.status, "success")
            self.assertEqual(result.exit_code, 0)
            self.assertFalse(result.timed_out)
            self.assertEqual(
                result.stdout_log_path.read_text(encoding="utf-8"), "done\n"
            )
            self.assertEqual(result.stderr_log_path.read_text(encoding="utf-8"), "")
            self.assertEqual(
                (plan.archive_dir / "out.md").read_text(encoding="utf-8"), "ok"
            )
            self.assertEqual(metadata["task_id"], "vendor_selection")
            self.assertEqual(metadata["harness"], "codex")
            self.assertEqual(metadata["model"], "gpt-5.2")
            self.assertEqual(metadata["track"], "smoke")
            self.assertEqual(
                metadata["archive_path"], "answers/vendor_selection/gpt-5.2/codex/r1"
            )
            self.assertEqual(metadata["settings"], {})
            self.assertEqual(summary["status_counts"], {"success": 1})
            self.assertEqual(summary["total_attempted"], 1)
            self.assertEqual(summary["total_planned"], 1)
            self.assertTrue(
                (repo_root / "tasks" / "vendor_selection" / "answer").is_dir()
            )
            self.assertFalse(
                (
                    repo_root / "tasks" / "vendor_selection" / "answer" / "out.md"
                ).exists()
            )

    def test_run_matrix_reports_progress_counts_and_current_task(self) -> None:
        success = (
            sys.executable,
            "-c",
            "from pathlib import Path; Path('answer/out.md').write_text('ok')",
        )
        failed = (sys.executable, "-c", "import sys; sys.exit(1)")
        with self.make_repo() as repo:
            repo_root = Path(repo)
            first = self.make_plan(
                repo_root, task_id="vendor_selection", command=success
            )
            second = self.make_plan(
                repo_root, task_id="travel_reimbursement_audit", command=failed
            )
            progress: list[orchestrator.RunProgress] = []

            orchestrator.run_matrix(
                repo_root,
                [first, second],
                model="gpt-5.2",
                timeout_seconds=5,
                run_id="progress-run",
                progress_callback=progress.append,
            )

        self.assertEqual(len(progress), 3)
        self.assertEqual(progress[0].total, 2)
        self.assertEqual(progress[0].completed, 0)
        self.assertEqual(progress[0].succeeded, 0)
        self.assertEqual(progress[0].failed_or_incomplete, 0)
        self.assertEqual(progress[0].current_plan, first)
        self.assertIsNone(progress[0].last_result)

        self.assertEqual(progress[1].completed, 1)
        self.assertEqual(progress[1].succeeded, 1)
        self.assertEqual(progress[1].failed_or_incomplete, 0)
        self.assertEqual(progress[1].current_plan, second)
        self.assertIsNotNone(progress[1].last_result)
        self.assertEqual(progress[1].last_result.task_id, "vendor_selection")
        self.assertEqual(progress[1].last_result.status, "success")

        self.assertEqual(progress[2].completed, 2)
        self.assertEqual(progress[2].succeeded, 1)
        self.assertEqual(progress[2].failed_or_incomplete, 1)
        self.assertIsNone(progress[2].current_plan)
        self.assertIsNotNone(progress[2].last_result)
        self.assertEqual(progress[2].last_result.task_id, "travel_reimbursement_audit")
        self.assertEqual(progress[2].last_result.status, "failed")

    def test_run_metadata_records_harness_settings(self) -> None:
        command = (
            sys.executable,
            "-c",
            "from pathlib import Path; Path('answer/out.md').write_text('ok')",
        )
        with self.make_repo() as repo:
            repo_root = Path(repo)
            plan = self.make_plan(
                repo_root,
                command=command,
                settings={"sandbox": "workspace-write", "approval_policy": "never"},
            )

            matrix = orchestrator.run_matrix(
                repo_root,
                [plan],
                model="gpt-5.2",
                timeout_seconds=5,
                run_id="settings-run",
            )
            metadata = json.loads(
                matrix.results[0].metadata_path.read_text(encoding="utf-8")
            )

            self.assertEqual(metadata["settings"]["sandbox"], "workspace-write")
            self.assertEqual(metadata["settings"]["approval_policy"], "never")

    def test_run_matrix_records_missing_answers_as_incomplete(self) -> None:
        command = (sys.executable, "-c", "print('no answer')")
        with self.make_repo() as repo:
            repo_root = Path(repo)
            plan = self.make_plan(repo_root, command=command)

            matrix = orchestrator.run_matrix(
                repo_root,
                [plan],
                model="gpt-5.2",
                timeout_seconds=5,
                run_id="incomplete-run",
            )
            result = matrix.results[0]

        self.assertEqual(result.status, "incomplete")
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.incomplete_reason, "empty answer directory")

    def test_run_matrix_records_nonzero_exit_as_failure(self) -> None:
        command = (
            sys.executable,
            "-c",
            "import sys; sys.stderr.write('bad\\n'); sys.exit(7)",
        )
        with self.make_repo() as repo:
            repo_root = Path(repo)
            plan = self.make_plan(repo_root, command=command)

            matrix = orchestrator.run_matrix(
                repo_root,
                [plan],
                model="gpt-5.2",
                timeout_seconds=5,
                run_id="failed-run",
            )
            result = matrix.results[0]

            self.assertEqual(result.status, "failed")
            self.assertEqual(result.exit_code, 7)
            self.assertFalse(result.timed_out)
            self.assertEqual(
                result.stderr_log_path.read_text(encoding="utf-8"), "bad\n"
            )

    def test_run_matrix_records_timeout_distinctly(self) -> None:
        command = (sys.executable, "-c", "import time; time.sleep(2)")
        with self.make_repo() as repo:
            repo_root = Path(repo)
            plan = self.make_plan(repo_root, command=command)

            matrix = orchestrator.run_matrix(
                repo_root,
                [plan],
                model="gpt-5.2",
                timeout_seconds=0.1,
                run_id="timeout-run",
            )
            result = matrix.results[0]

        self.assertEqual(result.status, "timed_out")
        self.assertIsNone(result.exit_code)
        self.assertTrue(result.timed_out)

    def test_run_matrix_continues_after_failure_by_default(self) -> None:
        failed = (sys.executable, "-c", "import sys; sys.exit(1)")
        success = (
            sys.executable,
            "-c",
            "from pathlib import Path; Path('answer/out.md').write_text('ok')",
        )
        with self.make_repo() as repo:
            repo_root = Path(repo)
            first = self.make_plan(
                repo_root, task_id="vendor_selection", command=failed
            )
            second = self.make_plan(
                repo_root, task_id="travel_reimbursement_audit", command=success
            )

            matrix = orchestrator.run_matrix(
                repo_root,
                [first, second],
                model="gpt-5.2",
                timeout_seconds=5,
                run_id="continue-run",
            )

        self.assertEqual(
            [result.status for result in matrix.results], ["failed", "success"]
        )
        self.assertFalse(matrix.stopped_after_failure)

    def test_run_matrix_summary_groups_task_derived_tracks(self) -> None:
        command = (
            sys.executable,
            "-c",
            "from pathlib import Path; Path('answer/out.md').write_text('ok')",
        )
        with self.make_repo() as repo:
            repo_root = Path(repo)
            smoke = self.make_plan(
                repo_root, task_id="vendor_selection", command=command
            )
            long_context = self.make_plan(
                repo_root, task_id="clinic_rollout_plan", command=command
            )

            matrix = orchestrator.run_matrix(
                repo_root,
                [smoke, long_context],
                model="gpt-5.2",
                timeout_seconds=5,
                run_id="mixed-track-run",
            )
            summary = json.loads(matrix.summary_path.read_text(encoding="utf-8"))

        self.assertEqual(
            [result.track for result in matrix.results], ["smoke", "long_context"]
        )
        self.assertEqual(summary["track_counts"], {"long_context": 1, "smoke": 1})
        self.assertEqual(
            summary["planned_track_counts"], {"long_context": 1, "smoke": 1}
        )

    def test_run_matrix_can_stop_on_first_failure(self) -> None:
        failed = (sys.executable, "-c", "import sys; sys.exit(1)")
        success = (
            sys.executable,
            "-c",
            "from pathlib import Path; Path('answer/out.md').write_text('ok')",
        )
        with self.make_repo() as repo:
            repo_root = Path(repo)
            first = self.make_plan(
                repo_root, task_id="vendor_selection", command=failed
            )
            second = self.make_plan(
                repo_root, task_id="travel_reimbursement_audit", command=success
            )

            matrix = orchestrator.run_matrix(
                repo_root,
                [first, second],
                model="gpt-5.2",
                timeout_seconds=5,
                run_id="stop-run",
                stop_on_first_failure=True,
            )
            summary = json.loads(matrix.summary_path.read_text(encoding="utf-8"))

        self.assertEqual([result.status for result in matrix.results], ["failed"])
        self.assertTrue(matrix.stopped_after_failure)
        self.assertTrue(summary["stopped_after_failure"])
        self.assertEqual(summary["total_attempted"], 1)
        self.assertEqual(summary["total_planned"], 2)

    def test_run_matrix_captures_json_event_logs_when_stdout_is_json_lines(
        self,
    ) -> None:
        command = (
            sys.executable,
            "-c",
            "from pathlib import Path; Path('answer/out.md').write_text('ok'); print('{\"event\":\"done\"}')",
        )
        with self.make_repo() as repo:
            repo_root = Path(repo)
            plan = self.make_plan(repo_root, command=command)

            matrix = orchestrator.run_matrix(
                repo_root,
                [plan],
                model="gpt-5.2",
                timeout_seconds=5,
                run_id="json-run",
                capture_json_events=True,
            )
            result = matrix.results[0]

            self.assertIsNotNone(result.json_event_log_path)
            assert result.json_event_log_path is not None
            self.assertEqual(
                result.json_event_log_path.read_text(encoding="utf-8"),
                '{"event":"done"}\n',
            )

    def test_run_matrix_records_and_cleans_task_local_scratch_files(self) -> None:
        command = (
            sys.executable,
            "-c",
            "from pathlib import Path; Path('answer/out.md').write_text('ok'); "
            "Path('scratch.md').write_text('scratch'); Path('task.md').write_text('changed')",
        )
        with self.make_repo() as repo:
            repo_root = Path(repo)
            task_dir = repo_root / "tasks" / "vendor_selection"
            plan = self.make_plan(repo_root, command=command)

            matrix = orchestrator.run_matrix(
                repo_root,
                [plan],
                model="gpt-5.2",
                timeout_seconds=5,
                run_id="scratch-run",
            )
            result = matrix.results[0]
            metadata = json.loads(result.metadata_path.read_text(encoding="utf-8"))

            self.assertEqual((task_dir / "task.md").read_text(encoding="utf-8"), "task")
            self.assertFalse((task_dir / "scratch.md").exists())
            self.assertEqual(result.scratch_cleanup.created_paths, ("scratch.md",))
            self.assertEqual(result.scratch_cleanup.modified_paths, ("task.md",))
            self.assertTrue(
                (result.scratch_cleanup.record_dir / "created" / "scratch.md").is_file()
            )
            self.assertTrue(
                (result.scratch_cleanup.record_dir / "modified" / "task.md").is_file()
            )
            self.assertEqual(
                metadata["scratch_cleanup"]["policy"],
                "restore_task_files_outside_answer_after_each_run",
            )


if __name__ == "__main__":
    unittest.main()
