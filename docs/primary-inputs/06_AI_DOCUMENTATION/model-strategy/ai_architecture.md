# AI Architecture — Generation Plane, Provider Abstraction, Retrieval, Contracts

Status: final · 2026-08-12 · Binds AD-4…AD-8, AD-11, AD-15 from `ARCHITECTURE-SPINE.md`.
Diagrams: `diagrams/model_routing.mmd`, `diagrams/c4_l3_components.mmd`, flow diagrams per feature.

## 1. Position in the System

AI is an **enrichment plane**: Python scripts run in GitHub Actions or a developer shell, read canonical
files, write derived files into a bot branch, and open PRs. The published site has zero AI dependency
(AD-4/§9 of the mission). If every provider is down: reads work, builds work, canonical authoring works;
only new generation waits.

## 2. Provider Abstraction (AD-5)

One interface, four adapters, no framework. The simpler alternative each component beat is noted inline.

```
ai/
├── provider.py      # Protocol: complete(task_meta, messages, opts) -> {text, usage, provider, model}
├── anthropic.py     # Messages API over HTTPS (stdlib/requests; no heavy SDK needed)
├── gemini.py        # generateContent REST
├── openai.py        # chat completions REST
├── local.py         # OpenAI-compatible endpoint (Ollama, llama.cpp server, vLLM)
└── router.py        # policy from ai.config.yaml → ordered provider chain
```

Beat: LangChain/LiteLLM-style frameworks (hundreds of transitive deps to wrap four HTTP POSTs — rejected;
adapters are ~40 lines each and fully auditable). Beat: per-task hard-coded clients (routing would fork).

### Routing policy

```yaml
ai:
  default_provider: anthropic
  providers:
    anthropic: {enabled: true,  env_key: ANTHROPIC_API_KEY, model: ${AI_MODEL_ANTHROPIC}}
    gemini:    {enabled: true,  env_key: GEMINI_API_KEY,    model: ${AI_MODEL_GEMINI}}
    openai:    {enabled: true,  env_key: OPENAI_API_KEY,    model: ${AI_MODEL_OPENAI}}
    local:     {enabled: false, endpoint: "http://localhost:11434/v1", model: ${AI_MODEL_LOCAL}}
  routing:
    - match: {privacy: private}          # privacy routing is enforced, not advisory
      chain: [local]                      # hard fail if local unavailable — never silently upgrade to cloud
    - match: {task: UpdateMermaidDiagram}
      chain: [anthropic, openai]
    - match: {context_tokens: ">100k"}
      chain: [gemini, anthropic]
    - match: {}                           # default
      chain: [anthropic, gemini, openai]
```

Model names are environment/config values only (AD-5): the repo never hard-codes a model id, so provider
model churn never requires a code change. Routing criteria supported: privacy class, task type, context
size, structured-output requirement, cost tier, availability (fallback on 5xx/timeout only — never on
content grounds). Deliberately absent: latency-based load balancing, multi-agent orchestration, autonomous
tool use (rejected under anti-overengineering — no requirement justifies them).

## 3. Retrieval / Context Engineering (AD-7)

**Level 1 (adopted).** Context assembly is deterministic and auditable:
1. Files explicitly named by the contract invocation (e.g. the canonical page being transformed).
2. Frontmatter closure: `sources[]` repo paths (truncated by budget) + `related[]` docs, one hop.
3. Keyword expansion: `git grep -l` over `docs/source/` for contract-declared key terms, capped.
4. Priority-ordered truncation to the task's context budget; every included file is listed in the run
   report, so grounding is reviewable in the PR.

**Escalation boundaries (recorded, not built):** Level 2 (build-time full-text index, reusing the search
plugin's index) when corpus >~1,500 pages or the grep step demonstrably misses relevant canon. Level 3
(embeddings) only after Level 2 fails measurably on retrieval quality — requires a persisted index and
becomes the first real "service-ish" component, hence deferred. Level 4 (hybrid+rerank) unjustifiable at
this scale. The decision boundary lives in ADR-006; revisit requires evidence (failed-grounding examples),
not enthusiasm.

## 4. Task Contracts (AD-6)

Contracts are YAML in `contracts/`, versioned, schema'd. Catalog:

| Contract | Inputs | Allowed evidence | Output | Persistence |
|---|---|---|---|---|
| GenerateRecruiterPage | audience depth | canonical docs + manifest repo facts | recruiter MDX (3 depths) | PR |
| GenerateInterviewPrep | canonical page id | that page + `related` closure | `<id>.interview.json` | PR |
| GenerateQuestionPage | user question text | retrieval per §3 | `q-NNN` MDX + citations | PR |
| GenerateTroubleshootingGuide | symptom scope | runbooks + ops canon | MDX | PR |
| GenerateArchitectureManual | scope | architecture canon + diagrams | MDX section | PR |
| GenerateDeveloperGuide | scope | dev canon + repo config files | MDX | PR |
| UpdateMermaidDiagram | diagram path + change intent | the .mmd + citing pages | .mmd | PR |
| SummarizeRepositoryChange | commit range | git diff + manifest | summary MDX (advisory) | PR |
| DetectDocumentationDrift | diff + manifest | deterministic inputs only | advisory labels/report | none (CI annotation) |

Every contract file defines: `inputs` (typed), `allowed_evidence` (path globs — the context assembler
refuses anything outside them), `output_schema` (JSON schema for structured outputs; MDX outputs validated
by frontmatter schema + build), `quality_gates` (deterministic checks that must pass), `prohibited`
(explicit list: invented metrics, unevidenced technologies, achievements, adoption claims, security
guarantees), `model_requirements` (structured output? min context?), `persistence` (always `pr` except
advisory tasks). Prompts are Markdown templates in `prompts/`, referenced by version
(`prompt_version: recruiter.v1`); changing a prompt bumps the version and marks dependent pages stale.

## 5. Generation Pipeline (per artifact)

contract load → evidence assembly (§3, restricted to `allowed_evidence`) → prompt render (instruction block
+ delimited evidence blocks; evidence is DATA, injected instructions in evidence are inert by construction
of the template — see security_architecture.md) → router (§2) → single model call → parse (schema or MDX) →
deterministic gates: frontmatter valid, citations present and resolving, external links allowlisted, Mermaid
compiles, `docusaurus build` of affected instance passes → on gate failure ONE repair retry with the
validator error appended → provenance stamp (hashes, provider, versions) → commit to `docs-gen/<task>-<id>`
→ PR with run report. No loops beyond the single retry; failures surface to a human.

## 6. Recruiter View Generation

Evidence base: `00-overview`, `03-architecture`, `11-adr` + manifest-derived repo facts (languages,
frameworks from lockfiles/manifests — extracted deterministically by script, not by the model). Output: three
depth sections, each claim wrapped in `<EvidenceLink to="...">`. Gate: every technology token in output must
appear in the deterministic fact list or cited canon — a named-entity check script, not AI judgment.
Prohibited by contract: metrics, user counts, performance numbers, seniority adjectives, any technology not
in evidence. What it demonstrates (competency mapping) must cite the ADR or page evidencing the practice.

## 7. InterviewPrep Component

Schema (`schemas/interview.schema.json`): `elevator_pitch` (30s), `technical_explanation` (2min),
`concepts[]`, `design_decisions[]` (each citing an ADR/page id), `tradeoffs[]`, `likely_questions[]`,
`example_answers[]`, `follow_ups[]`, `evidence_links[]`. Stored as generated JSON; rendered by the
`<InterviewPrep>` React component (collapsible section, provenance banner). Build-time generation chosen
over runtime (AD-11: readers never wait on AI; content is reviewable) and over fully hand-written MDX
(schema keeps sections consistent and machine-checkable). Hybrid rejected: two lifecycles for one feature.

## 8. Special Questions

Represented as structured requests: `{question, requester, audience, privacy_class}` via workflow_dispatch
inputs or an issue form. Classification maps to GenerateQuestionPage (or a more specific contract when the
question matches its scope — e.g. "explain architecture for a recruiter" → GenerateRecruiterPage). Lifecycle
per AD-9/solution §20: preview PR → human approval → versioned page under `generated/questions/`; drafts
expire unmerged. Questions with `privacy_class: private` route to the local provider chain, hard-fail
otherwise.

## 9. Failure Modes & Degradation

Provider down → chain fallback (except privacy-pinned) → job fails visibly, site unaffected. Malformed
output → repair retry → fail with artifacts attached. Contract violation (evidence outside allowlist)
→ assembler refuses before any model call. Key expiry/quota → generation jobs fail, everything else runs.
This section is the operational encoding of mission §9.
