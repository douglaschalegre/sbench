"""Regression checks for deterministic evaluation of equivalent answers."""

from pathlib import Path

import pytest

from evaluation.automatic_evaluator import (
    community_workshop_replan,
    evaluate_archive,
    grant_closeout_recovery,
    travel_reimbursement_audit,
)


ROOT = Path(__file__).resolve().parents[1]
LUNA_ANSWERS = ROOT / "answers"
MODEL = "openai__gpt-6-luna"


def archive_files(task: str, harness: str, names: tuple[str, ...]) -> dict[str, str]:
    archive = LUNA_ANSWERS / task / MODEL / harness / "r1"
    return {name: (archive / name).read_text(encoding="utf-8") for name in names}


@pytest.mark.parametrize(
    ("task", "harness"),
    [
        ("community_workshop_replan", "bdi"),
        ("grant_closeout_recovery", "codex"),
        ("travel_reimbursement_audit", "bdi"),
        ("travel_reimbursement_audit", "codex"),
        ("travel_reimbursement_audit", "opencode"),
    ],
)
def test_semantically_complete_luna_answers_pass(task: str, harness: str) -> None:
    archive = LUNA_ANSWERS / task / MODEL / harness / "r1"
    result = evaluate_archive(task, archive)
    assert result.issues == ()


def test_travel_policy_requires_correct_source_and_effective_date() -> None:
    files = archive_files(
        "travel_reimbursement_audit",
        "codex",
        ("policy_application.md", "expense_decisions.md", "reimbursement_summary.md"),
    )
    policy = files["policy_application.md"]
    files["policy_application.md"] = policy.replace("2026-04-20", "2026-03-01")
    assert any("controlling policy date" in issue for issue in travel_reimbursement_audit(files))

    files["policy_application.md"] = policy.replace("2026-05-01", "2026-06-01")
    assert any("effective date" in issue for issue in travel_reimbursement_audit(files))


def test_replan_requires_correct_final_assignment() -> None:
    files = archive_files(
        "community_workshop_replan",
        "bdi",
        ("initial_room_plan.md", "update_response.md", "final_room_plan.md"),
    )
    files["final_room_plan.md"] = files["final_room_plan.md"].replace(
        "| S-102 - Inventory Lab (16, afternoon) | Delta Annex |",
        "| S-102 - Inventory Lab (16, afternoon) | Bay Workshop |",
    )
    assert any("S-102 is not assigned to Delta Annex" in issue for issue in community_workshop_replan(files))


def test_replan_accepts_closes_as_closure_wording() -> None:
    archive = LUNA_ANSWERS / "community_workshop_replan" / "openai__gpt-5.4" / "codex" / "r3"
    assert evaluate_archive("community_workshop_replan", archive).issues == ()


def test_grant_decisions_require_omitted_expense() -> None:
    files = archive_files(
        "grant_closeout_recovery",
        "codex",
        ("audit_findings.md", "corrected_expense_decisions.md", "final_closeout_summary.md"),
    )
    files["corrected_expense_decisions.md"] = "\n".join(
        line for line in files["corrected_expense_decisions.md"].splitlines()
        if not line.startswith("| G-006 |")
    )
    assert any("missing G-006" in issue for issue in grant_closeout_recovery(files))

