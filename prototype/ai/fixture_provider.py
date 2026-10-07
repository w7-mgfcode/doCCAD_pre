"""Deterministic Fixture Provider for DOCCAD Demo Workflows.

Implements the Provider protocol without external network calls, API keys, or credentials.
Produces evidence-grounded, schema-compliant outputs for:
- GenerateRecruiterPage
- GenerateInterviewPrep
- GenerateQuestionPage (supported scenarios and honest insufficient-evidence handling)
"""

from __future__ import annotations

import re
from typing import Any, Dict, List
from .provider import Provider, ProviderContentError, ProviderError

_EVIDENCE_FILE_RE = re.compile(r"<<<EVIDENCE-DATA file=(docs/source/\S+?)\.mdx?\b")
_CITED_ROUTE_RE = re.compile(r'(?:\bto=|"to":\s*)"/docs/([^"#]+)')
_CITED_ID_RE = re.compile(r'"evidence":\s*"([a-z0-9-]+)"')


class FixtureProvider:
    name: str = "fixture"

    def __init__(self, model: str = "deterministic-demo-fixture"):
        self.model = model

    def complete(
        self,
        task_meta: Dict[str, Any],
        messages: List[Dict[str, str]],
        opts: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        task = task_meta.get("task", "")
        prompt = messages[-1]["content"] if messages else ""
        
        if task == "GenerateRecruiterPage":
            text = self._generate_recruiter(prompt, task_meta.get("target_id", ""))
        elif task == "GenerateInterviewPrep":
            text = self._generate_interview(prompt, task_meta.get("target_id", ""))
        elif task == "GenerateQuestionPage":
            text = self._generate_question(prompt, task_meta)
        else:
            text = self._generate_generic(prompt, task_meta)

        if task in ("GenerateRecruiterPage", "GenerateInterviewPrep"):
            self._require_citations_in_closure(text, messages)

        return {
            "text": text,
            "usage": {
                "input_tokens": len(prompt) // 4,
                "output_tokens": len(text) // 4,
            },
            "provider": "fixture",
            "model": self.model,
            "generation_mode": "demo",
            "request_id": None,
        }

    @staticmethod
    def _require_citations_in_closure(text: str, messages: List[Dict[str, str]]) -> None:
        """Refuse canned output that cites documents outside the target's evidence closure.

        The canned texts are written for specific targets. For any other target they would
        cite pages the pipeline never assembled, fail the grounding gate, and repeat the same
        citations on the repair retry. A content error stops the run before that happens.
        Calls without assembled evidence blocks (direct unit-test calls) are not checked.
        """
        closure = set()
        for m in messages:
            closure.update(p[len("docs/source/"):] for p in _EVIDENCE_FILE_RE.findall(str(m.get("content", ""))))
        if not closure:
            return
        closure_ids = {p.replace("/", "-") for p in closure}
        missing = sorted(
            {f"/docs/{r}" for r in _CITED_ROUTE_RE.findall(text) if r not in closure}
            | {i for i in _CITED_ID_RE.findall(text) if i not in closure_ids}
        )
        if missing:
            raise ProviderContentError(
                "Fixture has no canned output grounded in this target's evidence closure "
                f"(would cite {', '.join(missing)}); use a target the fixture supports or a live provider."
            )

    def _generate_recruiter(self, prompt: str, target_id: str = "") -> str:
        tid = target_id or "project-overview"
        recruiter_id = "recruiter-project-overview" if tid == "project-overview" else f"recruiter-{tid}"
        slug = f"/recruiter/{tid}"

        if tid == "architecture-system-overview":
            highlights = """- <EvidenceLink to="/docs/architecture/content-planes">Structural plane separation</EvidenceLink> preventing unverified AI hallucination from laundering into canonical documents.
- <EvidenceLink to="/docs/decisions/adr-002-docusaurus-foundation">88.6/100 weighted platform selection</EvidenceLink> favoring offline reproducibility and independent operation over vendor lock-in.
- <EvidenceLink to="/docs/architecture/ai-generation-plane">Governed generation plane</EvidenceLink> assembling evidence deterministically."""
            table = """| Competency | Implementation in DOCCAD | Canonical Verification |
|---|---|---|
| **System Architecture & Decomposition** | 6-component decoupled topology separating authoring, static serving, and CI generation. | <EvidenceLink to="/docs/architecture/system-overview">System Architecture Overview</EvidenceLink> |
| **Structural Plane Isolation** | Two independent Docusaurus docs plugins physically separating `/docs` and `/views`. | <EvidenceLink to="/docs/architecture/content-planes">Content Planes Separation</EvidenceLink> |
| **Offline Governed Generation** | Contract-driven generation pipeline with Level-1 deterministic retrieval and provenance hashes. | <EvidenceLink to="/docs/architecture/ai-generation-plane">AI Generation Plane</EvidenceLink> |
| **Publishing Platform Foundation** | Evaluated 6 platforms; Docusaurus 3.x selected (88.6/100) for dual-plugin support and offline build. | <EvidenceLink to="/docs/decisions/adr-002-docusaurus-foundation">ADR-002: Docusaurus Foundation</EvidenceLink> |"""
        else:
            highlights = """- <EvidenceLink to="/docs/architecture/content-planes">Structural plane separation</EvidenceLink> preventing unverified AI hallucination from laundering into canonical documents.
- <EvidenceLink to="/docs/decisions/adr-002-docusaurus-foundation">88.6/100 weighted platform selection</EvidenceLink> favoring offline reproducibility and independent operation over vendor lock-in.
- <EvidenceLink to="/docs/validation/drift-detection">Deterministic sha256 hash tracking</EvidenceLink> ensuring only out-of-date derived pages regenerate upon source edits."""
            table = """| Competency | Implementation in DOCCAD | Canonical Verification |
|---|---|---|
| **System Security & Threat Modeling** | 6-zone trust boundary model, strict demarcation of untrusted user input as inert data, and link allowlist gating. | <EvidenceLink to="/docs/security/trust-boundaries">Security Trust Boundaries</EvidenceLink> |
| **Drift & Invalidation Engineering** | Bidirectional dependency manifest (`.docs-manifest.json`) recomputing file hashes to drive targeted, non-full-corpus regeneration. | <EvidenceLink to="/docs/validation/drift-detection">Drift Detection Specification</EvidenceLink> |
| **Privacy Hard-Pinning** | Tasks flagged `privacy: private` route strictly to local models; fallback to cloud providers is prohibited and raises fatal exceptions. | <EvidenceLink to="/docs/decisions/adr-004-provider-abstraction">ADR-004: Provider Abstraction</EvidenceLink> |
| **Bilingual Architecture** | Filesystem-based Docusaurus i18n (`en` and `hu`), maintaining canonical English parity while providing localized UI and core onboarding. | <EvidenceLink to="/docs/overview/vision-and-goals">Vision & Goals: Bilingual Tenet</EvidenceLink> |"""

        return f"""---
id: {recruiter_id}
slug: {slug}
title: DOCCAD — Project Overview & Architecture (Recruiter View)
type: generated
audience: [recruiter, architect]
owners: [architecture]
last_validated: 2026-09-21
generated: true
generation:
  contract: GenerateRecruiterPage
  contract_version: 2
  prompt_version: recruiter.v2
  source_documents:
    - id: overview-index
      path: docs/source/overview/index.md
      content_hash: PLACEHOLDER_HASH_OVERVIEW
    - id: architecture-system-overview
      path: docs/source/architecture/system-overview.md
      content_hash: PLACEHOLDER_HASH_ARCH
    - id: architecture-content-planes
      path: docs/source/architecture/content-planes.md
      content_hash: PLACEHOLDER_HASH_PLANES
  provider: fixture
  model: deterministic-demo-fixture
  generation_mode: demo
  generated_at: 2026-09-21T00:00:00Z
  approval_status: draft
---

# Project Overview & Engineering Depth

An evidence-backed briefing on DOCCAD's architecture, design decisions, and engineering trade-offs.

## 1. 30-Second Elevator Pitch

DOCCAD is a GitHub-native documentation ecosystem designed for rigorous engineering organizations. It separates human-authored canonical knowledge (`/docs`) from AI-generated derived views (`/views`), enforcing docs-as-code principles where version-controlled files in Git remain the single source of truth. Built with Docusaurus 3.x, deterministic Level-1 retrieval, and hash-based drift detection, it delivers zero-AI-dependency static documentation that never leaves readers stranded if AI services fail.

Key verified accomplishments:
{highlights}

## 2. Two-Minute Technical Walkthrough

DOCCAD addresses the structural instability of traditional documentation by decomposing knowledge management into two isolated planes:
1. **The Human-Owned Canonical Plane (`docs/source/`)**: Engineers write Markdown/MDX documents and Mermaid diagrams subject to peer review. This plane serves `/docs` directly and constitutes the sole admissible evidence for any generation task.
2. **The Governed Generation Plane (`docs/generated/`)**: Background CLI and CI pipelines consume declarative task contracts (`contracts/*.yaml`) and assemble context strictly through Level-1 deterministic file selection. Model outputs are stamped with `sha256` content hashes of their input sources and land only as PR branches.

Readers access a static site generated via `docusaurus build`. External search, dynamic databases, and runtime AI calls are avoided by design, ensuring the site is deployable to static hosting (e.g. GitHub Pages) with zero operational attack surface.

## 3. Deep Dive: Architectural Competency Mapping

{table}
"""

    def _generate_interview(self, prompt: str, target_id: str) -> str:
        tid = target_id or "architecture-system-overview"
        return f"""{{
  "id": "{tid}",
  "elevator_pitch": "DOCCAD is a GitHub-native, docs-as-code documentation platform where canonical knowledge lives in Git and AI generates derived views in CI with full provenance and PR governance.",
  "technical_explanation": "DOCCAD decouples canonical human-written documentation from derived AI views using two Docusaurus docs-plugin instances. AI runs only in CLI/CI pipelines via a thin provider router, stamping every output with sha256 source hashes for mechanical drift detection. The published site is purely static with zero runtime AI dependencies.",
  "concepts": [
    {{
      "name": "Docs-as-code and version-controlled single source of truth",
      "explanation": "Version-controlled files in Git represent the primary ground truth. No external database or CMS is permitted in the serving path."
    }},
    {{
      "name": "Two-Plane Structural Separation",
      "explanation": "Canonical documentation (/docs) and AI-generated views (/views) run in separate Docusaurus plugin instances, physically isolating human truth from bot drafts."
    }},
    {{
      "name": "Mechanical Drift Detection",
      "explanation": "Derived pages record sha256 digests of their input sources. When source bytes change, CI detects drift and schedules targeted regeneration."
    }}
  ],
  "design_decisions": [
    {{
      "decision": "Docusaurus 3.x selected as publishing foundation",
      "rationale": "Scored 88.6/100 on weighted evaluation; offers full offline build, local search, React MDX flexibility, and multi-instance docs plugin support.",
      "evidence": "decisions-adr-002-docusaurus-foundation"
    }},
    {{
      "decision": "Two-plane structural content separation (/docs vs /views)",
      "rationale": "Two independent docs-plugin instances guarantee that unreviewed or bot-generated content cannot be served under canonical routes.",
      "evidence": "architecture-content-planes"
    }},
    {{
      "decision": "Offline governed AI generation plane with Level-1 deterministic retrieval",
      "rationale": "Zero runtime AI dependencies ensure complete offline independence and auditable PR diffs.",
      "evidence": "architecture-ai-generation-plane"
    }}
  ],
  "tradeoffs": [
    {{
      "choice": "Level-1 deterministic retrieval (file paths + frontmatter closure)",
      "benefit": "At corpus sizes under 1,500 documents, file-based grep and manifest closures are 100% reproducible and auditable in PRs.",
      "cost": "Avoids external vector infrastructure but requires frontmatter discipline."
    }},
    {{
      "choice": "Static site generation with build-time local search",
      "benefit": "Eliminates server maintenance, runtime CVEs, and vendor subscription lock-in.",
      "cost": "Ensures 100% read uptime even during complete cloud outages without runtime personalization."
    }}
  ],
  "likely_questions": [
    "How do you prevent AI-generated hallucinated content from contaminating human-authored documentation?",
    "How does the system know when a derived view is out of date after an architectural change?",
    "Why not use an agent swarm or LangChain for documentation generation?"
  ],
  "example_answers": [
    {{
      "question": "How do you prevent AI-generated hallucinated content from contaminating human-authored documentation?",
      "answer": "We enforce a physical separation using two Docusaurus docs-plugin instances: /docs for canonical human files and /views for generated views. Generated files can cite canonical docs, but canonical docs never import generated content. Furthermore, generated pages only persist through human-reviewed PRs."
    }},
    {{
      "question": "How does the system know when a derived view is out of date after an architectural change?",
      "answer": "Every generated artifact stores the sha256 content hashes of all canonical files used to create it. When CI runs detect_changes.py, it compares disk hashes against recorded provenance hashes; any mismatch flags that specific derived page as STALE, scheduling targeted regeneration."
    }},
    {{
      "question": "Why not use an agent swarm or LangChain for documentation generation?",
      "answer": "A single capable engineer operates DOCCAD. Multi-agent frameworks introduce hundreds of untracked dependencies, non-deterministic loops, and complex failure states without improving documentation grounding. A thin, 40-line provider adapter executing declarative YAML contracts is easier to audit and maintain."
    }}
  ],
  "follow_ups": [
    "When would you cross the threshold to introduce a vector database?",
    "How does private routing prevent intellectual property leakage to third-party LLMs?"
  ],
  "evidence_links": [
    {{
      "label": "System Architecture Overview",
      "to": "/docs/architecture/system-overview"
    }},
    {{
      "label": "Content Planes Separation",
      "to": "/docs/architecture/content-planes"
    }},
    {{
      "label": "AI Generation Plane",
      "to": "/docs/architecture/ai-generation-plane"
    }},
    {{
      "label": "Docusaurus Foundation",
      "to": "/docs/decisions/adr-002-docusaurus-foundation"
    }}
  ]
}}"""

    def _generate_question(self, prompt: str, task_meta: Dict[str, Any]) -> str:
        q = task_meta.get("question", "").lower()
        if not q:
            # Try to extract question from prompt
            m = (re.search(r"<<<QUESTION-DATA\s*\n(.+?)\n\s*QUESTION-DATA>>>", prompt, re.DOTALL)
                 or re.search(r"User Question:\s*(.+)", prompt, re.IGNORECASE))
            if m:
                q = m.group(1).lower()

        # Check for unsupported scenario
        if any(k in q for k in ["kubernetes", "high-frequency", "k8s", "trading", "crypto", "blockchain", "docker swarm"]):
            return """---
id: q-006-kubernetes-topology
title: "DOCCAD Question: Kubernetes Deployment Topology"
type: generated
audience: [developer, architect]
owners: [architecture]
last_validated: 2026-09-21
generated: true
generation:
  contract: GenerateQuestionPage
  contract_version: 4
  prompt_version: question-page.v4
  source_documents:
    - id: decisions-adr-009-deployment-github-pages
      path: docs/source/decisions/adr-009-deployment-github-pages.md
      content_hash: PLACEHOLDER_HASH_ADR009
  provider: fixture
  model: deterministic-demo-fixture
  generation_mode: demo
  generated_at: 2026-09-21T00:00:00Z
  approval_status: draft
---

# Question: What is DOCCAD's multi-cluster Kubernetes deployment topology?

## Status: Insufficient Canonical Evidence

> [!WARNING]
> **Refusal to Speculate**: As governed by task contract `GenerateQuestionPage` and architecture decision `AD-14`, DOCCAD models are strictly prohibited from inventing architectural details, infrastructure topologies, or technologies not evidenced in canonical repository sources.

### Findings from Canonical Knowledge
The canonical documentation contains **no evidence** for Kubernetes, multi-cluster topologies, container orchestration, or high-frequency trading configurations. 

Per canonical Architectural Decision Record [ADR-009: Deployment via GitHub Pages](/docs/decisions/adr-009-deployment-github-pages), DOCCAD is deliberately designed as a **serverless, static build artifact**:
- **Target Platform**: GitHub Pages (or any static object store / CDN).
- **Runtime Compute**: Zero runtime servers or Kubernetes clusters.
- **Architectural Rationale**: A static site eliminates cluster management overhead, node autoscaling, and container CVE patching, allowing a single engineer to operate the entire platform.

If multi-cluster container hosting is required in the future, it must first be recorded as an accepted Architectural Decision Record in `docs/source/decisions/` before this question workflow can answer it.
"""

        # Scenario 1: Canonical Separation
        if any(k in q for k in ["pollute", "separation", "plane", "clean", "human"]):
            return """---
id: q-001-canonical-separation
title: "DOCCAD Question: Separation of Canonical and Generated Planes"
type: generated
audience: [developer, architect]
owners: [architecture]
last_validated: 2026-09-21
generated: true
generation:
  contract: GenerateQuestionPage
  contract_version: 4
  prompt_version: question-page.v4
  source_documents:
    - id: architecture-content-planes
      path: docs/source/architecture/content-planes.md
      content_hash: PLACEHOLDER_HASH_PLANES
    - id: decisions-adr-003-canonical-generated-separation
      path: docs/source/decisions/adr-003-canonical-generated-separation.md
      content_hash: PLACEHOLDER_HASH_ADR003
  provider: fixture
  model: deterministic-demo-fixture
  generation_mode: demo
  generated_at: 2026-09-21T00:00:00Z
  approval_status: draft
---

# Question: How does DOCCAD prevent AI content from polluting canonical docs?

## Answer Summary
DOCCAD prevents AI pollution through a strict architectural and physical separation called the **Two Content Planes** model, enforced via separate Docusaurus plugin instances, separate routes, and PR branch protection.

## Core Architectural Mechanisms

### 1. Two Separate Docs Plugin Instances
Rather than relying on directory naming conventions, `docusaurus.config.ts` mounts two distinct `@docusaurus/plugin-content-docs` instances:
- **Canonical Plane (`docs/source/`)**: Human-authored, route `/docs`. Only human PRs may edit this plane.
- **Generated Plane (`docs/generated/`)**: Bot-authored, route `/views`. Automated generation jobs write solely to this directory.

A bot PR touching any path under `docs/source/` is automatically rejected by CI quality gates.

### 2. Unidirectional Citation Rule
- Generated views can cite canonical documentation using relative links or `<EvidenceLink>` components.
- Canonical pages are strictly forbidden from importing or citing generated views (except from a dedicated index page).
- AI generation scripts are prohibited from using generated pages as context, preventing recursive AI hallucinating on AI feedback loops.

### 3. Human PR Approval Gate
All generated files persist only through pull requests into `docs-gen/*` branches. Branch protection requires human review before any generated artifact can merge into the default branch.

## Supporting Canonical Evidence
- [Content Planes Architecture](/docs/architecture/content-planes)
- [ADR-003: Structural Separation of Canonical and Generated Knowledge](/docs/decisions/adr-003-canonical-generated-separation)
"""

        # Scenario 2: Drift Detection
        if any(k in q for k in ["drift", "hash", "stale", "change", "detect"]):
            return """---
id: q-002-drift-detection
title: "DOCCAD Question: Hash-Based Drift Detection"
type: generated
audience: [developer, architect, operator]
owners: [architecture]
last_validated: 2026-09-21
generated: true
generation:
  contract: GenerateQuestionPage
  contract_version: 4
  prompt_version: question-page.v4
  source_documents:
    - id: validation-drift-detection
      path: docs/source/validation/drift-detection.md
      content_hash: PLACEHOLDER_HASH_DRIFT
    - id: operations-runbook-stale-views
      path: docs/source/operations/runbook-stale-views.md
      content_hash: PLACEHOLDER_HASH_RUNBOOK
  provider: fixture
  model: deterministic-demo-fixture
  generation_mode: demo
  generated_at: 2026-09-21T00:00:00Z
  approval_status: draft
---

# Question: How does DOCCAD detect drift when canonical architecture changes?

## Answer Summary
DOCCAD detects drift mechanically using **sha256 content hashes** stored directly in the frontmatter of generated pages. When a canonical file changes, a deterministic script re-evaluates all hashes against disk and flags only the affected derived pages as stale.

## Detailed Drift Workflow

### 1. Hash Recording at Generation Time
When a view (such as a recruiter page or question answer) is generated, `generate_page.py` computes the `sha256` digest of each canonical document included in the context and stores it in the `generation.source_documents` frontmatter array:
```yaml
generation:
  source_documents:
    - id: architecture-system-overview
      path: docs/source/architecture/system-overview.md
      content_hash: sha256:4f8a1...
```

### 2. CI Verification (`detect_changes.py`)
On every push or scheduled audit:
1. `scripts/detect_changes.py` inspects `.docs-manifest.json` and parses all files.
2. For every generated view, it computes the current on-disk `sha256` of each referenced source.
3. If any recorded hash differs from disk, the view is labeled `STALE` in `impact.json`.

### 3. Targeted, Non-Full-Corpus Regeneration
Instead of costly full-corpus re-runs, the system schedules regeneration **only** for the specific views identified in `impact.json`. Unaffected pages remain untouched.

## Supporting Canonical Evidence
- [Drift Detection & Freshness Specification](/docs/validation/drift-detection)
- [Runbook: Managing Stale Views](/docs/operations/runbook-stale-views)
"""

        # Scenario 3: Security & Trust Zones
        if any(k in q for k in ["security", "injection", "trust", "untrusted", "zone"]):
            return """---
id: q-003-security-trust-zones
title: "DOCCAD Question: Security Architecture and Trust Zones"
type: generated
audience: [developer, architect, operator]
owners: [architecture]
last_validated: 2026-09-21
generated: true
generation:
  contract: GenerateQuestionPage
  contract_version: 4
  prompt_version: question-page.v4
  source_documents:
    - id: security-trust-boundaries
      path: docs/source/security/trust-boundaries.md
      content_hash: PLACEHOLDER_HASH_TRUST
    - id: security-prompt-injection-defense
      path: docs/source/security/prompt-injection-defense.md
      content_hash: PLACEHOLDER_HASH_INJECTION
  provider: fixture
  model: deterministic-demo-fixture
  generation_mode: demo
  generated_at: 2026-09-21T00:00:00Z
  approval_status: draft
---

# Question: What is DOCCAD's security model for prompt injection and untrusted inputs?

## Answer Summary
DOCCAD enforces a **6-Zone Trust Boundary Model** with a strict rule: repository content and user questions are treated strictly as **DATA**, never as model instructions.

## Key Defenses Against Prompt Injection

1. **Explicit Data Delimiters**: Evidence files enter prompt templates wrapped in `<<<EVIDENCE-DATA` and `EVIDENCE-DATA>>>` tokens. Templates instruct the model to treat text between delimiters purely as inert documentation facts.
2. **Context Secret Scan**: Before any prompt payload is passed to a provider, an automated regex scan checks for accidental tokens or credentials.
3. **Structured Output Validation**: Model responses must conform to schema contracts (`schemas/document.schema.json`). Executable JavaScript/MDX constructs (`script tags`, dynamic code evaluation, dangerous React imports) are rejected by deterministic static analysis before compilation.
4. **Link Allowlist**: External hyperlinks in generated content must match `contracts/link-allowlist.yaml`; non-allowlisted domains trigger security rejection.
5. **No Serving Backend**: The published documentation is a static website. There is no runtime prompt endpoint, eliminating real-time jailbreaking of the reading audience.

## Supporting Canonical Evidence
- [Security Architecture: Trust Boundaries](/docs/security/trust-boundaries)
- [Prompt Injection Defenses](/docs/security/prompt-injection-defense)
"""

        # Scenario 4: Docusaurus Platform Selection
        if any(k in q for k in ["docusaurus", "mintlify", "mkdocs", "decision", "platform", "select"]):
            return """---
id: q-004-docusaurus-selection
title: "DOCCAD Question: Docusaurus Platform Selection Rationale"
type: generated
audience: [developer, architect]
owners: [architecture]
last_validated: 2026-09-21
generated: true
generation:
  contract: GenerateQuestionPage
  contract_version: 4
  prompt_version: question-page.v4
  source_documents:
    - id: decisions-adr-002-docusaurus-foundation
      path: docs/source/decisions/adr-002-docusaurus-foundation.md
      content_hash: PLACEHOLDER_HASH_ADR002
    - id: architecture-platform-research
      path: docs/source/architecture/platform-research.md
      content_hash: PLACEHOLDER_HASH_RESEARCH
  provider: fixture
  model: deterministic-demo-fixture
  generation_mode: demo
  generated_at: 2026-09-21T00:00:00Z
  approval_status: draft
---

# Question: Why did DOCCAD select Docusaurus over Mintlify or MkDocs?

## Answer Summary
Docusaurus 3.x won the 11-criterion weighted evaluation with an **88.6/100** score, surpassing Mintlify (85.0), MkDocs+Material (83.8), and GitBook (72.2). The critical deciding factors were multi-instance plugin support, native offline static generation, and provider independence.

## Comparative Decision Matrix

| Evaluation Criterion | Docusaurus 3.x (88.6) | Mintlify (85.0) | MkDocs+Material (83.8) |
|---|---|---|---|
| **Two-Plane Separation** | Native via dual `plugin-content-docs` | Single flat structure; requires path hack | Flat docs structure |
| **Offline Independence** | Complete local build; zero cloud dependency | Hosted SaaS dependency for advanced features | Complete local build via Python |
| **Component Extensibility** | Full React 19 / TypeScript ecosystem | Proprietary components | Jinja2 templates / Python hooks |
| **Mermaid Support** | Official theme integration | Native support | Supported via pymdownx superfences |
| **Search Architecture** | Local offline search index plugin | Hosted SaaS search index | Client-side Lunr/search index |

Mintlify had strong styling but was disqualified as primary choice due to SaaS lock-in and lack of multi-instance docs separation. MkDocs was a solid runner-up, but Docusaurus provided superior interactive React component capabilities (essential for `<InterviewPrep>` and `<EvidenceLink>`).

## Supporting Canonical Evidence
- [ADR-002: Docusaurus 3.x Publishing Foundation](/docs/decisions/adr-002-docusaurus-foundation)
- [Six-Platform Research Synthesis](/docs/architecture/platform-research)
"""

        # Scenario 5: Private Routing Policy
        return """---
id: q-005-private-routing
title: "DOCCAD Question: Private Routing and Zero Cloud Fallback"
type: generated
audience: [developer, architect, operator]
owners: [architecture]
last_validated: 2026-09-21
generated: true
generation:
  contract: GenerateQuestionPage
  contract_version: 4
  prompt_version: question-page.v4
  source_documents:
    - id: decisions-adr-004-provider-abstraction
      path: docs/source/decisions/adr-004-provider-abstraction.md
      content_hash: PLACEHOLDER_HASH_ADR004
    - id: architecture-ai-generation-plane
      path: docs/source/architecture/ai-generation-plane.md
      content_hash: PLACEHOLDER_HASH_GENPLANE
  provider: fixture
  model: deterministic-demo-fixture
  generation_mode: demo
  generated_at: 2026-09-21T00:00:00Z
  approval_status: draft
---

# Question: How does private routing prevent data leakage to cloud model providers?

## Answer Summary
DOCCAD's `Router` implements an irrevocable **privacy hard-pinning rule**: any generation task flagged with `privacy: private` is strictly confined to local execution. If the local provider is unavailable, the pipeline terminates immediately rather than falling back to cloud providers.

## Technical Routing Mechanism

1. **Policy in `ai.config.yaml`**:
   ```yaml
   routing:
     - match: {privacy: private}
       chain: [local]
   ```
2. **Deterministic Code Enforcement**:
   In `ai/router.py`, the check is non-negotiable:
   ```python
   if task_meta.get("privacy") == "private":
       if not self.providers_cfg.get("local", {}).get("enabled", False):
           raise PrivacyRoutingError(
               "Task is privacy: private but local provider is disabled. "
               "Refusing to route to any cloud provider."
           )
       return ["local"]
   ```
3. **Zero Fallback Guarantee**: If local model execution times out or errors, `run_with_fallback` catches the failure, suppresses cloud fallback, and raises a fatal `PrivacyRoutingError`.

This structural guarantee ensures that confidential internal code or proprietary architectural discussions never leak to third-party APIs.

## Supporting Canonical Evidence
- [ADR-004: Thin Provider Abstraction](/docs/decisions/adr-004-provider-abstraction)
- [AI Generation Plane Architecture](/docs/architecture/ai-generation-plane)
"""

    def _generate_generic(self, prompt: str, task_meta: Dict[str, Any]) -> str:
        return """---
id: generic-derived-view
title: Derived Architectural Summary
type: generated
audience: [developer]
owners: [architecture]
last_validated: 2026-09-21
generated: true
generation:
  contract: GenerateArchitectureManual
  contract_version: 1
  prompt_version: general.v1
  source_documents:
    - id: architecture-system-overview
      path: docs/source/architecture/system-overview.md
      content_hash: PLACEHOLDER_HASH_ARCH
  provider: fixture
  model: deterministic-demo-fixture
  generation_mode: demo
  generated_at: 2026-09-21T00:00:00Z
  approval_status: draft
---

# Derived Architectural Summary

This view was generated deterministically by the fixture provider based on canonical evidence.
"""
