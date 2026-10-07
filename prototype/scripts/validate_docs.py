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
  8. Citation & link resolution: internal links [text](/docs/...) or (/views/...),
     <EvidenceLink to="..."> and interview evidence_links[].to must target a known page route.
     Routes follow Docusaurus: plugin base (/docs, /views) + slug, else directory + id.
     Links inside code fences and inline code are ignored. Docusaurus' slug-less conventions
     (foo/foo.md category index, numeric prefixes, _-prefixed files) are not modelled; every
     current page sets an explicit slug, and the build's onBrokenLinks: 'throw' is the backstop.

Exit code 0 = all green; 1 = violations found.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import os
import re
import sys
import urllib.parse
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_grounding import check_grounding_document, check_grounding_interview

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SCHEMAS = ROOT / "schemas"
LINK_ALLOWLIST_FILE = ROOT / "contracts" / "link-allowlist.yaml"

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
UNSAFE_PATTERNS = [
    re.compile(r"<script\b", re.IGNORECASE),
    re.compile(r"javascript:\s*", re.IGNORECASE),
    re.compile(r"\beval\s*\(", re.IGNORECASE),
    re.compile(r"<\s*(?:iframe|object)\b", re.IGNORECASE),
    re.compile(r"\bon[a-z]+\s*=", re.IGNORECASE),
    re.compile(r"\bdata:[^\s'\">]+", re.IGNORECASE),
]
IMPORT_EXPORT_RE = re.compile(r"^\s*(?:import|export)\s+", re.MULTILINE)
ALLOWED_JSX_COMPONENTS = {"EvidenceLink", "InterviewPrep"}
JSX_COMPONENT_RE = re.compile(r"<([A-Z][a-zA-Z0-9_]*)")
EXTERNAL_LINK_RE = re.compile(r"\]\((https?://[^)\s]+)(?:\s+\"[^\"]*\")?\)|href=[\"'](https?://[^\"']+)[\"']")
PLANE_BASES = {"source": "/docs", "generated": "/views"}
MD_LINK_RE = re.compile(r"\]\((/(?:docs|views)(?:/[^)\s]*)?)(?:\s+\"[^\"]*\")?\)")
EVIDENCE_LINK_RE = re.compile(r"<EvidenceLink\b[^>]*?\bto=[\"']([^\"']*)[\"']")
CODE_FENCE_RE = re.compile(r"^(```|~~~).*?^\1[^\n]*$", re.DOTALL | re.MULTILINE)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")


def check_mdx_security(body: str, allowed_domains: set[str] | None = None) -> List[str]:
    """Check MDX body for unsafe patterns, imports/exports, disallowed JSX components, and external links."""
    errs: List[str] = []
    if allowed_domains is None:
        allowed_domains = load_link_allowlist()

    for pattern in UNSAFE_PATTERNS:
        if pattern.search(body):
            errs.append(f"SECURITY: Unsafe executable pattern matched in generated MDX: {pattern.pattern}")

    prose = INLINE_CODE_RE.sub("", CODE_FENCE_RE.sub("", body))

    if IMPORT_EXPORT_RE.search(prose):
        errs.append("SECURITY: import/export statement forbidden in generated MDX (T3)")

    for m in JSX_COMPONENT_RE.finditer(prose):
        tag = m.group(1)
        if tag not in ALLOWED_JSX_COMPONENTS:
            errs.append(f"SECURITY: Unallowlisted JSX component <{tag}> forbidden in generated MDX (T3)")

    for m in EXTERNAL_LINK_RE.finditer(prose):
        url = m.group(1) or m.group(2)
        parsed = urllib.parse.urlparse(url)
        hostname = (parsed.hostname or "").lower()
        if hostname and hostname not in allowed_domains:
            errs.append(f"SECURITY: External link domain '{hostname}' not in contracts/link-allowlist.yaml (T4)")

    return errs


def load_link_allowlist() -> set[str]:
    if LINK_ALLOWLIST_FILE.is_file():
        try:
            data = yaml.safe_load(LINK_ALLOWLIST_FILE.read_text(encoding="utf-8")) or {}
            return set(data.get("allowed_domains", []))
        except Exception:
            pass
    return set()


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
            errs = [
                f"{'/'.join(str(p) for p in e.absolute_path) or '<root>'}: {e.message}"
                for e in v.iter_errors(instance)
            ]
            if which == "document" and instance.get("type") == "generated" and not instance.get("visibility"):
                errs.append("<root>: generated document missing explicit 'visibility' frontmatter")
            return errs

        return validate
    except ImportError:
        if os.environ.get("DOCCAD_REQUIRE_JSONSCHEMA") == "1":
            sys.stderr.write("ERROR: jsonschema (and referencing) required by DOCCAD_REQUIRE_JSONSCHEMA=1 but not installed\n")
            sys.exit(1)
        sys.stderr.write("WARNING: jsonschema not installed — minimal fallback\n")
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
                    if not instance.get("visibility"):
                        errs.append("missing required 'visibility'")
                    gen = instance.get("generation") or {}
                    if gen.get("approval_status") == "approved" and "approval_record" not in gen:
                        errs.append("approval_status is approved but missing required 'approval_record'")
                elif instance.get("type") == "stub":
                    for req in ["stub_version", "audience", "owners", "hold_reason"]:
                        if req not in instance:
                            errs.append(f"missing required '{req}'")
            return errs
        return fallback_validate


def page_route(page: Path, fm: Dict[str, Any]) -> str:
    """Site route Docusaurus serves a page at: plugin base + slug, else directory + id/stem."""
    plane, *rest = page.relative_to(DOCS).parts
    rel_dir = Path(*rest).parent.as_posix() if rest else "."
    slug = fm.get("slug")
    if isinstance(slug, str) and slug:
        route = slug if slug.startswith("/") else f"{rel_dir}/{slug}"
    elif not fm.get("id") and page.stem in ("index", "README"):
        route = rel_dir
    else:
        route = f"{rel_dir}/{fm.get('id') or page.stem}"
    parts = [p for p in route.split("/") if p not in ("", ".")]
    return "/".join([PLANE_BASES.get(plane, "/" + plane), *parts])


def normalize_route(target: str) -> str:
    return target.split("#", 1)[0].split("?", 1)[0].rstrip("/") or "/"


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
    known_routes: set[str] = set()

    pages = sorted(
        p for plane in ("source", "generated")
        for p in (DOCS / plane).rglob("*")
        if p.suffix in (".md", ".mdx") and p.is_file()
    )
    if not pages:
        print("No pages found under docs/source or docs/generated", file=sys.stderr)
        return 1

    hash_checks: List[Tuple[Path, Dict[str, Any]]] = []
    allowed_domains = load_link_allowlist()

    # First pass: collect the route of every page, for citation resolution
    for page in pages:
        fm = parse_frontmatter(page)
        if fm:
            known_routes.add(page_route(page, fm))

    def check_citations(rel: Path, targets: List[Any]) -> None:
        for target in targets:
            if not isinstance(target, str) or not target:
                continue  # a missing or non-string target is a schema error, reported there
            if normalize_route(target) not in known_routes:
                problems.append(f"{rel}: broken citation: {target} matches no page route")

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
        if fm.get("type") in ("generated", "stub") and not in_generated:
            problems.append(f"{rel}: type={fm.get('type')} but file is outside docs/generated/")
        if fm.get("type") == "canonical" and in_generated:
            problems.append(f"{rel}: type=canonical inside docs/generated/ (forbidden)")
        if in_generated and fm.get("type") not in ("generated", "stub"):
            problems.append(f"{rel}: files under docs/generated/ must declare type: generated or stub")

        body = get_body_text(page)
        prose = INLINE_CODE_RE.sub("", CODE_FENCE_RE.sub("", body))  # code samples are not citations
        check_citations(rel, MD_LINK_RE.findall(prose) + EVIDENCE_LINK_RE.findall(prose))

        # Security and Grounding checks on generated files (AD-15, T3, T4, P2-06)
        if in_generated:
            for sec_err in check_mdx_security(body, allowed_domains):
                problems.append(f"{rel}: {sec_err}")

            if fm.get("type") == "generated":
                for g_err in check_grounding_document(fm, body, root_dir=ROOT):
                    problems.append(f"{rel}: {g_err}")

        if isinstance(fm.get("generation"), dict):
            hash_checks.append((rel, fm["generation"]))
            if fm["generation"].get("approval_status") == "approved":
                rec = fm["generation"].get("approval_record")
                if isinstance(rec, dict):
                    approved_hash = rec.get("approved_hash")
                    actual_hash = "sha256:" + hashlib.sha256(body.encode("utf-8")).hexdigest()
                    if actual_hash != approved_hash:
                        problems.append(
                            f"{rel}: approval_record.approved_hash mismatch: recorded {approved_hash}, "
                            f"actual {actual_hash} — body was modified after approval; artifact must return to in-review"
                        )

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
        check_citations(rel, [link.get("to", "") for link in data.get("evidence_links", [])
                              if isinstance(link, dict)])
        for g_err in check_grounding_interview(data, root_dir=ROOT):
            problems.append(f"{rel}: {g_err}")
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
