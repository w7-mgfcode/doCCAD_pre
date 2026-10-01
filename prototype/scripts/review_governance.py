#!/usr/bin/env python3
"""Review Governance CLI (AD-9).

Tracks review lifecycle for generated artifacts:
  - draft: freshly generated, unreviewed
  - in-review: assigned to reviewer
  - approved-for-demo: simulated local approval (eligible for demo preview build only)
  - rejected: reviewed and discarded

Enforces the critical boundary:
  Simulated approvals set approved-for-demo, but NEVER set production approval_status: approved.
  Production eligibility requires verified human PR approval.

Transitions are checked against ALLOWED_TRANSITIONS: approved-for-demo is reachable only
from in-review, so no artifact skips review; a rejected artifact must be re-drafted first.
"""

from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
REVIEWS_FILE = ROOT / ".work" / "demo_reviews.json"

STATES = ("draft", "in-review", "approved-for-demo", "rejected")
# None = no ledger record yet. A generated page is already a draft on disk, so review may start
# at in-review directly (the README's CLI walkthrough does).
ALLOWED_TRANSITIONS: Dict[str | None, set[str]] = {
    None: {"draft", "in-review"},
    "draft": {"in-review", "rejected"},
    "in-review": {"approved-for-demo", "rejected", "draft"},
    "approved-for-demo": {"rejected", "draft"},  # revoke, or re-draft after regeneration
    "rejected": {"draft"},
}


class InvalidTransitionError(ValueError):
    """A review decision that the lifecycle does not allow from the current state."""


def load_reviews() -> Dict[str, Any]:
    if REVIEWS_FILE.is_file():
        try:
            return json.loads(REVIEWS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"reviews": {}}


def save_reviews(data: Dict[str, Any]) -> None:
    REVIEWS_FILE.parent.mkdir(parents=True, exist_ok=True)
    REVIEWS_FILE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def set_review_status(
    artifact_id: str,
    decision: str,
    reviewer: str = "local-engineer",
    notes: str = "",
    path: str = "",
) -> Dict[str, Any]:
    if decision not in STATES:
        raise ValueError(f"Invalid decision state: {decision}")

    reviews = load_reviews()
    current = reviews["reviews"].get(artifact_id, {}).get("approval_state")
    if decision not in ALLOWED_TRANSITIONS.get(current, set()):
        raise InvalidTransitionError(
            f"Invalid transition for {artifact_id}: {current or '(no record)'} -> {decision}"
        )
    is_simulated = decision == "approved-for-demo"
    eligible_for_prod = False  # Simulated approval is never eligible for production

    record = {
        "artifact_id": artifact_id,
        "path": path,
        "approval_state": decision,
        "reviewed_by": reviewer,
        "reviewed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "notes": notes or f"Set to {decision} via review_governance CLI",
        "is_simulated": is_simulated,
        "eligible_for_production": eligible_for_prod,
    }
    reviews["reviews"][artifact_id] = record
    save_reviews(reviews)
    return record


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="action", required=True)

    # list
    sub.add_parser("list", help="List review records")

    # review
    p_rev = sub.add_parser("review", help="Record a review decision")
    p_rev.add_argument("--artifact", required=True, help="Artifact ID")
    p_rev.add_argument("--decision", required=True, choices=STATES)
    p_rev.add_argument("--reviewer", default="local-evaluator")
    p_rev.add_argument("--notes", default="")
    p_rev.add_argument("--path", default="")

    # check-production
    p_chk = sub.add_parser("check-production", help="Check if artifact is eligible for production publication")
    p_chk.add_argument("--artifact", required=True)

    args = ap.parse_args()

    if args.action == "list":
        reviews = load_reviews()
        print("Recorded Demo Reviews:")
        if not reviews.get("reviews"):
            print("  (no reviews recorded yet)")
        for aid, rec in reviews.get("reviews", {}).items():
            print(f"  [{rec['approval_state']}] {aid} by {rec['reviewed_by']} at {rec['reviewed_at']}")
            if rec.get("notes"):
                print(f"      Notes: {rec['notes']}")
        return 0

    if args.action == "review":
        try:
            rec = set_review_status(args.artifact, args.decision, args.reviewer, args.notes, args.path)
        except InvalidTransitionError as e:
            print(f"REJECTED: {e}", file=sys.stderr)
            return 1
        print(f"Updated review status for {args.artifact}:")
        print(f"  State:                   {rec['approval_state']}")
        print(f"  Simulated Approval:      {rec['is_simulated']}")
        print(f"  Production Eligible:     {rec['eligible_for_production']}")
        return 0

    if args.action == "check-production":
        reviews = load_reviews()
        rec = reviews.get("reviews", {}).get(args.artifact)
        if not rec:
            print(f"REJECTED: No review record found for {args.artifact}", file=sys.stderr)
            return 1
        if rec.get("is_simulated", True):
            print(f"BLOCKED: {args.artifact} only has simulated demo approval ({rec.get('approval_state')}). It is NOT eligible for production publication build!", file=sys.stderr)
            return 1
        if rec.get("approval_state") != "approved":
            print(f"BLOCKED: {args.artifact} status is {rec.get('approval_state')}, not approved.", file=sys.stderr)
            return 1
        print(f"APPROVED: {args.artifact} is verified and eligible for production publication.")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
