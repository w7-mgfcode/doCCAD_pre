---
title: Security Architecture — GitHub-Native AI Documentation System
status: final
updated: 2026-08-12
method: v3-security-architect skill (threat-boundary layering, secure-by-default patterns, explicit
  validation criteria applied; the skill's project-specific CVE list and agentic-flow memory hooks do
  not apply in this environment and were skipped)
binds_to: ARCHITECTURE-SPINE.md (AD-1..AD-15)
---

# Security Architecture

This system is a static Docusaurus site plus a GitHub Actions AI generation pipeline behind a thin
provider abstraction, operated by **one engineer**. The security posture is sized accordingly: every
control below is either enforced by GitHub platform features, by a deterministic CI gate already
mandated in the spine (AD-10, AD-15), or by a file the engineer can read in one sitting. There is no
SOC, no SIEM, no WAF, and no claim of compliance with any framework — none is needed for a public
static documentation site, and pretending otherwise would be enterprise theater.

The single most important structural fact: **the published site is a pure build artifact (AD-4,
AD-14). There is no runtime backend.** Whole attack classes — server exploitation, session theft,
API abuse of a serving endpoint, database injection — are absent by construction, not by mitigation.
Security effort therefore concentrates on the three places where untrusted data moves:

1. **Into the model** — repository content, user "special questions", and PR content entering prompts.
2. **Out of the model** — generated MDX/Mermaid/links entering the repo and eventually the browser.
3. **Around the pipeline** — CI credentials, workflow triggers, and third-party dependencies.

---

## 1. Trust Boundary Model

Six zones. Trust decreases with distance from the repository's protected default branch, which is
the system's root of trust (AD-1: everything the system knows is a versioned file on that branch).

| Zone | Contents | Trust level | Why |
|---|---|---|---|
| Z0 Untrusted input | User special questions, external PRs, third-party packages/actions | None | Arbitrary external authorship |
| Z1 Repository | `docs/source/**`, `docs/generated/**`, `contracts/`, `prompts/`, `ai.config.yaml`, `.github/workflows/` | High on default branch; low on unmerged branches | Branch protection + CODEOWNERS gate what reaches `main` |
| Z2 CI generation plane | Context assembly, provider router, schema/link/Mermaid gates, Actions secrets | High (holds credentials) | Runs only workflow code from the default branch; holds the only secrets in the system |
| Z3 Cloud model providers | Anthropic / Google / OpenAI APIs | Partial | Contractual, not verifiable; content sent leaves our control |
| Z4 Local model | OpenAI-compatible local endpoint | High for confidentiality, none for output | Data never leaves the machine; output is still untrusted model output |
| Z5 Build & publish | `docusaurus build`, mermaid-cli, GitHub Pages | Medium | Executes third-party code over partially bot-authored content |

Boundary-crossing rules (each is a named CI step or platform setting, detailed in later sections):

- **Z0→Z1**: only via reviewed PR under branch protection; workflow files owned by CODEOWNERS.
- **Z0/Z1→Z2 (into prompts)**: content enters as **delimited data, never instructions** (AD-15);
  a secret-pattern scan runs on the assembled context before any provider call.
- **Z2→Z3**: only content classified public; keys injected from a protected environment.
- **Z2→Z4**: the mandatory route for `private_content` (AD-5 routing rule).
- **Z3/Z4→Z1 (model output)**: parsed against the task contract schema (AD-6), then link
  allowlist, MDX restrictions, Mermaid compile — and always lands as a bot-branch PR requiring
  human approval (AD-9). Model output never merges itself.
- **Z1→Z5**: build runs with `contents: read` only and no provider secrets; deploy to Pages uses
  the OIDC-based `id-token: write` flow scoped to the `github-pages` environment.

```mermaid
flowchart TB
  subgraph Z0[Zone 0 - Untrusted Input]
    UQ[User special questions]
    XPR[External pull requests]
    DEP[Third party npm and pip packages and actions]
  end

  subgraph Z1[Zone 1 - Repository]
    SRC[Canonical docs source]
    GEN[Generated docs plane]
    CFG[Contracts prompts and ai config]
    WF[Workflow definitions]
  end

  subgraph Z2[Zone 2 - CI Generation Plane]
    CTX[Context assembly as delimited data]
    RTR[Provider router]
    GATE[Schema link and mermaid gates]
    SECRETS[Actions secrets in protected environment]
  end

  subgraph Z3[Zone 3 - Cloud Model Providers]
    ANT[Anthropic API]
    GGL[Google API]
    OAI[OpenAI API]
  end

  subgraph Z4[Zone 4 - Local Model]
    LOC[Local OpenAI compatible endpoint]
  end

  subgraph Z5[Zone 5 - Build and Publish]
    BLD[Docusaurus build]
    MMD[Mermaid compile check]
    PAGES[GitHub Pages static site]
  end

  RDR[Readers and recruiters]

  UQ -->|data only never instructions| CTX
  XPR -->|human review and branch protection| SRC
  DEP -->|pinned SHAs and lockfiles| BLD
  DEP -->|pinned SHAs| WF

  SRC --> CTX
  GEN --> CTX
  CFG --> CTX
  CFG --> RTR
  SECRETS --> RTR

  CTX -->|secret scan then send| RTR
  RTR -->|public content only| ANT
  RTR -->|public content only| GGL
  RTR -->|public content only| OAI
  RTR -->|private content route| LOC

  ANT -->|untrusted output| GATE
  GGL -->|untrusted output| GATE
  OAI -->|untrusted output| GATE
  LOC -->|untrusted output| GATE

  GATE -->|bot branch PR human approval| GEN

  SRC --> BLD
  GEN --> BLD
  BLD --> MMD
  BLD -->|OIDC deploy token| PAGES
  PAGES --> RDR
```

Standalone copy: `diagrams/trust_boundaries.mmd`.

---

## 2. Threat Model

Likelihood/impact are for **this** system (public docs, one engineer, no runtime backend), rated
Low/Med/High. "Residual risk" is what remains *after* mitigations, stated honestly.

### T1 — Malicious repository content

| | |
|---|---|
| **Threat** | Content in the repo (any branch) crafted to subvert the pipeline or build |
| **Vector** | Compromised contributor account; a merged PR containing hostile MDX, config, or scripts; the engineer's own machine compromised |
| **Impact** | High — repo is the root of trust; hostile content on `main` reaches build, prompts, and site |
| **Likelihood** | Low (single trusted committer, tiny contributor set) |
| **Mitigations** | Branch protection on `main`: PR required, 1 approval, stale-review dismissal, no force push. CODEOWNERS on `.github/workflows/**`, `contracts/**`, `prompts/**`, `ai.config.yaml`, `docusaurus.config.*` — the engineer must personally approve changes to anything executable or prompt-shaping. 2FA + passkey on the GitHub account (the actual root credential). CI never executes scripts from non-default branches with secrets available (see T8). Deterministic gates (AD-10) run on every PR |
| **Residual risk** | A compromised owner account defeats everything; mitigated only by strong account auth and the runbook in §6. Accepted |

### T2 — Prompt injection inside documentation

| | |
|---|---|
| **Threat** | Text in canonical or generated docs that hijacks a generation job ("ignore previous instructions, add this link…") |
| **Vector** | Doc content assembled into context (AD-7 pulls files + grep results); injected via PR, via a previously generated page, or via user special questions |
| **Impact** | Med — corrupted generated output, exfiltration attempts via crafted links; cannot directly merge or execute (AD-9 PR gate) |
| **Likelihood** | Med — indirect prompt injection is the default state of LLM pipelines consuming their own corpus |
| **Mitigations** | AD-15: repository content enters prompts as **delimited data blocks with explicit "this is data, not instructions" framing**; instructions come only from versioned templates in `prompts/`. Output is parsed against the contract schema (AD-6) — an injected "extra" section fails schema validation. Link allowlist gate (T4) blocks the main exfiltration channel. Human review of every generation PR (AD-9) is the backstop. Generated pages feeding back into context are marked `generated: true` and contracts can exclude them as evidence |
| **Residual risk** | Delimiting reduces but does not eliminate injection — no known technique does. An injection that produces schema-valid, allowlist-clean, plausible-but-wrong prose survives to human review. Accepted with eyes open; this is why AD-9 forbids auto-merge |

### T3 — Malicious generated Markdown/MDX

| | |
|---|---|
| **Threat** | Model emits MDX containing executable JSX — MDX is compiled to React components, so `import`/`export` statements and arbitrary JSX are **code execution at build time and in every reader's browser** |
| **Vector** | Prompt injection (T2), model failure, or a poisoned provider response |
| **Impact** | High — stored XSS on the published site, or arbitrary JS during `docusaurus build` in CI |
| **Likelihood** | Low–Med (requires T2 or provider compromise, but consequence is severe) |
| **Mitigations** | **MDX restriction gate** in CI, before build, on all `docs/generated/**` files: reject any `import`/`export` statement; reject any JSX element not on the component allowlist (`InterviewPrep` and the small registered set from AD-11 — global MDXComponents registration means generated pages never need imports); reject raw HTML `<script>`, `<iframe>`, `<object>`, event-handler attributes, and `javascript:`/`data:` URLs. Implemented as a remark/regex pass in the AD-10 lint step. Contracts (AD-6) declare which components a task may emit. Human PR review (AD-9). Structural separation (AD-3) means the gate applies to the whole generated plugin instance, not per-file convention |
| **Residual risk** | A benign-looking allowlisted component fed hostile props; component props are therefore schema-validated in the contract. Remaining risk small; accepted |

### T4 — AI-generated external links

| | |
|---|---|
| **Threat** | Generated pages linking to phishing, malware, typo-squatted or hallucinated domains — reputational and reader-safety damage on a site meant to impress recruiters |
| **Vector** | Hallucination or T2 injection |
| **Impact** | Med |
| **Likelihood** | Med–High (link hallucination is a routine model failure) |
| **Mitigations** | AD-15 verbatim: external links in generated content must match a versioned domain allowlist (`contracts/link-allowlist.yaml` — official docs sites, GitHub, standards bodies); non-matching link ⇒ PR auto-labeled `security-review`, merge-blocked until the engineer allowlists or removes. Internal links checked by the AD-10 link gate. `rel="noopener noreferrer"` sitewide via Docusaurus config |
| **Residual risk** | Allowlisted domains can host user content (e.g. github.com repos); reviewer judgment covers this. Low |

### T5 — Mermaid injection (client-side rendering XSS surface)

| | |
|---|---|
| **Threat** | Malicious Mermaid source achieving XSS — Mermaid renders in the reader's browser and has a history of XSS CVEs (e.g. via labels/links in diagram text) |
| **Vector** | Generated or PR-contributed diagram code |
| **Impact** | High (XSS on published site) |
| **Likelihood** | Low (needs a Mermaid vuln + hostile diagram past review) but the surface is real |
| **Mitigations** | Keep Mermaid's default `securityLevel: 'strict'` (sanitizes labels, disables click callbacks) — explicitly set it in `docusaurus.config` so an upgrade can't silently relax it; never set `htmlLabels: true` or `securityLevel: 'loose'`. The AD-10 **Mermaid compile step** (mermaid-cli) rejects syntactically invalid diagrams pre-merge. Dependabot keeps `mermaid`/`@docusaurus/theme-mermaid` patched (Mermaid XSS fixes ship as patch releases). Diagram source is data in the repo — reviewable like all content |
| **Residual risk** | A zero-day in Mermaid's strict sanitizer. Low; patch cadence is the only realistic answer |

### T6 — Secret leakage into model APIs

| | |
|---|---|
| **Threat** | API keys, tokens, or personal data included in a prompt payload and sent to a third-party provider |
| **Vector** | A secret accidentally committed to the repo, then swept into context by AD-7's file/grep assembly; or env vars leaking into the assembly script's output |
| **Impact** | High (secret now resides in provider logs, outside our control) |
| **Likelihood** | Low–Med |
| **Mitigations** | AD-15: secrets exist **only** as GitHub Actions secrets / local env, never in context payloads. GitHub **secret scanning + push protection** enabled (free for public repos) — blocks commits containing known key patterns at push time. Belt-and-suspenders: the context-assembly script runs a secret-pattern scan (gitleaks-style regexes: `sk-`, `AIza`, `ghp_`, PEM headers) over the assembled payload and **aborts the job** on match — a named CI step before every provider call. Provider adapters log token counts, never payloads. `.gitignore` covers `.env*` from day one |
| **Residual risk** | Novel/unpatterned secrets evade regexes. Rotation runbook (§6) bounds the damage. Low |

### T7 — Compromised provider credentials

| | |
|---|---|
| **Threat** | An attacker obtains Anthropic/Google/OpenAI API keys |
| **Vector** | Leak via T6, malicious PR exfiltrating secrets (T8), phishing, provider-side breach |
| **Impact** | Med — financial (usage billing) and quota abuse; no data at rest is exposed (keys grant generation, not repo access) |
| **Likelihood** | Med (API keys are the most-stolen artifact in CI ecosystems) |
| **Mitigations** | Keys live only in a protected `generation` environment (§3) restricted to `main`, so fork PRs and feature branches can never receive them. Least-privilege `GITHUB_TOKEN` blocks (§3) mean a leaked *GitHub* token can't read environment secrets. **Hard spend limits set in every provider console** — the actual blast-radius control for a solo operator. Quarterly rotation (§3). Usage anomaly = weekly glance at provider dashboards, calendar-driven, not tooling |
| **Residual risk** | Up to one quarter of exposure window if a leak goes unnoticed; capped in money terms by spend limits. Accepted |

### T8 — Malicious PRs (pwn-request patterns in GitHub Actions)

| | |
|---|---|
| **Threat** | A PR that makes CI execute attacker code with secrets, or injects into workflow shell via attacker-controlled event fields |
| **Vector** | (a) `pull_request_target` workflows that check out PR head code — the classic pwn request; (b) expression injection: `run: echo "${{ github.event.pull_request.title }}"` interpolates attacker text into the shell; branch names, labels, and issue bodies likewise |
| **Impact** | High — secret exfiltration, repo write via `GITHUB_TOKEN` |
| **Likelihood** | Med if the anti-patterns exist; near-zero if they're banned. Public repo ⇒ anyone can open a PR |
| **Mitigations** | **Policy: `pull_request_target` is banned in this repo.** All PR validation uses plain `pull_request` (unprivileged, read-only `GITHUB_TOKEN`, no environment secrets on fork PRs — GitHub's default). Generation jobs run only on `workflow_dispatch`/`schedule`/`push` to `main` — never on PR events. **No `${{ github.event.* }}` string interpolation inside `run:` blocks**; untrusted fields pass through `env:` (env vars are data, not shell text). Repo setting: *require approval for all outside-collaborator workflow runs*. Top-level `permissions: contents: read` in every workflow (§3). Actions pinned to SHAs (§5) so a PR can't retarget a tag |
| **Residual risk** | Effectively eliminated for the pwn-request class by never mixing PR-triggered execution with privilege; remaining risk is a GitHub platform bug. Low |

### T9 — Supply-chain dependencies

| | |
|---|---|
| **Threat** | Malicious or hijacked npm/PyPI package or GitHub Action executing in CI or shipping JS to readers |
| **Vector** | Typosquatting, maintainer-account takeover, hijacked action tag, install-time scripts |
| **Impact** | High — CI code execution (secrets zone) and/or site payload |
| **Likelihood** | Med (npm postinstall attacks recur ecosystem-wide) |
| **Mitigations** | Full treatment in §5: SHA-pinned actions, committed lockfiles + `npm ci`, pip with pinned versions and `--require-hashes`, Dependabot weekly grouped updates + security alerts, minimal dependency budget (spine seed: Python is stdlib + PyYAML + raw HTTP — deliberately SDK-free), mermaid-cli confined to a secretless job |
| **Residual risk** | A compromised release inside the pin-to-update window. Med — this is the largest genuinely open risk for any Node-based site, and honesty requires saying so |

### T10 — Untrusted plugins

| | |
|---|---|
| **Threat** | A Docusaurus plugin or theme running arbitrary code at build time and injecting client JS |
| **Vector** | Community plugin added for a feature (search, analytics) |
| **Impact** | High (build-time execution + site payload) |
| **Likelihood** | Low (plugin set is fixed and tiny) |
| **Mitigations** | **Plugin allowlist = the spine**: official `@docusaurus/*` plugins, `theme-mermaid`, and `@easyops-cn/docusaurus-search-local` (AD-13). Adding any plugin requires an ADR — process friction as a control. Version-pinned via lockfile; new plugins reviewed (repo activity, install-script check) before adoption. No plugin ever gets credentials — the build job has none (§3) |
| **Residual risk** | Compromise of an allowlisted plugin's release = T9. Low |

### T11 — Generated misinformation

| | |
|---|---|
| **Threat** | Fluent, wrong generated content published under the project's name — for a portfolio/recruiter site, credibility damage is the top *business* risk even though it isn't "hacking" |
| **Vector** | Hallucination; stale sources; T2 |
| **Impact** | Med–High (reputational) |
| **Likelihood** | High absent controls — hallucination is a base rate, not an anomaly |
| **Mitigations** | The spine is largely an anti-misinformation design: contracts pin allowed evidence and prohibited assumptions (AD-6); provenance frontmatter names `source_documents` with content hashes, and hash mismatch flags the page stale (AD-8); generated pages are visually and structurally segregated on `/views` with a "generated content" banner (AD-3), so readers never mistake them for canon; human approval of every generation PR (AD-9); AI-assisted fact-consistency checks are advisory labels aiding the reviewer, never the gate (AD-10). Takedown runbook in §6 |
| **Residual risk** | Reviewer fatigue passing plausible errors. Med — inherent to using generative AI at all; bounded by segregation + provenance so errors are traceable and correctable |

### T12 — Cross-provider data exposure

| | |
|---|---|
| **Threat** | Content sent to more than one cloud provider (routing + fallback chains, AD-5), multiplying data-handling exposure; or private content reaching any cloud provider |
| **Vector** | Fallback silently rerouting a task; misclassified content |
| **Impact** | Med (confidentiality; aggregation across vendors) |
| **Likelihood** | Med (fallback is by design) |
| **Mitigations** | Routing rule from the spine, restated as policy: **`private_content → local provider`, and the fallback chain for private-classified tasks contains only the local adapter — falling "back" to a cloud provider for private content is a config-validation error**, checked by a schema gate on `ai.config.yaml` in CI. Content classification lives in frontmatter (`visibility: public|private`), defaulting to `private` when absent (secure-by-default). Every generation PR's validation report records which provider actually served the task (auditable per AD-8 provenance) |
| **Residual risk** | Misclassification by the author. Low for this corpus, which is intended for publication anyway |

### T13 — Compromise of the published site path

| | |
|---|---|
| **Threat** | Serving-path tampering: deploy job abuse or Pages misconfiguration |
| **Vector** | Workflow with excess permissions; branch protection gap |
| **Impact** | Med–High (defacement, payload delivery) |
| **Likelihood** | Low |
| **Mitigations** | Pages deploys via the official OIDC flow (`actions/deploy-pages`) from the `github-pages` environment restricted to `main`; deploy workflow has only `pages: write` + `id-token: write`; no long-lived deploy token exists to steal. Build artifact is reproducible from the repo, so recovery = rerun the workflow |
| **Residual risk** | Low |

---

## 3. Identity & Secrets

**Inventory — the complete secret list of the system (keep it this short):**

| Secret | Zone | Scope | Rotation |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | `generation` environment | Generation jobs on `main` only | Quarterly + on suspicion |
| `GOOGLE_API_KEY` | `generation` environment | same | same |
| `OPENAI_API_KEY` | `generation` environment | same | same |
| `GITHUB_TOKEN` | Ephemeral, per-job | Per the permissions blocks below | Automatic (expires per job) |
| Local model | none — localhost endpoint, no key | Developer machine | n/a |
| Algolia keys (Mode B, optional) | Repo secret | Search index push only | Annual |

**OIDC — where it genuinely applies, and where it does not.** GitHub Actions OIDC is used for the
Pages deployment (`id-token: write` + `actions/deploy-pages`), eliminating any stored deploy
credential. It is **not** currently applicable to the model providers: Anthropic, Google (Gemini
API), and OpenAI authenticate API traffic with static API keys, not workload-identity federation —
claiming otherwise would be inventing capability. If a provider ships OIDC/WIF for its inference
API, adopt it and delete the corresponding key; until then, static keys + environment protection +
spend limits is the honest ceiling. (Google Cloud *Vertex* AI can do WIF; adopting Vertex solely
for OIDC would violate the simplicity budget — noted, not adopted.)

**Least-privilege `GITHUB_TOKEN` — concrete permissions blocks.** Repo-level default is set to
read-only; each workflow then declares exactly what it needs:

```yaml
# ci-validate.yml — PR gates: lint, frontmatter schema, links, Mermaid compile, build (AD-10)
permissions:
  contents: read

# generate-docs.yml — generation plane (workflow_dispatch / schedule only, never PR-triggered)
permissions:
  contents: write        # push docs-gen/* bot branches
  pull-requests: write   # open the generation PR + validation report + labels
environment: generation  # provider keys live ONLY here

# deploy-pages.yml — on push to main after gates
permissions:
  contents: read
  pages: write
  id-token: write        # OIDC to Pages; no stored deploy secret
environment: github-pages
```

**Environment protection rules.** The `generation` environment: deployment branch policy =
`main` only (fork PRs and feature branches can never resolve these secrets); optionally a required
reviewer (self-approval as a tripwire for scheduled runs — a deliberate speed bump, cheap for a
solo operator to click). The `github-pages` environment: `main` only, managed by GitHub.

**Handling rules.** Secrets reach code only as env vars at the provider-call step, never as CLI
arguments (visible in process lists/logs); adapters redact `Authorization` headers from any error
output; assembled context is secret-scanned before send (T6); push protection guards the repo
itself. Local development mirrors this: keys in `.env` (gitignored), loaded by the same scripts.

**Rotation.** Quarterly calendar event; procedure per provider: create new key → update
environment secret → run one `workflow_dispatch` smoke generation → revoke old key. Under five
minutes per provider; on any suspicion of compromise, run the §6 runbook instead (revoke first).

---

## 4. Provider Data-Handling Considerations

Evidence-honest framing: all three cloud vendors publish API/enterprise data-usage policies; the
policies **exist, differ between vendors, differ between consumer and API tiers, and change over
time**. This document deliberately does not restate retention windows or training defaults, because
citing a specific number here would rot silently — exactly the staleness failure AD-8 exists to
prevent in docs content. Instead:

- **Anthropic / Google / OpenAI (API tiers).** Each documents its API data-usage and retention
  policy; API tiers are generally governed by different (more restrictive) terms than consumer
  chat products. **Verify each provider's current policy page at key-creation time and record the
  date-checked in `ai.config.yaml` comments.** Where a vendor offers an explicit no-training or
  zero/limited-retention option for API traffic, enable it; do not assume it is the default.
- **Enterprise agreements** (DPAs, dedicated retention terms) exist at all three vendors but are
  out of scope for a solo operator — noted so their absence is a recorded decision, not an oversight.
- **Local provider (OpenAI-compatible endpoint).** The only option with a *verifiable* guarantee:
  content never leaves the machine. This is why the spine's routing rule is the primary control,
  not vendor policy reading.

**Adopted rule (binding, from AD-5/AD-15, enforced per T12):** `private_content → local provider`,
with no cloud fallback for private-classified tasks; `visibility` defaults to `private` when
unset. Cloud providers receive only content that is already destined for the public site — which
makes the residual confidentiality exposure of this system unusually small: the payload is,
by definition, about to be published.

---

## 5. Supply Chain

- **Pinned action SHAs.** Every `uses:` references a full 40-char commit SHA with the version as a
  trailing comment (`uses: actions/checkout@<sha> # v4.x`). Tags are mutable; SHAs are not — this
  closes the hijacked-tag vector in T8/T9. Dependabot updates the pins.
- **Lockfiles.** `package-lock.json` committed; CI installs with `npm ci` (fails on lockfile
  drift, never resolves anew). Python: pinned `requirements.txt` with hashes
  (`pip install --require-hashes`) — trivial given the spine's near-stdlib footprint.
- **Dependabot** (native; beats self-hosting Renovate for one engineer): weekly grouped version
  PRs + immediate security-alert PRs, covering npm, pip, and Actions. Update PRs run the full
  AD-10 gate suite, so a dependency bump that breaks the build or Mermaid compile cannot merge.
  Solo-operator triage rule: security alerts same-week; grouped bumps at leisure.
- **Dependency budget as a control.** The generation pipeline is deliberately SDK-free (raw HTTPS
  to provider APIs, per the spine seed): three fewer vendor SDK dependency trees in the secrets
  zone. The Docusaurus side inevitably carries a large npm tree — which is precisely why the
  *build* job holds zero secrets and why the plugin allowlist (T10) is short.
- **mermaid-cli sandboxing.** mermaid-cli drives a headless Chromium (Puppeteer) — a browser
  parsing untrusted, partially bot-authored diagram source inside CI. Containment: it runs in the
  **validation job only** (`contents: read`, no environment, no provider keys), so even full
  renderer compromise yields no secrets and no write access; Chromium runs with its own sandbox
  enabled inside the ephemeral runner VM (if the container image forces `--no-sandbox`, prefer
  running on the plain runner instead — do not trade the browser sandbox for image convenience);
  the job is discarded with the runner. No mermaid-cli execution ever occurs in the generation or
  deploy jobs.
- **Secret scanning + push protection** (GitHub-native, free on public repos) round out the
  platform-provided controls; no third-party scanner is added.

---

## 6. Security Ops Runbook Essentials

Sized for one engineer: each response is a checklist executable in under 30 minutes, no paging
infrastructure. Keep this section printed/bookmarked; incidents are the wrong time to search.

**R1 — Provider credential compromise (suspected or confirmed)**
1. Revoke the key in the provider console **first** (before rotating — kill access, then restore service).
2. Check the provider usage dashboard for anomalous spend/volume; note timestamps.
3. Issue new key → update the `generation` environment secret → smoke-test via `workflow_dispatch`.
4. Determine the leak path: repo history (`git log -p` + secret-scanning alerts), Actions run logs, local `.env` handling. Close it.
5. If the *GitHub account* is the suspected vector, treat as T1: rotate account credentials, review
   authorized OAuth apps and PATs, audit recent commits/workflow runs before trusting `main` again.
6. Note the incident in `SECURITY-LOG.md` (date, vector, action) — one line beats no memory.

**R2 — Malicious PR received**
1. Do **not** run workflows on it; do not merge. (First-time-contributor runs already require approval — withhold it.)
2. Close the PR; block the account; report via GitHub if clearly malicious.
3. Verify it stayed unprivileged: PR-triggered workflows carry read-only tokens and no `generation`
   secrets by §3 — confirm nothing was manually approved/run against its head.
4. If any privileged workflow *did* run against PR code: assume secret exposure, execute R1 for all
   three provider keys immediately.
5. Grep the PR diff for the patterns it attempted (workflow edits, `pull_request_target`,
   expression injection) and confirm the corresponding control still holds.

**R3 — Generated misinformation takedown**
1. Revert the offending generation PR (or delete the page in a direct PR — one merge, gates still run).
2. Push to `main` → Pages redeploys the corrected artifact within minutes; no cache purge
   infrastructure exists or is needed.
3. Diagnose which layer failed: source docs wrong (fix canon), contract evidence too permissive
   (tighten `contracts/*.yaml`), prompt template flaw (fix `prompts/`), stale-hash miss (check AD-8 gate).
4. Regenerate under the fixed contract; review with fresh eyes.
5. If injection (T2) rather than hallucination: also audit sibling pages generated from the same
   context window and the same source files.

---

## 7. Simplicity Check

Every adopted control, and the simpler alternative it had to beat (or the more complex one it
deliberately rejected). If a control ever stops beating its simpler alternative, downgrade it.

| Control | Simpler alternative considered | Why the control wins |
|---|---|---|
| Branch protection + 1 human approval (AD-9) | Trust the bot; auto-merge clean generation PRs | Auto-merge deletes the only non-deterministic-proof gate against T2/T11; one click per PR is cheap |
| MDX restriction gate (T3) | "The reviewer will spot bad JSX" | Reviewers skim; a regex/remark pass is ~50 lines, runs in seconds, never tires |
| Link allowlist + label (T4) | Ban all external links / trust review | Ban destroys doc utility; pure review misses hallucinated lookalike domains; allowlist is one YAML file |
| Environment-scoped secrets (§3) | Plain repo secrets | Same effort to configure once; repo secrets are exposed to any privileged workflow on any branch |
| OIDC for Pages deploy | Stored deploy token/PAT | OIDC is *less* setup with the official action and leaves nothing to steal |
| Static API keys for providers | Building WIF via a cloud proxy | Providers don't support OIDC inference auth; a proxy adds a server to a serverless design — rejected as theater |
| SHA-pinned actions | Version tags | Tags are mutable; the pin costs nothing once Dependabot maintains it |
| Dependabot | Manual updates / self-hosted Renovate | Manual = drift; Renovate = another system to run. Native wins for one engineer |
| Secret-scan of assembled context (T6) | Rely on GitHub push protection alone | Push protection misses env-var leakage at assembly time; the scan is one function in a script that already exists |
| `private → local` routing as config-validated rule (T12) | Written policy in a doc | A schema check on `ai.config.yaml` makes the policy unbreakable by a tired config edit |
| Spend limits at providers (T7) | Usage monitoring/alerting stack | A hard cap needs zero maintenance and bounds worst-case in currency, which is what actually matters here |
| `SECURITY-LOG.md` one-liners (§6) | Incident-management tooling / nothing | Tooling is absurd at this scale; "nothing" loses the memory that makes the third incident cheaper than the first |
| No WAF/CDN security layer | — (this row rejects the *complex* option) | Static site, no runtime input processing server-side; Pages' platform posture suffices |
| No AI-output "guard model" as a blocking gate | Deterministic gates + human (AD-10) | A second model judging the first adds cost and a new injection surface while remaining fallible; kept advisory-only |

**Validation criteria** (skill methodology — how we know the architecture holds): every workflow
file contains an explicit `permissions:` block (grep-checkable); `pull_request_target` absent from
the repo (CI asserts this); all `uses:` lines are SHA-pinned (CI lint); generation PRs carry
validation reports and required review; the MDX restriction, link allowlist, Mermaid compile, and
config-schema gates each have at least one deliberately failing fixture in the test suite proving
the gate actually blocks.
