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
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SOURCE = DOCS / "source"
GENERATED = DOCS / "generated"
WORK = ROOT / ".work"
STASH = WORK / "stashed_unapproved"
STASH_PRIVATE = WORK / "stashed_private"
REVIEWS_FILE = WORK / "demo_reviews.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))
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


def filter_for_production() -> int:
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
        if visibility == "private":
            rel = page.relative_to(SOURCE)
            dest = STASH_PRIVATE / "source" / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(page), str(dest))
            stashed_count += 1
            print(f"  [production filter] Excluded private canonical document: {rel}")

    # 2. Exclude unapproved, simulated, or private generated documents under docs/generated/
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
        is_private = (visibility == "private")

        approval = gen_block.get("approval_status", "draft")
        review_rec = reviews.get(doc_id, {})
        is_simulated = review_rec.get("is_simulated", True)

        # Exclude if private, draft, rejected, or simulated demo approval
        should_exclude = False
        if is_private:
            should_exclude = True
        elif approval in ("draft", "rejected", "approved-for-demo"):
            should_exclude = True
        elif is_simulated and approval != "approved":
            should_exclude = True

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
                    f"The derived document **{doc_id}** is currently in **draft** or **simulated demo** status.\n\n"
                    f"Per DOCCAD production governance policy, simulated approvals (`approved-for-demo`) cannot be published to production.\n"
                    f"Full publication requires a verified human pull request review.\n"
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


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mode", required=True, choices=["demo", "production"])
    args = ap.parse_args()

    if args.mode == "production":
        filter_for_production()
    else:
        filter_for_demo()
    return 0


if __name__ == "__main__":
    sys.exit(main())
