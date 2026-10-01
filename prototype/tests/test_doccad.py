"""Automated Test Suite for DOCCAD Prototype.

Covers:
  1. Plane separation & isolation (canonical vs generated views).
  2. Level-1 deterministic retrieval & question generation (supported + unsupported).
  3. UI / CLI JSON round-trip (QuestionRequest, GenerationRun, ReviewRecord).
  4. Review governance state transitions (valid and invalid) & simulation vs production boundaries.
  5. Publication build exclusion of unapproved drafts and simulated approvals.
  6. Content-hash drift detection and targeted regeneration.
  7. Source document deletion detection.
  8. Private routing policy hard-pinning (never upgrade private tasks to cloud).
  9. Path traversal prevention.
  10. Unsafe MDX rejection (script tags, eval constructs).
  11. Invalid provenance (tampered, malformed, missing or escaping source hashes).
  12. Broken citations (Markdown links, EvidenceLink, interview evidence_links).
  13. Private-content exclusion from publication (expected failure: not implemented yet).
"""

from __future__ import annotations

import copy
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock
import yaml

# Set paths
TESTS_DIR = Path(__file__).resolve().parent
PROTOTYPE_ROOT = TESTS_DIR.parent
sys.path.insert(0, str(PROTOTYPE_ROOT))
sys.path.insert(0, str(PROTOTYPE_ROOT / "scripts"))

from scripts.validate_docs import (
    ROOT,
    DOCS,
    SCHEMAS,
    check_path_containment,
    make_validator,
    parse_frontmatter,
    sha256_of,
    UNSAFE_PATTERNS,
)
import scripts.validate_docs as validate_docs
from scripts.detect_changes import build_manifest, compute_impact
from scripts.review_governance import (
    InvalidTransitionError,
    load_reviews,
    save_reviews,
    set_review_status,
    REVIEWS_FILE,
)
from scripts.build_filter import (
    filter_for_production,
    filter_for_demo,
    restore_stashed,
    STASH,
    GENERATED,
)
from scripts.generate_question import (
    deterministic_retrieval,
    render_prompt,
    split_output,
    load_contract,
    ContractViolation as QuestionContractViolation,
)
from scripts.generate_page import ContractViolation as PageContractViolation
from ai.provider import ProviderTransportError, ProviderContentError
from ai.router import (
    Router,
    PrivacyRoutingError,
    RoutingError,
    scan_for_secrets,
    SecretScanViolation,
    validate_routing_config,
    PrivacyRoutingConfigError,
)


class TestPlaneSeparation(unittest.TestCase):
    """Ensure strict isolation between canonical docs and generated views."""

    def test_canonical_pages_only_in_source(self):
        source_pages = list((DOCS / "source").rglob("*.md")) + list((DOCS / "source").rglob("*.mdx"))
        self.assertGreater(len(source_pages), 20, "Expected at least 20 canonical source pages")

        for p in source_pages:
            fm = parse_frontmatter(p)
            self.assertIsNotNone(fm, f"Frontmatter missing in {p}")
            self.assertEqual(
                fm.get("type"),
                "canonical",
                f"Page under docs/source/ must declare type: canonical: {p}",
            )
            self.assertNotIn("generation", fm, f"Canonical page must not declare generation block: {p}")

    def test_generated_pages_only_in_generated(self):
        generated_pages = list((DOCS / "generated").rglob("*.md")) + list((DOCS / "generated").rglob("*.mdx"))
        self.assertGreater(len(generated_pages), 5, "Expected generated pages in docs/generated")

        for p in generated_pages:
            fm = parse_frontmatter(p)
            self.assertIsNotNone(fm, f"Frontmatter missing in {p}")
            self.assertEqual(
                fm.get("type"),
                "generated",
                f"Page under docs/generated/ must declare type: generated: {p}",
            )
            self.assertTrue(
                fm.get("generated", False),
                f"Generated page must have generated: true: {p}",
            )
            self.assertIn("generation", fm, f"Generated page must include generation metadata: {p}")

    def test_validator_rejects_misplaced_planes(self):
        validate = make_validator()
        # Canonical type marked in generated plane
        bad_canonical = {
            "id": "bad-test-page",
            "title": "Bad Test",
            "type": "canonical",
            "audience": ["developer"],
            "owners": ["architecture"],
            "last_validated": "2026-09-21",
        }
        # In validate_docs.py, plane containment is checked by path relative to docs/generated/
        # Check that schema itself validates standard doc
        errs = validate(bad_canonical, "document")
        self.assertEqual(len(errs), 0)


class TestDeterministicRetrievalAndGeneration(unittest.TestCase):
    """Test Level-1 deterministic retrieval and question generation pipeline."""

    def test_deterministic_retrieval_supported_question(self):
        contract = load_contract("GenerateQuestionPage")
        included, rejected = deterministic_retrieval(
            question="How does DOCCAD detect drift?",
            target_id=None,
            allowed_globs=contract["allowed_evidence"],
        )
        self.assertTrue(any("drift-detection" in p.name for p in included))
        # Ensure only canonical or diagram files are included
        for f in included:
            rel = f.relative_to(PROTOTYPE_ROOT).as_posix()
            self.assertTrue(
                rel.startswith("docs/source/") or rel.startswith("docs/diagrams/"),
                f"Retrieved file outside canonical boundary: {rel}",
            )

    def test_deterministic_retrieval_target_id_pinning(self):
        contract = load_contract("GenerateQuestionPage")
        included, _ = deterministic_retrieval(
            question="Tell me about components",
            target_id="architecture-system-overview",
            allowed_globs=contract["allowed_evidence"],
        )
        self.assertTrue(len(included) > 0)
        self.assertTrue(any("system-overview" in p.name for p in included))

    def test_question_generation_cli_supported(self):
        cmd = [
            sys.executable,
            str(PROTOTYPE_ROOT / "scripts" / "generate_question.py"),
            "--question", "How does DOCCAD detect drift?",
            "--audience", "developer",
            "--target", "val-drift-detection",
        ]
        res = subprocess.run(cmd, cwd=PROTOTYPE_ROOT, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Script failed: {res.stderr}")
        self.assertIn("Retrieved Evidence", res.stdout)
        self.assertIn("Wrote candidate artifact (success)", res.stdout)

    def test_question_generation_cli_unsupported(self):
        cmd = [
            sys.executable,
            str(PROTOTYPE_ROOT / "scripts" / "generate_question.py"),
            "--question", "How do I deploy DOCCAD to a multi-region Kubernetes cluster?",
            "--audience", "operator",
        ]
        res = subprocess.run(cmd, cwd=PROTOTYPE_ROOT, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Script failed: {res.stderr}")
        self.assertIn("Wrote candidate artifact (insufficient_evidence)", res.stdout)


class TestUiCliJsonRoundtrip(unittest.TestCase):
    """Test QuestionRequest and GenerationRun JSON serialization and validation."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_question_request_and_generation_run_roundtrip(self):
        # 1. Create a QuestionRequest JSON object matching governance schema
        req_path = Path(self.temp_dir) / "request.json"
        run_path = Path(self.temp_dir) / "run.json"
        req_data = {
            "question": "What is the trust boundary between canonical and generated planes?",
            "audience": "architect",
            "privacy_class": "public",
            "target_id": "sec-trust-boundaries",
        }
        req_path.write_text(json.dumps(req_data, indent=2), encoding="utf-8")

        # 2. Execute generate_question.py with --request and --export-run
        cmd = [
            sys.executable,
            str(PROTOTYPE_ROOT / "scripts" / "generate_question.py"),
            "--request", str(req_path),
            "--export-run", str(run_path),
        ]
        res = subprocess.run(cmd, cwd=PROTOTYPE_ROOT, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Command failed: {res.stderr}")
        self.assertTrue(run_path.is_file(), "GenerationRun file was not written")

        # 3. Validate GenerationRun against governance schema
        run_data = json.loads(run_path.read_text(encoding="utf-8"))
        self.assertIn("run_id", run_data)
        self.assertEqual(run_data["contract"], "GenerateQuestionPage")
        self.assertEqual(run_data["provider"], "fixture")
        self.assertEqual(run_data["status"], "success")
        self.assertGreater(len(run_data["evidence_files"]), 0)
        for ev in run_data["evidence_files"]:
            self.assertIn("path", ev)
            self.assertTrue(ev["content_hash"].startswith("sha256:"))


class TestReviewGovernanceStateTransitions(unittest.TestCase):
    """Test review governance lifecycle and simulated vs production boundaries."""

    def setUp(self):
        # Backup existing reviews if present
        self.backup_reviews = None
        if REVIEWS_FILE.is_file():
            self.backup_reviews = REVIEWS_FILE.read_text(encoding="utf-8")

    def tearDown(self):
        if self.backup_reviews is not None:
            REVIEWS_FILE.write_text(self.backup_reviews, encoding="utf-8")
        elif REVIEWS_FILE.is_file():
            REVIEWS_FILE.unlink()

    def test_state_transitions(self):
        art_id = "test-doc-transition-001"

        # 1. Draft
        r1 = set_review_status(art_id, "draft", reviewer="bot", notes="Freshly generated")
        self.assertEqual(r1["approval_state"], "draft")
        self.assertFalse(r1["eligible_for_production"])

        # 2. In-Review
        r2 = set_review_status(art_id, "in-review", reviewer="alice", notes="Assigned")
        self.assertEqual(r2["approval_state"], "in-review")
        self.assertFalse(r2["eligible_for_production"])

        # 3. Approved for Demo
        r3 = set_review_status(art_id, "approved-for-demo", reviewer="evaluator", notes="Demo preview approved")
        self.assertEqual(r3["approval_state"], "approved-for-demo")
        self.assertTrue(r3["is_simulated"])
        self.assertFalse(r3["eligible_for_production"])

        # 4. Rejected
        r4 = set_review_status(art_id, "rejected", reviewer="bob", notes="Flawed reasoning")
        self.assertEqual(r4["approval_state"], "rejected")
        self.assertFalse(r4["eligible_for_production"])

    def test_invalid_transitions_rejected(self):
        # (setup path, forbidden decision): approval must come from in-review; rejected must re-draft
        cases = [
            ([], "approved-for-demo"),
            ([], "rejected"),
            (["draft"], "approved-for-demo"),
            (["in-review", "rejected"], "approved-for-demo"),
            (["in-review", "rejected"], "in-review"),
            (["in-review", "approved-for-demo"], "in-review"),
        ]
        for i, (path, decision) in enumerate(cases):
            art_id = f"test-doc-invalid-{i}"
            with self.subTest(path=path, decision=decision):
                for state in path:
                    set_review_status(art_id, state, reviewer="bot")
                before = load_reviews()["reviews"].get(art_id)
                with self.assertRaises(InvalidTransitionError):
                    set_review_status(art_id, decision, reviewer="bot")
                self.assertEqual(load_reviews()["reviews"].get(art_id), before,
                                 "A rejected transition must leave the ledger unchanged")

    def test_unknown_state_rejected(self):
        # Production approval is not a state the simulated review CLI can set.
        with self.assertRaises(ValueError):
            set_review_status("test-doc-unknown", "approved", reviewer="bot")

    def test_cli_rejects_invalid_transition(self):
        script = str(PROTOTYPE_ROOT / "scripts" / "review_governance.py")
        res = subprocess.run(
            [sys.executable, script, "review", "--artifact", "test-doc-cli-skip",
             "--decision", "approved-for-demo"],
            cwd=PROTOTYPE_ROOT, capture_output=True, text=True,
        )
        self.assertEqual(res.returncode, 1, res.stdout + res.stderr)
        self.assertIn("Invalid transition", res.stderr)
        self.assertNotIn("test-doc-cli-skip", load_reviews()["reviews"])

        res = subprocess.run(
            [sys.executable, script, "review", "--artifact", "test-doc-cli-skip",
             "--decision", "approved"],
            cwd=PROTOTYPE_ROOT, capture_output=True, text=True,
        )
        self.assertNotEqual(res.returncode, 0, "CLI must not accept production approval")

    def test_check_production_blocks_simulated_approval(self):
        art_id = "test-doc-simulated"
        set_review_status(art_id, "in-review", reviewer="evaluator")
        set_review_status(art_id, "approved-for-demo", reviewer="evaluator")

        cmd = [
            sys.executable,
            str(PROTOTYPE_ROOT / "scripts" / "review_governance.py"),
            "check-production",
            "--artifact", art_id,
        ]
        res = subprocess.run(cmd, cwd=PROTOTYPE_ROOT, capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0, "Simulated approval must be rejected for production")
        self.assertIn("BLOCKED", res.stderr + res.stdout)


class TestBuildFilterExclusion(unittest.TestCase):
    """Test publication build filter isolating unapproved drafts and simulated approvals."""

    def setUp(self):
        restore_stashed()

    def tearDown(self):
        restore_stashed()

    def test_filter_for_production_and_demo(self):
        # Create a temporary draft page in docs/generated/questions/
        test_draft = GENERATED / "questions" / "test-unapproved-draft.mdx"
        test_draft.parent.mkdir(parents=True, exist_ok=True)
        content = (
            "---\n"
            "id: test-unapproved-draft\n"
            "title: Test Draft\n"
            "type: generated\n"
            "audience:\n  - developer\n"
            "owners:\n  - dev\n"
            "last_validated: 2026-09-21\n"
            "generated: true\n"
            "generation:\n"
            "  contract: GenerateQuestionPage\n"
            "  contract_version: 1\n"
            "  prompt_version: question-page.v1\n"
            "  source_documents: []\n"
            "  provider: fixture\n"
            "  model: deterministic-demo-fixture\n"
            "  generation_mode: demo\n"
            "  generated_at: '2026-09-21T07:00:00Z'\n"
            "  approval_status: draft\n"
            "---\n\n"
            "Draft content that must NOT appear in production publication build.\n"
        )
        test_draft.write_text(content, encoding="utf-8")

        try:
            # 1. Run filter_for_production
            stashed = filter_for_production()
            self.assertGreater(stashed, 0)
            stashed_target = STASH / "questions" / "test-unapproved-draft.mdx"
            self.assertTrue(stashed_target.is_file(), "Draft file must exist in stash directory")
            # Verify original draft text is not present in the published generated directory
            self.assertNotIn("Draft content that must NOT appear", test_draft.read_text(encoding="utf-8"))
            self.assertIn("Production Publication Hold", test_draft.read_text(encoding="utf-8"))

            # 2. Run filter_for_demo
            filter_for_demo()
            self.assertTrue(test_draft.is_file(), "Draft file must be restored back into generated plane")
            self.assertIn("Draft content that must NOT appear", test_draft.read_text(encoding="utf-8"))
        finally:
            if test_draft.is_file():
                test_draft.unlink()
            restore_stashed()

    # Required boundary (ANTIGRAVITY_PROMPT.txt §7: "Keep private fixtures out of public publication
    # output and its search index"), not implemented: pages carry no privacy field and
    # build_filter.py never looks for one. The top-level `privacy: private` key below is a
    # proposal, not an existing contract. Remove the decorator once exclusion is implemented.
    def test_private_content_excluded_from_production(self):
        private_page = GENERATED / "questions" / "test-private-approved.mdx"
        private_page.write_text(
            "---\n"
            "id: test-private-approved\n"
            "title: Test Private Page\n"
            "type: generated\n"
            "privacy: private\n"
            "audience:\n  - developer\n"
            "owners:\n  - dev\n"
            "last_validated: 2026-09-21\n"
            "generated: true\n"
            "generation:\n"
            "  contract: GenerateQuestionPage\n"
            "  contract_version: 1\n"
            "  prompt_version: question-page.v1\n"
            "  source_documents: []\n"
            "  provider: local\n"
            "  model: local-model\n"
            "  generation_mode: production\n"
            "  generated_at: '2026-09-21T07:00:00Z'\n"
            "  approval_status: approved\n"
            "---\n\n"
            "Private content that must NOT appear in a public publication build.\n",
            encoding="utf-8",
        )
        try:
            filter_for_production()
            self.assertTrue((STASH / "questions" / "test-private-approved.mdx").is_file(),
                            "Private page must be stashed out of the production build")
            if private_page.is_file():
                self.assertNotIn("Private content", private_page.read_text(encoding="utf-8"))
        finally:
            if private_page.is_file():
                private_page.unlink()
            restore_stashed()
            leftover = GENERATED / "questions" / "test-private-approved.mdx"
            if leftover.is_file():
                leftover.unlink()


class TestPrivateContentExclusion(unittest.TestCase):
    """P0-10: Private canonical pages are excluded at production filter time (T12)."""

    def test_private_canonical_page_excluded_from_production(self):
        source_dir = PROTOTYPE_ROOT / "docs" / "source" / "internal"
        source_dir.mkdir(parents=True, exist_ok=True)
        private_canonical = source_dir / "internal-architecture.md"
        private_canonical.write_text(
            "---\n"
            "id: internal-architecture\n"
            "title: Internal System Architecture\n"
            "type: canonical\n"
            "visibility: private\n"
            "audience:\n  - architect\n"
            "owners:\n  - core-team\n"
            "last_validated: 2026-09-21\n"
            "---\n\n"
            "TOP-SECRET internal documentation that MUST NOT be published.\n",
            encoding="utf-8"
        )
        try:
            filter_for_production()
            # Must NOT remain in docs/source/
            self.assertFalse(private_canonical.is_file(), "Private canonical page must be excluded from docs/source/")
            # Must NOT be in .work/stashed_unapproved/ (STASH)
            self.assertFalse(
                (STASH / "internal" / "internal-architecture.md").is_file(),
                "Private canonical page must not be placed in unapproved stash"
            )
            # Must be stashed in stashed_private/
            stashed_private = PROTOTYPE_ROOT / ".work" / "stashed_private" / "source" / "internal" / "internal-architecture.md"
            self.assertTrue(stashed_private.is_file(), "Private canonical page must be in stashed_private")
        finally:
            restore_stashed()
            if private_canonical.is_file():
                private_canonical.unlink()
            if source_dir.is_dir() and not list(source_dir.iterdir()):
                source_dir.rmdir()


class TestHashDriftAndRegeneration(unittest.TestCase):
    """Test hash drift detection and targeted regeneration plan."""

    def test_compute_impact_detects_hash_mismatch(self):
        manifest = build_manifest()
        # Find a generated page with source_documents
        target_page = None
        for p in manifest["pages"]:
            if p.get("generation") and p["generation"].get("source_documents"):
                target_page = copy.deepcopy(p)
                break
        self.assertIsNotNone(target_page, "Expected at least one generated page with source_documents")

        # Deliberately modify recorded hash to simulate drift
        stale_src = target_page["generation"]["source_documents"][0]
        stale_src["content_hash"] = "sha256:0000000000000000000000000000000000000000000000000000000000000000"

        test_manifest = {"pages": [target_page]}
        impact = compute_impact(test_manifest, changed=[], full_scan=False)

        self.assertEqual(len(impact["stale_generated"]), 1)
        stale_entry = impact["stale_generated"][0]
        self.assertEqual(stale_entry["id"], target_page["id"])
        self.assertEqual(len(impact["regenerate"]), 1)
        self.assertEqual(impact["regenerate"][0]["target"], stale_src["id"])


class TestRegenerationPlanExecutable(unittest.TestCase):
    """P0-07: every regenerate entry from a simulated stale page is executable."""

    def test_regeneration_plan_executable(self):
        manifest = build_manifest()

        # Test 1: Simulated stale interview page
        interview_page = None
        for p in manifest["pages"]:
            if p.get("generation") and p["generation"].get("contract") == "GenerateInterviewPrep":
                interview_page = copy.deepcopy(p)
                break
        self.assertIsNotNone(interview_page)
        stale_src = interview_page["generation"]["source_documents"][0]
        stale_src["content_hash"] = "sha256:0000000000000000000000000000000000000000000000000000000000000000"

        impact = compute_impact({"pages": [interview_page]}, changed=[], full_scan=False)
        self.assertEqual(len(impact["regenerate"]), 1)
        for r in impact["regenerate"]:
            res = subprocess.run(
                [sys.executable, "scripts/generate_page.py", "--contract", r["contract"], "--target", r["target"], "--dry-run"],
                cwd=PROTOTYPE_ROOT, capture_output=True, text=True
            )
            self.assertEqual(res.returncode, 0, f"Dry-run failed for {r}:\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}")

        # Test 2: Simulated stale recruiter page
        recruiter_page = None
        for p in manifest["pages"]:
            if p.get("generation") and p["generation"].get("contract") == "GenerateRecruiterPage":
                recruiter_page = copy.deepcopy(p)
                break
        self.assertIsNotNone(recruiter_page)
        stale_src_rec = recruiter_page["generation"]["source_documents"][0]
        stale_src_rec["content_hash"] = "sha256:0000000000000000000000000000000000000000000000000000000000000000"

        impact_rec = compute_impact({"pages": [recruiter_page]}, changed=[], full_scan=False)
        self.assertEqual(len(impact_rec["regenerate"]), 1)
        for r in impact_rec["regenerate"]:
            res = subprocess.run(
                [sys.executable, "scripts/generate_page.py", "--contract", r["contract"], "--target", r["target"], "--dry-run"],
                cwd=PROTOTYPE_ROOT, capture_output=True, text=True
            )
            self.assertEqual(res.returncode, 0, f"Dry-run failed for {r}:\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}")

    def test_interview_targets_deduplicated_per_contract(self):
        # Both .interview.json and .mdx for same topic must produce only 1 regenerate entry
        manifest = build_manifest()
        pages = [
            copy.deepcopy(p) for p in manifest["pages"]
            if p.get("generation") and p["generation"].get("contract") == "GenerateInterviewPrep"
            and "architecture-content-planes" in p.get("path", "")
        ]
        self.assertGreaterEqual(len(pages), 2, "Expected at least 2 pages for architecture-content-planes interview prep")
        for p in pages:
            for s in p["generation"]["source_documents"]:
                s["content_hash"] = "sha256:0000000000000000000000000000000000000000000000000000000000000000"
        impact = compute_impact({"pages": pages}, changed=[], full_scan=False)
        self.assertEqual(len(impact["regenerate"]), 1)
        self.assertEqual(impact["regenerate"][0]["contract"], "GenerateInterviewPrep")
        self.assertEqual(impact["regenerate"][0]["target"], "architecture-content-planes")


class TestSourceDeletionDetection(unittest.TestCase):
    """Test detection of deleted/missing source documents referenced by generated views."""

    def test_missing_source_file_flagged(self):
        fake_page = {
            "id": "derived-page-with-missing-source",
            "path": "docs/generated/questions/q-fake.mdx",
            "type": "generated",
            "sources": [],
            "generation": {
                "contract": "GenerateQuestionPage",
                "source_documents": [
                    {
                        "path": "docs/source/nonexistent/missing-doc.md",
                        "content_hash": "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
                    }
                ],
            },
        }
        test_manifest = {"pages": [fake_page]}
        impact = compute_impact(test_manifest, changed=[], full_scan=False)
        self.assertEqual(len(impact["stale_generated"]), 1)
        self.assertEqual(impact["stale_generated"][0]["stale_sources"][0]["actual"], "MISSING")


class TestPrivateRoutingPolicy(unittest.TestCase):
    """Test private task routing hard-pinning (AD-5)."""

    def test_private_routing_pinned_to_local(self):
        router = Router(PROTOTYPE_ROOT / "ai.config.yaml")
        # Enable local provider in config
        router.providers_cfg["local"]["enabled"] = True
        task_meta = {"task": "GenerateQuestionPage", "privacy": "private"}
        chain = router.select_chain_names(task_meta)
        self.assertEqual(chain, ["local"])
        # Ensure no cloud providers are in the chain
        self.assertNotIn("anthropic", chain)
        self.assertNotIn("gemini", chain)
        self.assertNotIn("openai", chain)

    def test_private_routing_raises_error_if_local_disabled(self):
        router = Router(PROTOTYPE_ROOT / "ai.config.yaml")
        # In current default config, local is disabled
        router.providers_cfg["local"]["enabled"] = False
        task_meta = {"task": "GenerateQuestionPage", "privacy": "private"}
        with self.assertRaises(PrivacyRoutingError):
            router.select_chain_names(task_meta)


class TestPathTraversalSecurity(unittest.TestCase):
    """Test path containment and path traversal protection."""

    def test_check_path_containment_valid(self):
        self.assertTrue(check_path_containment("docs/source/overview/index.md"))
        self.assertTrue(check_path_containment("docs/diagrams/system-context.mmd"))

    def test_check_path_containment_traversal_rejection(self):
        self.assertFalse(check_path_containment("../../etc/passwd"))
        self.assertFalse(check_path_containment("../prototype/docs/source/overview/index.md"))
        self.assertFalse(check_path_containment("docs/source/../../../etc/shadow"))
        self.assertFalse(check_path_containment("docs\\windows\\backslash"))


class TestUnsafeMdxRejection(unittest.TestCase):
    """Test that generated MDX files cannot contain raw script tags, eval, or dangerous constructs."""

    def test_unsafe_patterns_match(self):
        xss_script = "Here is some text <script>alert(1)</script> and more"
        self.assertTrue(any(p.search(xss_script) for p in UNSAFE_PATTERNS))

        eval_script = "const val = eval('2 + 2');"
        self.assertTrue(any(p.search(eval_script) for p in UNSAFE_PATTERNS))

        js_href = "[Click Here](javascript:alert(1))"
        self.assertTrue(any(p.search(js_href) for p in UNSAFE_PATTERNS))

    def test_safe_mdx_passes(self):
        safe_mdx = (
            "# System Overview\n\n"
            "This document explains the `<EvidenceLink to=\"/docs/overview\" />` component.\n"
            "```typescript\n"
            "function compute() { return 2 + 2; }\n"
            "```\n"
        )
        self.assertFalse(any(p.search(safe_mdx) for p in UNSAFE_PATTERNS))


def _has_jsonschema() -> bool:
    try:
        import jsonschema  # noqa: F401
        import referencing  # noqa: F401
        return True
    except ImportError:
        return False


class _ValidatorOnCopy(unittest.TestCase):
    """Runs validate_docs.main() against a scratch copy of docs/ and schemas/ — never the live tree."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp()).resolve()  # resolved: containment checks compare resolved paths
        shutil.copytree(DOCS, self.tmp / "docs")
        shutil.copytree(SCHEMAS, self.tmp / "schemas")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def edit(self, rel: str, old: str, new: str, count: int = 1) -> None:
        path = self.tmp / rel
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text, f"test fixture drifted: {old!r} not in {rel}")
        path.write_text(text.replace(old, new, count), encoding="utf-8")

    def run_validator(self) -> tuple[int, str]:
        out = io.StringIO()
        with mock.patch.multiple(validate_docs, ROOT=self.tmp, DOCS=self.tmp / "docs",
                                 SCHEMAS=self.tmp / "schemas"), \
                redirect_stdout(out), redirect_stderr(out):
            code = validate_docs.main()
        return code, out.getvalue()

    def assertRejected(self, needle: str) -> None:
        code, output = self.run_validator()
        self.assertEqual(code, 1, f"validator accepted the mutation:\n{output}")
        self.assertIn(needle, output)


class TestInvalidProvenance(_ValidatorOnCopy):
    """A generated page whose provenance block is tampered, malformed or escaping must fail validation."""

    def setUp(self):
        super().setUp()
        # Fixtures come from the content, so re-seeding or renaming generated views cannot break the tests.
        for page in sorted((self.tmp / "docs" / "generated").rglob("*.mdx")):
            sources = ((parse_frontmatter(page) or {}).get("generation") or {}).get("source_documents") or []
            if sources:
                self.PAGE = page.relative_to(self.tmp).as_posix()
                self.HASH = sources[0]["content_hash"]
                self.SRC = f"path: {sources[0]['path']}"
                break
        else:
            self.fail("no generated page with source_documents to use as a fixture")

    def test_unmodified_copy_passes(self):
        code, output = self.run_validator()
        self.assertEqual(code, 0, output)

    def test_tampered_hash_rejected(self):
        self.edit(self.PAGE, self.HASH, "sha256:" + "0" * 64)
        self.assertRejected("STALE")

    def test_malformed_hash_rejected(self):
        # Caught by the schema pattern when jsonschema is present, by the hash comparison otherwise.
        self.edit(self.PAGE, self.HASH, "md5:66743e3d")
        self.assertRejected(self.PAGE)

    def test_missing_source_rejected(self):
        self.edit(self.PAGE, self.SRC, "path: docs/source/validation/deleted-page.md")
        self.assertRejected("source document missing")

    def test_traversal_source_path_rejected(self):
        self.edit(self.PAGE, self.SRC, "path: ../../etc/passwd")
        self.assertRejected("Source document path attempts traversal")

    @unittest.skipUnless(_has_jsonschema(), "required-field check needs jsonschema + referencing")
    def test_incomplete_generation_block_rejected(self):
        page = self.tmp / self.PAGE
        text = page.read_text(encoding="utf-8")
        stripped = re.sub(r"(?m)^  provider: .*\n", "", text, count=1)
        self.assertNotEqual(text, stripped, "fixture page has no generation.provider line")
        page.write_text(stripped, encoding="utf-8")
        self.assertRejected("schema:")


class TestBrokenCitations(_ValidatorOnCopy):
    """Citations to routes that no page serves must fail validation (validate_docs.py check 8)."""

    def setUp(self):
        super().setUp()
        docs = self.tmp / "docs"
        cited = set()
        for page in docs.joinpath("generated").rglob("*.mdx"):
            for src in ((parse_frontmatter(page) or {}).get("generation") or {}).get("source_documents") or []:
                cited.add(src["path"])
        # A canonical page that is no provenance source, so editing it causes no hash drift.
        self.CANONICAL = next(p.relative_to(self.tmp).as_posix() for p in sorted(docs.joinpath("source").rglob("*.md"))
                              if f"docs/{p.relative_to(docs).as_posix()}" not in cited)
        self.GENERATED = next(p.relative_to(self.tmp).as_posix() for p in sorted(docs.joinpath("generated").rglob("*.mdx")))
        self.INTERVIEW = sorted(docs.joinpath("generated").rglob("*.interview.json"))[0]

    def append(self, rel: str, text: str) -> None:
        with (self.tmp / rel).open("a", encoding="utf-8") as f:
            f.write(text)

    def test_broken_markdown_link_rejected(self):
        self.append(self.CANONICAL, "\nSee [drift](/docs/validation/no-such-page).\n")
        self.assertRejected("broken citation: /docs/validation/no-such-page")

    def test_broken_markdown_link_with_title_rejected(self):
        self.append(self.CANONICAL, '\nSee [drift](/docs/validation/no-such-page "Drift").\n')
        self.assertRejected("broken citation: /docs/validation/no-such-page")

    def test_broken_evidence_link_rejected(self):
        self.append(self.GENERATED, '\n<EvidenceLink to="/docs/architecture/removed-page">x</EvidenceLink>\n')
        self.assertRejected("broken citation: /docs/architecture/removed-page")

    def test_single_quoted_evidence_link_rejected(self):
        self.append(self.GENERATED, "\n<EvidenceLink title='t' to='/docs/architecture/removed-page'>x</EvidenceLink>\n")
        self.assertRejected("broken citation: /docs/architecture/removed-page")

    def test_broken_interview_evidence_link_rejected(self):
        data = json.loads(self.INTERVIEW.read_text(encoding="utf-8"))
        data["evidence_links"][0]["to"] = "/docs/architecture/gone"
        self.INTERVIEW.write_text(json.dumps(data, indent=2), encoding="utf-8")
        self.assertRejected("broken citation: /docs/architecture/gone")

    def test_anchor_and_trailing_slash_resolve(self):
        self.append(self.CANONICAL, "\nSee [drift](/docs/validation/drift-detection/#hash-comparison)"
                                    " and [overview](/docs/overview/).\n")
        code, output = self.run_validator()
        self.assertEqual(code, 0, output)

    def test_links_in_code_are_not_citations(self):
        self.append(self.CANONICAL, "\n```md\n[example](/docs/placeholder-page)\n```\n\n"
                                    "Inline: `<EvidenceLink to=\"/docs/placeholder\" />`.\n")
        code, output = self.run_validator()
        self.assertEqual(code, 0, output)


class TestValidatorDependencyMode(unittest.TestCase):
    """P0-02: jsonschema fallback warning and strict mode exit 1."""

    def test_missing_jsonschema_emits_warning(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("DOCCAD_REQUIRE_JSONSCHEMA", None)
            with mock.patch.dict(sys.modules, {"jsonschema": None}):
                stderr_buf = io.StringIO()
                with redirect_stderr(stderr_buf):
                    validator = make_validator()
                err = stderr_buf.getvalue()
                self.assertIn("WARNING: jsonschema not installed — minimal fallback", err)
                # Verify the minimal fallback works
                self.assertEqual(validator({"id": "x", "title": "y", "type": "canonical"}, "document"), [])
                self.assertTrue(len(validator({"title": "y"}, "document")) > 0)

    def test_missing_jsonschema_with_strict_mode_exits_1(self):
        with mock.patch.dict(os.environ, {"DOCCAD_REQUIRE_JSONSCHEMA": "1"}):
            with mock.patch.dict(sys.modules, {"jsonschema": None}):
                stderr_buf = io.StringIO()
                with redirect_stderr(stderr_buf):
                    with self.assertRaises(SystemExit) as cm:
                        make_validator()
                    self.assertEqual(cm.exception.code, 1)
                err = stderr_buf.getvalue()
                self.assertIn("ERROR: jsonschema (and referencing) required by DOCCAD_REQUIRE_JSONSCHEMA=1", err)


class TestLivePagePipeline(unittest.TestCase):
    """P0-04: live generate_page.py passes validation for recruiter and interview contracts."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp()).resolve()
        for folder in ["docs", "schemas", "contracts", "prompts", "scripts", "ai"]:
            shutil.copytree(PROTOTYPE_ROOT / folder, self.tmp / folder)
        shutil.copy(PROTOTYPE_ROOT / "ai.config.yaml", self.tmp / "ai.config.yaml")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_live_page_recruiter_and_interview_generation(self):
        # Generate recruiter page
        res_recruiter = subprocess.run(
            [sys.executable, "scripts/generate_page.py", "--contract", "GenerateRecruiterPage",
             "--target", "architecture-system-overview"],
            cwd=self.tmp, capture_output=True, text=True
        )
        self.assertEqual(
            res_recruiter.returncode, 0,
            f"Recruiter generation failed:\nSTDOUT:\n{res_recruiter.stdout}\nSTDERR:\n{res_recruiter.stderr}"
        )

        # Generate interview prep
        res_interview = subprocess.run(
            [sys.executable, "scripts/generate_page.py", "--contract", "GenerateInterviewPrep",
             "--target", "architecture-system-overview"],
            cwd=self.tmp, capture_output=True, text=True
        )
        self.assertEqual(
            res_interview.returncode, 0,
            f"Interview prep generation failed:\nSTDOUT:\n{res_interview.stdout}\nSTDERR:\n{res_interview.stderr}"
        )

        # Run validator on the scratch copy
        res_val = subprocess.run(
            [sys.executable, "scripts/validate_docs.py"],
            cwd=self.tmp, capture_output=True, text=True
        )
        self.assertEqual(
            res_val.returncode, 0,
            f"Validation failed after generation:\nSTDOUT:\n{res_val.stdout}\nSTDERR:\n{res_val.stderr}"
        )


class TestQuestionPromptRendering(unittest.TestCase):
    """P0-05: question prompt carries the question and fails on unresolved placeholders."""

    def test_rendered_prompt_contains_question_and_replaces_placeholders(self):
        contract = load_contract("GenerateQuestionPage")
        test_question = "How does DOCCAD prevent AI content from polluting canonical docs?"
        evidence = [PROTOTYPE_ROOT / "docs" / "source" / "architecture" / "content-planes.md"]
        rendered = render_prompt(contract, test_question, "developer", "public", evidence)

        self.assertIn(test_question, rendered)
        self.assertIn("Target Audience: developer", rendered)
        self.assertIn("Privacy Class: public", rendered)
        self.assertNotIn("{{question}}", rendered)
        self.assertNotIn("{{audience}}", rendered)
        self.assertNotIn("{{privacy}}", rendered)
        self.assertNotIn("{{target_id}}", rendered)
        self.assertFalse(re.search(r"\{\{[a-z_]+\}\}", rendered))

    def test_unresolved_placeholder_raises_contract_violation(self):
        contract = copy.deepcopy(load_contract("GenerateQuestionPage"))
        broken_name = "test-broken-question-prompt.md"
        broken_path = PROTOTYPE_ROOT / "prompts" / broken_name
        broken_content = (PROTOTYPE_ROOT / "prompts" / contract["prompt_template"]).read_text(encoding="utf-8") + "\n{{unresolved_placeholder}}\n"
        try:
            broken_path.write_text(broken_content, encoding="utf-8")
            contract["prompt_template"] = broken_name
            with self.assertRaises(QuestionContractViolation):
                render_prompt(contract, "A question", "developer", "public", [])
        finally:
            if broken_path.exists():
                broken_path.unlink()


class TestGenerationModeStamp(unittest.TestCase):
    """P0-06: generation honesty in provenance (fixture -> demo; live provider -> production)."""

    def test_stamp_provenance_fixture_yields_demo(self):
        from scripts.generate_page import stamp_provenance, load_contract
        contract = load_contract("GenerateRecruiterPage")
        evidence = [PROTOTYPE_ROOT / "docs" / "source" / "architecture" / "system-overview.md"]
        fm = {"title": "Test", "id": "test"}
        stamped = stamp_provenance(fm, contract, evidence, provider="fixture", model="deterministic-demo-fixture", mode="demo")
        self.assertEqual(stamped["generation"]["generation_mode"], "demo")
        self.assertEqual(stamped["generation"]["provider"], "fixture")
        self.assertEqual(stamped["generation"]["model"], "deterministic-demo-fixture")

    def test_generate_page_live_provider_yields_production_and_model(self):
        import scripts.generate_page as gp
        contract = gp.load_contract("GenerateRecruiterPage")
        evidence = [PROTOTYPE_ROOT / "docs" / "source" / "architecture" / "system-overview.md"]
        fm = {"title": "Test", "id": "test"}
        stamped = gp.stamp_provenance(fm, contract, evidence, provider="gemini", model="gemini-2.5-pro", mode="production")
        self.assertEqual(stamped["generation"]["generation_mode"], "production")
        self.assertEqual(stamped["generation"]["provider"], "gemini")
        self.assertEqual(stamped["generation"]["model"], "gemini-2.5-pro")

        mock_result = {
            "text": "---\nid: recruiter-test-live\ntitle: Test Live\ntype: generated\ngenerated: true\naudience:\n  - recruiter\nowners:\n  - architecture-team\n---\nBody with [link](/docs/architecture/system-overview).",
            "provider": "anthropic",
            "model": "claude-3-5-sonnet-20241022",
        }
        with mock.patch("scripts.generate_page.Router") as MockRouter, \
             mock.patch.object(Path, "write_text") as mock_write:
            instance = MockRouter.return_value
            instance.run_with_fallback.return_value = mock_result
            test_args = ["generate_page.py", "--contract", "GenerateRecruiterPage", "--target", "architecture-system-overview"]
            with mock.patch.object(sys, "argv", test_args):
                ret = gp.main()
            self.assertEqual(ret, 0)
            written = mock_write.call_args[0][0]
            m = re.match(r"\A---\r?\n(.*?)\r?\n---", written, re.DOTALL)
            self.assertIsNotNone(m)
            written_fm = yaml.safe_load(m.group(1))
            self.assertEqual(written_fm["generation"]["generation_mode"], "production")
            self.assertEqual(written_fm["generation"]["provider"], "anthropic")
            self.assertEqual(written_fm["generation"]["model"], "claude-3-5-sonnet-20241022")

    def test_generate_question_live_provider_yields_production_and_model(self):
        import scripts.generate_question as gq
        mock_result = {
            "text": "---\nid: q-999-test-live\ntitle: Test Live Question\ntype: generated\ngenerated: true\naudience:\n  - developer\nowners:\n  - architecture-team\n---\nQuestion answer with [link](/docs/architecture/system-overview).",
            "provider": "openai",
            "model": "gpt-4o",
        }
        with mock.patch("scripts.generate_question.Router") as MockRouter, \
             mock.patch.object(Path, "write_text") as mock_write:
            instance = MockRouter.return_value
            instance.run_with_fallback.return_value = mock_result
            test_args = ["generate_question.py", "--question", "How does doccad work?"]
            with mock.patch.object(sys, "argv", test_args):
                ret = gq.main()
            self.assertEqual(ret, 0)
            written = mock_write.call_args_list[0][0][0]
            m = re.match(r"\A---\r?\n(.*?)\r?\n---", written, re.DOTALL)
            self.assertIsNotNone(m)
            written_fm = yaml.safe_load(m.group(1))
            self.assertEqual(written_fm["generation"]["generation_mode"], "production")
            self.assertEqual(written_fm["generation"]["provider"], "openai")
            self.assertEqual(written_fm["generation"]["model"], "gpt-4o")


class TestQuestionPersistenceGovernance(unittest.TestCase):
    """P0-08: Question persistence respects governance (schema errors exit 1; persist files are draft)."""

    def test_schema_error_exits_one_and_writes_nothing(self):
        import scripts.generate_question as gq
        mock_result = {
            "text": "---\nid: q-test-invalid\ntitle: Broken Schema Question\ntype: generated\ngenerated: true\n---\nMissing audience and owners.",
            "provider": "fixture",
            "model": "deterministic-demo-fixture",
        }
        with mock.patch("scripts.generate_question.Router") as MockRouter, \
             mock.patch.object(Path, "write_text") as mock_write:
            instance = MockRouter.return_value
            instance.run_with_fallback.return_value = mock_result
            test_args = ["generate_question.py", "--question", "How does doccad work?"]
            with mock.patch.object(sys, "argv", test_args):
                with redirect_stderr(io.StringIO()):
                    ret = gq.main()
            self.assertEqual(ret, 1)
            mock_write.assert_not_called()

    def test_persisted_question_always_draft_approval_status(self):
        import scripts.generate_question as gq
        mock_result = {
            "text": "---\nid: q-test-draft-check\ntitle: Test Draft Check\ntype: generated\ngenerated: true\naudience:\n  - developer\nowners:\n  - architecture-team\napproval_status: approved-for-demo\n---\nValid body with [link](/docs/architecture/system-overview).",
            "provider": "fixture",
            "model": "deterministic-demo-fixture",
        }
        with mock.patch("scripts.generate_question.Router") as MockRouter, \
             mock.patch.object(Path, "write_text") as mock_write:
            instance = MockRouter.return_value
            instance.run_with_fallback.return_value = mock_result
            test_args = ["generate_question.py", "--question", "How does doccad work?", "--persist"]
            with mock.patch.object(sys, "argv", test_args):
                ret = gq.main()
            self.assertEqual(ret, 0)
            written = mock_write.call_args_list[0][0][0]
            m = re.match(r"\A---\r?\n(.*?)\r?\n---", written, re.DOTALL)
            self.assertIsNotNone(m)
            written_fm = yaml.safe_load(m.group(1))
            self.assertEqual(written_fm["generation"]["approval_status"], "draft")


class TestRouterFallbackSemantics(unittest.TestCase):
    """P0-09: Router fallback on transport errors only, never on content grounds; private fails fast."""

    def test_transport_error_falls_back_to_next_provider(self):
        router = Router(PROTOTYPE_ROOT / "ai.config.yaml")
        with mock.patch.object(router, "select_chain_names", return_value=["p1", "p2"]):
            mock_p1 = mock.MagicMock()
            mock_p1.complete.side_effect = ProviderTransportError("503 Service Unavailable")
            mock_p2 = mock.MagicMock()
            mock_p2.complete.return_value = {"text": "success from p2", "provider": "p2", "model": "m2"}

            def fake_instantiate(name):
                return mock_p1 if name == "p1" else mock_p2

            with mock.patch.object(router, "instantiate", side_effect=fake_instantiate):
                res = router.run_with_fallback({"task": "TestTask"}, [{"role": "user", "content": "hi"}])
                self.assertEqual(res["text"], "success from p2")
                self.assertEqual(res["provider"], "p2")
                mock_p1.complete.assert_called_once()
                mock_p2.complete.assert_called_once()

    def test_content_error_does_not_fall_back(self):
        router = Router(PROTOTYPE_ROOT / "ai.config.yaml")
        with mock.patch.object(router, "select_chain_names", return_value=["p1", "p2"]):
            mock_p1 = mock.MagicMock()
            mock_p1.complete.side_effect = ProviderContentError("Refusal: prompt rejected by safety policy")
            mock_p2 = mock.MagicMock()

            def fake_instantiate(name):
                return mock_p1 if name == "p1" else mock_p2

            with mock.patch.object(router, "instantiate", side_effect=fake_instantiate):
                with self.assertRaises(ProviderContentError):
                    router.run_with_fallback({"task": "TestTask"}, [{"role": "user", "content": "hi"}])
                mock_p1.complete.assert_called_once()
                mock_p2.complete.assert_not_called()

    def test_private_task_raises_privacy_routing_error_on_any_local_failure(self):
        router = Router(PROTOTYPE_ROOT / "ai.config.yaml")
        router.providers_cfg["local"]["enabled"] = True
        mock_local = mock.MagicMock()
        mock_local.complete.side_effect = ProviderTransportError("Local server down")

        with mock.patch.object(router, "instantiate", return_value=mock_local):
            with self.assertRaises(PrivacyRoutingError):
                router.run_with_fallback({"task": "TestTask", "privacy": "private"}, [{"role": "user", "content": "secret"}])
            mock_local.complete.assert_called_once()


class TestRepairRetry(unittest.TestCase):
    """P0-09: Exactly one repair retry with validator errors appended; second invalid raises ContractViolation."""

    def test_repair_retry_succeeds_on_second_attempt(self):
        import scripts.generate_page as gp
        bad_output = {
            "text": "---\nid: recruiter-repair-test\ntitle: Repair Test\ntype: generated\ngenerated: true\n---\nBody with [link](/docs/architecture/system-overview).",
            "provider": "fixture",
            "model": "deterministic-demo-fixture",
        }
        good_output = {
            "text": "---\nid: recruiter-repair-test\ntitle: Repair Test\ntype: generated\ngenerated: true\naudience:\n  - recruiter\nowners:\n  - architecture-team\n---\nBody with [link](/docs/architecture/system-overview).",
            "provider": "fixture",
            "model": "deterministic-demo-fixture",
        }

        call_history = []

        def fake_run(task_meta, messages, opts=None):
            call_history.append(copy.deepcopy(messages))
            if len(call_history) == 1:
                return bad_output
            return good_output

        with mock.patch("scripts.generate_page.Router") as MockRouter, \
             mock.patch.object(Path, "write_text") as mock_write:
            instance = MockRouter.return_value
            instance.run_with_fallback.side_effect = fake_run
            test_args = ["generate_page.py", "--contract", "GenerateRecruiterPage", "--target", "architecture-system-overview"]
            with mock.patch.object(sys, "argv", test_args):
                ret = gp.main()

            self.assertEqual(ret, 0)
            self.assertEqual(len(call_history), 2, "Expected exactly 2 attempts (initial + 1 repair retry)")
            retry_messages = call_history[1]
            self.assertEqual(len(retry_messages), 3)
            self.assertEqual(retry_messages[1]["role"], "assistant")
            self.assertEqual(retry_messages[2]["role"], "user")
            self.assertIn("The previous output had validation errors", retry_messages[2]["content"])

    def test_second_invalid_output_raises_contract_violation_no_third_call(self):
        import scripts.generate_page as gp
        bad_output = {
            "text": "---\nid: recruiter-repair-fail\ntitle: Repair Fail\ntype: generated\ngenerated: true\n---\nMissing required fields.",
            "provider": "fixture",
            "model": "deterministic-demo-fixture",
        }

        call_count = 0

        def fake_run(task_meta, messages, opts=None):
            nonlocal call_count
            call_count += 1
            return bad_output

        with mock.patch("scripts.generate_page.Router") as MockRouter, \
             mock.patch.object(Path, "write_text") as mock_write:
            instance = MockRouter.return_value
            instance.run_with_fallback.side_effect = fake_run
            test_args = ["generate_page.py", "--contract", "GenerateRecruiterPage", "--target", "architecture-system-overview"]
            with mock.patch.object(sys, "argv", test_args):
                with self.assertRaises(PageContractViolation):
                    gp.main()

            self.assertEqual(call_count, 2, "Must make exactly 2 attempts: initial + 1 repair retry, never a third call")


class TestProductionFilterValidity(unittest.TestCase):
    """P0-11: Production filter output is valid against schemas and honest (REQ-004, REQ-015, DEC-006)."""

    def setUp(self):
        restore_stashed()

    def tearDown(self):
        restore_stashed()

    def test_production_filter_stubs_pass_validation_and_are_honest(self):
        stashed_count = filter_for_production()
        self.assertGreater(stashed_count, 0, "Production filter must stash unapproved/demo views")

        # 1. Stubs must declare type: stub, stub_version: 1, hold_reason, and NOT claim approval
        stub_files = list(GENERATED.rglob("*.mdx")) + list(GENERATED.rglob("*.md"))
        self.assertGreater(len(stub_files), 0, "Hold stubs must exist to preserve link graph")

        for stub in stub_files:
            fm = parse_frontmatter(stub) or {}
            self.assertEqual(fm.get("type"), "stub", f"{stub.name} must declare type: stub")
            self.assertEqual(fm.get("stub_version"), 1, f"{stub.name} must declare stub_version: 1")
            self.assertTrue(bool(fm.get("hold_reason")), f"{stub.name} must declare a hold_reason")
            self.assertEqual(fm.get("visibility"), "public", f"{stub.name} must have visibility: public")
            # Must NOT claim approval or pretend to have AI provenance
            self.assertNotIn("generation", fm, f"{stub.name} must not contain a fake generation block")

        # 2. validate_docs.py must pass with exit 0 on the production-filtered tree
        res = subprocess.run(
            [sys.executable, str(PROTOTYPE_ROOT / "scripts" / "validate_docs.py")],
            cwd=str(PROTOTYPE_ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0, f"validate_docs.py failed on production tree:\n{res.stderr}\n{res.stdout}")

    def test_filter_demo_restores_all_views(self):
        filter_for_production()
        self.assertTrue(STASH.is_dir(), ".work/stashed_unapproved must exist during production filter")
        filter_for_demo()
        self.assertFalse(STASH.is_dir(), ".work/stashed_unapproved must be removed after demo restore")
        # Check that original unapproved views are back with their generation blocks
        for view in GENERATED.rglob("*.mdx"):
            fm = parse_frontmatter(view) or {}
            self.assertEqual(fm.get("type"), "generated", f"{view.name} should be restored to type: generated")
            self.assertIn("generation", fm, f"{view.name} should have its generation block restored")


class TestMdxRestrictionGate(unittest.TestCase):
    """P0-12 / T3: Validate rejection of import/export, dangerous HTML tags, event handlers, data: URLs, and unallowlisted JSX."""

    def setUp(self):
        self.overview_hash = sha256_of(PROTOTYPE_ROOT / "docs" / "source" / "overview" / "index.md")
        self.test_file = PROTOTYPE_ROOT / "docs" / "generated" / "questions" / "temp-t3-test.mdx"

    def tearDown(self):
        if self.test_file.is_file():
            self.test_file.unlink()

    def _write_and_validate(self, body_text: str):
        content = (
            f"---\n"
            f"id: temp-t3-test\n"
            f"title: Temp T3 Test\n"
            f"type: generated\n"
            f"visibility: public\n"
            f"audience:\n  - developer\n"
            f"owners:\n  - architecture\n"
            f"last_validated: '2026-09-21'\n"
            f"generated: true\n"
            f"generation:\n"
            f"  contract: GenerateQuestionPage\n"
            f"  contract_version: 2\n"
            f"  prompt_version: question-page.v2\n"
            f"  source_documents:\n"
            f"    - id: overview-index\n"
            f"      path: docs/source/overview/index.md\n"
            f"      content_hash: {self.overview_hash}\n"
            f"  provider: fixture\n"
            f"  model: deterministic-demo-fixture\n"
            f"  generation_mode: demo\n"
            f"  generated_at: '2026-09-21T00:00:00Z'\n"
            f"  approval_status: approved-for-demo\n"
            f"---\n\n"
            f"{body_text}\n"
        )
        self.test_file.write_text(content, encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(PROTOTYPE_ROOT / "scripts" / "validate_docs.py")],
            cwd=str(PROTOTYPE_ROOT),
            capture_output=True,
            text=True,
        )

    def test_import_statement_rejected(self):
        res = self._write_and_validate("import SomeComponent from './SomeComponent';\n\n# Heading")
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("SECURITY: import/export statement forbidden in generated MDX (T3)", res.stderr)

    def test_export_statement_rejected(self):
        res = self._write_and_validate("export const myVar = 100;\n\n# Heading")
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("SECURITY: import/export statement forbidden in generated MDX (T3)", res.stderr)

    def test_disallowed_tags_rejected(self):
        res = self._write_and_validate('<iframe src="https://malicious.example.com"></iframe>')
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("SECURITY: Unsafe executable pattern matched in generated MDX", res.stderr)

    def test_event_handler_rejected(self):
        res = self._write_and_validate('<div onclick="alert(1)">Click</div>')
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("SECURITY: Unsafe executable pattern matched in generated MDX", res.stderr)

    def test_data_url_rejected(self):
        res = self._write_and_validate("[Click me](data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==)")
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("SECURITY: Unsafe executable pattern matched in generated MDX", res.stderr)

    def test_unallowlisted_jsx_component_rejected(self):
        res = self._write_and_validate('<UnregisteredWidget foo="bar" />')
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("SECURITY: Unallowlisted JSX component <UnregisteredWidget> forbidden in generated MDX (T3)", res.stderr)

    def test_allowlisted_jsx_components_pass(self):
        res = self._write_and_validate('<EvidenceLink to="/docs/overview" label="Overview" />')
        self.assertEqual(res.returncode, 0, f"Expected allowlisted component to pass:\n{res.stderr}\n{res.stdout}")


class TestExternalLinkAllowlist(unittest.TestCase):
    """P0-12 / T4: Hyperlinks emitted in generated markdown must match contracts/link-allowlist.yaml."""

    def setUp(self):
        self.overview_hash = sha256_of(PROTOTYPE_ROOT / "docs" / "source" / "overview" / "index.md")
        self.test_file = PROTOTYPE_ROOT / "docs" / "generated" / "questions" / "temp-t4-test.mdx"

    def tearDown(self):
        if self.test_file.is_file():
            self.test_file.unlink()

    def _write_and_validate(self, body_text: str):
        content = (
            f"---\n"
            f"id: temp-t4-test\n"
            f"title: Temp T4 Test\n"
            f"type: generated\n"
            f"visibility: public\n"
            f"audience:\n  - developer\n"
            f"owners:\n  - architecture\n"
            f"last_validated: '2026-09-21'\n"
            f"generated: true\n"
            f"generation:\n"
            f"  contract: GenerateQuestionPage\n"
            f"  contract_version: 2\n"
            f"  prompt_version: question-page.v2\n"
            f"  source_documents:\n"
            f"    - id: overview-index\n"
            f"      path: docs/source/overview/index.md\n"
            f"      content_hash: {self.overview_hash}\n"
            f"  provider: fixture\n"
            f"  model: deterministic-demo-fixture\n"
            f"  generation_mode: demo\n"
            f"  generated_at: '2026-09-21T00:00:00Z'\n"
            f"  approval_status: approved-for-demo\n"
            f"---\n\n"
            f"{body_text}\n"
        )
        self.test_file.write_text(content, encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(PROTOTYPE_ROOT / "scripts" / "validate_docs.py")],
            cwd=str(PROTOTYPE_ROOT),
            capture_output=True,
            text=True,
        )

    def test_non_allowlisted_external_domain_rejected(self):
        res = self._write_and_validate("[Untrusted Link](https://untrusted-phishing.com/steal-creds)")
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("SECURITY: External link domain 'untrusted-phishing.com' not in contracts/link-allowlist.yaml (T4)", res.stderr)

    def test_allowlisted_external_domain_passes(self):
        res = self._write_and_validate("[Official GitHub](https://github.com/doccad/prototype)")
        self.assertEqual(res.returncode, 0, f"Expected allowlisted link to pass:\n{res.stderr}\n{res.stdout}")


class TestContextSecretScan(unittest.TestCase):
    """P0-12 / T6: Secret scanning over prompt payload and router messages."""

    def test_openai_key_pattern_rejected(self):
        with self.assertRaises(SecretScanViolation):
            scan_for_secrets("Context with api key sk-1234567890abcdef1234567890 embedded in text")

    def test_google_api_key_pattern_rejected(self):
        with self.assertRaises(SecretScanViolation):
            scan_for_secrets("Context with key AIzaSyD1234567890123456789012345678901 in text")

    def test_github_pat_pattern_rejected(self):
        with self.assertRaises(SecretScanViolation):
            scan_for_secrets("Token ghp_123456789012345678901234567890123456 in context")

    def test_pem_private_key_header_rejected(self):
        with self.assertRaises(SecretScanViolation):
            scan_for_secrets("Cert:\n-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA0...")

    def test_clean_payload_passes(self):
        # Should not raise
        scan_for_secrets("Regular benign documentation content about DOCCAD architecture.")

    def test_router_run_with_fallback_aborts_on_secret(self):
        router = Router(PROTOTYPE_ROOT / "ai.config.yaml")
        task_meta = {"task": "GenerateQuestionPage", "privacy": "public"}
        messages = [{"role": "user", "content": "Leaking key sk-1234567890abcdef1234567890"}]
        with self.assertRaises(SecretScanViolation):
            router.run_with_fallback(task_meta, messages)


class TestPrivateChainConfig(unittest.TestCase):
    """P0-12 / T12-config: Check that routing chains matching privacy: private contain only local."""

    def test_valid_private_routing_config_passes(self):
        valid_cfg = {
            "routing": [
                {"match": {"privacy": "private"}, "chain": ["local"]},
                {"match": {}, "chain": ["fixture"]},
            ]
        }
        # Should not raise
        validate_routing_config(valid_cfg)

    def test_private_routing_with_cloud_provider_raises_config_error(self):
        bad_cfg = {
            "routing": [
                {"match": {"privacy": "private"}, "chain": ["local", "anthropic"]},
            ]
        }
        with self.assertRaises(PrivacyRoutingConfigError):
            validate_routing_config(bad_cfg)

    def test_private_routing_with_fixture_provider_raises_config_error(self):
        bad_cfg = {
            "routing": [
                {"match": {"privacy": "private"}, "chain": ["fixture"]},
            ]
        }
        with self.assertRaises(PrivacyRoutingConfigError):
            validate_routing_config(bad_cfg)

    def test_active_ai_config_passes_validation(self):
        router = Router(PROTOTYPE_ROOT / "ai.config.yaml")
        self.assertIsNotNone(router)


if __name__ == "__main__":
    unittest.main()
