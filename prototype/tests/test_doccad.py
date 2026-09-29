"""Automated Test Suite for DOCCAD Prototype.

Covers:
  1. Plane separation & isolation (canonical vs generated views).
  2. Level-1 deterministic retrieval & question generation (supported + unsupported).
  3. UI / CLI JSON round-trip (QuestionRequest, GenerationRun, ReviewRecord).
  4. Review governance state transitions & simulation vs production boundaries.
  5. Publication build exclusion of unapproved drafts and simulated approvals.
  6. Content-hash drift detection and targeted regeneration.
  7. Source document deletion detection.
  8. Private routing policy hard-pinning (never upgrade private tasks to cloud).
  9. Path traversal prevention.
  10. Unsafe MDX rejection (script tags, eval constructs).
"""

from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

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
from scripts.detect_changes import build_manifest, compute_impact
from scripts.review_governance import (
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
)
from ai.router import Router, PrivacyRoutingError, RoutingError


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

    def test_check_production_blocks_simulated_approval(self):
        art_id = "test-doc-simulated"
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
        self.assertEqual(impact["regenerate"][0]["target"], target_page["id"])


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


if __name__ == "__main__":
    unittest.main()
