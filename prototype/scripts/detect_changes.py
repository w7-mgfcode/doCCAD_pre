#!/usr/bin/env python3
"""Change-impact detection (AD-8): manifest + hashes, no graph database.

Usage:
  python3 scripts/detect_changes.py --all                 # full scan, no git needed
  python3 scripts/detect_changes.py --range <git-range>   # e.g. origin/main...HEAD

Rebuilds .docs-manifest.json from frontmatter, maps changed repo paths to
  * affected canonical pages (any frontmatter sources[] entry prefix-matches a
    changed path), and
  * stale generated pages (recorded content_hash of a source document no longer
    matches the file on disk — the mechanical drift signal).
Writes impact.json and prints a human summary. Exit 0 always (reporting tool);
downstream jobs decide what to do with the impact.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_docs import ROOT, DOCS, parse_frontmatter, sha256_of  # noqa: E402

MANIFEST = ROOT / ".docs-manifest.json"
IMPACT = ROOT / "impact.json"


def build_manifest() -> Dict[str, Any]:
    pages: List[Dict[str, Any]] = []
    for plane in ("source", "generated"):
        for p in sorted((DOCS / plane).rglob("*")):
            if p.suffix not in (".md", ".mdx") or not p.is_file():
                continue
            fm = parse_frontmatter(p) or {}
            entry: Dict[str, Any] = {
                "id": fm.get("id"),
                "path": p.relative_to(ROOT).as_posix(),
                "type": fm.get("type"),
                "content_hash": sha256_of(p),
                "sources": fm.get("sources", []),
                "related": fm.get("related", []),
            }
            if fm.get("type") == "canonical":
                entry["derived_pages"] = (fm.get("ai_generation") or {}).get(
                    "derived_pages", [])
            if isinstance(fm.get("generation"), dict):
                g = fm["generation"]
                entry["generation"] = {
                    "contract": g.get("contract"),
                    "source_documents": g.get("source_documents", []),
                }
            pages.append(entry)
    # Interview datasets participate in drift detection too.
    for jf in sorted((DOCS / "generated").rglob("*.interview.json")):
        data = json.loads(jf.read_text(encoding="utf-8"))
        pages.append({
            "id": data.get("id"),
            "path": jf.relative_to(ROOT).as_posix(),
            "type": "generated-data",
            "content_hash": sha256_of(jf),
            "sources": [],
            "related": [],
            "generation": {
                "contract": (data.get("generation") or {}).get("contract"),
                "source_documents": (data.get("generation") or {}).get(
                    "source_documents", []),
            },
        })
    return {"pages": pages}


def changed_paths_from_git(git_range: str) -> List[str]:
    out = subprocess.run(
        ["git", "diff", "--name-only", git_range],
        cwd=ROOT, capture_output=True, text=True, check=True,
    )
    return [line.strip() for line in out.stdout.splitlines() if line.strip()]


def compute_impact(manifest: Dict[str, Any], changed: List[str],
                   full_scan: bool) -> Dict[str, Any]:
    canonical = [p for p in manifest["pages"] if p["type"] == "canonical"]
    generated = [p for p in manifest["pages"] if p.get("generation")]

    affected_canonical: List[Dict[str, Any]] = []
    for page in canonical:
        hits = sorted({
            c for c in changed
            for src in page["sources"] + [page["path"]]
            if c == src or c.startswith(src.rstrip("/") + "/") or src.startswith(c)
        })
        if hits or full_scan:
            affected_canonical.append({"id": page["id"], "path": page["path"],
                                       "matched_changes": hits})

    stale_generated: List[Dict[str, Any]] = []
    for page in generated:
        stale_srcs = []
        for src in page["generation"]["source_documents"]:
            f = ROOT / src["path"]
            actual = sha256_of(f) if f.is_file() else "MISSING"
            if actual != src["content_hash"]:
                stale_srcs.append({"path": src["path"],
                                   "recorded": src["content_hash"],
                                   "actual": actual})
        if stale_srcs:
            stale_generated.append({
                "id": page["id"], "path": page["path"],
                "contract": page["generation"]["contract"],
                "source_documents": page["generation"].get("source_documents", []),
                "stale_sources": stale_srcs,
            })

    regenerate: List[Dict[str, Any]] = []
    seen = set()
    for s in stale_generated:
        contract = s["contract"]
        src_docs = s.get("source_documents", [])
        canonical_target = src_docs[0]["id"] if src_docs and "id" in src_docs[0] else s["id"]
        key = (contract, canonical_target)
        if key not in seen:
            seen.add(key)
            item = {"contract": contract, "target": canonical_target}
            if s.get("path", "").startswith("docs/generated/questions/"):
                item["tool"] = "generate_question.py"
            else:
                item["tool"] = "generate_page.py"
            regenerate.append(item)

    return {
        "mode": "full-scan" if full_scan else "git-range",
        "changed_paths": changed,
        "affected_canonical": affected_canonical,
        "stale_generated": stale_generated,
        "regenerate": regenerate,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--all", action="store_true",
                      help="full scan without git (works in a non-git directory)")
    mode.add_argument("--range", metavar="GIT_RANGE",
                      help="git range, e.g. origin/main...HEAD")
    args = ap.parse_args()

    manifest = build_manifest()
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    changed = [] if args.all else changed_paths_from_git(args.range)
    impact = compute_impact(manifest, changed, full_scan=args.all)
    IMPACT.write_text(json.dumps(impact, indent=2) + "\n", encoding="utf-8")

    print(f"Manifest: {MANIFEST.name} ({len(manifest['pages'])} entries)")
    print(f"Impact:   {IMPACT.name} (mode: {impact['mode']})")
    print(f"  changed paths:        {len(impact['changed_paths'])}")
    print(f"  affected canonical:   {len(impact['affected_canonical'])}"
          + (" (all — full scan)" if args.all else ""))
    print(f"  stale generated:      {len(impact['stale_generated'])}")
    for s in impact["stale_generated"]:
        print(f"    - {s['path']} (contract {s['contract']}):")
        for src in s["stale_sources"]:
            print(f"        drifted source: {src['path']}")
    if impact["regenerate"]:
        print("  regeneration plan:")
        for r in impact["regenerate"]:
            if r.get("tool") == "generate_question.py":
                print(f"    - {r['contract']} --target {r['target']} (generate_question.py)")
            else:
                print(f"    - {r['contract']} --target {r['target']}")
    else:
        print("  nothing to regenerate — all provenance hashes current.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
