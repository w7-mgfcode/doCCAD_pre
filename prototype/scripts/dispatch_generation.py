#!/usr/bin/env python3
"""Dispatch generation contracts for DOCCAD (P2-17, P2-18, G15, G17).

Single tested dispatcher for GitHub workflows and local execution.
Validates inputs (contract, target, privacy, provider), enforces policy
(private privacy requires local provider), computes unique docs-gen/* branch
names, and dispatches generation with argument lists (never shell).
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from typing import Callable, Sequence

VALID_CONTRACTS = {
    "GenerateRecruiterPage",
    "GenerateInterviewPrep",
    "GenerateQuestionPage",
}
VALID_PRIVACY = {"public", "private"}
VALID_PROVIDERS = {"fixture", "anthropic", "gemini", "openai", "local"}


def build_parser() -> argparse.ArgumentParser:
    """Build and return CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Dispatch DOCCAD generation contracts."
    )
    parser.add_argument(
        "--contract",
        choices=sorted(VALID_CONTRACTS),
        help="Task contract to execute",
    )
    parser.add_argument(
        "--target",
        help="Canonical doc id (or question text for GenerateQuestionPage)",
    )
    parser.add_argument(
        "--privacy",
        choices=sorted(VALID_PRIVACY),
        help="Privacy class (private hard-pins to local provider)",
    )
    parser.add_argument(
        "--provider",
        choices=sorted(VALID_PROVIDERS),
        help="AI provider (fixture, anthropic, gemini, openai, local)",
    )
    parser.add_argument(
        "--branch-only",
        action="store_true",
        help="Compute and print unique branch name only and exit",
    )
    parser.add_argument(
        "--run-id",
        help="Run ID used for branch name computation (defaults to GITHUB_RUN_ID env var)",
    )
    return parser


def compute_branch_name(contract: str, target: str, run_id: str | int | None) -> str:
    """Compute unique docs-gen branch name: docs-gen/<contract-slug>-<target-slug>-<run-id>.

    Raises ValueError if run_id is missing or empty.
    Enforces that branch starts with docs-gen/ and length <= 100.
    """
    if run_id is None:
        raise ValueError("run_id is required to compute branch name")
    run_id_str = str(run_id).strip()
    if not run_id_str:
        raise ValueError("run_id cannot be empty")

    run_id_slug = re.sub(r"[^a-zA-Z0-9]+", "-", run_id_str).strip("-")
    if not run_id_slug:
        raise ValueError("run_id slug cannot be empty")

    target_clean = (target or "").strip()
    target_slug = re.sub(r"[^a-z0-9]+", "-", target_clean.lower()).strip("-")[:30] or "gen"

    contract_clean = (contract or "").strip()
    contract_slug = re.sub(r"[^a-z0-9]+", "-", contract_clean.lower()).strip("-")
    if not contract_slug:
        contract_slug = "gen"

    branch = f"docs-gen/{contract_slug}-{target_slug}-{run_id_slug}"
    if len(branch) > 100:
        branch = branch[:100].rstrip("-")

    if not branch.startswith("docs-gen/"):
        raise ValueError(f"Invalid branch prefix in '{branch}'")

    return branch


def validate_inputs(contract: str, target: str, privacy: str, provider: str) -> None:
    """Validate generation inputs against allowlists and policy rules.

    Raises SystemExit(1) on any validation failure.
    """
    if contract not in VALID_CONTRACTS:
        sys.stderr.write(f"ERROR: Invalid contract '{contract}'\n")
        sys.exit(1)

    if privacy not in VALID_PRIVACY:
        sys.stderr.write(f"ERROR: Invalid privacy '{privacy}'\n")
        sys.exit(1)

    if provider not in VALID_PROVIDERS:
        sys.stderr.write(f"ERROR: Invalid provider '{provider}'\n")
        sys.exit(1)

    if not target:
        sys.stderr.write("ERROR: Target input cannot be empty\n")
        sys.exit(1)

    if privacy == "private" and provider != "local":
        sys.stderr.write(
            f"ERROR: Privacy 'private' is only permitted with 'local' provider (got '{provider}')\n"
        )
        sys.exit(1)


def build_command(contract: str, target: str, privacy: str, provider: str) -> list[str]:
    """Build argv list for child generation script."""
    if contract == "GenerateQuestionPage":
        return [
            "python3",
            "scripts/generate_question.py",
            "--question",
            target,
            "--privacy",
            privacy,
            "--provider",
            provider,
            "--persist",
        ]
    return [
        "python3",
        "scripts/generate_page.py",
        "--contract",
        contract,
        "--target",
        target,
        "--privacy",
        privacy,
        "--provider",
        provider,
    ]


def dispatch(
    contract: str,
    target: str,
    privacy: str,
    provider: str,
    runner: Callable[[list[str]], int | None] = subprocess.check_call,
) -> int:
    """Validate inputs and dispatch generation command using injected runner."""
    validate_inputs(contract, target, privacy, provider)

    cmd = build_command(contract, target, privacy, provider)
    print(
        f"Executing contract {contract} for target '{target}' (privacy: {privacy}, provider: {provider})..."
    )
    result = runner(cmd)
    if isinstance(result, int):
        return result
    return 0


def main(
    argv: Sequence[str] | None = None,
    runner: Callable[[list[str]], int | None] = subprocess.check_call,
) -> int:
    """CLI entrypoint reading CLI args and environment variables."""
    parser = build_parser()
    args = parser.parse_args(argv)

    contract = (args.contract or os.environ.get("INPUT_CONTRACT", "")).strip()
    target = (args.target or os.environ.get("INPUT_TARGET", "")).strip()
    privacy = (args.privacy or os.environ.get("INPUT_PRIVACY", "public")).strip()
    provider = (args.provider or os.environ.get("INPUT_PROVIDER", "fixture")).strip()

    if args.branch_only:
        run_id = (args.run_id or os.environ.get("GITHUB_RUN_ID", "")).strip()
        branch = compute_branch_name(contract, target, run_id)
        print(branch)
        return 0

    return dispatch(contract, target, privacy, provider, runner=runner)


if __name__ == "__main__":
    sys.exit(main())
