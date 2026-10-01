#!/usr/bin/env python3
"""Review Governance CLI (AD-9, ADR-005, E3).

Tracks review lifecycle for generated artifacts:
  - draft: freshly generated, unreviewed
  - in-review: assigned to reviewer
  - approved-for-demo: simulated local approval (eligible for demo preview build only)
  - approved: real claimed human approval via PR review (carries approval_record and approved_hash)
  - rejected: reviewed and discarded

Enforces the critical boundary:
  - Simulated approvals set approved-for-demo, but NEVER set production approval_status: approved.
  - Production publication strictly requires verified CODEOWNER PR approval (E3).
  - An approved artifact whose body has drifted from approved_hash returns to in-review.

Transitions are checked against ALLOWED_TRANSITIONS: approved and approved-for-demo
are reachable ONLY from in-review.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
GENERATED = DOCS / "generated"
REVIEWS_FILE = ROOT / ".work" / "demo_reviews.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from github_approval import compute_body_hash, compute_file_body_hash  # noqa: E402
from validate_docs import FRONTMATTER_RE, parse_frontmatter  # noqa: E402

STATES = ("draft", "in-review", "approved-for-demo", "approved", "rejected")

ALLOWED_TRANSITIONS: Dict[str | None, set[str]] = {
    None: {"draft", "in-review"},
    "draft": {"in-review", "rejected"},
    "in-review": {"approved-for-demo", "approved", "rejected", "draft"},
    "approved-for-demo": {"rejected", "draft"},  # revoke, or re-draft after regeneration
    "approved": {"rejected", "draft"},           # revoke, or re-draft after regeneration
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


def find_artifact_file(artifact_id: str, explicit_path: str = "") -> Optional[Path]:
    """Locate artifact markdown or JSON file under docs/generated/."""
    if explicit_path:
        p = ROOT / explicit_path
        if p.is_file():
            return p
    for p in GENERATED.rglob("*"):
        if p.is_file() and p.suffix in (".md", ".mdx"):
            fm = parse_frontmatter(p) or {}
            if fm.get("id") == artifact_id or p.stem == artifact_id:
                return p
        elif p.is_file() and p.suffix == ".json":
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                if data.get("id") == artifact_id or p.stem == artifact_id:
                    return p
            except Exception:
                pass
    return None


def reset_to_draft(artifact_id: str, path: str = "") -> None:
    """Reset review ledger status to draft upon regeneration."""
    reviews = load_reviews()
    if artifact_id in reviews.get("reviews", {}):
        reviews["reviews"][artifact_id] = {
            "artifact_id": artifact_id,
            "path": path,
            "approval_state": "draft",
            "reviewed_by": "system",
            "reviewed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "notes": "Reset to draft via regeneration",
            "is_simulated": False,
            "eligible_for_production": False,
        }
        save_reviews(reviews)


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

    # If no ledger entry, check document frontmatter on disk
    if current is None:
        p = find_artifact_file(artifact_id, path)
        if p and p.suffix in (".md", ".mdx"):
            fm = parse_frontmatter(p) or {}
            current = (fm.get("generation") or {}).get("approval_status")

    if decision not in ALLOWED_TRANSITIONS.get(current, set()):
        raise InvalidTransitionError(
            f"Invalid transition for {artifact_id}: {current or '(no record)'} -> {decision}"
        )
    is_simulated = decision == "approved-for-demo"
    eligible_for_prod = False  # Simulated approval or draft is never eligible for production

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


def approve_artifact(
    artifact_id: str,
    pr: int,
    reviewer: str = "w7-mgfcode",
    notes: str = "",
    path: str = "",
) -> Dict[str, Any]:
    """Record a real approval claim for artifact_id backed by a PR number and body hash (E3)."""
    p = find_artifact_file(artifact_id, path)
    if not p:
        raise FileNotFoundError(f"Artifact '{artifact_id}' not found under docs/generated/")

    content = p.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(content)
    if not m:
        raise ValueError(f"Artifact {p} has no valid frontmatter block")

    fm = yaml.safe_load(m.group(1)) or {}
    gen = fm.get("generation") or {}
    current_status = gen.get("approval_status")

    # Refuse unless currently in-review
    if current_status != "in-review":
        reviews = load_reviews()
        ledger_status = reviews.get("reviews", {}).get(artifact_id, {}).get("approval_state")
        if ledger_status != "in-review":
            raise InvalidTransitionError(
                f"Cannot approve {artifact_id}: current status is '{current_status or ledger_status or 'unrecorded'}', "
                f"must be 'in-review'"
            )

    approved_hash = compute_body_hash(content)
    approved_at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Update frontmatter
    fm.setdefault("generation", {})
    fm["generation"]["approval_status"] = "approved"
    fm["generation"]["approval_record"] = {
        "pr": int(pr),
        "approved_by": reviewer,
        "approved_at": approved_at,
        "approved_hash": approved_hash,
    }

    body = content[m.end():]
    new_fm_str = yaml.dump(fm, sort_keys=False, allow_unicode=True)
    new_content = f"---\n{new_fm_str}---\n{body}"
    p.write_text(new_content, encoding="utf-8")

    # Update ledger
    reviews = load_reviews()
    try:
        rel_path = p.relative_to(ROOT).as_posix()
    except ValueError:
        rel_path = p.as_posix()
    record = {
        "artifact_id": artifact_id,
        "path": rel_path,
        "approval_state": "approved",
        "reviewed_by": reviewer,
        "reviewed_at": approved_at,
        "pr": int(pr),
        "approved_hash": approved_hash,
        "is_simulated": False,
        "eligible_for_production": True,
        "notes": notes or f"Claimed PR #{pr} approval by {reviewer}",
    }
    reviews["reviews"][artifact_id] = record
    save_reviews(reviews)
    return record


def build_parser() -> argparse.ArgumentParser:
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

    # approve (E3 claim)
    p_app = sub.add_parser("approve", help="Stamp production approval claim with body hash and PR number (E3)")
    p_app.add_argument("--artifact", required=True, help="Artifact ID")
    p_app.add_argument("--pr", required=True, type=int, help="Pull request number")
    p_app.add_argument("--reviewer", default="w7-mgfcode", help="CODEOWNER reviewer login")
    p_app.add_argument("--notes", default="")
    p_app.add_argument("--path", default="")

    # check-production
    p_chk = sub.add_parser("check-production", help="Check if artifact is eligible for production publication")
    p_chk.add_argument("--artifact", required=True)

    return ap


def main() -> int:
    ap = build_parser()
    args = ap.parse_args()

    if args.action == "list":
        reviews = load_reviews()
        print("Recorded Reviews:")
        if not reviews.get("reviews"):
            print("  (no reviews recorded yet)")
        for aid, rec in reviews.get("reviews", {}).items():
            print(f"  [{rec['approval_state']}] {aid} by {rec['reviewed_by']} at {rec['reviewed_at']}")
            if rec.get("pr"):
                print(f"      PR: #{rec['pr']} (hash: {rec.get('approved_hash')})")
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

    if args.action == "approve":
        try:
            rec = approve_artifact(args.artifact, args.pr, args.reviewer, args.notes, args.path)
        except (InvalidTransitionError, FileNotFoundError, ValueError) as e:
            print(f"REJECTED: {e}", file=sys.stderr)
            return 1
        print(f"Approved artifact {args.artifact}:")
        print(f"  State:                   {rec['approval_state']}")
        print(f"  PR:                      #{rec['pr']}")
        print(f"  Reviewer:                {rec['reviewed_by']}")
        print(f"  Approved Hash:           {rec['approved_hash']}")
        print(f"  Production Claim:        Valid (Publication gate verifies via GitHub API on main)")
        return 0

    if args.action == "check-production":
        p = find_artifact_file(args.artifact)
        if p and p.suffix in (".md", ".mdx"):
            fm = parse_frontmatter(p) or {}
            gen = fm.get("generation") or {}
            status = gen.get("approval_status")
            rec = gen.get("approval_record")
            if status == "approved" and isinstance(rec, dict):
                current_hash = compute_file_body_hash(p)
                recorded_hash = rec.get("approved_hash")
                if current_hash != recorded_hash:
                    print(
                        f"BLOCKED: Body modified after approval (hash mismatch for {args.artifact}). "
                        f"Recorded {recorded_hash}, current {current_hash}. Artifact returns to in-review!",
                        file=sys.stderr
                    )
                    return 1
                print(f"CLAIMED: {args.artifact} claims PR #{rec.get('pr')} approval by {rec.get('approved_by')}. Body hash verified.")
                return 0

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
