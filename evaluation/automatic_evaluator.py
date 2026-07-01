#!/usr/bin/env python3
"""Deterministic checker for archived SBench answers.

This is a local evaluation helper for the hidden `evaluation/` folder. It checks
archived deliverables under `answers/` against the concrete facts in
`evaluation/expected_answers/`. It is intentionally conservative: it verifies
required files, expected source handling, selected/rejected entities, and key
totals, but it does not attempt to replace the manual rubric for prose quality.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable


REQUIRED_FILES: dict[str, tuple[str, ...]] = {
    "vendor_selection": (
        "source_resolution.md",
        "vendor_screen.md",
        "purchase_recommendation.md",
    ),
    "travel_reimbursement_audit": (
        "policy_application.md",
        "expense_decisions.md",
        "reimbursement_summary.md",
    ),
    "incident_staffing_plan": (
        "access_resolution.md",
        "candidate_screen.md",
        "staffing_assignment.md",
    ),
    "clinic_rollout_plan": (
        "source_resolution.md",
        "clinic_screen.md",
        "launch_recommendation.md",
    ),
    "community_workshop_replan": (
        "initial_room_plan.md",
        "update_response.md",
        "final_room_plan.md",
    ),
    "grant_closeout_recovery": (
        "audit_findings.md",
        "corrected_expense_decisions.md",
        "final_closeout_summary.md",
    ),
    "shelter_restock_scope": (
        "core_purchase_list.md",
        "scope_control.md",
        "final_restock_note.md",
    ),
}


@dataclass(frozen=True)
class RunResult:
    task_id: str
    archive_path: Path
    issues: tuple[str, ...]

    @property
    def passed(self) -> bool:
        return not self.issues

    def to_json(self, repo_root: Path) -> dict[str, object]:
        return {
            "task_id": self.task_id,
            "archive_path": relative_path(self.archive_path, repo_root),
            "status": "pass" if self.passed else "fail",
            "issues": list(self.issues),
        }


FilesByName = dict[str, str]
TaskChecker = Callable[[FilesByName], list[str]]


def normalize(value: str) -> str:
    normalized = value.lower()
    normalized = normalized.replace("\u2011", "-")
    normalized = normalized.replace("\u2012", "-")
    normalized = normalized.replace("\u2013", "-")
    normalized = normalized.replace("\u2014", "-")
    normalized = normalized.replace("\u00a0", " ")
    for char in "$,`*_":
        normalized = normalized.replace(char, "")
    return re.sub(r"\s+", " ", normalized).strip()


def has(text: str, *terms: str) -> bool:
    normalized = normalize(text)
    return all(normalize(term) in normalized for term in terms)


def has_any(text: str, *terms: str) -> bool:
    return any(has(text, term) for term in terms)


def matching_lines(text: str, term: str, *, context: int = 1) -> str:
    lines = text.splitlines()
    normalized_term = normalize(term)
    matches: list[str] = []
    for index, line in enumerate(lines):
        if normalized_term not in normalize(line):
            continue
        start = max(0, index - context)
        end = min(len(lines), index + context + 1)
        matches.extend(lines[start:end])
    return "\n".join(matches)


def add_issue(issues: list[str], condition: bool, message: str) -> None:
    if not condition:
        issues.append(message)


def require_terms(
    issues: list[str], text: str, terms: Iterable[str], *, prefix: str
) -> None:
    for term in terms:
        add_issue(issues, has(text, term), f"{prefix} missing {term}")


def vendor_selection(files: FilesByName) -> list[str]:
    issues: list[str] = []
    source = files["source_resolution.md"]
    screen = files["vendor_screen.md"]
    recommendation = files["purchase_recommendation.md"]

    require_terms(
        issues,
        source,
        (
            "northstar_update_2026-04-30.md",
            "178",
            "12",
            "2026-05-16",
            "10.1",
            "11",
            "rugged",
            "warranty",
        ),
        prefix="source_resolution.md",
    )
    add_issue(
        issues,
        has_any(source, "vendor_quotes.csv", "stale", "2026-04-24"),
        "source_resolution.md does not identify the stale Northstar conflict",
    )

    for vendor in ("Northstar", "Atlas", "BrightPath", "Cobalt", "Dockside"):
        add_issue(issues, has(screen, vendor), f"vendor_screen.md missing {vendor}")
    add_issue(
        issues,
        has_any(matching_lines(screen, "Northstar"), "yes", "eligible")
        and has(matching_lines(screen, "Northstar"), "2136"),
        "vendor_screen.md does not clearly accept Northstar at total cost 2136",
    )
    expected_rejections = {
        "Atlas": "delivery",
        "BrightPath": "screen",
        "Cobalt": "battery",
        "Dockside": "11",
    }
    for vendor, reason in expected_rejections.items():
        add_issue(
            issues,
            has(matching_lines(screen, vendor), reason),
            f"vendor_screen.md missing expected {vendor} rejection reason",
        )

    require_terms(
        issues,
        recommendation,
        ("Northstar", "12", "178", "2136", "2200", "2026-05-16"),
        prefix="purchase_recommendation.md",
    )
    return issues


def travel_reimbursement_audit(files: FilesByName) -> list[str]:
    issues: list[str] = []
    policy = files["policy_application.md"]
    decisions = files["expense_decisions.md"]
    summary = files["reimbursement_summary.md"]

    add_issue(
        issues,
        has(policy, "current_policy.md"),
        "policy_application.md missing current_policy.md",
    )
    add_issue(
        issues,
        has_any(
            policy, "stale_policy_excerpt.md", "stale excerpt", "older travel policy"
        ),
        "policy_application.md does not say current policy supersedes stale policy",
    )
    require_terms(
        issues,
        policy,
        ("75", "preapproval", "alcohol", "20", "supplies"),
        prefix="policy_application.md",
    )
    add_issue(
        issues,
        has(policy, "440") or (has(policy, "220") and has(policy, "2")),
        "policy_application.md missing lodging cap basis",
    )

    expected_decisions = {
        "T-001": ("approved", "480"),
        "T-002": ("rejected", "45", "0"),
        "T-003": ("partial", "440", "70"),
        "T-004": ("partial", "58", "18"),
        "T-005": ("partial", "60", "10"),
        "T-006": ("rejected", "82", "0"),
        "T-007": ("approved", "18"),
    }
    for expense_id, terms in expected_decisions.items():
        row = matching_lines(decisions, expense_id)
        add_issue(issues, bool(row), f"expense_decisions.md missing {expense_id}")
        for term in terms:
            add_issue(
                issues,
                has(row, term),
                f"expense_decisions.md {expense_id} missing {term}",
            )

    require_terms(
        issues,
        summary,
        ("1056", "225", "T-001", "T-007", "T-003", "T-004", "T-005", "T-002", "T-006"),
        prefix="reimbursement_summary.md",
    )
    return issues


def incident_staffing_plan(files: FilesByName) -> list[str]:
    issues: list[str] = []
    access = files["access_resolution.md"]
    candidates = files["candidate_screen.md"]
    assignment = files["staffing_assignment.md"]

    add_issue(
        issues,
        has(access, "access_update_2026-05-04.md"),
        "access_resolution.md missing access_update_2026-05-04.md",
    )
    expected_access = {
        "Asha": "active",
        "Ben": "active",
        "Carmen": "suspended",
        "Deepa": "active",
        "Eli": "active",
        "Farah": "active",
    }
    for responder, status in expected_access.items():
        add_issue(
            issues,
            has(matching_lines(access, responder), status),
            f"access_resolution.md {responder} missing {status}",
        )
    add_issue(
        issues,
        has_any(matching_lines(access, "Gabe"), "not provisioned", "none", "no active"),
        "access_resolution.md Gabe status is not clear",
    )

    require_terms(
        issues,
        candidates,
        ("2026-05-06", "18:00", "22:00"),
        prefix="candidate_screen.md",
    )
    for responder in ("Asha", "Ben", "Carmen", "Deepa", "Eli", "Farah", "Gabe"):
        add_issue(
            issues,
            has(candidates, responder),
            f"candidate_screen.md missing {responder}",
        )
    add_issue(
        issues,
        has(matching_lines(candidates, "Ben"), "yes")
        or has(matching_lines(candidates, "Ben"), "eligible"),
        "candidate_screen.md does not mark Ben eligible",
    )
    add_issue(
        issues,
        has(matching_lines(candidates, "Deepa"), "no")
        and has(matching_lines(candidates, "Deepa"), "yes"),
        "candidate_screen.md does not show Deepa as no-primary/yes-backup",
    )
    expected_reasons = {
        "Asha": ("active incidents", "limit", ">=2"),
        "Carmen": ("suspended", "access"),
        "Eli": ("incident manager", "role"),
        "Farah": ("20:00", "full"),
        "Gabe": ("not provisioned", "no active", "access", "none"),
    }
    for responder, reasons in expected_reasons.items():
        add_issue(
            issues,
            has_any(matching_lines(candidates, responder), *reasons),
            f"candidate_screen.md missing expected {responder} rejection reason",
        )

    require_terms(
        issues,
        assignment,
        ("INC-4472", "2026-05-06", "18:00", "22:00", "Ben", "Deepa"),
        prefix="staffing_assignment.md",
    )
    return issues


def clinic_rollout_plan(files: FilesByName) -> list[str]:
    issues: list[str] = []
    source = files["source_resolution.md"]
    screen = files["clinic_screen.md"]
    recommendation = files["launch_recommendation.md"]

    require_terms(
        issues,
        source,
        ("01_selection_rules.md", "newest", "04_storage_update_2026-05-06.md"),
        prefix="source_resolution.md",
    )
    expected_statuses = {
        "N-101": "certified",
        "N-102": "certified",
        "N-103": "certified",
        "N-104": "suspended",
        "N-105": "certified",
        "N-106": "certified",
        "N-107": "pending",
        "S-201": "certified",
    }
    for clinic_id, status in expected_statuses.items():
        add_issue(
            issues,
            has(matching_lines(source, clinic_id), status),
            f"source_resolution.md {clinic_id} missing status {status}",
        )
    for marker in ("archived", "future", "optional"):
        add_issue(
            issues,
            has(source, marker),
            f"source_resolution.md missing non-controlling {marker} source note",
        )

    expected_screen = {
        "N-101": ("yes", "7400"),
        "N-102": ("yes", "6450"),
        "N-103": ("no",),
        "N-104": ("no",),
        "N-105": ("no",),
        "N-106": ("yes", "4950"),
        "N-107": ("no",),
        "S-201": ("no",),
    }
    for clinic_id, terms in expected_screen.items():
        row = matching_lines(screen, clinic_id)
        add_issue(issues, bool(row), f"clinic_screen.md missing {clinic_id}")
        for term in terms:
            add_issue(
                issues,
                has(row, term),
                f"clinic_screen.md {clinic_id} missing {term}",
            )
    require_terms(
        issues,
        screen,
        ("18800", "20000"),
        prefix="clinic_screen.md",
    )

    require_terms(
        issues,
        recommendation,
        (
            "Maple",
            "SwiftRoute",
            "2026-06-06",
            "7400",
            "Riverbend",
            "NorthLine",
            "2026-06-07",
            "6450",
            "Hillcrest",
            "Valley Freight",
            "4950",
            "18800",
            "1200",
            "MJ-14",
        ),
        prefix="launch_recommendation.md",
    )
    for rejected in ("Pine Ridge", "Lakeside", "Cedar", "Old Mill", "South Gate"):
        add_issue(
            issues,
            has(recommendation, rejected),
            f"launch_recommendation.md missing rejected clinic {rejected}",
        )
    return issues


def community_workshop_replan(files: FilesByName) -> list[str]:
    issues: list[str] = []
    initial = files["initial_room_plan.md"]
    update = files["update_response.md"]
    final = files["final_room_plan.md"]

    expected_initial = {
        "S-101": "Harbor Hall",
        "S-102": "Bay Workshop",
        "S-103": "Elm Room",
    }
    for session_id, room in expected_initial.items():
        add_issue(
            issues,
            has(matching_lines(initial, session_id), room),
            f"initial_room_plan.md {session_id} is not assigned to {room}",
        )
    require_terms(issues, initial, ("675", "800"), prefix="initial_room_plan.md")

    require_terms(
        issues,
        update,
        (
            "05_facility_update_2026-06-10.md",
            "Bay Workshop",
            "floor repair",
            "Harbor Hall",
            "Elm Room",
            "Delta Annex",
            "70",
            "745",
        ),
        prefix="update_response.md",
    )

    expected_final = {
        "S-101": "Harbor Hall",
        "S-102": "Delta Annex",
        "S-103": "Elm Room",
    }
    for session_id, room in expected_final.items():
        add_issue(
            issues,
            has(matching_lines(final, session_id), room),
            f"final_room_plan.md {session_id} is not assigned to {room}",
        )
    require_terms(issues, final, ("745", "55", "800"), prefix="final_room_plan.md")
    return issues


def grant_closeout_recovery(files: FilesByName) -> list[str]:
    issues: list[str] = []
    findings = files["audit_findings.md"]
    decisions = files["corrected_expense_decisions.md"]
    summary = files["final_closeout_summary.md"]

    require_terms(
        issues,
        findings,
        (
            "G-001",
            "980",
            "G-003",
            "420",
            "G-004",
            "1600",
            "03_award_update_2026-05-22.md",
            "G-002",
            "120",
            "G-005",
            "receipt",
            "G-006",
            "68",
        ),
        prefix="audit_findings.md",
    )
    for outcome_fact in ("140", "36"):
        add_issue(
            issues,
            has(findings, outcome_fact) or has(summary, outcome_fact),
            f"outcome fact missing {outcome_fact}",
        )

    expected_decisions = {
        "G-001": ("approve", "980"),
        "G-002": ("120",),
        "G-003": ("approve", "420"),
        "G-004": ("reject", "0"),
        "G-005": ("reject", "0"),
        "G-006": ("approve", "68"),
    }
    for expense_id, terms in expected_decisions.items():
        row = matching_lines(decisions, expense_id)
        add_issue(
            issues, bool(row), f"corrected_expense_decisions.md missing {expense_id}"
        )
        for term in terms:
            add_issue(
                issues,
                has(row, term),
                f"corrected_expense_decisions.md {expense_id} missing {term}",
            )

    require_terms(
        issues,
        summary,
        (
            "1588",
            "1600",
            "12",
            "G-001",
            "G-003",
            "G-004",
            "140",
            "36",
            "G-002",
            "G-005",
            "G-006",
            "18",
        ),
        prefix="final_closeout_summary.md",
    )
    return issues


def shelter_restock_scope(files: FilesByName) -> list[str]:
    issues: list[str] = []
    core = files["core_purchase_list.md"]
    scope = files["scope_control.md"]
    note = files["final_restock_note.md"]

    expected_core = {
        "R-101": ("yes", "480"),
        "R-102": ("yes", "900"),
        "R-103": ("yes", "420"),
        "R-104": ("no",),
        "R-105": ("no",),
        "R-106": ("yes", "330"),
    }
    for request_id, terms in expected_core.items():
        row = matching_lines(core, request_id)
        add_issue(issues, bool(row), f"core_purchase_list.md missing {request_id}")
        for term in terms:
            add_issue(
                issues,
                has(row, term),
                f"core_purchase_list.md {request_id} missing {term}",
            )
    require_terms(issues, core, ("2130", "70", "2200"), prefix="core_purchase_list.md")

    require_terms(
        issues,
        scope,
        (
            "phase 1",
            "North Shelter",
            "medical",
            "shelter",
            "power",
            "water",
            "budget",
            "banner",
            "volunteer",
            "drone",
        ),
        prefix="scope_control.md",
    )
    add_issue(
        issues,
        has_any(scope, "phase-two", "phase two"),
        "scope_control.md missing phase-two deferral",
    )

    final_note_checks = {
        "selected first aid": has_any(note, "R-101", "first aid"),
        "selected blankets": has_any(note, "R-102", "thermal blankets"),
        "selected lanterns": has_any(note, "R-103", "LED lanterns"),
        "selected water jugs": has_any(note, "R-106", "water storage"),
        "excluded banner": has_any(note, "R-104", "banner"),
        "excluded drone": has_any(note, "R-105", "drone"),
        "total 2130": has(note, "2130"),
        "remaining 70": has(note, "70"),
    }
    for label, condition in final_note_checks.items():
        add_issue(issues, condition, f"final_restock_note.md missing {label}")
    add_issue(
        issues,
        has_any(note, "defer", "out of scope", "secondary"),
        "final_restock_note.md deferral is not clear",
    )
    return issues


TASK_CHECKERS: dict[str, TaskChecker] = {
    "vendor_selection": vendor_selection,
    "travel_reimbursement_audit": travel_reimbursement_audit,
    "incident_staffing_plan": incident_staffing_plan,
    "clinic_rollout_plan": clinic_rollout_plan,
    "community_workshop_replan": community_workshop_replan,
    "grant_closeout_recovery": grant_closeout_recovery,
    "shelter_restock_scope": shelter_restock_scope,
}


def relative_path(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def discover_archives(
    task_answers_dir: Path, required_files: tuple[str, ...]
) -> list[Path]:
    required = set(required_files)
    archives: list[Path] = []
    if not task_answers_dir.is_dir():
        return archives
    for path in sorted(task_answers_dir.rglob("*")):
        if not path.is_dir():
            continue
        child_files = {child.name for child in path.iterdir() if child.is_file()}
        if child_files & required:
            archives.append(path)
    return archives


def evaluate_archive(task_id: str, archive_path: Path) -> RunResult:
    required_files = REQUIRED_FILES[task_id]
    files: FilesByName = {}
    issues: list[str] = []
    for filename in required_files:
        path = archive_path / filename
        if not path.is_file():
            files[filename] = ""
            issues.append(f"missing file: {filename}")
            continue
        files[filename] = path.read_text(encoding="utf-8", errors="replace")

    if not issues:
        issues.extend(TASK_CHECKERS[task_id](files))

    return RunResult(task_id=task_id, archive_path=archive_path, issues=tuple(issues))


def evaluate_answers(repo_root: Path, task_ids: Iterable[str]) -> list[RunResult]:
    answers_root = repo_root / "answers"
    results: list[RunResult] = []
    for task_id in task_ids:
        required_files = REQUIRED_FILES[task_id]
        for archive_path in discover_archives(answers_root / task_id, required_files):
            results.append(evaluate_archive(task_id, archive_path))
    return results


def render_text(results: list[RunResult], repo_root: Path) -> str:
    by_task: dict[str, list[RunResult]] = {task_id: [] for task_id in REQUIRED_FILES}
    for result in results:
        by_task.setdefault(result.task_id, []).append(result)

    total_passed = sum(1 for result in results if result.passed)
    lines = ["Automatic Evaluation Summary"]
    for task_id in REQUIRED_FILES:
        task_results = by_task.get(task_id, [])
        if not task_results:
            lines.append(f"{task_id}: 0/0 archived runs found")
            continue
        passed = sum(1 for result in task_results if result.passed)
        lines.append(f"{task_id}: {passed}/{len(task_results)} pass")
    lines.append(f"total: {total_passed}/{len(results)} pass")

    failures = [result for result in results if not result.passed]
    if not failures:
        lines.append("")
        lines.append("No issues found.")
        return "\n".join(lines)

    lines.append("")
    lines.append("Runs With Issues")
    for result in failures:
        archive_path = relative_path(result.archive_path, repo_root)
        lines.append(f"- {archive_path}: {len(result.issues)} issue(s)")
        for issue in result.issues:
            lines.append(f"  - {issue}")
    return "\n".join(lines)


def render_json(results: list[RunResult], repo_root: Path) -> str:
    total_passed = sum(1 for result in results if result.passed)
    task_summary: dict[str, dict[str, int]] = {}
    for task_id in REQUIRED_FILES:
        task_results = [result for result in results if result.task_id == task_id]
        task_summary[task_id] = {
            "passed": sum(1 for result in task_results if result.passed),
            "total": len(task_results),
        }
    payload = {
        "summary": {
            "passed": total_passed,
            "total": len(results),
            "failed": len(results) - total_passed,
            "tasks": task_summary,
        },
        "results": [result.to_json(repo_root) for result in results],
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate archived SBench answers against deterministic expected facts."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root containing answers/ and evaluation/.",
    )
    parser.add_argument(
        "--task",
        action="append",
        choices=tuple(REQUIRED_FILES),
        help="Task ID to evaluate. May be passed multiple times. Defaults to all tasks.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of text.",
    )
    parser.add_argument(
        "--fail-on-issues",
        action="store_true",
        help="Exit with status 1 when any archive fails deterministic checks.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    repo_root = args.repo_root.resolve()
    task_ids = args.task or list(REQUIRED_FILES)
    answers_root = repo_root / "answers"
    if not answers_root.is_dir():
        print(f"answers directory not found: {answers_root}", file=sys.stderr)
        return 2

    results = evaluate_answers(repo_root, task_ids)
    output = (
        render_json(results, repo_root)
        if args.json
        else render_text(results, repo_root)
    )
    print(output)

    has_issues = any(not result.passed for result in results)
    if args.fail_on_issues and has_issues:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
