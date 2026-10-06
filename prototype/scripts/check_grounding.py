#!/usr/bin/env python3
"""Deterministic Grounding Gate (P2-06 / NV-REQ-021 / ai_architecture.md §6).

Checks:
  1. Citation resolution & hash matching: Every cited canonical document resolves
     to an allowed evidence document and its recorded content hash matches disk.
  2. Quoted span containment: Explicitly quoted spans are contained in cited
     canonical source documents (whitespace-normalized).
  3. Recruiter technology tokens: In recruiter views, technology tokens must appear
     in the deterministic fact list or in cited canonical documents.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

EVIDENCE_LINK_RE = re.compile(r"<EvidenceLink\b[^>]*?\bto=[\"']([^\"']*)[\"']")
MD_LINK_RE = re.compile(r"\]\((/(?:docs|views)(?:/[^)\s]*)?)(?:\s+\"[^\"]*\")?\)")
CODE_FENCE_RE = re.compile(r"^(```|~~~).*?^\1[^\n]*$", re.DOTALL | re.MULTILINE)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")

# Quoted spans in text: double quotes or blockquotes
DOUBLE_QUOTE_RE = re.compile(r'["“]([^"”\n]{15,})["”]')
BLOCKQUOTE_RE = re.compile(r"^>\s+(.{15,})$", re.MULTILINE)

# Deterministic fact list of verified project technologies and platforms
DETERMINISTIC_FACT_TECHNOLOGIES = {
    "docusaurus", "react", "typescript", "javascript", "node", "nodejs", "npm",
    "python", "pyyaml", "jsonschema", "referencing", "mermaid", "lunr", "git",
    "github", "github actions", "github pages", "markdown", "mdx", "yaml", "json",
    "html", "css", "rest", "http", "https", "cli", "bash", "linux", "sha256",
    "anthropic", "claude", "gemini", "openai", "gpt", "local", "ollama",
    # platforms evaluated in platform-research.md
    "mintlify", "mkdocs", "nextjs", "astro", "vitepress", "starlight", "sphinx",
}

# Known prohibited/invented enterprise technology tokens that must be evidenced
COMMON_UNGROUNDED_TECH_TOKENS = {
    "kubernetes", "k8s", "kafka", "redis", "postgresql", "postgres", "mongodb",
    "docker", "terraform", "aws", "gcp", "azure", "spark", "hadoop", "graphql",
    "elasticsearch", "rabbitmq", "solr", "airflow", "cassandra", "consul",
    "vault", "istio", "flink", "snowflake", "bigquery", "dynamodb",
}


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def sha256_of_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_canonical_route(route: str, root_dir: Path = ROOT) -> Path | None:
    clean = route.split("#")[0].split("?")[0].strip()
    if clean.startswith("/docs/"):
        rel_sub = clean[len("/docs/"):]
    elif clean.startswith("/docs"):
        rel_sub = clean[len("/docs"):]
    else:
        return None

    rel_sub = rel_sub.strip("/")
    if not rel_sub:
        p = root_dir / "docs" / "source" / "overview" / "index.md"
        return p if p.is_file() else None

    # Try direct .md / .mdx
    for cand in [
        root_dir / "docs" / "source" / f"{rel_sub}.md",
        root_dir / "docs" / "source" / f"{rel_sub}.mdx",
        root_dir / "docs" / "source" / rel_sub / "index.md",
    ]:
        if cand.is_file():
            return cand

    # Match by frontmatter slug or id
    for f in (root_dir / "docs" / "source").rglob("*"):
        if f.is_file() and f.suffix in (".md", ".mdx"):
            text = f.read_text(encoding="utf-8", errors="replace")
            m = re.match(r"\A---\r?\n(.*?)\r?\n---", text, re.DOTALL)
            if m:
                try:
                    fm = yaml.safe_load(m.group(1)) or {}
                    if fm.get("slug") == clean or fm.get("slug") == f"/{rel_sub}":
                        return f
                    if fm.get("id") == rel_sub:
                        return f
                except Exception:
                    pass
    return None


def get_cited_sources_texts(generation: Dict[str, Any], root_dir: Path = ROOT) -> Dict[str, str]:
    texts = {}
    for src in generation.get("source_documents", []):
        spath = root_dir / src.get("path", "")
        if spath.is_file():
            texts[src.get("path", "")] = spath.read_text(encoding="utf-8", errors="replace")
    return texts


TAG_RE = re.compile(r"<[^>]+>", re.DOTALL)


def check_allowed_evidence(rel_path: str, contract_name: str, root_dir: Path = ROOT) -> bool:
    if not contract_name:
        return True
    cpath = root_dir / "contracts" / f"{contract_name}.yaml"
    if not cpath.is_file():
        return True
    try:
        cdata = yaml.safe_load(cpath.read_text(encoding="utf-8")) or {}
        globs = cdata.get("allowed_evidence", [])
        return any(
            fnmatch.fnmatch(rel_path, g) or rel_path.startswith(g.rstrip("*/") + "/") or rel_path == g
            for g in globs
        )
    except Exception:
        return True


ALERT_BLOCK_RE = re.compile(r"^>\s*\[!(?:NOTE|TIP|IMPORTANT|WARNING|CAUTION)\].*?(?=(?:\n[^\n>])|\Z)", re.DOTALL | re.MULTILINE)


def check_grounding_document(fm: Dict[str, Any], body: str, root_dir: Path = ROOT) -> List[str]:
    violations: List[str] = []
    generation = fm.get("generation")
    if not isinstance(generation, dict):
        return violations

    contract_name = generation.get("contract", "")
    prose = INLINE_CODE_RE.sub("", CODE_FENCE_RE.sub("", body))
    source_docs = generation.get("source_documents", [])
    source_paths = {s.get("path"): s for s in source_docs if isinstance(s, dict)}

    # Rule 1: Citation resolution & hash matching
    # Check that all recorded source documents exist, match disk hashes, and are allowed by contract
    for src in source_docs:
        spath_str = src.get("path", "")
        spath = root_dir / spath_str
        if not spath.is_file():
            violations.append(f"Grounding Rule 1: Recorded source document missing on disk: {spath_str}")
            continue
        if not check_allowed_evidence(spath_str, contract_name, root_dir=root_dir):
            violations.append(f"Grounding Rule 1: Source document {spath_str} not permitted by contract {contract_name}")
        actual_hash = sha256_of_file(spath)
        if actual_hash != src.get("content_hash"):
            violations.append(
                f"Grounding Rule 1: Hash mismatch for {spath_str} (recorded {src.get('content_hash')}, actual {actual_hash})"
            )

    # Check all EvidenceLink elements
    evidence_links = EVIDENCE_LINK_RE.findall(prose)
    for link in evidence_links:
        resolved = resolve_canonical_route(link, root_dir=root_dir)
        if not resolved:
            violations.append(f"Grounding Rule 1: EvidenceLink '{link}' does not resolve to canonical documentation")
        else:
            rel = resolved.relative_to(root_dir).as_posix()
            if not check_allowed_evidence(rel, contract_name, root_dir=root_dir):
                violations.append(f"Grounding Rule 1: EvidenceLink '{link}' targets {rel} not permitted by contract {contract_name}")
            if rel not in source_paths:
                violations.append(f"Grounding Rule 1: EvidenceLink '{link}' resolves to {rel} which is not in generation.source_documents")

    # Rule 2: Quoted span containment
    cited_texts = get_cited_sources_texts(generation, root_dir=root_dir)
    normalized_corpus = [normalize_whitespace(t) for t in cited_texts.values()]

    # Strip markdown alerts and JSX/HTML tags so tag attributes (e.g. className, to) and alert callouts are not extracted as prose quotes
    prose_no_alerts = ALERT_BLOCK_RE.sub(" ", prose)
    prose_for_quotes = TAG_RE.sub(" ", prose_no_alerts)
    quotes = DOUBLE_QUOTE_RE.findall(prose_for_quotes) + BLOCKQUOTE_RE.findall(prose_for_quotes)
    for q in quotes:
        clean_q = q.strip()
        # Skip markdown titles, formatting artifacts, or alert markers
        if len(clean_q) < 15 or clean_q.startswith("#") or clean_q.startswith("[!"):
            continue
        norm_q = normalize_whitespace(clean_q)
        if not any(norm_q in corpus for corpus in normalized_corpus):
            violations.append(f"Grounding Rule 2: Quoted span not contained in cited canonical sources: '{clean_q}'")

    # Rule 3: Recruiter technology tokens
    is_recruiter = (contract_name == "GenerateRecruiterPage") or ("recruiter" in fm.get("audience", []))
    if is_recruiter:
        body_lower = prose.lower()
        # Collect allowed technologies: fact list + words in cited canon
        canon_words = set()
        for t in cited_texts.values():
            canon_words.update(re.findall(r"\b[a-z0-9_-]+\b", t.lower()))

        for tech in COMMON_UNGROUNDED_TECH_TOKENS:
            pattern = rf"\b{re.escape(tech)}\b"
            if re.search(pattern, body_lower):
                if tech not in DETERMINISTIC_FACT_TECHNOLOGIES and tech not in canon_words:
                    violations.append(
                        f"Grounding Rule 3: Unevidenced technology token '{tech}' in recruiter view (not in deterministic fact list or cited canon)"
                    )

    return violations


def check_grounding_interview(data: Dict[str, Any], root_dir: Path = ROOT) -> List[str]:
    violations: List[str] = []
    generation = data.get("generation")
    if not isinstance(generation, dict):
        return violations

    contract_name = generation.get("contract", "")
    source_docs = generation.get("source_documents", [])
    source_paths = {s.get("path"): s for s in source_docs if isinstance(s, dict)}
    source_ids = {s.get("id"): s for s in source_docs if isinstance(s, dict)}

    # Rule 1: Citation resolution & hash matching
    for src in source_docs:
        spath_str = src.get("path", "")
        spath = root_dir / spath_str
        if not spath.is_file():
            violations.append(f"Grounding Rule 1: Recorded source document missing on disk: {spath_str}")
            continue
        if not check_allowed_evidence(spath_str, contract_name, root_dir=root_dir):
            violations.append(f"Grounding Rule 1: Source document {spath_str} not permitted by contract {contract_name}")
        actual_hash = sha256_of_file(spath)
        if actual_hash != src.get("content_hash"):
            violations.append(
                f"Grounding Rule 1: Hash mismatch for {spath_str} (recorded {src.get('content_hash')}, actual {actual_hash})"
            )

    for link in data.get("evidence_links", []):
        if isinstance(link, dict) and "to" in link:
            to_val = link["to"]
            resolved = resolve_canonical_route(to_val, root_dir=root_dir)
            if not resolved:
                violations.append(f"Grounding Rule 1: Interview evidence_link '{to_val}' does not resolve")
            else:
                rel = resolved.relative_to(root_dir).as_posix()
                if not check_allowed_evidence(rel, contract_name, root_dir=root_dir):
                    violations.append(f"Grounding Rule 1: Interview evidence_link '{to_val}' targets {rel} not permitted by contract {contract_name}")
                if rel not in source_paths:
                    violations.append(f"Grounding Rule 1: Interview evidence_link '{to_val}' target {rel} not in source_documents")

    for dd in data.get("design_decisions", []):
        if isinstance(dd, dict) and "evidence" in dd:
            ev_id = dd["evidence"]
            if ev_id not in source_ids:
                # Check if it resolves as doc id
                found = False
                for s in source_docs:
                    if s.get("id") == ev_id:
                        found = True
                        break
                if not found:
                    violations.append(f"Grounding Rule 1: Design decision evidence '{ev_id}' not found in source_documents")

    return violations


def check_grounding_file(path: Path, root_dir: Path = ROOT) -> List[str]:
    if not path.is_file():
        return [f"File not found: {path}"]
    if path.suffix == ".json":
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return check_grounding_interview(data, root_dir=root_dir)
        except Exception as e:
            return [f"JSON parse error: {e}"]
    elif path.suffix in (".md", ".mdx"):
        text = path.read_text(encoding="utf-8")
        m = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z", text, re.DOTALL)
        if not m:
            return [f"Missing frontmatter: {path}"]
        try:
            fm = yaml.safe_load(m.group(1)) or {}
            body = m.group(2)
            return check_grounding_document(fm, body, root_dir=root_dir)
        except Exception as e:
            return [f"YAML parse error: {e}"]
    return []


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paths", nargs="*", help="Files or globs to validate for grounding")
    return ap


def main(argv: List[str] | None = None) -> int:
    ap = build_parser()
    args = ap.parse_args(argv)

    if args.paths:
        target_paths = []
        for p_str in args.paths:
            p = Path(p_str)
            if p.is_file():
                target_paths.append(p)
            else:
                target_paths.extend(ROOT.glob(p_str))
    else:
        # Default: scan all generated files
        target_paths = sorted((DOCS / "generated").rglob("*.mdx")) + sorted((DOCS / "generated").rglob("*.interview.json"))

    all_violations: List[str] = []
    for path in target_paths:
        rel = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.as_posix()
        errs = check_grounding_file(path, root_dir=ROOT)
        for err in errs:
            all_violations.append(f"{rel}: {err}")

    if all_violations:
        print(f"Grounding Gate FAIL ({len(all_violations)} violations):", file=sys.stderr)
        for v in all_violations:
            print(f"  - {v}", file=sys.stderr)
        return 1

    print(f"Grounding Gate PASS ({len(target_paths)} files verified).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
