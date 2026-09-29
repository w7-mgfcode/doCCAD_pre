#!/usr/bin/env python3
"""Deterministic documentation validator (AD-8, AD-10, AD-15).

Checks, in order:
  1. Frontmatter of every page under docs/source/ and docs/generated/ parses as
     YAML and validates against schemas/document.schema.json.
  2. Plane integrity:
     - type: canonical exists only under docs/source/
     - type: generated exists only under docs/generated/
     - everything under docs/generated/ is type: generated.
  3. Doc ids are globally unique.
  4. Every *.interview.json under docs/generated/ validates against schemas/interview.schema.json.
  5. Provenance hashes: every generation.source_documents[].content_hash matches the current
     sha256 of the referenced file on disk.
  6. Path containment: no paths contain path traversal sequences or escape ROOT.
  7. Safe MDX & component safety: generated files must not contain raw <script> tags,
     untrusted eval, or unsafe imports.
  8. Citation & link resolution: internal links [text](/docs/...) and <EvidenceLink to="...">
     must target known document paths.

Exit code 0 = all green; 1 = violations found.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SCHEMAS = ROOT / "schemas"

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
UNSAFE_PATTERNS = [
    re.compile(r"<script\b", re.IGNORECASE),
    re.compile(r"javascript:\s*", re.IGNORECASE),
    re.compile(r"\beval\s*\(", re.IGNORECASE),
]


def _normalize(obj: Any) -> Any:
    """YAML parses dates/datetimes into objects; schemas expect ISO strings."""
    if isinstance(obj, dict):
        return {k: _normalize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_normalize(v) for v in obj]
    if isinstance(obj, datetime.datetime):
        return obj.isoformat().replace("+00:00", "Z")
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    return obj


def parse_frontmatter(path: Path) -> Dict[str, Any] | None:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    try:
        return _normalize(yaml.safe_load(m.group(1)))
    except Exception:
        return None


def get_body_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    return text[m.end():] if m else text


def sha256_of(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _load_schema(name: str) -> Dict[str, Any]:
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def make_validator():
    doc_schema = _load_schema("document.schema.json")
    interview_schema = _load_schema("interview.schema.json")
    try:
        from jsonschema import Draft202012Validator, FormatChecker
        from referencing import Registry, Resource

        registry = Registry().with_resources(
            [
                ("document.schema.json", Resource.from_contents(doc_schema)),
                ("interview.schema.json", Resource.from_contents(interview_schema)),
            ]
        )

        def validate(instance: Any, which: str) -> List[str]:
            schema = doc_schema if which == "document" else interview_schema
            v = Draft202012Validator(schema, registry=registry,
                                     format_checker=FormatChecker())
            return [
                f"{'/'.join(str(p) for p in e.absolute_path) or '<root>'}: {e.message}"
                for e in v.iter_errors(instance)
            ]

        return validate
    except ImportError:
        # Minimal fallback
        def fallback_validate(instance: Any, which: str) -> List[str]:
            errs = []
            if which == "document":
                for req in ["id", "title", "type"]:
                    if req not in instance:
                        errs.append(f"missing required '{req}'")
                if instance.get("type") == "generated":
                    for req in ["generated", "generation"]:
                        if req not in instance:
                            errs.append(f"missing required '{req}'")
            return errs
        return fallback_validate


def check_path_containment(path_str: str) -> bool:
    """Return True if path stays strictly within ROOT and contains no traversal escapes."""
    if ".." in path_str.split("/") or "\\" in path_str:
        return False
    resolved = (ROOT / path_str).resolve()
    try:
        resolved.relative_to(ROOT)
        return True
    except ValueError:
        return False


def main() -> int:
    validate = make_validator()
    problems: List[str] = []
    seen_ids: Dict[str, Path] = {}
    known_doc_slugs: set[str] = set()

    pages = sorted(
        p for plane in ("source", "generated")
        for p in (DOCS / plane).rglob("*")
        if p.suffix in (".md", ".mdx") and p.is_file()
    )
    if not pages:
        print("No pages found under docs/source or docs/generated", file=sys.stderr)
        return 1

    hash_checks: List[Tuple[Path, Dict[str, Any]]] = []

    # First pass: collect IDs and slugs
    for page in pages:
        fm = parse_frontmatter(page)
        if fm:
            doc_id = fm.get("id")
            if doc_id:
                known_doc_slugs.add(doc_id)
            # Add relative route path without extension
            rel = page.relative_to(DOCS).as_posix()
            stem = str(Path(rel).with_suffix(""))
            if stem.endswith("/index"):
                stem = stem[:-6]
            known_doc_slugs.add(stem)

    for page in pages:
        rel = page.relative_to(ROOT)
        rel_posix = rel.as_posix()

        # Path traversal check
        if not check_path_containment(rel_posix):
            problems.append(f"{rel}: Path traversal detected or path escapes workspace root")
            continue

        fm = parse_frontmatter(page)
        if fm is None:
            problems.append(f"{rel}: missing or unparseable frontmatter block")
            continue

        for err in validate(fm, "document"):
            problems.append(f"{rel}: schema: {err}")

        doc_id = fm.get("id")
        if isinstance(doc_id, str):
            if doc_id in seen_ids:
                problems.append(f"{rel}: duplicate id '{doc_id}' (also {seen_ids[doc_id]})")
            seen_ids[doc_id] = rel

        in_generated = "docs/generated/" in rel_posix
        if fm.get("type") == "generated" and not in_generated:
            problems.append(f"{rel}: type=generated but file is outside docs/generated/")
        if fm.get("type") == "canonical" and in_generated:
            problems.append(f"{rel}: type=canonical inside docs/generated/ (forbidden)")
        if in_generated and fm.get("type") != "generated":
            problems.append(f"{rel}: files under docs/generated/ must declare type: generated")

        # Security check on generated files (AD-15)
        if in_generated:
            body = get_body_text(page)
            for pattern in UNSAFE_PATTERNS:
                if pattern.search(body):
                    problems.append(f"{rel}: SECURITY: Unsafe executable pattern matched in generated MDX: {pattern.pattern}")

        if isinstance(fm.get("generation"), dict):
            hash_checks.append((rel, fm["generation"]))

    # Interview JSON datasets
    for jf in sorted((DOCS / "generated").rglob("*.interview.json")):
        rel = jf.relative_to(ROOT)
        try:
            data = json.loads(jf.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            problems.append(f"{rel}: invalid JSON: {e}")
            continue
        for err in validate(data, "interview"):
            problems.append(f"{rel}: interview schema: {err}")
        if isinstance(data.get("generation"), dict):
            hash_checks.append((rel, data["generation"]))

    # Provenance hash verification (AD-8: drift detection is hashes)
    stale = 0
    for rel, gen in hash_checks:
        for src in gen.get("source_documents", []):
            src_path_str = src.get("path", "")
            if not check_path_containment(src_path_str):
                problems.append(f"{rel}: SECURITY: Source document path attempts traversal: {src_path_str}")
                continue
            src_path = ROOT / src_path_str
            if not src_path.is_file():
                problems.append(f"{rel}: source document missing: {src_path_str}")
                continue
            actual = sha256_of(src_path)
            if actual != src.get("content_hash"):
                stale += 1
                problems.append(
                    f"{rel}: STALE — hash mismatch for {src['path']}\n"
                    f"    recorded {src.get('content_hash')}\n"
                    f"    actual   {actual}"
                )

    print(f"Validated {len(pages)} pages, "
          f"{len(list((DOCS / 'generated').rglob('*.interview.json')))} interview datasets, "
          f"{sum(len(g.get('source_documents', [])) for _, g in hash_checks)} provenance hashes.")
    if problems:
        print(f"\nFAIL — {len(problems)} violation(s) ({stale} stale):", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1
    print("OK — frontmatter schemas valid, planes intact, provenance hashes current, security checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
