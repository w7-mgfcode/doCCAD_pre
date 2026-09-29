#!/usr/bin/env python3
"""Deterministic documentation validator (AD-8, AD-10).

Checks, in order:
  1. Frontmatter of every page under docs/source/ and docs/generated/ parses as
     YAML and validates against schemas/document.schema.json (canonical vs
     generated requirements are conditional in the schema).
  2. Plane integrity: type: generated pages exist only under docs/generated/,
     type: canonical only under docs/source/, and everything under docs/generated/
     is type: generated.
  3. Doc ids are globally unique.
  4. Every *.interview.json under docs/generated/ validates against
     schemas/interview.schema.json.
  5. Every generation.source_documents[].content_hash matches the current sha256
     of the referenced file (stale/drifted pages are reported).

Exit code 0 = all green; 1 = violations (printed). Requires PyYAML; uses the
`jsonschema` package when available and falls back to a minimal built-in subset
validator otherwise (required/type/enum/pattern/const/minItems/if-then).
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
    m = FRONTMATTER_RE.match(path.read_text(encoding="utf-8"))
    if not m:
        return None
    return _normalize(yaml.safe_load(m.group(1)))


def sha256_of(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


# --------------------------------------------------------------------------
# Schema validation: jsonschema if importable, else minimal subset fallback.
# --------------------------------------------------------------------------
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
        return _make_fallback_validator(doc_schema, interview_schema)


def _make_fallback_validator(doc_schema, interview_schema):
    """Minimal subset: required/type/enum/const/pattern/minItems/properties/
    items/allOf/if-then/not/anyOf/$ref (local + the one cross-file ref)."""

    schemas = {"document.schema.json": doc_schema, "interview.schema.json": interview_schema}
    TYPES = {"object": dict, "array": list, "string": str,
             "integer": int, "boolean": bool, "number": (int, float)}

    def resolve(ref: str, current: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        if "#" in ref:
            base, frag = ref.split("#", 1)
        else:
            base, frag = ref, ""
        root = schemas[base] if base else current
        node: Any = root
        for part in [p for p in frag.split("/") if p]:
            node = node[part]
        return node, root

    def check(inst, schema, root, path="") -> List[str]:
        errs: List[str] = []
        if "$ref" in schema:
            sub, subroot = resolve(schema["$ref"], root)
            return check(inst, sub, subroot, path)
        t = schema.get("type")
        if t and not isinstance(inst, TYPES.get(t, object)):
            return [f"{path or '<root>'}: expected {t}"]
        if isinstance(t, str) and t == "integer" and isinstance(inst, bool):
            return [f"{path}: expected integer"]
        if "enum" in schema and inst not in schema["enum"]:
            errs.append(f"{path or '<root>'}: {inst!r} not in {schema['enum']}")
        if "const" in schema and inst != schema["const"]:
            errs.append(f"{path or '<root>'}: expected const {schema['const']!r}")
        if "pattern" in schema and isinstance(inst, str) and not re.search(schema["pattern"], inst):
            errs.append(f"{path or '<root>'}: {inst!r} !~ /{schema['pattern']}/")
        if "minLength" in schema and isinstance(inst, str) and len(inst) < schema["minLength"]:
            errs.append(f"{path}: shorter than {schema['minLength']}")
        if "maxLength" in schema and isinstance(inst, str) and len(inst) > schema["maxLength"]:
            errs.append(f"{path}: longer than {schema['maxLength']}")
        if "minimum" in schema and isinstance(inst, (int, float)) and inst < schema["minimum"]:
            errs.append(f"{path}: below minimum {schema['minimum']}")
        if isinstance(inst, dict):
            for req in schema.get("required", []):
                if req not in inst:
                    errs.append(f"{path or '<root>'}: missing required '{req}'")
            for key, sub in schema.get("properties", {}).items():
                if key in inst:
                    errs.extend(check(inst[key], sub, root, f"{path}/{key}"))
        if isinstance(inst, list):
            if "minItems" in schema and len(inst) < schema["minItems"]:
                errs.append(f"{path}: fewer than {schema['minItems']} items")
            if "items" in schema:
                for i, item in enumerate(inst):
                    errs.extend(check(item, schema["items"], root, f"{path}[{i}]"))
        for sub in schema.get("allOf", []):
            errs.extend(check(inst, sub, root, path))
        if "anyOf" in schema:
            if all(check(inst, sub, root, path) for sub in schema["anyOf"]):
                errs.append(f"{path or '<root>'}: matches no anyOf branch")
        if "not" in schema and not check(inst, schema["not"], root, path):
            errs.append(f"{path or '<root>'}: must NOT match 'not' schema")
        if "if" in schema:
            if not check(inst, schema["if"], root, path):
                if "then" in schema:
                    errs.extend(check(inst, schema["then"], root, path))
            elif "else" in schema:
                errs.extend(check(inst, schema["else"], root, path))
        return errs

    def validate(instance: Any, which: str) -> List[str]:
        schema = doc_schema if which == "document" else interview_schema
        return check(instance, schema, schema)

    return validate


# --------------------------------------------------------------------------
def main() -> int:
    validate = make_validator()
    problems: List[str] = []
    seen_ids: Dict[str, Path] = {}

    pages = sorted(
        p for plane in ("source", "generated")
        for p in (DOCS / plane).rglob("*")
        if p.suffix in (".md", ".mdx") and p.is_file()
    )
    if not pages:
        print("No pages found under docs/source or docs/generated", file=sys.stderr)
        return 1

    hash_checks: List[Tuple[Path, Dict[str, Any]]] = []

    for page in pages:
        rel = page.relative_to(ROOT)
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

        in_generated = "docs/generated/" in rel.as_posix()
        if fm.get("type") == "generated" and not in_generated:
            problems.append(f"{rel}: type=generated but file is outside docs/generated/")
        if fm.get("type") == "canonical" and in_generated:
            problems.append(f"{rel}: type=canonical inside docs/generated/ (forbidden)")
        if in_generated and fm.get("type") != "generated":
            problems.append(f"{rel}: files under docs/generated/ must declare type: generated")

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
            src_path = ROOT / src.get("path", "")
            if not src_path.is_file():
                problems.append(f"{rel}: source document missing: {src.get('path')}")
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
    print("OK — frontmatter schemas valid, planes intact, provenance hashes current.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
