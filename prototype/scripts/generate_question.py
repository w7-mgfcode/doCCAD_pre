#!/usr/bin/env python3
"""Deterministic Question Generation Pipeline (AD-6, AD-7, AD-9, AD-15).

Usage:
  python3 scripts/generate_question.py --question "How does DOCCAD detect drift?" \
      --audience developer [--privacy public|private] [--target doc-id] [--persist]

Or from an exported UI request JSON:
  python3 scripts/generate_question.py --request request.json [--persist] [--export-run run.json]
"""

from __future__ import annotations

import argparse
import datetime
import fnmatch
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from validate_docs import ROOT, DOCS, parse_frontmatter, sha256_of, make_validator, check_path_containment, _normalize  # noqa: E402
from ai.router import Router, PrivacyRoutingError, scan_for_secrets  # noqa: E402
from review_governance import reset_to_draft  # noqa: E402

CONTRACTS = ROOT / "contracts"
PROMPTS = ROOT / "prompts"
WORK_DIR = ROOT / ".work" / "drafts"

EVIDENCE_OPEN = "<<<EVIDENCE-DATA"
EVIDENCE_CLOSE = "EVIDENCE-DATA>>>"


class ContractViolation(RuntimeError):
    pass


def load_contract(name: str = "GenerateQuestionPage") -> Dict[str, Any]:
    path = CONTRACTS / f"{name}.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def deterministic_retrieval(
    question: str,
    target_id: str | None,
    allowed_globs: List[str],
    max_tokens: int = 32000,
) -> Tuple[List[Path], List[str]]:
    """Level-1 Deterministic Retrieval (AD-7).
    
    1. Only selects permitted canonical documents (docs/source/**, docs/diagrams/**).
    2. Excludes generated content (/views, docs/generated/**).
    3. Respects context token budgets.
    4. Stable tie-breaking: score descending, then path alphabetical.
    5. Reports included and rejected paths.
    """
    candidate_files: List[Path] = []
    rejected: List[str] = []

    # Collect all canonical files
    for p in sorted((DOCS / "source").rglob("*")):
        if p.is_file() and p.suffix in (".md", ".mdx"):
            candidate_files.append(p)
    for p in sorted((DOCS / "diagrams").rglob("*")):
        if p.is_file() and p.suffix == ".mmd":
            candidate_files.append(p)

    # Keywords from question (lowercase words >= 3 chars)
    words = set(re.findall(r"\b[a-z0-9-]{3,}\b", question.lower()))
    scored: List[Tuple[int, str, Path]] = []

    for f in candidate_files:
        rel = f.relative_to(ROOT).as_posix()
        # Allowlist check
        is_allowed = any(
            fnmatch.fnmatch(rel, g) or rel.startswith(g.rstrip("*/") + "/") or rel == g
            for g in allowed_globs
        )
        if not is_allowed:
            rejected.append(f"{rel} (outside contract allowed_evidence)")
            continue

        fm = parse_frontmatter(f) or {} if f.suffix in (".md", ".mdx") else {}
        score = 0
        if target_id and fm.get("id") == target_id:
            score += 100

        text = f.read_text(encoding="utf-8", errors="replace").lower()
        for w in words:
            if w in text:
                score += 1

        scored.append((score, rel, f))

    # Stable sort: score desc, then rel path asc
    scored.sort(key=lambda item: (-item[0], item[1]))

    included: List[Path] = []
    current_tokens = 0
    token_budget = max_tokens

    for score, rel, f in scored:
        content_len = len(f.read_bytes())
        est_tokens = content_len // 4
        if current_tokens + est_tokens > token_budget:
            rejected.append(f"{rel} (exceeds context budget: +{est_tokens} tokens)")
            continue
        # Only include if targeted or has keyword score or is primary overview
        if score > 0 or len(included) < 2:
            included.append(f)
            current_tokens += est_tokens

    return included, rejected


def render_prompt(
    contract: Dict[str, Any],
    question: str,
    audience: str,
    privacy: str,
    evidence: List[Path],
) -> str:
    template_path = PROMPTS / contract["prompt_template"]
    template = template_path.read_text(encoding="utf-8") if template_path.is_file() else """
Task: Answer the user's question grounded strictly in canonical evidence.
Audience: {{audience}}
Privacy: {{privacy}}
Prohibited:
{{prohibited}}

Canonical Evidence:
{{evidence}}

User Question: {{question}}
"""
    blocks = []
    for f in evidence:
        rel = f.relative_to(ROOT).as_posix()
        body = f.read_text(encoding="utf-8", errors="replace")
        blocks.append(
            f"{EVIDENCE_OPEN} file={rel} sha256={sha256_of(f)}\n{body}\n{EVIDENCE_CLOSE}"
        )
    evidence_block = "\n\n".join(blocks)

    rendered = (
        template.replace("{{question}}", question)
        .replace("{{audience}}", audience)
        .replace("{{privacy}}", privacy)
        .replace("{{contract_name}}", contract.get("contract", "GenerateQuestionPage"))
        .replace("{{prohibited}}", "\n".join(f"- {p}" for p in contract.get("prohibited", [])))
        .replace("{{evidence}}", evidence_block)
    )
    unresolved = re.findall(r"\{\{[a-z_]+\}\}", rendered)
    if unresolved:
        raise ContractViolation(f"Unresolved prompt placeholders: {unresolved}")
    return rendered


def split_output(text: str) -> Tuple[Dict[str, Any], str]:
    m = re.match(
        r"\A(?:```(?:mdx|markdown)?\s*\n)?---\r?\n(.*?)\r?\n---\r?\n(.*)\Z",
        text.strip(),
        re.DOTALL,
    )
    if not m:
        # Create minimal frontmatter wrapper
        fm = {
            "id": "q-generated-answer",
            "title": "Generated Answer",
            "type": "generated",
            "audience": ["developer"],
            "owners": ["architecture"],
            "last_validated": datetime.date.today().isoformat(),
            "generated": True,
        }
        return fm, text.strip()
    return yaml.safe_load(m.group(1)), m.group(2).rstrip("`\n ")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--request", help="Path to QuestionRequest JSON file")
    ap.add_argument("--question", help="Question text")
    ap.add_argument("--audience", default="developer")
    ap.add_argument("--privacy", choices=["public", "private"], default="public")
    ap.add_argument("--target", help="Canonical doc id")
    ap.add_argument("--persist", action="store_true", help="Write directly to docs/generated/questions/")
    ap.add_argument("--export-run", help="Output path for GenerationRun JSON")
    args = ap.parse_args()

    if args.request:
        req_data = json.loads(Path(args.request).read_text(encoding="utf-8"))
        question = req_data.get("question", "")
        audience = req_data.get("audience", "developer")
        privacy = req_data.get("privacy_class", "public")
        target_id = req_data.get("target_id")
    else:
        if not args.question:
            print("Error: either --request or --question is required", file=sys.stderr)
            return 1
        question = args.question
        audience = args.audience
        privacy = args.privacy
        target_id = args.target

    start_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
    contract = load_contract("GenerateQuestionPage")

    print("==================================================")
    print("DOCCAD Question Generation Pipeline")
    print(f"Question: {question}")
    print(f"Audience: {audience} | Privacy: {privacy} | Target: {target_id or 'None'}")
    print("==================================================")

    # Retrieval
    included_files, rejected_files = deterministic_retrieval(
        question, target_id, contract["allowed_evidence"]
    )
    print(f"Retrieved Evidence ({len(included_files)} files):")
    for f in included_files:
        print(f"  + {f.relative_to(ROOT)} ({sha256_of(f)[:16]}...)")
    if rejected_files:
        print(f"Rejected / Excluded ({len(rejected_files)} files):")
        for r in rejected_files[:5]:
            print(f"  - {r}")

    for f in included_files:
        if f.suffix in (".md", ".mdx"):
            efm = parse_frontmatter(f) or {}
            if efm.get("visibility") == "private" or efm.get("privacy") == "private":
                privacy = "private"
                break

    prompt = render_prompt(contract, question, audience, privacy, included_files)
    scan_for_secrets(prompt)

    task_meta = {
        "task": contract["contract"],
        "question": question,
        "audience": audience,
        "privacy": privacy,
        "target_id": target_id,
        "context_tokens": len(prompt) // 4,
    }

    router = Router(ROOT / "ai.config.yaml")
    chain = router.select_chain_names(task_meta)
    print(f"Router chain: {' -> '.join(chain)}")

    try:
        call_res = router.run_with_fallback(task_meta, [{"role": "user", "content": prompt}])
    except PrivacyRoutingError as e:
        print(f"\n[FATAL] Privacy Routing Policy Enforced: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\n[ERROR] Generation failed: {e}", file=sys.stderr)
        return 1

    fm, body = split_output(call_res["text"])

    # Update placeholders with real sha256 hashes
    source_docs = []
    for f in included_files:
        if f.suffix in (".md", ".mdx"):
            pf = parse_frontmatter(f) or {}
            source_docs.append({
                "id": pf.get("id", f.stem),
                "path": f.relative_to(ROOT).as_posix(),
                "content_hash": sha256_of(f),
            })

    provider_name = call_res.get("provider", "fixture")
    gen_mode = "demo" if provider_name == "fixture" else "production"
    model_name = call_res.get("model", "deterministic-demo-fixture" if provider_name == "fixture" else "")

    fm["type"] = "generated"
    fm["generated"] = True
    fm["generation"] = {
        "contract": contract["contract"],
        "contract_version": contract.get("version", 2),
        "prompt_version": contract.get("prompt_version", "question-page.v2"),
        "source_documents": source_docs,
        "repo_evidence": [
            f.relative_to(ROOT).as_posix()
            for f in included_files
            if f.suffix not in (".md", ".mdx")
        ],
        "provider": provider_name,
        "model": model_name,
        "generation_mode": gen_mode,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "approval_status": "draft",
    }
    fm.get("generation", {}).pop("approval_record", None)

    # Validate output schema
    validate = make_validator()
    fm = _normalize(fm)
    val_errors = validate(fm, "document")
    if val_errors:
        print(f"[ERROR] Generated frontmatter validation failed: {val_errors}", file=sys.stderr)
        return 1

    doc_id = fm.get("id", f"q-{abs(hash(question)) % 1000:03d}")
    front_str = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).strip()
    full_output = f"---\n{front_str}\n---\n\n{body}\n"

    # Destination
    if args.persist:
        out_dir = DOCS / "generated" / "questions"
    else:
        out_dir = WORK_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{doc_id}.mdx"
    out_path.write_text(full_output, encoding="utf-8")
    reset_to_draft(doc_id, out_path.relative_to(ROOT).as_posix())

    status = "insufficient_evidence" if "insufficient" in body.lower() else "success"
    print(f"\nWrote candidate artifact ({status}): {out_path.relative_to(ROOT)}")

    completed_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
    run_record = {
        "run_id": f"run-{int(datetime.datetime.now().timestamp())}",
        "contract": contract["contract"],
        "contract_version": contract.get("version", 2),
        "prompt_version": contract.get("prompt_version", "question-page.v2"),
        "provider": provider_name,
        "model": model_name,
        "mode": gen_mode,
        "target_id": target_id,
        "evidence_files": source_docs,
        "rejected_files": rejected_files,
        "started_at": start_time,
        "completed_at": completed_time,
        "status": status,
        "candidate_path": out_path.relative_to(ROOT).as_posix(),
        "output_text": full_output,
    }

    if args.export_run:
        Path(args.export_run).write_text(json.dumps(run_record, indent=2) + "\n", encoding="utf-8")
        print(f"Exported GenerationRun record to: {args.export_run}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
