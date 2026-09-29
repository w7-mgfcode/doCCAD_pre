#!/usr/bin/env python3
"""Contract-driven generation pipeline (ai_architecture.md §5, AD-4..AD-9, AD-15).

Usage:
  python3 scripts/generate_page.py --contract GenerateRecruiterPage \
      --target architecture-system-overview [--privacy private] [--dry-run]

Pipeline: contract load -> deterministic evidence assembly (allowed_evidence globs
+ frontmatter sources/related closure) -> prompt render (evidence as delimited
DATA blocks) -> router chain selection -> [dry-run stops here] -> single model
call with fallback -> output frontmatter validation -> provenance stamp -> write
under docs/generated/ -> print the docs-gen/* branch a CI job would open a PR from.

--dry-run prints the assembled prompt and the selected provider chain, writes
NOTHING and performs NO network call — it must work with zero API keys set.
"""

from __future__ import annotations

import argparse
import datetime
import fnmatch
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from validate_docs import ROOT, DOCS, parse_frontmatter, sha256_of, make_validator  # noqa: E402
from ai.router import Router  # noqa: E402

CONTRACTS = ROOT / "contracts"
PROMPTS = ROOT / "prompts"

EVIDENCE_OPEN = "<<<EVIDENCE-DATA"
EVIDENCE_CLOSE = "EVIDENCE-DATA>>>"


class ContractViolation(RuntimeError):
    pass


def load_contract(name: str) -> Dict[str, Any]:
    path = CONTRACTS / f"{name}.yaml"
    if not path.is_file():
        raise ContractViolation(f"Unknown contract: {name} (no {path.relative_to(ROOT)})")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def find_canonical_page(doc_id: str) -> Path:
    for p in (DOCS / "source").rglob("*"):
        if p.suffix in (".md", ".mdx") and p.is_file():
            fm = parse_frontmatter(p) or {}
            if fm.get("id") == doc_id:
                return p
    raise ContractViolation(f"No canonical page with id '{doc_id}' under docs/source/")


def _allowed(rel_path: str, globs: List[str]) -> bool:
    return any(fnmatch.fnmatch(rel_path, g) or rel_path.startswith(g.rstrip("*/") + "/")
               or rel_path == g for g in globs)


def assemble_evidence(contract: Dict[str, Any], target: Path) -> List[Path]:
    """Deterministic Level-1 retrieval (AD-7). Refuses out-of-allowlist files."""
    globs: List[str] = contract["allowed_evidence"]
    files: List[Path] = [target]

    fm = parse_frontmatter(target) or {}
    # sources[] closure: repo paths the target documents
    for src in fm.get("sources", []):
        p = ROOT / src
        if p.is_file():
            files.append(p)
        elif p.is_dir():
            files.extend(sorted(f for f in p.rglob("*")
                                if f.is_file() and f.suffix in (".py", ".yaml", ".json", ".ts")))
    # related[] closure, one hop
    for rid in fm.get("related", []):
        try:
            files.append(find_canonical_page(rid))
        except ContractViolation:
            pass  # related id may be non-canonical; skip silently in PoC

    seen, result = set(), []
    for f in files:
        rel = f.relative_to(ROOT).as_posix()
        if rel in seen:
            continue
        seen.add(rel)
        if not _allowed(rel, globs):
            # AD-6/§9: the assembler refuses evidence outside the contract allowlist
            # BEFORE any model call. Closure hits outside the allowlist are dropped
            # with a warning (the contract is the authority, not the frontmatter).
            print(f"  [assembler] dropped (outside allowed_evidence): {rel}")
            continue
        result.append(f)
    return result


def render_prompt(contract: Dict[str, Any], target_id: str,
                  evidence: List[Path]) -> str:
    template_path = PROMPTS / contract["prompt_template"]
    template = template_path.read_text(encoding="utf-8")

    blocks = []
    for f in evidence:
        rel = f.relative_to(ROOT).as_posix()
        body = f.read_text(encoding="utf-8", errors="replace")
        blocks.append(
            f"{EVIDENCE_OPEN} file={rel} sha256={sha256_of(f).split(':')[1][:16]}\n"
            f"{body}\n{EVIDENCE_CLOSE}"
        )
    evidence_block = "\n\n".join(blocks)

    rendered = (template
                .replace("{{target_id}}", target_id)
                .replace("{{contract_name}}", contract["contract"])
                .replace("{{prohibited}}", "\n".join(f"- {p}" for p in contract["prohibited"]))
                .replace("{{evidence}}", evidence_block))
    unresolved = re.findall(r"\{\{[a-z_]+\}\}", rendered)
    if unresolved:
        raise ContractViolation(f"Unresolved prompt placeholders: {unresolved}")
    return rendered


def stamp_provenance(fm: Dict[str, Any], contract: Dict[str, Any],
                     evidence_docs: List[Path], provider: str, model: str) -> Dict[str, Any]:
    fm["type"] = "generated"
    fm["generated"] = True
    fm["generation"] = {
        "contract": contract["contract"],
        "contract_version": contract["version"],
        "prompt_version": contract["prompt_version"],
        "source_documents": [
            {"id": (parse_frontmatter(p) or {}).get("id", p.stem),
             "path": p.relative_to(ROOT).as_posix(),
             "content_hash": sha256_of(p)}
            for p in evidence_docs if p.suffix in (".md", ".mdx")
        ],
        "repo_evidence": [p.relative_to(ROOT).as_posix()
                          for p in evidence_docs if p.suffix not in (".md", ".mdx")],
        "provider": provider,
        "model": model,  # comes from run config/env — never hard-coded (AD-5)
        "generated_at": datetime.datetime.now(datetime.timezone.utc)
                        .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "approval_status": "draft",
    }
    return fm


def split_model_output(text: str) -> tuple[Dict[str, Any], str]:
    m = re.match(r"\A(?:```(?:mdx|markdown)?\s*\n)?---\r?\n(.*?)\r?\n---\r?\n(.*)\Z",
                 text.strip(), re.DOTALL)
    if not m:
        raise ContractViolation("Model output has no frontmatter block — rejected.")
    return yaml.safe_load(m.group(1)), m.group(2).rstrip("`\n ")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--contract", required=True)
    ap.add_argument("--target", required=True, help="canonical doc id")
    ap.add_argument("--privacy", choices=["public", "private"], default="public")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    contract = load_contract(args.contract)
    target_page = find_canonical_page(args.target)
    target_fm = parse_frontmatter(target_page) or {}
    if not (target_fm.get("ai_generation") or {}).get("allowed", False):
        raise ContractViolation(
            f"Canonical page '{args.target}' has ai_generation.allowed != true — refusing.")

    print(f"Contract: {contract['contract']} v{contract['version']} "
          f"(prompt {contract['prompt_version']})")
    print(f"Target:   {args.target} -> {target_page.relative_to(ROOT)}")

    evidence = assemble_evidence(contract, target_page)
    print(f"Evidence ({len(evidence)} files, allowed_evidence-filtered):")
    for f in evidence:
        print(f"  - {f.relative_to(ROOT)}")

    prompt = render_prompt(contract, args.target, evidence)

    task_meta = {"task": contract["contract"], "privacy": args.privacy,
                 "context_tokens": len(prompt) // 4}
    router = Router(ROOT / "ai.config.yaml")
    chain = router.select_chain_names(task_meta)
    print(f"Provider chain (from ai.config.yaml): {' -> '.join(chain)}")

    branch = f"docs-gen/{contract['contract'].lower()}-{args.target}"

    if args.dry_run:
        print("\n--- DRY RUN: assembled prompt (no call made, nothing written) ---")
        print(prompt)
        print("--- END DRY RUN ---")
        print(f"Live mode would write under docs/generated/{contract['output']['dir']}/ "
              f"and push branch: {branch}")
        return 0

    # ---- live mode: single call + one repair retry (ai_architecture §5) ----
    messages = [{"role": "user", "content": prompt}]
    result = router.run_with_fallback(task_meta, messages,
                                      {"max_tokens": contract.get("max_tokens", 4096)})
    validate = make_validator()
    fm, body = split_model_output(result["text"])
    fm = stamp_provenance(fm, contract, evidence, result["provider"], result["model"])
    errors = validate(fm, "document")
    if errors:
        # ONE repair retry with validator errors appended, then hard fail.
        repair = prompt + "\n\nYour previous output failed validation:\n" + \
            "\n".join(errors) + "\nRegenerate the full page, fixing these issues."
        result = router.run_with_fallback(task_meta,
                                          [{"role": "user", "content": repair}],
                                          {"max_tokens": contract.get("max_tokens", 4096)})
        fm, body = split_model_output(result["text"])
        fm = stamp_provenance(fm, contract, evidence, result["provider"], result["model"])
        errors = validate(fm, "document")
        if errors:
            raise ContractViolation("Output invalid after one repair retry:\n"
                                    + "\n".join(errors))

    out_dir = DOCS / "generated" / contract["output"]["dir"]
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{args.target}.mdx"
    front = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).strip()
    out_path.write_text(f"---\n{front}\n---\n\n{body}\n", encoding="utf-8")
    print(f"Wrote {out_path.relative_to(ROOT)}")
    print(f"PR branch (persistence: {contract['persistence']}): {branch}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
