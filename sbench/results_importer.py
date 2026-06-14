from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Sequence

from .tasks import task_track


TOKEN_COLUMNS = (
    "token_total",
    "token_input",
    "token_output",
    "token_cached_input",
    "token_cache_read",
    "token_cache_write",
    "token_reasoning",
    "token_audio_input",
    "token_audio_output",
    "llm_calls",
    "tool_calls",
)


@dataclass
class TokenUsage:
    available: bool = False
    source: str | None = None
    token_total: int | None = None
    token_input: int | None = None
    token_output: int | None = None
    token_cached_input: int | None = None
    token_cache_read: int | None = None
    token_cache_write: int | None = None
    token_reasoning: int | None = None
    token_audio_input: int | None = None
    token_audio_output: int | None = None
    llm_calls: int | None = None
    tool_calls: int | None = None

    def add(self, other: "TokenUsage") -> None:
        for column in TOKEN_COLUMNS:
            value = getattr(other, column)
            if value is not None:
                current = getattr(self, column)
                setattr(self, column, value if current is None else current + value)
        self.available = self.available or other.available


@dataclass
class ImportResult:
    execution_count: int
    warning_count: int


@dataclass
class ImportContext:
    repo_root: Path
    run_id: str
    metadata_path: Path
    metadata: dict[str, object]
    warnings: list[tuple[str, str]] = field(default_factory=list)

    @property
    def execution_id(self) -> str:
        archive_run = Path(str(self.metadata.get("archive_path", "unknown/r0"))).name
        return execution_id(
            self.run_id,
            str(self.metadata["task_id"]),
            str(self.metadata["harness"]),
            archive_run,
        )

    def warn(self, code: str, message: str) -> None:
        self.warnings.append((code, message))


def create_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS executions (
            execution_id TEXT PRIMARY KEY,
            run_id TEXT NOT NULL,
            task_id TEXT NOT NULL,
            track TEXT NOT NULL,
            harness TEXT NOT NULL,
            model TEXT NOT NULL,
            archive_run TEXT NOT NULL,
            status TEXT NOT NULL,
            timed_out INTEGER NOT NULL,
            timeout_seconds REAL,
            elapsed_seconds REAL,
            elapsed_bucket TEXT NOT NULL,
            archive_path TEXT,
            metadata_path TEXT NOT NULL,
            stdout_log_path TEXT,
            stderr_log_path TEXT,
            archived_file_count INTEGER NOT NULL,
            deliverables_present INTEGER,
            token_usage_available INTEGER NOT NULL DEFAULT 0,
            token_usage_source TEXT,
            token_total INTEGER,
            token_input INTEGER,
            token_output INTEGER,
            token_cached_input INTEGER,
            token_cache_read INTEGER,
            token_cache_write INTEGER,
            token_reasoning INTEGER,
            token_audio_input INTEGER,
            token_audio_output INTEGER,
            llm_calls INTEGER,
            tool_calls INTEGER
        );

        CREATE TABLE IF NOT EXISTS execution_items (
            execution_id TEXT NOT NULL,
            item TEXT NOT NULL,
            PRIMARY KEY (execution_id, item),
            FOREIGN KEY (execution_id) REFERENCES executions(execution_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS import_warnings (
            execution_id TEXT NOT NULL,
            code TEXT NOT NULL,
            message TEXT NOT NULL,
            PRIMARY KEY (execution_id, code, message),
            FOREIGN KEY (execution_id) REFERENCES executions(execution_id) ON DELETE CASCADE
        );
        """
    )


def import_run_records(repo_root: Path, database_path: Path | str) -> ImportResult:
    repo_root = repo_root.resolve()
    with sqlite3.connect(database_path) as connection:
        create_schema(connection)
        count = 0
        warnings = 0
        for metadata_path in discover_metadata_files(repo_root):
            context = load_import_context(repo_root, metadata_path)
            row = build_execution_row(context)
            upsert_execution(connection, row)
            replace_items(connection, row["execution_id"], transaction_items(row))
            replace_warnings(connection, row["execution_id"], context.warnings)
            count += 1
            warnings += len(context.warnings)
        return ImportResult(execution_count=count, warning_count=warnings)


def discover_metadata_files(repo_root: Path) -> list[Path]:
    runs_root = repo_root / "runs"
    if not runs_root.is_dir():
        return []
    return sorted(runs_root.glob("*/entries/*/*/*/metadata.json"))


def load_import_context(repo_root: Path, metadata_path: Path) -> ImportContext:
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    relative = metadata_path.relative_to(repo_root)
    run_id = relative.parts[1]
    return ImportContext(
        repo_root=repo_root,
        run_id=run_id,
        metadata_path=metadata_path,
        metadata=metadata,
    )


def build_execution_row(context: ImportContext) -> dict[str, object]:
    metadata = context.metadata
    archive_path = str(metadata.get("archive_path") or "")
    archive_run = Path(archive_path).name if archive_path else "unknown"
    task_id = str(metadata["task_id"])
    harness = str(metadata["harness"])
    archived_paths = [str(path) for path in metadata.get("archived_paths", [])]
    deliverables = detect_deliverables_present(context, archived_paths)
    token_usage = parse_token_usage(context, harness)
    if not token_usage.available:
        context.warn(
            "token_usage_missing", f"No token usage was found for {harness} logs."
        )

    row: dict[str, object] = {
        "execution_id": execution_id(context.run_id, task_id, harness, archive_run),
        "run_id": context.run_id,
        "task_id": task_id,
        "track": str(metadata.get("track") or task_track(task_id)),
        "harness": harness,
        "model": str(metadata.get("model") or ""),
        "archive_run": archive_run,
        "status": str(metadata.get("status") or "unknown"),
        "timed_out": bool(metadata.get("timed_out")),
        "timeout_seconds": metadata.get("timeout_seconds"),
        "elapsed_seconds": metadata.get("elapsed_seconds"),
        "elapsed_bucket": elapsed_bucket(metadata.get("elapsed_seconds")),
        "archive_path": archive_path or None,
        "metadata_path": display_path(context.metadata_path, context.repo_root),
        "stdout_log_path": metadata.get("stdout_log_path"),
        "stderr_log_path": metadata.get("stderr_log_path"),
        "archived_file_count": len(archived_paths),
        "deliverables_present": deliverables,
        "token_usage_available": token_usage.available,
        "token_usage_source": token_usage.source,
    }
    for column in TOKEN_COLUMNS:
        row[column] = getattr(token_usage, column)
    return row


def execution_id(run_id: str, task_id: str, harness: str, archive_run: str) -> str:
    return f"{run_id}:{task_id}:{harness}:{archive_run}"


def elapsed_bucket(value: object) -> str:
    seconds = as_float(value)
    if seconds is None:
        return "elapsed:unknown"
    if seconds < 60:
        return "elapsed:<1m"
    if seconds < 300:
        return "elapsed:1-5m"
    if seconds < 600:
        return "elapsed:5-10m"
    return "elapsed:>=10m"


def detect_deliverables_present(
    context: ImportContext, archived_paths: Sequence[str]
) -> int | None:
    contract_path = (
        context.repo_root
        / "tasks"
        / str(context.metadata["task_id"])
        / "output_contract.md"
    )
    required = required_deliverables(contract_path)
    if required is None:
        context.warn(
            "deliverable_contract_unknown",
            f"Cannot determine required deliverables from {contract_path}.",
        )
        return None

    archived = {Path(path).name for path in archived_paths if path}
    return int(all(Path(path).name in archived for path in required))


def required_deliverables(contract_path: Path) -> tuple[str, ...] | None:
    if not contract_path.is_file():
        return None
    text = contract_path.read_text(encoding="utf-8")
    matches = tuple(dict.fromkeys(re.findall(r"`answer/([^`]+)`", text)))
    return matches or None


def parse_token_usage(context: ImportContext, harness: str) -> TokenUsage:
    stdout_path = resolve_log_path(context, "stdout_log_path")
    if stdout_path is None or not stdout_path.is_file():
        context.warn(
            "stdout_log_missing",
            "stdout log is missing; token usage may be incomplete.",
        )
        return TokenUsage(source=f"{harness}:unavailable")
    lines = stdout_path.read_text(encoding="utf-8", errors="replace").splitlines()
    if harness == "bdi":
        return parse_bdi_tokens(lines, context)
    if harness == "codex":
        return parse_codex_tokens(lines, context)
    if harness == "opencode":
        return parse_opencode_tokens(lines, context)
    return TokenUsage(source=f"{harness}:unsupported")


def resolve_log_path(context: ImportContext, field: str) -> Path | None:
    value = context.metadata.get(field)
    if not value:
        return None
    path = Path(str(value))
    return path if path.is_absolute() else context.repo_root / path


def parse_bdi_tokens(lines: Sequence[str], context: ImportContext) -> TokenUsage:
    events = parse_json_lines(lines, context, warn_malformed=False)
    aggregates: list[TokenUsage] = []
    agent_completed: list[TokenUsage] = []
    for event in events:
        usage = usage_from_mapping(find_usage_mapping(event))
        if not usage.available:
            continue
        event_name = str(event.get("event") or event.get("type") or "").lower()
        if "agent" in event_name and "complete" in event_name:
            agent_completed.append(usage)
        else:
            aggregates.append(usage)
    if aggregates:
        result = aggregates[-1]
        result.source = "bdi:aggregate_run_event"
        return result
    if agent_completed:
        result = TokenUsage(available=True, source="bdi:per_agent_completed_events")
        for usage in agent_completed:
            result.add(usage)
        return result
    return TokenUsage(source="bdi:unavailable")


def parse_codex_tokens(lines: Sequence[str], context: ImportContext) -> TokenUsage:
    result = TokenUsage(source="codex:turn_completed_events")
    for event in parse_json_lines(lines, context, warn_malformed=True):
        event_name = str(
            event.get("event") or event.get("type") or event.get("msg") or ""
        ).lower()
        if "turn" not in event_name and "complete" not in event_name:
            continue
        usage = usage_from_mapping(find_usage_mapping(event))
        if usage.available:
            result.add(usage)
            result.llm_calls = (result.llm_calls or 0) + 1
    if result.available:
        result.token_total = derive_total(result)
    else:
        result.source = "codex:unavailable"
    return result


def parse_opencode_tokens(lines: Sequence[str], context: ImportContext) -> TokenUsage:
    result = TokenUsage(source="opencode:step_completed_events")
    for event in parse_json_lines(lines, context, warn_malformed=True):
        event_name = str(event.get("event") or event.get("type") or "").lower()
        if "step" not in event_name and "complete" not in event_name:
            continue
        usage = usage_from_mapping(find_usage_mapping(event))
        if usage.available:
            result.add(usage)
            result.llm_calls = (result.llm_calls or 0) + 1
    if result.available:
        result.token_total = derive_total(result)
    else:
        result.source = "opencode:unavailable"
    return result


def parse_json_lines(
    lines: Sequence[str], context: ImportContext, *, warn_malformed: bool
) -> list[dict[str, object]]:
    events: list[dict[str, object]] = []
    for index, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or not stripped.startswith("{"):
            continue
        try:
            payload = json.loads(stripped)
        except json.JSONDecodeError:
            if warn_malformed:
                context.warn(
                    "malformed_json_log_line", f"Malformed JSON in stdout line {index}."
                )
            continue
        if isinstance(payload, dict):
            events.append(payload)
    return events


def find_usage_mapping(value: object) -> dict[str, object] | None:
    if isinstance(value, dict):
        for key in ("usage", "token_usage", "tokens"):
            nested = value.get(key)
            if isinstance(nested, dict):
                return nested
        if any(normalize_usage_key(key) for key in value):
            return value
        for nested in value.values():
            found = find_usage_mapping(nested)
            if found is not None:
                return found
    elif isinstance(value, list):
        for nested in value:
            found = find_usage_mapping(nested)
            if found is not None:
                return found
    return None


def usage_from_mapping(mapping: dict[str, object] | None) -> TokenUsage:
    usage = TokenUsage()
    if mapping is None:
        return usage
    for key, value in mapping.items():
        column = normalize_usage_key(str(key))
        if column is None:
            continue
        number = as_int(value)
        if number is not None:
            setattr(usage, column, number)
            usage.available = True
    if usage.available:
        usage.token_total = (
            usage.token_total if usage.token_total is not None else derive_total(usage)
        )
    return usage


def normalize_usage_key(key: str) -> str | None:
    normalized = re.sub(r"[^a-z0-9]+", "_", key.lower()).strip("_")
    return {
        "total": "token_total",
        "total_tokens": "token_total",
        "input": "token_input",
        "input_tokens": "token_input",
        "prompt_tokens": "token_input",
        "output": "token_output",
        "output_tokens": "token_output",
        "completion_tokens": "token_output",
        "cached_input": "token_cached_input",
        "cached_input_tokens": "token_cached_input",
        "cache_read": "token_cache_read",
        "cache_read_tokens": "token_cache_read",
        "cache_creation_input_tokens": "token_cache_write",
        "cache_write": "token_cache_write",
        "cache_write_tokens": "token_cache_write",
        "reasoning": "token_reasoning",
        "reasoning_tokens": "token_reasoning",
        "audio": "token_audio_input",
        "audio_input": "token_audio_input",
        "audio_input_tokens": "token_audio_input",
        "audio_output": "token_audio_output",
        "audio_output_tokens": "token_audio_output",
        "llm_calls": "llm_calls",
        "tool_calls": "tool_calls",
    }.get(normalized)


def derive_total(usage: TokenUsage) -> int | None:
    parts = [usage.token_input, usage.token_output]
    if any(value is not None for value in parts):
        return sum(value or 0 for value in parts)
    return usage.token_total


def transaction_items(row: dict[str, object]) -> set[str]:
    items = {
        f"task:{row['task_id']}",
        f"track:{row['track']}",
        f"harness:{row['harness']}",
        f"status:{row['status']}",
        f"timeout:{str(bool(row['timed_out'])).lower()}",
        str(row["elapsed_bucket"]),
        f"archived_files:{count_bucket(row.get('archived_file_count'))}",
    }
    deliverables = row.get("deliverables_present")
    if deliverables is None:
        items.add("deliverables:unknown")
    else:
        items.add(f"deliverables:{'present' if deliverables else 'missing'}")

    if row.get("token_usage_available"):
        items.add("tokens:available")
        items.add(f"token_total:{token_bucket(row.get('token_total'))}")
        if (
            row.get("token_cache_read") is not None
            or row.get("token_cache_write") is not None
            or row.get("token_cached_input") is not None
        ):
            items.add("cache_tokens:available")
        if row.get("llm_calls") is not None:
            items.add(f"llm_calls:{count_bucket(row.get('llm_calls'))}")
        if row.get("tool_calls") is not None:
            items.add(f"tool_calls:{count_bucket(row.get('tool_calls'))}")
    else:
        items.add("tokens:unavailable")
    return items


def count_bucket(value: object) -> str:
    number = as_int(value)
    if number is None:
        return "unknown"
    if number == 0:
        return "0"
    if number <= 2:
        return "1-2"
    if number <= 5:
        return "3-5"
    return ">5"


def token_bucket(value: object) -> str:
    number = as_int(value)
    if number is None:
        return "unknown"
    if number == 0:
        return "0"
    if number < 1_000:
        return "1-999"
    if number < 10_000:
        return "1k-10k"
    return ">=10k"


def upsert_execution(connection: sqlite3.Connection, row: dict[str, object]) -> None:
    columns = tuple(row.keys())
    assignments = ", ".join(
        f"{column}=excluded.{column}" for column in columns if column != "execution_id"
    )
    connection.execute(
        f"""
        INSERT INTO executions ({", ".join(columns)})
        VALUES ({", ".join("?" for _ in columns)})
        ON CONFLICT(execution_id) DO UPDATE SET {assignments}
        """,
        tuple(row[column] for column in columns),
    )


def replace_items(
    connection: sqlite3.Connection, execution_id: str, items: Iterable[str]
) -> None:
    connection.execute(
        "DELETE FROM execution_items WHERE execution_id = ?", (execution_id,)
    )
    connection.executemany(
        "INSERT INTO execution_items (execution_id, item) VALUES (?, ?)",
        [(execution_id, item) for item in sorted(items)],
    )


def replace_warnings(
    connection: sqlite3.Connection,
    execution_id: str,
    warnings: Sequence[tuple[str, str]],
) -> None:
    connection.execute(
        "DELETE FROM import_warnings WHERE execution_id = ?", (execution_id,)
    )
    connection.executemany(
        "INSERT INTO import_warnings (execution_id, code, message) VALUES (?, ?, ?)",
        [(execution_id, code, message) for code, message in warnings],
    )


def as_int(value: object) -> int | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str) and value.strip().isdigit():
        return int(value)
    return None


def as_float(value: object) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int | float):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


def display_path(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)
