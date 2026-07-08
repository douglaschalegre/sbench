from __future__ import annotations

import json
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from sbench import results_importer


class ResultsImporterTest(unittest.TestCase):
    def make_repo(self) -> tempfile.TemporaryDirectory[str]:
        temp_dir = tempfile.TemporaryDirectory()
        repo_root = Path(temp_dir.name)
        task_dir = repo_root / "tasks" / "vendor_selection"
        task_dir.mkdir(parents=True)
        (task_dir / "task.md").write_text("task", encoding="utf-8")
        (task_dir / "output_contract.md").write_text(
            "# Contract\n\n## `answer/source_resolution.md`\n## `answer/vendor_screen.md`\n",
            encoding="utf-8",
        )
        return temp_dir

    def write_entry(
        self,
        repo_root: Path,
        *,
        run_id: str = "run-1",
        task_id: str = "vendor_selection",
        harness: str = "codex",
        archive_run: str = "r1",
        stdout: str = "",
        archived_paths: list[str] | None = None,
        elapsed_seconds: float = 61.0,
        status: str = "success",
    ) -> Path:
        record_dir = (
            repo_root / "runs" / run_id / "entries" / task_id / harness / archive_run
        )
        record_dir.mkdir(parents=True)
        (record_dir / "stdout.log").write_text(stdout, encoding="utf-8")
        (record_dir / "stderr.log").write_text("", encoding="utf-8")
        metadata = {
            "task_id": task_id,
            "track": "smoke",
            "harness": harness,
            "model": "gpt-5.2",
            "status": status,
            "timed_out": status == "timed_out",
            "timeout_seconds": 600,
            "elapsed_seconds": elapsed_seconds,
            "archive_path": f"answers/{task_id}/gpt-5.2/{harness}/{archive_run}",
            "archived_paths": archived_paths
            if archived_paths is not None
            else [
                f"answers/{task_id}/gpt-5.2/{harness}/{archive_run}/source_resolution.md",
                f"answers/{task_id}/gpt-5.2/{harness}/{archive_run}/vendor_screen.md",
            ],
            "stdout_log_path": str((record_dir / "stdout.log").relative_to(repo_root)),
            "stderr_log_path": str((record_dir / "stderr.log").relative_to(repo_root)),
            "metadata_path": str((record_dir / "metadata.json").relative_to(repo_root)),
        }
        (record_dir / "metadata.json").write_text(
            json.dumps(metadata), encoding="utf-8"
        )
        return record_dir / "metadata.json"

    def write_automatic_evaluator(self, repo_root: Path) -> None:
        evaluator_dir = repo_root / "evaluation"
        evaluator_dir.mkdir(parents=True)
        (evaluator_dir / "automatic_evaluator.py").write_text(
            "REQUIRED_FILES = {'vendor_selection': ('source_resolution.md',)}\n"
            "\n"
            "class Result:\n"
            "    def __init__(self, issues):\n"
            "        self.issues = issues\n"
            "\n"
            "def evaluate_archive(task_id, archive_path):\n"
            "    text = (archive_path / 'source_resolution.md').read_text(encoding='utf-8')\n"
            "    return Result(()) if 'PASS' in text else Result(('missing PASS',))\n",
            encoding="utf-8",
        )

    def write_answer_archive(
        self, repo_root: Path, *, archive_run: str, source_text: str
    ) -> None:
        archive_dir = (
            repo_root
            / "answers"
            / "vendor_selection"
            / "gpt-5.2"
            / "codex"
            / archive_run
        )
        archive_dir.mkdir(parents=True)
        (archive_dir / "source_resolution.md").write_text(source_text, encoding="utf-8")

    def rows(self, database_path: Path, table: str) -> list[sqlite3.Row]:
        connection = sqlite3.connect(database_path)
        connection.row_factory = sqlite3.Row
        try:
            return list(connection.execute(f"SELECT * FROM {table} ORDER BY 1"))
        finally:
            connection.close()

    def item_names(self, database_path: Path) -> set[str]:
        return {row["item"] for row in self.rows(database_path, "execution_items")}

    def test_issue_015_imports_common_execution_rows_idempotently(self) -> None:
        with self.make_repo() as repo:
            repo_root = Path(repo)
            database_path = repo_root / "results.sqlite"
            self.write_entry(repo_root, elapsed_seconds=30.0)

            first = results_importer.import_run_records(repo_root, database_path)
            second = results_importer.import_run_records(repo_root, database_path)
            rows = self.rows(database_path, "executions")

        self.assertEqual(first.execution_count, 1)
        self.assertEqual(second.execution_count, 1)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["execution_id"], "run-1:vendor_selection:codex:r1")
        self.assertEqual(rows[0]["elapsed_bucket"], "elapsed:<1m")
        self.assertEqual(rows[0]["archived_file_count"], 2)
        self.assertEqual(
            rows[0]["stdout_log_path"],
            "runs/run-1/entries/vendor_selection/codex/r1/stdout.log",
        )

    def test_issue_016_detects_deliverables_present_missing_and_unknown(self) -> None:
        with self.make_repo() as repo:
            repo_root = Path(repo)
            database_path = repo_root / "results.sqlite"
            self.write_entry(repo_root, archive_run="r1")
            self.write_entry(
                repo_root,
                archive_run="r2",
                archived_paths=[
                    "answers/vendor_selection/gpt-5.2/codex/r2/source_resolution.md"
                ],
            )
            (repo_root / "tasks" / "vendor_selection" / "output_contract.md").unlink()
            self.write_entry(repo_root, archive_run="r3")

            results_importer.import_run_records(repo_root, database_path)
            values = {
                row["archive_run"]: row["deliverables_present"]
                for row in self.rows(database_path, "executions")
            }
            items = self.item_names(database_path)

        self.assertEqual(values, {"r1": None, "r2": None, "r3": None})
        self.assertIn("deliverables:unknown", items)
        self.assertIn("archived_files:1-2", items)

    def test_issue_016_detects_all_present_and_partially_present_when_contract_exists(
        self,
    ) -> None:
        with self.make_repo() as repo:
            repo_root = Path(repo)
            database_path = repo_root / "results.sqlite"
            self.write_entry(repo_root, archive_run="r1")
            self.write_entry(
                repo_root,
                archive_run="r2",
                archived_paths=[
                    "answers/vendor_selection/gpt-5.2/codex/r2/source_resolution.md"
                ],
            )

            results_importer.import_run_records(repo_root, database_path)
            values = {
                row["archive_run"]: row["deliverables_present"]
                for row in self.rows(database_path, "executions")
            }

        self.assertEqual(values, {"r1": 1, "r2": 0})

    def test_imports_automatic_evaluation_summary_without_issue_items(self) -> None:
        with self.make_repo() as repo:
            repo_root = Path(repo)
            database_path = repo_root / "results.sqlite"
            self.write_automatic_evaluator(repo_root)
            self.write_entry(repo_root, archive_run="r1")
            self.write_answer_archive(repo_root, archive_run="r1", source_text="PASS")
            self.write_entry(repo_root, archive_run="r2")
            self.write_answer_archive(repo_root, archive_run="r2", source_text="wrong")
            self.write_entry(repo_root, archive_run="r3")

            results_importer.import_run_records(repo_root, database_path)
            rows = {
                row["archive_run"]: row
                for row in self.rows(database_path, "executions")
            }
            items = self.item_names(database_path)

        self.assertEqual(rows["r1"]["automatic_evaluation_status"], "pass")
        self.assertEqual(rows["r1"]["automatic_evaluation_issue_count"], 0)
        self.assertEqual(
            rows["r1"]["automatic_evaluation_source"],
            "evaluation/automatic_evaluator.py",
        )
        self.assertEqual(rows["r2"]["automatic_evaluation_status"], "fail")
        self.assertEqual(rows["r2"]["automatic_evaluation_issue_count"], 1)
        self.assertEqual(rows["r3"]["automatic_evaluation_status"], "unavailable")
        self.assertEqual(rows["r3"]["automatic_evaluation_issue_count"], 0)
        self.assertEqual(
            rows["r3"]["automatic_evaluation_source"],
            "evaluation/automatic_evaluator.py:archive_missing",
        )
        self.assertIn("auto_eval:pass", items)
        self.assertIn("auto_eval:fail", items)
        self.assertIn("auto_eval:unavailable", items)
        self.assertFalse(any(item.startswith("auto_eval_issues:") for item in items))

    def test_create_schema_migrates_existing_executions_table_for_automatic_evaluation(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as repo:
            database_path = Path(repo) / "results.sqlite"
            with closing(sqlite3.connect(database_path)) as connection:
                with connection:
                    connection.execute(
                        "CREATE TABLE executions (execution_id TEXT PRIMARY KEY)"
                    )
                    results_importer.create_schema(connection)
                    columns = {
                        row[1]
                        for row in connection.execute("PRAGMA table_info(executions)")
                    }

        self.assertIn("automatic_evaluation_status", columns)
        self.assertIn("automatic_evaluation_issue_count", columns)
        self.assertIn("automatic_evaluation_source", columns)

    def test_issue_017_imports_bdi_aggregate_fallback_and_no_token_logs(self) -> None:
        with self.make_repo() as repo:
            repo_root = Path(repo)
            database_path = repo_root / "results.sqlite"
            self.write_entry(
                repo_root,
                harness="bdi",
                archive_run="r1",
                stdout=json.dumps(
                    {
                        "event": "run_completed",
                        "usage": {
                            "total_tokens": 10,
                            "input_tokens": 4,
                            "output_tokens": 6,
                            "cache_read_tokens": 0,
                            "cache_write_tokens": 2,
                            "audio_input_tokens": 0,
                            "llm_calls": 1,
                            "tool_calls": 3,
                        },
                    }
                ),
            )
            self.write_entry(
                repo_root,
                harness="bdi",
                archive_run="r2",
                stdout="\n".join(
                    [
                        json.dumps(
                            {
                                "event": "agent_completed",
                                "usage": {"input_tokens": 1, "output_tokens": 2},
                            }
                        ),
                        json.dumps(
                            {
                                "event": "agent_completed",
                                "usage": {"input_tokens": 3, "output_tokens": 4},
                            }
                        ),
                    ]
                ),
            )
            self.write_entry(
                repo_root, harness="bdi", archive_run="r3", stdout="no token events"
            )

            results_importer.import_run_records(repo_root, database_path)
            rows = {
                row["archive_run"]: row
                for row in self.rows(database_path, "executions")
            }

        self.assertEqual(rows["r1"]["token_usage_source"], "bdi:aggregate_run_event")
        self.assertEqual(rows["r1"]["token_cache_read"], 0)
        self.assertEqual(rows["r1"]["token_audio_output"], None)
        self.assertEqual(
            rows["r2"]["token_usage_source"], "bdi:per_agent_completed_events"
        )
        self.assertEqual(rows["r2"]["token_total"], 10)
        self.assertEqual(rows["r3"]["token_usage_available"], 0)

    def test_issue_018_imports_codex_turn_usage(self) -> None:
        with self.make_repo() as repo:
            repo_root = Path(repo)
            database_path = repo_root / "results.sqlite"
            self.write_entry(
                repo_root,
                harness="codex",
                stdout=json.dumps(
                    {
                        "type": "turn_completed",
                        "usage": {
                            "input_tokens": 100,
                            "cached_input_tokens": 25,
                            "output_tokens": 40,
                            "reasoning_tokens": 7,
                        },
                    }
                ),
            )

            results_importer.import_run_records(repo_root, database_path)
            row = self.rows(database_path, "executions")[0]

        self.assertEqual(row["token_usage_source"], "codex:turn_completed_events")
        self.assertEqual(row["token_total"], 140)
        self.assertEqual(row["token_cached_input"], 25)
        self.assertEqual(row["token_reasoning"], 7)
        self.assertEqual(row["llm_calls"], 1)

    def test_issue_019_imports_opencode_mixed_stdout_step_usage(self) -> None:
        with self.make_repo() as repo:
            repo_root = Path(repo)
            database_path = repo_root / "results.sqlite"
            self.write_entry(
                repo_root,
                harness="opencode",
                stdout="noise\n"
                + json.dumps(
                    {
                        "event": "step_completed",
                        "tokens": {"input": 5, "output": 6, "reasoning": 1},
                    }
                )
                + "\n"
                + json.dumps(
                    {
                        "event": "step_completed",
                        "tokens": {
                            "input": 7,
                            "output": 8,
                            "cache_read": 2,
                            "cache_write": 3,
                        },
                    }
                ),
            )

            results_importer.import_run_records(repo_root, database_path)
            row = self.rows(database_path, "executions")[0]

        self.assertEqual(row["token_usage_source"], "opencode:step_completed_events")
        self.assertEqual(row["token_total"], 26)
        self.assertEqual(row["token_reasoning"], 1)
        self.assertEqual(row["token_cache_read"], 2)
        self.assertEqual(row["llm_calls"], 2)

    def test_issue_020_generates_stable_transaction_items_and_replaces_stale_items(
        self,
    ) -> None:
        with self.make_repo() as repo:
            repo_root = Path(repo)
            database_path = repo_root / "results.sqlite"
            self.write_entry(
                repo_root,
                stdout=json.dumps(
                    {
                        "type": "turn_completed",
                        "usage": {"input_tokens": 600, "output_tokens": 500},
                    }
                ),
            )
            results_importer.import_run_records(repo_root, database_path)
            execution = self.rows(database_path, "executions")[0]["execution_id"]
            with closing(sqlite3.connect(database_path)) as connection:
                with connection:
                    connection.execute(
                        "INSERT INTO execution_items (execution_id, item) VALUES (?, ?)",
                        (execution, "stale:old"),
                    )
            results_importer.import_run_records(repo_root, database_path)
            items = self.item_names(database_path)

        self.assertIn("task:vendor_selection", items)
        self.assertIn("track:smoke", items)
        self.assertIn("harness:codex", items)
        self.assertIn("status:success", items)
        self.assertIn("timeout:false", items)
        self.assertIn("elapsed:1-1.5m", items)
        self.assertIn("deliverables:present", items)
        self.assertIn("tokens:available", items)
        self.assertIn("token_total:1k-10k", items)
        self.assertIn("llm_calls:1-2", items)
        self.assertNotIn("stale:old", items)

    def test_issue_020_generates_granular_elapsed_buckets(self) -> None:
        self.assertEqual(results_importer.elapsed_bucket(30), "elapsed:<1m")
        self.assertEqual(results_importer.elapsed_bucket(60), "elapsed:1-1.5m")
        self.assertEqual(results_importer.elapsed_bucket(90), "elapsed:1.5-2m")
        self.assertEqual(results_importer.elapsed_bucket(120), "elapsed:2-3m")
        self.assertEqual(results_importer.elapsed_bucket(180), "elapsed:3-5m")
        self.assertEqual(results_importer.elapsed_bucket(300), "elapsed:>=5m")

    def test_issue_020_generates_granular_token_total_buckets(self) -> None:
        with self.make_repo() as repo:
            repo_root = Path(repo)
            database_path = repo_root / "results.sqlite"
            self.write_entry(
                repo_root,
                archive_run="r1",
                stdout=json.dumps(
                    {
                        "type": "turn_completed",
                        "usage": {"input_tokens": 10_000, "output_tokens": 5_000},
                    }
                ),
            )
            self.write_entry(
                repo_root,
                archive_run="r2",
                stdout=json.dumps(
                    {
                        "type": "turn_completed",
                        "usage": {"input_tokens": 20_000, "output_tokens": 10_000},
                    }
                ),
            )
            self.write_entry(
                repo_root,
                archive_run="r3",
                stdout=json.dumps(
                    {
                        "type": "turn_completed",
                        "usage": {"input_tokens": 50_000, "output_tokens": 25_000},
                    }
                ),
            )
            self.write_entry(
                repo_root,
                archive_run="r4",
                stdout=json.dumps(
                    {
                        "type": "turn_completed",
                        "usage": {"input_tokens": 100_000, "output_tokens": 25_000},
                    }
                ),
            )

            results_importer.import_run_records(repo_root, database_path)
            items = self.item_names(database_path)

        self.assertIn("token_total:10k-25k", items)
        self.assertIn("token_total:25k-50k", items)
        self.assertIn("token_total:50k-100k", items)
        self.assertIn("token_total:>=100k", items)
        self.assertNotIn("token_total:>=10k", items)

    def test_issue_021_records_nonfatal_import_diagnostics_and_replaces_stale_warnings(
        self,
    ) -> None:
        with self.make_repo() as repo:
            repo_root = Path(repo)
            database_path = repo_root / "results.sqlite"
            metadata_path = self.write_entry(repo_root, stdout="{bad json\n")
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            metadata["stdout_log_path"] = (
                "runs/run-1/entries/vendor_selection/codex/r1/missing.log"
            )
            metadata_path.write_text(json.dumps(metadata), encoding="utf-8")

            results_importer.import_run_records(repo_root, database_path)
            metadata["stdout_log_path"] = (
                "runs/run-1/entries/vendor_selection/codex/r1/stdout.log"
            )
            (repo_root / "tasks" / "vendor_selection" / "output_contract.md").unlink()
            metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
            results_importer.import_run_records(repo_root, database_path)
            warnings = {
                (row["code"], row["message"])
                for row in self.rows(database_path, "import_warnings")
            }

        self.assertTrue(any(code == "malformed_json_log_line" for code, _ in warnings))
        self.assertTrue(
            any(code == "deliverable_contract_unknown" for code, _ in warnings)
        )
        self.assertTrue(any(code == "token_usage_missing" for code, _ in warnings))
        self.assertFalse(any(code == "stdout_log_missing" for code, _ in warnings))

    def test_issue_022_imports_representative_cross_harness_entries_end_to_end(
        self,
    ) -> None:
        with self.make_repo() as repo:
            repo_root = Path(repo)
            database_path = repo_root / "results.sqlite"
            self.write_entry(
                repo_root,
                harness="bdi",
                archive_run="r1",
                stdout=json.dumps(
                    {
                        "event": "run_completed",
                        "usage": {"input_tokens": 1, "output_tokens": 1},
                    }
                ),
            )
            self.write_entry(
                repo_root,
                harness="codex",
                archive_run="r1",
                stdout=json.dumps(
                    {
                        "type": "turn_completed",
                        "usage": {
                            "input_tokens": 2,
                            "output_tokens": 2,
                            "reasoning_tokens": 1,
                        },
                    }
                ),
            )
            self.write_entry(
                repo_root,
                harness="opencode",
                archive_run="r1",
                stdout=json.dumps(
                    {
                        "event": "step_completed",
                        "tokens": {"input": 3, "output": 3, "cache_read": 1},
                    }
                ),
            )

            first = results_importer.import_run_records(repo_root, database_path)
            second = results_importer.import_run_records(repo_root, database_path)
            rows = self.rows(database_path, "executions")
            items = self.rows(database_path, "execution_items")

        self.assertEqual(first.execution_count, 3)
        self.assertEqual(second.execution_count, 3)
        self.assertEqual(len(rows), 3)
        self.assertEqual({row["harness"] for row in rows}, {"bdi", "codex", "opencode"})
        self.assertTrue(all(row["token_usage_available"] for row in rows))
        self.assertGreaterEqual(len(items), 3)


if __name__ == "__main__":
    unittest.main()
