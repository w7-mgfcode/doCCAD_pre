#!/usr/bin/env python3
"""Build filter for Demo Preview vs Production Publication builds.

Modes:
  --mode demo:
      Restores all demo-approved fixtures and draft views into docs/generated/
      for a rich local demonstration.

  --mode production:
      Strictly enforces publication integrity: excludes unapproved drafts and
      simulated-only approvals (approved-for-demo). Stashes them under
      .work/stashed_unapproved/ so the production build compiles only verified canon
      and genuine human-approved derived content.
      Verifies real approved views via GitHub Approval Verifier (E3):
      - Verification negatives (unmerged PR, hash mismatch, missing review) exclude the page.
      - API / permission errors fail the build immediately.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, Optional

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SOURCE = DOCS / "source"
GENERATED = DOCS / "generated"
WORK = ROOT / ".work"
STASH = WORK / "stashed_unapproved"
STASH_PRIVATE = WORK / "stashed_private"
REVIEWS_FILE = WORK / "demo_reviews.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from github_approval import (  # noqa: E402
    ApprovalVerifier,
    ApiPermissionError,
    VerificationNegative,
)
from validate_docs import parse_frontmatter  # noqa: E402


def restore_stashed() -> None:
    """Restore any previously stashed unapproved or private files back."""
    if STASH.is_dir():
        for f in STASH.rglob("*"):
            if f.is_file():
                rel = f.relative_to(STASH)
                target = GENERATED / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, target)
        shutil.rmtree(STASH)

    if (STASH_PRIVATE / "source").is_dir():
        for f in (STASH_PRIVATE / "source").rglob("*"):
            if f.is_file():
                rel = f.relative_to(STASH_PRIVATE / "source")
                target = SOURCE / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, target)
        shutil.rmtree(STASH_PRIVATE)


def filter_for_production(verifier: Optional[ApprovalVerifier] = None, require_api: bool = False) -> int:
    """Scan docs/source/ and docs/generated/ to exclude private content and unapproved drafts."""
    restore_stashed()
    STASH.mkdir(parents=True, exist_ok=True)
    STASH_PRIVATE.mkdir(parents=True, exist_ok=True)

    reviews: Dict[str, Any] = {}
    if REVIEWS_FILE.is_file():
        try:
            reviews = json.loads(REVIEWS_FILE.read_text(encoding="utf-8")).get("reviews", {})
        except Exception:
            pass

    stashed_count = 0

    # 1. Exclude private canonical documents under docs/source/
    for page in list(SOURCE.rglob("*")):
        if not page.is_file() or page.suffix not in (".md", ".mdx"):
            continue
        fm = parse_frontmatter(page) or {}
        visibility = fm.get("visibility") or fm.get("privacy")
        # Absent visibility or privacy fails closed to private (T12, NV-REQ-028)
        if visibility != "public":
            rel = page.relative_to(SOURCE)
            dest = STASH_PRIVATE / "source" / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(page), str(dest))
            stashed_count += 1
            print(f"  [production filter] Excluded private canonical document: {rel}")

    # 2. Exclude unapproved, simulated, or private generated documents under docs/generated/
    verifier_instance = verifier or ApprovalVerifier()

    for page in list(GENERATED.rglob("*")):
        if not page.is_file() or page.suffix not in (".md", ".mdx", ".json"):
            continue

        fm = parse_frontmatter(page) if page.suffix in (".md", ".mdx") else {}
        doc_id = fm.get("id") if fm else page.stem
        gen_block = (fm.get("generation") or {}) if fm else {}

        # Also check JSON interview datasets
        if page.suffix == ".json":
            try:
                jdata = json.loads(page.read_text(encoding="utf-8"))
                doc_id = jdata.get("id", page.stem)
                gen_block = jdata.get("generation", {})
                fm = jdata
            except Exception:
                pass

        visibility = fm.get("visibility") or fm.get("privacy")
        if page.suffix == ".json":
            # Option (a): a dataset takes the visibility of the companion MDX page that loads it. When both
            # carry one, the stricter wins (public only if both say public). The stashed copy is the real
            # page: the live file may already be a hold stub, which always says "public".
            companion_mdx = page.parent / f"{doc_id}.mdx"
            companion_in_stash = STASH / companion_mdx.relative_to(GENERATED)
            comp_path = companion_in_stash if companion_in_stash.is_file() else (companion_mdx if companion_mdx.is_file() else None)
            comp_fm = (parse_frontmatter(comp_path) or {}) if comp_path else {}
            if comp_fm.get("type") == "stub":
                comp_fm = {}
            comp_visibility = comp_fm.get("visibility") or comp_fm.get("privacy")
            if not visibility:
                visibility = comp_visibility
            elif comp_path and comp_visibility != "public":
                visibility = comp_visibility or "private"

        # Absent visibility or privacy fails closed to private (T12, NV-REQ-028)
        is_private = (visibility != "public")

        approval = gen_block.get("approval_status", "draft")
        review_rec = reviews.get(doc_id, {})
        is_simulated = review_rec.get("is_simulated", True)

        should_exclude = False
        hold_reason = "Governance Policy AD-9 Enforcement"

        if is_private:
            should_exclude = True
            hold_reason = "Private Content Hold"
        elif approval in ("draft", "rejected", "approved-for-demo"):
            should_exclude = True
            hold_reason = "Governance Policy AD-9 Enforcement: Unapproved or Demo View"
        elif is_simulated and approval != "approved":
            should_exclude = True
            hold_reason = "Governance Policy AD-9 Enforcement: Simulated Approval"
        elif approval == "approved":
            # Real claimed approval: verify body hash and GitHub API gate
            try:
                verifier_instance.verify(page, fm, require_api_gate=require_api)
                print(f"  [production filter] Approved view verified: {page.relative_to(GENERATED)}")
            except VerificationNegative as vn:
                should_exclude = True
                hold_reason = f"Approval Verification Negative: {vn}"
                print(f"  [production filter] Verification negative for {page.relative_to(GENERATED)}: {vn}. Stashing and holding.")
            except ApiPermissionError as ape:
                print(f"FATAL: GitHub API / permission error verifying {page.relative_to(GENERATED)}: {ape}", file=sys.stderr)
                raise
            except Exception as e:
                print(f"FATAL: Unexpected error verifying {page.relative_to(GENERATED)}: {e}", file=sys.stderr)
                raise

        if should_exclude:
            rel = page.relative_to(GENERATED)
            dest = STASH / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(page), str(dest))
            stashed_count += 1
            print(f"  [production filter] Excluded {'private' if is_private else 'unapproved'} view: {rel}")

            # If it's a documentation page, replace with an audited production hold tombstone
            if page.suffix in (".md", ".mdx"):
                slug_line = f"slug: {fm['slug']}\n" if fm.get("slug") else ""
                reason = "Private Content Hold" if is_private else "Governance Policy AD-9 Enforcement"
                desc = (
                    f"The derived document **{doc_id}** is classified as **private**.\n\n"
                    f"Per DOCCAD security architecture (T12), private content is strictly excluded from public publication builds.\n"
                    if is_private else
                    f"The derived document **{doc_id}** is currently in **draft**, **simulated demo**, or **unverified** status ({hold_reason}).\n\n"
                    f"Per DOCCAD production governance policy, only verified human CODEOWNER pull request approvals can be published to production.\n"
                )
                tombstone = (
                    f"---\n"
                    f"id: {doc_id}\n"
                    f"{slug_line}"
                    f"title: \"[Production Hold] {fm.get('title', doc_id)}\"\n"
                    f"type: stub\n"
                    f"stub_version: 1\n"
                    f"visibility: public\n"
                    f"hold_reason: \"{reason}\"\n"
                    f"audience:\n  - developer\n"
                    f"owners:\n  - governance\n"
                    f"last_validated: '2026-09-21'\n"
                    f"---\n\n"
                    f"# 🔒 Production Publication Hold\n\n"
                    f":::caution {reason}\n"
                    f"{desc}"
                    f":::\n"
                )
                page.write_text(tombstone, encoding="utf-8")

    print(f"Production publication filter complete. Stashed {stashed_count} unapproved/simulated files.")
    return stashed_count


def filter_for_demo() -> None:
    restore_stashed()
    print("Demo mode active: All demo-approved fixtures and draft views available.")


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mode", required=True, choices=["demo", "production"])
    ap.add_argument("--require-api", action="store_true", help="Require GitHub API verification for approved pages")
    return ap


def main() -> int:
    ap = build_parser()
    args = ap.parse_args()

    if args.mode == "production":
        try:
            filter_for_production(require_api=args.require_api)
        except ApiPermissionError as ape:
            print(f"Production filter failed due to GitHub API error: {ape}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Production filter failed with error: {e}", file=sys.stderr)
            return 1
    else:
        filter_for_demo()
    return 0


if __name__ == "__main__":
    sys.exit(main())
