#!/usr/bin/env python3
"""Contract-driven generation pipeline (ai_architecture.md §5, AD-4..AD-9, AD-15).

Usage:
  python3 scripts/generate_page.py --contract GenerateRecruiterPage \
      --target architecture-system-overview [--privacy private] [--dry-run]
"""

from __future__ import annotations

import argparse
import datetime
import fnmatch
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from validate_docs import ROOT, DOCS, parse_frontmatter, sha256_of, make_validator, _normalize, check_mdx_security  # noqa: E402
from check_grounding import check_grounding_document, check_grounding_interview  # noqa: E402
from ai.router import Router, PrivacyRoutingError, log_safe, scan_for_secrets  # noqa: E402
from review_governance import reset_to_draft  # noqa: E402
from dispatch_generation import compute_branch_name, run_identity  # noqa: E402

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
    raise ContractViolation(f"No canonical page with id '{log_safe(doc_id)}' under docs/source/")


def _allowed(rel_path: str, globs: List[str]) -> bool:
    return any(fnmatch.fnmatch(rel_path, g) or rel_path.startswith(g.rstrip("*/") + "/")
               or rel_path == g for g in globs)


def assemble_evidence(contract: Dict[str, Any], target: Path) -> List[Path]:
    globs: List[str] = contract["allowed_evidence"]
    files: List[Path] = [target]

    fm = parse_frontmatter(target) or {}
    for src in fm.get("sources", []):
        p = ROOT / src
        if p.is_file():
            files.append(p)
        elif p.is_dir():
            files.extend(sorted(f for f in p.rglob("*")
                                if f.is_file() and f.suffix in (".py", ".yaml", ".json", ".ts", ".md")))
    for rid in fm.get("related", []):
        try:
            files.append(find_canonical_page(rid))
        except ContractViolation:
            pass

    seen, result = set(), []
    for f in files:
        rel = f.relative_to(ROOT).as_posix()
        if rel in seen:
            continue
        seen.add(rel)
        if not _allowed(rel, globs):
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
            f"{EVIDENCE_OPEN} file={rel} sha256={sha256_of(f)}\n"
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
                     evidence_docs: List[Path], provider: str, model: str,
                     mode: str = "demo") -> Dict[str, Any]:
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
        "model": model,
        "generation_mode": mode,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "approval_status": "draft",
    }
    fm.get("generation", {}).pop("approval_record", None)
    return fm


def report_rejection(attempt: int, errors: List[str]) -> None:
    """Say why an attempt was rejected before the repair retry, so live runs are diagnosable."""
    print(f"  [repair] attempt {attempt} rejected ({len(errors)} error(s)); retrying:", file=sys.stderr)
    for err in errors:
        print(f"    - {err[:300]}", file=sys.stderr)


def split_model_output(text: str) -> tuple[Dict[str, Any], str]:
    m = re.match(r"\A(?:```(?:mdx|markdown)?\s*\n)?---\r?\n(.*?)\r?\n---\r?\n(.*)\Z",
                 text.strip(), re.DOTALL)
    if not m:
        raise ContractViolation("Model output has no frontmatter block — rejected.")
    return _normalize(yaml.safe_load(m.group(1))), m.group(2).rstrip("`\n ")


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--contract", required=True)
    ap.add_argument("--target", required=True, help="canonical doc id")
    ap.add_argument("--privacy", choices=["public", "private"], default="public")
    ap.add_argument("--provider", choices=["fixture", "anthropic", "gemini", "openai", "local"], default=None,
                    help="Explicit provider selection: builds a 1-provider chain")
    ap.add_argument("--dry-run", action="store_true")
    return ap


def main() -> int:
    ap = build_parser()
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
    scan_for_secrets(prompt)

    privacy = args.privacy
    for f in evidence:
        if f.suffix in (".md", ".mdx"):
            efm = parse_frontmatter(f) or {}
            ev_vis = efm.get("visibility") or efm.get("privacy")
            if ev_vis != "public":
                privacy = "private"
                break

    task_meta = {"task": contract["contract"], "target_id": args.target, "privacy": privacy,
                 "context_tokens": len(prompt) // 4}
    router = Router(ROOT / "ai.config.yaml")
    chain = router.select_chain_names(task_meta, provider=args.provider)
    chain_source = f"Provider chain (--provider): {' -> '.join(chain)}" if args.provider is not None else f"Provider chain (from ai.config.yaml): {' -> '.join(chain)}"
    print(chain_source)

    # Same name generate.yml pushes; outside Actions the run part is a placeholder.
    run_id = run_identity()
    branch = compute_branch_name(contract["contract"], args.target, run_id or "RUN-ID")
    if not run_id:
        branch += " (RUN-ID = the generate.yml run ID)"

    if args.dry_run:
        print("\n--- DRY RUN: assembled prompt (no call made, nothing written) ---")
        print(prompt[:1000] + "\n... [truncated for brevity] ...")
        print("--- END DRY RUN ---")
        print(f"Live mode would write under docs/generated/{contract['output']['dir']}/ "
              f"and push branch: {branch}")
        return 0

    # Every run that reaches the provider prints one usage line and writes one run report,
    # also when it fails (P2-14, G11): a failed repair retry has still spent tokens.
    report = {"gate_results": "FAIL", "output_path": "none", "approval_status": "n/a",
              "generation_mode": "demo" if chain == ["fixture"] else "production"}
    evidence_ids = [(parse_frontmatter(p) or {}).get("id", p.stem) for p in evidence if p.suffix in (".md", ".mdx")]
    try:
        # Execute generation with exactly one repair retry
        messages = [{"role": "user", "content": prompt}]
        validate = make_validator()
        max_retries = 1
        attempts = 0

        while True:
            attempts += 1
            run_opts: Dict[str, Any] = {"max_tokens": contract.get("max_tokens", 4096), "contract": contract}
            run_kw = {"provider": args.provider} if args.provider is not None else {}
            result = router.run_with_fallback(task_meta, messages, run_opts, **run_kw)

            if contract["output"]["format"] == "json":
                # Structured JSON output (e.g. InterviewPrep)
                parse_errors = []
                data = None
                try:
                    data = json.loads(result["text"])
                except Exception as e:
                    parse_errors.append(f"JSON parse error: {e}")

                if not parse_errors and isinstance(data, dict):
                    provider_name = result.get("provider", "fixture")
                    gen_mode = "demo" if provider_name == "fixture" else "production"
                    # The pipeline owns the dataset's visibility, as it does for MDX pages: a model-chosen
                    # "public" from a private run must not reach the production filter.
                    data["visibility"] = "private" if privacy == "private" else "public"
                    data["generation"] = {
                        "contract": contract["contract"],
                        "contract_version": contract["version"],
                        "prompt_version": contract["prompt_version"],
                        "source_documents": [
                            {"id": (parse_frontmatter(p) or {}).get("id", p.stem),
                             "path": p.relative_to(ROOT).as_posix(),
                             "content_hash": sha256_of(p)}
                            for p in evidence if p.suffix in (".md", ".mdx")
                        ],
                        "provider": provider_name,
                        "model": result.get("model", ""),
                        "generation_mode": gen_mode,
                        "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "approval_status": "draft",
                    }
                    val_errors = validate(data, "interview")
                    # Pre-write Grounding Gate
                    val_errors.extend(check_grounding_interview(data, root_dir=ROOT))
                else:
                    val_errors = parse_errors

                if val_errors:
                    if attempts <= max_retries:
                        report_rejection(attempts, val_errors)
                        messages.append({"role": "assistant", "content": result["text"]})
                        messages.append({
                            "role": "user",
                            "content": "The previous output had validation/grounding errors:\n"
                                       + "\n".join(val_errors)
                                       + "\nPlease correct the JSON output according to the schema and grounding rules."
                        })
                        continue
                    report["gate_results"] = "FAIL (schema/grounding after repair retry)"
                    raise ContractViolation(f"Interview validation/grounding failed after repair retry: {val_errors}")

                out_dir = DOCS / "generated" / contract["output"]["dir"]
                out_dir.mkdir(parents=True, exist_ok=True)
                out_path = out_dir / f"{args.target}.interview.json"
                out_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
                reset_to_draft(args.target, out_path.relative_to(ROOT).as_posix())
                print(f"Wrote {out_path.relative_to(ROOT)}")
                report.update(gate_results="PASS (schema, grounding)", generation_mode=gen_mode,
                              output_path=out_path.relative_to(ROOT).as_posix(), approval_status="draft")
                return 0

            else:
                parse_errors = []
                fm, body = None, None
                try:
                    fm, body = split_model_output(result["text"])
                except Exception as e:
                    parse_errors.append(str(e))

                if not parse_errors and isinstance(fm, dict):
                    provider_name = result.get("provider", "fixture")
                    gen_mode = "demo" if provider_name == "fixture" else "production"
                    fm = stamp_provenance(fm, contract, evidence, provider_name, result.get("model", ""),
                                          mode=gen_mode)
                    # The pipeline owns page identity. A model-chosen slug can land outside the
                    # contract's route (live Gemini smoke test, 2026-10-06: /views/views/...).
                    fm["id"] = f"{contract['output']['dir']}-{args.target}"
                    fm["slug"] = f"/{contract['output']['dir']}/{args.target}"
                    fm["visibility"] = "private" if privacy == "private" else "public"
                    errors = validate(fm, "document")
                    # Pre-write MDX restriction gate and link allowlist
                    errors.extend(check_mdx_security(body))
                    # Pre-write Grounding Gate
                    errors.extend(check_grounding_document(fm, body, root_dir=ROOT))
                else:
                    errors = parse_errors

                if errors:
                    if attempts <= max_retries:
                        report_rejection(attempts, errors)
                        messages.append({"role": "assistant", "content": result["text"]})
                        messages.append({
                            "role": "user",
                            "content": "The previous output had validation errors:\n"
                                       + "\n".join(errors)
                                       + "\nPlease correct the output to ensure valid frontmatter, secure MDX, and strict grounding."
                        })
                        continue
                    report["gate_results"] = "FAIL (schema/mdx/grounding after repair retry)"
                    raise ContractViolation("Output invalid after generation (repair retry failed):\n" + "\n".join(errors))

                out_dir = DOCS / "generated" / contract["output"]["dir"]
                out_dir.mkdir(parents=True, exist_ok=True)
                out_path = out_dir / f"{args.target}.mdx"
                front = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).strip()
                out_path.write_text(f"---\n{front}\n---\n\n{body}\n", encoding="utf-8")
                reset_to_draft(fm.get("id", args.target), out_path.relative_to(ROOT).as_posix())
                print(f"Wrote {out_path.relative_to(ROOT)}")
                print(f"PR branch (persistence: {contract['persistence']}): {branch}")
                report.update(gate_results="PASS (schema, mdx, grounding)", generation_mode=gen_mode,
                              output_path=out_path.relative_to(ROOT).as_posix(), approval_status="draft")
                return 0
    finally:
        print(router.format_usage_line())
        router.write_step_summary(
            contract=contract["contract"],
            target=args.target,
            privacy=privacy,
            generation_mode=report["generation_mode"],
            evidence_ids=evidence_ids,
            gate_results=report["gate_results"],
            output_path=report["output_path"],
            approval_status=report["approval_status"],
        )


if __name__ == "__main__":
    sys.exit(main())
