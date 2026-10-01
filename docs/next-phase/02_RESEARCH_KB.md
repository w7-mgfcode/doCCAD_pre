# 02 — Research Knowledge Base

Web research for the next DOCCAD phase, carried out 2026-10-01 by three parallel research agents
(A: Antigravity 2.0 + Gemini 3.8 Flash long runs; B: docs-as-code delivery stack; C: governed live AI
generation). All sources were **accessed 2026-10-01** unless another date is given.

Status labels: **VERIFIED** = the agent read the claim in the cited page on the access date (pages were
fetched through a summarizing tool, so wording can be lossy — re-read the source before relying on an
exact value); **UNVERIFIED** = inferred, secondhand, snippet-only, or the page could not be loaded.
Model names that appear in provider documentation are recorded as *documentation content only*; DOCCAD
never hard-codes a model ID (AD-5, `docs/primary-inputs/04_ARCHITECTURE/SAD/ARCHITECTURE-SPINE.md:44-48`).

Each finding ends with **→ DOCCAD:** its consequence. Sections: A, B, C, then D (conflicts with the
archive and prototype, with proposed resolutions) and E (open questions).

---

## A. Antigravity 2.0 + Gemini 3.8 Flash for long autonomous runs (Agent A)

Official Antigravity documentation pages carry no publication dates. "3P" marks third-party sources, all
UNVERIFIED against official docs. Several official URLs returned 404 on the access date and their features
are therefore unconfirmed for 2.0: `/docs/knowledge`, `/docs/terminal-sandbox`, `/docs/goal`,
`/docs/ide/artifacts`, `/docs/ide/permissions`, `/docs/ide/source-control`.

### A1. Re-check of the sources cited by the first run (`docs/prototype-planning/ANALYSIS.md:63-65`)

| Source | Finding | Status |
|---|---|---|
| https://www.antigravity.google/docs/overview | Loads; lists Artifacts, Implementation Plans, Walkthroughs, Skills, Rules, AGENTS.md, Workflows, review policies, terminal auto-execution, subagents, MCP | VERIFIED |
| https://antigravity.google/docs/models | Loads; Gemini 3.8 Flash is the latest model, on all plans; also lists 3.7 Flash, 3.6 Flash, 3.1 Pro, Claude Sonnet/Opus 4.6 (not Enterprise), GPT-OSS-120b; no context sizes or quotas | VERIFIED |
| https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash | Loads; model page for Gemini 3.8 Flash | VERIFIED |
| https://www.antigravity.google/blog/introducing-google-antigravity-2 | Loads; launch 2026-05-19; documents `/browser`, `/goal`, `/grill-me`, `/schedule`, dynamic subagents, Agent Manager, artifacts, CLI and SDK | VERIFIED |

### A2. Planning, tracking, review, autonomy

| # | Claim | Source | Status | → DOCCAD |
|---|---|---|---|---|
| A2.1 | Artifacts (task lists, implementation plans, walkthroughs, diffs, screenshots, browser recordings) communicate progress; plan approval follows the artifact review policy; artifacts live in Antigravity's own store, not the repo | https://www.antigravity.google/docs/artifacts ; https://www.antigravity.google/docs/implementation-plan | VERIFIED (storage location from agent reading) | **Mirror the task list and evidence into repo files** — `PROGRESS.md` is the only record a reviewer or resumed run can trust |
| A2.2 | Artifact review policy: `asks-for-review` (default), `agent-decides`, `always-proceed`; terminal policy Request Review or Always Proceed | https://www.antigravity.google/docs/settings (CLI-flavoured page) | VERIFIED for CLI; 2.0 app labels UNVERIFIED | Choose deliberately; ask for review of the plan only |
| A2.3 | `/plan` = analysis → clarification → plan → user review before code; `/goal` works "continuously until the objective is fully achieved"; also `/grill-me`, `/schedule`, `/btw` | https://www.antigravity.google/docs/slash-commands ; launch blog | VERIFIED | `/goal` stops when the agent judges the objective met → the objective must be command-checkable |
| A2.4 | Permissions: Deny > Ask > Allow; rules `command(prefix)` or `regex:`; workspace files auto-allowed; web browsing defaults to Ask. **Default preset runs terminal commands in a sandbox with no network**, restricted to workspace + temp; `npm install`, `git push` etc. must run outside the sandbox and prompt unless allow-listed; Turbo = no sandbox; settings in the 2.0 app under Settings → General → Permission Settings or per project; CLI uses `~/.gemini/antigravity-cli/settings.json` | https://www.antigravity.google/docs/permissions | VERIFIED | **An unattended run stalls on its first `npm ci` unless the owner pre-sets allow rules** (human action) |
| A2.5 | CLI best-practice page names permission levels `proceed-in-sandbox`, `strict`, `request-review` — inconsistent with the settings page's preset names | https://www.antigravity.google/docs/cli/best-practices | VERIFIED; names unreconciled | Describe intent, not label names, in the setup checklist |
| A2.6 | 3P: `/goal` auto-approves its plan into the `.gemini` scratch directory, asks once per tool class per session even under always-proceed, and can leave a half-applied state; recommends a branch and `/rewind` | https://neurals.ca/tech/gemini/antigravity/goal-mode/ ; …/permission-modes/ | UNVERIFIED (3P) | Run on a dedicated branch |
| A2.7 | Subagents: `.agents/agents/<name>.md` with `name`, `description`, `tools`, `model` (inherit/flash/pro), `commandExecutionPolicy`; run concurrently with **no parent context**; nesting ≤10; misspelled tool names may hang the subagent | https://www.antigravity.google/docs/subagents | VERIFIED | Subagent briefs must be self-contained |
| A2.8 | Projects: git worktrees (local or new-worktree mode), per-project settings, parallel agents on one folder in local mode, `/resume`, `/fork`; launch `agy`, `--project=<id>`, `--new-project` | https://www.antigravity.google/docs/projects | VERIFIED | **No parallel agents on one tree**: `detect`, tests and `build:production` rewrite shared state |
| A2.9 | Workflows are deprecated in favour of skills by **2026-11-01**; workflow files ≤12,000 chars | https://www.antigravity.google/docs/ide/workflows | VERIFIED | Do not build the run on Antigravity workflows |

### A3. Instruction and rules files

| # | Claim | Source | Status | → DOCCAD |
|---|---|---|---|---|
| A3.1 | Antigravity reads **`AGENTS.md`, `GEMINI.md` and `.agents/rules/*.md`** at any directory level, walking up from the touched file to the workspace root; rules are cumulative, the more specific directory wins; global: `~/.gemini/AGENTS.md`, `~/.gemini/GEMINI.md`, `~/.gemini/config/rules/*.md` | https://www.antigravity.google/docs/rules | VERIFIED | The canonical `AGENTS.md` is read; **no `GEMINI.md` is needed** — do not create a conflicting one. 3P claim that GEMINI.md always outranks AGENTS.md (agentpedia.codes) contradicts the official wording — UNVERIFIED |
| A3.2 | Rule activation modes `always_on`, `model_decision`, `glob`, `manual`; **24 KB per file, 20,000-token aggregate for global + always-on rules**; oversized rules demoted to pointers; only immediate `.md` children of `.agents/rules/` are scanned (subfolders need `.agents/rules.json`) | same | VERIFIED (glob-mode frontmatter syntax UNVERIFIED) | **`.claude/rules/*.md` are not read by Antigravity.** Binding rules must be in `AGENTS.md` or flat `.agents/rules/*.md` |
| A3.3 | Workspace skills: `<workspace>/.agents/skills/<name>/SKILL.md` (`description` required); global `~/.gemini/config/skills/` | https://www.antigravity.google/docs/skills | VERIFIED | The repo's `.agents/skills` symlink matches; **whether git-ignored `.agents/` is loaded is undocumented** — UNVERIFIED → canary test |
| A3.4 | `.agents/` also holds `hooks.json`, `mcp_config.json`, `agents/`; hooks PreToolUse, PostToolUse, PreInvocation, PostInvocation, Stop; **only PreToolUse can block** (allow/deny/ask/force_ask/deny_unless_prior_grant); default timeout 30 s; exit-code semantics undocumented | https://www.antigravity.google/docs/hooks | VERIFIED | A PreToolUse hook can deny writes to `11_RAW_ARCHIVE/`, `03_PROMPTS/` and `.env` — the Antigravity equivalent of `.claude/settings.json`. 3P claim "Antigravity has no hooks" (neurals.ca) is stale |
| A3.5 | Knowledge items: `/docs/knowledge` returned 404; `/learn` distills feedback into project rules | https://www.antigravity.google/docs/slash-commands | Knowledge items UNVERIFIED for 2.0 | Use repo files for continuity |

### A4. Browser verification

| # | Claim | Source | Status | → DOCCAD |
|---|---|---|---|---|
| A4.1 | `/browser` spawns a sandboxed Chrome subagent: navigate, inspect DOM, screenshots, WebM recordings saved as artifacts; DevTools integration; separate Chrome profile; **on demand only** | https://www.antigravity.google/docs/ide/browser ; https://www.antigravity.google/docs/ide/browser-recordings ; slash-commands page | VERIFIED | The prompt must say exactly when to call `/browser` |
| A4.2 | Browser allowlist is a local file starting with only `localhost`; other URLs prompt "Always allow"; denylist always wins | https://www.antigravity.google/docs/ide/allowlist-denylist | VERIFIED | `npm run serve` on localhost works; checking the live Pages URL needs a pre-allowlisted URL or a human |
| A4.3 | `/browser` is not available in the Antigravity CLI (IDE and 2.0 app only); works over CDP with Chrome/Chromium — the codelab says no extension, the official browser page mentions "Chrome extension setup" | https://codelabs.developers.google.com/agentic-ui-automation-with-antigravity ; browser page | VERIFIED (conflict on extension unresolved) | Run the browser step in the 2.0 app; write evidence (screenshot paths, console errors) to a repo file |
| A4.4 | Recording limits and storage are undocumented | browser-recordings page | VERIFIED (absence) | Keep evidence small: screenshots + a text log |

### A5. Gemini 3.8 Flash

| # | Claim | Source | Status | → DOCCAD |
|---|---|---|---|---|
| A5.1 | Model ID `gemini-3.8-flash`; input 1,048,576 tokens, output 65,536; thinking levels low/medium (default)/high, no `minimal`; `max_output_tokens` caps thinking + output | https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash ; https://ai.google.dev/gemini-api/docs/thinking | VERIFIED | Context size is not the bottleneck; tool reliability is |
| A5.2 | Model card: release 2026-09-02; knowledge cutoff March 2026 for some domains, January 2025 for others; limitations: hallucination, occasional slowness/timeouts, extra tokens at higher effort, jailbreak resistance still improving | https://deepmind.google/models/model-cards/gemini-3-8-flash/ | VERIFIED | **Pin versions in the prompt and require reading installed `node_modules` docs/types instead of memory** |
| A5.3 | Which thinking level Antigravity uses; any UI setting for it | — | UNVERIFIED | — |
| A5.4 | Gemini API price $0.75 / $3.75 per M tokens (input/output) through 2026-12-31, then $1.50 / $7.50; Antigravity quota is separate: Ultra refreshed every 5 h, Pro every 5 h until a weekly cap, standard plans weekly; complexity-based, no published numbers, no bring-your-own-key | https://ai.google.dev/gemini-api/docs/pricing ; https://www.antigravity.google/docs/plans | VERIFIED | A multi-hour run can exhaust a weekly quota → phase the work and stop cleanly |
| A5.5 | Official forum: endless tool-use loops on 3.8 Flash resend the whole history and burn quota (~10% of weekly quota per incident in one report); staff recommend starting fresh rather than steering a stuck thread and bounding prompts ("inspect X once; if you cannot identify the issue, stop and ask") | https://discuss.ai.google.dev/t/antigravity-and-gemini-3-8-flash/180588 (2026-09-02…04) | VERIFIED (thread content) | Stop-and-record bounds in the prompt; fresh conversation per phase |
| A5.6 | Bug report: the model emits raw `:call:default_api:replace_file_content` text instead of executing the tool call — **no file changes while the agent may believe it acted**; Google asked for repro 2026-09-30, no fix | https://discuss.ai.google.dev/t/antigravity-gemini-3-8-flash-outputs-raw-string-calls-default-api-instead-of-executing-tool-calls/186134 | VERIFIED (thread content; Windows report, Linux applicability unknown) | **Require `git diff --stat` / re-read after every edit; verify by command output, never by narration.** Likely contributor to the first run's "documented but not implemented" checks |
| A5.7 | 3P: intermittent HTTP 400 "function call turn comes immediately after a user turn" at ~440 messages in a third-party proxy | https://github.com/lidge-jun/opencodex/issues/5008 | UNVERIFIED (3P) | Another reason to restart per phase |

### A6. Session limits, context, resume

| # | Claim | Source | Status | → DOCCAD |
|---|---|---|---|---|
| A6.1 | No documented context-window size or auto-compaction behaviour for the Antigravity session; CLI has no `/compact` (open feature request) | https://github.com/google-antigravity/antigravity-cli/issues/999 ; 3P changelog https://www.gradually.ai/en/changelogs/antigravity/ | VERIFIED (issue); compaction details UNVERIFIED | Do not rely on the initial prompt surviving a long session |
| A6.2 | 3P research: compaction drops side constraints, including verification steps | https://arxiv.org/pdf/2608.11242 ; https://tianpan.co/blog/2026/04/19/compaction-traps-long-running-agents | UNVERIFIED (3P) | **Binding rules go in `AGENTS.md` (re-read), not only in the prompt**; keep a "tried and failed" log in `PROGRESS.md` |
| A6.3 | `/resume` (alias `/switch`), `/rewind` (alias `/undo`), `/fork`, `/rename`; IDE side panel shows task list, context usage, checkpoints | https://www.antigravity.google/docs/cli/features ; projects page ; https://www.antigravity.google/docs/ide/agent-side-panel | VERIFIED (CLI; IDE names only) | Resume from files: first step on resume = `git status`, `npm run validate`, `npm run test` |
| A6.4 | Antigravity prevents sleep during active agent operation; remote monitoring from a phone exists | https://www.antigravity.google/docs/faq | VERIFIED | — |

### A7. MCP, git, human-only actions

| # | Claim | Source | Status | → DOCCAD |
|---|---|---|---|---|
| A7.1 | MCP config `~/.gemini/config/mcp_config.json` and `.agents/mcp_config.json`; stdio, Streamable HTTP/SSE, WebSocket; MCP Store (76+ servers) includes GitHub; unconfigured MCP tools run in Ask mode | https://www.antigravity.google/docs/mcp | VERIFIED | A GitHub MCP needs a human-provided token, never written to the repo; required scope UNVERIFIED |
| A7.2 | 2.0 app has a git review panel (diffs, staging, commits) and worktrees; PR creation from Antigravity undocumented | features page | VERIFIED (summary) / UNVERIFIED (PRs) | Keep pushes and PR creation out of the autonomous run |
| A7.3 | Human-only: Google sign-in and plan, network-command approvals unless allow-listed, non-workspace file access, browser allowlist additions, MCP approvals, GitHub auth, repo secrets, Pages settings | synthesis of A2.4, A4.2, A7.1 | INFERRED | Pre-run checklist in `03_NEXT_VERSION_PLAN.md` |

### A8. Long-run guidance

| # | Claim | Source | Status | → DOCCAD |
|---|---|---|---|---|
| A8.1 | "The single most effective way to ensure reliable, correct modifications from an autonomous agent is to provide … a local verification mechanism"; Explore → Plan → Execute with an approved plan; `Esc`, `/rewind`, `/fork` | https://www.antigravity.google/docs/cli/best-practices | VERIFIED | Tests before implementation; a hard green gate per phase |
| A8.2 | No official guidance specific to "claimed but unexecuted" checks | — | UNVERIFIED (absence) | Mitigation is DOCCAD's own: evidence log with command, exit code and date per ticked item |

### A9. Local verification on this machine (2026-10-01, agy 1.2.13)

Executed with the installed `agy` CLI in throwaway git repositories under the session scratchpad, plus
Antigravity's bundled documentation (`~/.gemini/antigravity/builtin/skills/agy-customizations/docs/`).
These are first-hand results, not web claims.

| # | Finding | Evidence | → DOCCAD |
|---|---|---|---|
| A9.1 | Hook contract: stdin JSON with `toolCall.name` / `toolCall.args`; stdout JSON with `decision` (`allow`/`deny`/`ask`/`force_ask`); `PreInvocation` may return `injectSteps` with an `ephemeralMessage`; hooks run with cwd = the directory holding `hooks.json` | bundled `hooks.md` | Guard written to this contract |
| A9.2 | Real tool names and argument keys: `run_command` (`CommandLine`, `Cwd`), `write_to_file` (`TargetFile`, `CodeContent`, `Overwrite`), `view_file` (`AbsolutePath`) | hook payload log of a test run | Guard matches these |
| A9.3 | **A `PreToolUse` hook that prints `{}` silently blocks every tool call — the command did not run, the file was not written — and the agent still replied "DONE"** | three test runs (`{}` vs `ask` vs no hook) | Any hook must print an explicit decision. Also direct evidence that an Antigravity agent can report success for actions that never happened → the prompt's evidence rules |
| A9.4 | `{"decision":"ask"}` preserves default behaviour: commands and writes ran; without `--dangerously-skip-permissions` a workspace write needed no prompt | test runs | Guard's no-objection answer is `ask` |
| A9.5 | `{"decision":"deny"}` blocks even under `--dangerously-skip-permissions`; the agent receives the reason text | live guard test | Deny is a real backstop |
| A9.6 | Hooks in a **git-ignored** `.agents/` are loaded (resolves open question A3.3 for hooks) | live guard test with `.agents/` in `.gitignore` | `.agents/hooks.json` works in this repo |
| A9.7 | `PreInvocation` `ephemeralMessage` reaches the model (it quoted the reminder verbatim) | live guard test | Compaction defence for the binding rules |
| A9.8 | The bundled rules doc names only `AGENTS.md` / `GEMINI.md` as rule files (no `.agents/rules/`) | bundled `rules.md` | Binding rules belong in `AGENTS.md` (as planned) |
| A9.9 | The owner's global CLI allow-list (`~/.gemini/antigravity-cli/settings.json`) includes `git push --force origin main` and other pushes; the 2.0 app's global setting is `CASCADE_COMMANDS_AUTO_EXECUTION_OFF` (every command needs approval); a `doCCAD_pre` project exists with empty settings | local config files (secrets not read) | Workspace guard denies pushes (Deny > Allow); auto-execution for this project is an owner decision |

**Agent A top recommendations:** (1) every "done" claim is backed by a command, exit code and date in a
repo file, and no check may be documented without an implementing script; (2) the owner pre-configures
permissions (allow npm/python/git-read, deny `git push`, secrets and archive writes — a PreToolUse hook is
the documented mechanism); (3) binding rules in `AGENTS.md`, canary-test `.agents/` loading, no
`GEMINI.md`; (4) phases with file-based state, a green gate and a fresh conversation at each boundary, one
branch, no parallel agents on the tree; (5) bounded loops and explicit `/browser` use against localhost in
the 2.0 app; GitHub auth, Pages and PR approval stay human.

---

## B. Docs-as-code delivery stack (Agent B)

Release dates come from the GitHub releases API (`published_at`), treated as authoritative. Local facts
the agent checked: `prototype/docusaurus.config.ts` has `url: 'https://doccad.local'`, `baseUrl: '/'`, no
`trailingSlash`, search `language: ['en']` only; `prototype/package-lock.json` pins Docusaurus 3.10.2,
mermaid 11.17.2, `@mermaid-js/layout-elk` 0.1.9, TypeScript 5.6.3; there is no `static/` and no `.github/`.

### B1. Docusaurus release line

| # | Claim | Source | Status | → DOCCAD |
|---|---|---|---|---|
| B1.1 | Latest 3.x is **3.10.2 (2026-07-10)**; earlier 3.10.1 (2026-04-30), 3.10.0 (2026-04-07), 3.9.2 (2025-10-17) | https://api.github.com/repos/facebook/docusaurus/releases | VERIFIED | Prototype is current; nothing to bump |
| B1.2 | 3.10 is "the last release in the v3.x line"; v4 will drop React 18; no v4 date published | https://docusaurus.io/blog/releases/3.10 | VERIFIED (no date elsewhere UNVERIFIED) | Stay on 3.10.x; rehearse v4 flags incrementally |
| B1.3 | `onBrokenMarkdownLinks` deprecated since 3.9, removed in v4 → `markdown.hooks.onBrokenMarkdownLinks` + new `markdown.hooks.onBrokenMarkdownImages` (`ignore`/`log`/`warn`/`throw` or callback) | https://docusaurus.io/docs/api/docusaurus-config | VERIFIED (summary) | Set both hooks to `throw` |
| B1.4 | `future.v4` flags: `removeLegacyPostBuildHeadAttribute`, `useCssCascadeLayers`, `siteStorageNamespacing`, `fasterByDefault`, `mdx1CompatDisabledByDefault`; `future.v4: true` enables all; `siteStorageNamespacing` resets visitor theme state once; `mdx1CompatDisabledByDefault` makes MDX stricter | config docs ; 3.10 post | VERIFIED | Enable one at a time, each in a PR with CI |
| B1.5 | Docusaurus Faster (Rspack, SWC, Lightning CSS) is stable in 3.10; needs optional `@docusaurus/faster` + `future.faster` | 3.10 post | VERIFIED | Optional; **new dependency — owner approval** |
| B1.6 | React 19 supported: core and theme-mermaid 3.10.2 peer `react ^18 \|\| ^19` | https://raw.githubusercontent.com/facebook/docusaurus/v3.10.2/packages/docusaurus/package.json (+ theme-mermaid) | VERIFIED | Current stack supported |
| B1.7 | Docusaurus itself requires Node ≥20.0 | https://docusaurus.io/docs/installation | VERIFIED | Bump driven by Node EOL (B2), not Docusaurus |
| B1.8 | TypeScript 6.0 usable with `"ignoreDeprecations": "6.0"` | 3.10 post | VERIFIED (summary) | Keep `~5.6` |
| B1.9 | **Mermaid 12.0.0 released 2026-09-10**: ELK bundled and auto-registered; diagrams without `layout` (flowchart, state, class, ER, requirement, use-case) now default to ELK instead of dagre; theme-mermaid peer is `mermaid >=11.6.0` | https://api.github.com/repos/mermaid-js/mermaid/releases | VERIFIED | Keep `npm ci` + committed lockfile (stays on 11.17.2); a Mermaid 12 upgrade is a separate PR with a visual check; `@mermaid-js/layout-elk` becomes redundant at 12 |

### B2. Node.js status on 2026-10-01

| Version | Maintenance from | End of life | Status 2026-10-01 |
|---|---|---|---|
| 20 | 2024-10-22 | **2026-04-30** | **EOL** |
| 22 | 2025-10-21 | 2027-04-30 | Maintenance LTS |
| 24 | 2026-10-20 | 2028-04-30 | Active LTS (maintenance from 2026-10-20) |
| 26 | — | 2029-04-30 | Current; LTS from 2026-10-28 |

Source: https://raw.githubusercontent.com/nodejs/Release/main/schedule.json — VERIFIED (status labels derived
from the dates). → DOCCAD: `engines.node` `>=20.0` (`prototype/package.json:38`) points at an EOL line;
raise to `>=22`, run CI on Node 24 (local is already v24.19.0), add `.nvmrc` = 24. This also moves toward
ADR-002's "Node ≥24.14" (`PI/04_ARCHITECTURE/ADR/adr-002-docusaurus-framework.md:18`).

### B3. GitHub Pages deployment with Actions

| # | Claim | Source | Status | → DOCCAD |
|---|---|---|---|---|
| B3.1 | The official Docusaurus deploy workflow is stale (`checkout@v4`, `setup-node@v4` Node 20, `upload-pages-artifact@v3`, `deploy-pages@v4`; no `configure-pages`; no i18n note) | https://docusaurus.io/docs/deployment | VERIFIED | Do not copy versions verbatim |
| B3.2 | Current majors: `actions/checkout` **v7** (v7.0.1, 2026-07-20; v7.0.0 blocks checkout of fork PRs under `pull_request_target`/`workflow_run`); `actions/setup-node` **v7** (2026-07-14; v5+ on Node 24, auto npm cache when `packageManager` is set); `actions/setup-python` **v7** (2026-07-20; runner ≥ v2.327.1); `actions/configure-pages` **v6** (2026-03-25); `actions/upload-pages-artifact` **v5** (2026-04-10; adds `include-hidden-files`); `actions/deploy-pages` **v5** (v5.0.1, 2026-09-01) | https://api.github.com/repos/actions/{checkout,setup-node,setup-python,configure-pages,upload-pages-artifact,deploy-pages}/releases | VERIFIED | Use these majors, pinned by full SHA with a version comment |
| B3.3 | `upload-pages-artifact` v4+ excludes dotfiles unless `include-hidden-files: true` | same | VERIFIED; harmlessness of a missing `.nojekyll` for Actions-based deploys UNVERIFIED | No `static/.nojekyll` needed today |
| B3.4 | `deploy-pages` needs `pages: write`, `id-token: write`, `contents: read` (v4+ also `actions: read` — UNVERIFIED for v5); deploy job in the `github-pages` environment with `needs:` on the build job; artifact = one tarball without symlinks | https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages | VERIFIED | Matches archive T13 |
| B3.5 | Project sites live at `https://<owner>.github.io/<repo>/` → `url: 'https://<owner>.github.io'`, `baseUrl: '/<repo>/'` (custom domain keeps `/`); Docusaurus recommends setting `trailingSlash` explicitly | https://docusaurus.io/docs/deployment ; https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages | VERIFIED | Current `url: 'https://doccad.local'`, `baseUrl: '/'`, no `trailingSlash` must change — **depends on owner's repo name / domain** |
| B3.6 | **On GitHub Free, Pages requires a public repository**; limits: 1 GB site, soft 100 GB/month bandwidth, 10-minute deploy timeout | https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site ; …/github-pages-limits | VERIFIED | Owner decision: public repo (free) or paid plan |
| B3.7 | One `docusaurus build` emits `build/` + `build/hu/` under one base path | https://docusaurus.io/docs/i18n/tutorial | VERIFIED | One build job deploys both locales |

### B4. PR-gated governance on GitHub

| # | Claim | Source | Status | → DOCCAD |
|---|---|---|---|---|
| B4.1 | Rulesets: layered (up to 75), visible to readers, enforcement toggle, aggregate with classic protection (most restrictive wins), bypass list optionally "for pull requests only"; rules include require PR, approvals, code-owner review, approval of most recent push, dismiss stale approvals, conversation resolution, required status checks, block force pushes, linear history, restrict file paths | https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets ; …/available-rules-for-rulesets | VERIFIED (private-repo-on-Free availability UNVERIFIED) | Use a ruleset on `main` |
| B4.2 | CODEOWNERS in `.github/`, root or `docs/`; last match wins; owners need write access; enforced only with "require review from code owners"; not requested on draft PRs; protect the CODEOWNERS file itself | https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners | VERIFIED | `/prototype/docs/generated/** @owner` plus the ruleset rule = path-specific human gate |
| B4.3 | **"Pull request authors cannot approve their own pull requests"**; admins can merge without approval via bypass | https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/approving-a-pull-request-with-required-reviews | VERIFIED | 1 required approval + no bypass deadlocks the owner's own PRs. INFERRED: bot-authored generation PRs *can* be approved by the owner (the owner is not the author) — the archive's ADR-005 design works for bot PRs; the owner's own PRs need a "PRs only" bypass |
| B4.4 | Strict status checks optional; "do not allow bypassing" exists; merge queue needs a `merge_group:` trigger and suits high-volume repos | https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches ; …/managing-a-merge-queue | VERIFIED | Skip merge queue |
| B4.5 | PR previews: `rossjrw/pr-preview-action` needs Pages "deploy from branch" (incompatible with the Actions-source `deploy-pages` flow) and does not support fork PRs; Cloudflare Pages previews need an external account | https://github.com/rossjrw/pr-preview-action ; https://developers.cloudflare.com/pages/configuration/preview-deployments/ | VERIFIED | Start with `upload-artifact` of `build/` per PR (archive's MVP preview strategy, `automation_architecture.md:64-68`) |

### B5. CI quality gates and workflow hardening

| # | Claim | Source | Status | → DOCCAD |
|---|---|---|---|---|
| B5.1 | `onBrokenLinks` checks internal links only, in production builds; `onBrokenAnchors` covers Docusaurus `Heading` anchors and defaults to warn | https://docusaurus.io/docs/api/docusaurus-config#onBrokenLinks | VERIFIED (summary) | Add `onBrokenAnchors: 'throw'`; external links need a separate checker |
| B5.2 | `lycheeverse/lychee-action` v2.9.0 (2026-07-09) | GitHub releases API | VERIFIED (version); inputs UNVERIFIED | Optional weekly external-link job (archive: non-blocking) |
| B5.3 | `@mermaid-js/mermaid-cli` 12.0.0 (2026-09-24) bundles Mermaid 12, needs Puppeteer ≥25 and Node ≥22.13; breaking CLI changes; `mmdc -i file.md -o out.md` processes fenced blocks | https://api.github.com/repos/mermaid-js/mermaid-cli/releases/latest ; https://github.com/mermaid-js/mermaid-cli | VERIFIED | Parser-version mismatch with site Mermaid 11.17.2 → pin an 11.x CLI if available (UNVERIFIED) or use the headless-browser check (B7) instead. **New dependency — owner approval** |
| B5.4 | Mermaid renders client-side, so a syntax error may not fail `npm run build` | — | UNVERIFIED for theme-mermaid 3.10.2 | The browser smoke check is the layer that catches it |
| B5.5 | `markdownlint-cli2` release data could not be loaded | — | UNVERIFIED | Prefer extending `validate_docs.py` |
| B5.6 | `actions/setup-python@v7` + `pip install pyyaml jsonschema referencing` with `cache: pip`; without `jsonschema` the validator silently degrades | setup-python releases ; `AGENTS.md` (Setup) | VERIFIED | CI must install `jsonschema` |
| B5.7 | Pin actions to a full commit SHA ("currently the only way to use an action as an immutable release"; a policy can require it); default token read-only; avoid `pull_request_target`/`workflow_run` with untrusted code (write tokens, secrets, shared cache); pass untrusted input via `env:` | https://docs.github.com/en/actions/reference/security/secure-use | VERIFIED | Confirms archive T8 and §5 |
| B5.8 | Dependabot *alerts* cover semver-versioned actions, not SHA-pinned ones; whether version updates bump SHA pins | https://docs.github.com/en/code-security/dependabot/working-with-dependabot/keeping-your-actions-up-to-date-with-dependabot | VERIFIED (alerts) / UNVERIFIED (updates) | Add `dependabot.yml` and check behaviour after the first run |

### B6. i18n (en + hu)

| # | Claim | Source | Status | → DOCCAD |
|---|---|---|---|---|
| B6.1 | `docusaurus write-translations --locale hu` writes `code.json` plus `docusaurus-theme-classic/navbar.json` and `footer.json`; re-running appends without overwriting; static analysis only; mark strings with `<Translate>` / `translate()`; docs under `i18n/<locale>/docusaurus-plugin-content-docs[-<id>]/current`; explicit heading IDs keep anchors stable | https://docusaurus.io/docs/i18n/tutorial ; https://docusaurus.io/docs/i18n/git | VERIFIED (summaries) | Exactly the M6 work |
| B6.2 | Untranslated docs fall back to the source locale | search excerpt only | UNVERIFIED | Test with a build missing one `hu` doc (archive sources also disagree — see D) |
| B6.3 | `@easyops-cn/docusaurus-search-local` v0.55.3 (2026-07-29) = pinned; supports lunr-languages + zh; built-in UI strings only en/de/vi/zh-Hans; lunr-languages includes `hu` | https://github.com/easyops-cn/docusaurus-search-local ; https://raw.githubusercontent.com/MihaiValentin/lunr-languages/master/README.md | VERIFIED (summaries) | Change search `language: ['en']` → `['en','hu']`; translate search UI strings |

### B7. Headless smoke testing

| # | Claim | Source | Status | → DOCCAD |
|---|---|---|---|---|
| B7.1 | Playwright CI: checkout, setup-node, `npm ci`, `npx playwright install --with-deps`, run, upload report; latest v1.63.0 (2026-09-04) | https://playwright.dev/docs/ci-intro ; https://api.github.com/repos/microsoft/playwright/releases | VERIFIED | **New devDependency + ~150 MB browser download — owner approval** |
| B7.2 | Minimal smoke = serve `build/`, load `/`, a `/docs/…` page, a `/views/…` page and `/hu/`; fail on `pageerror`, console errors, non-200; one screenshot per route; check a Mermaid page renders an `svg` and search returns hits | agent design | INFERRED | Complements Antigravity `/browser` evidence; runs in CI unattended |

**Agent B minimal setup (condensed):** `engines >=22`, `.nvmrc` 24, CI on Node 24; real `url`/`baseUrl`,
explicit `trailingSlash`; one `ci.yml` on `pull_request` + `push: main`, `contents: read`, steps checkout
v7 → setup-node v7 → setup-python v7 + `pip install pyyaml jsonschema referencing` → `npm ci` →
`typecheck`, `validate`, `test`, `build`, all actions SHA-pinned; fail CI on stale pages by parsing
`detect` output / `impact.json`; deploy job on `push: main` only with `configure-pages` v6,
`upload-pages-artifact` v5, `deploy-pages` v5 in `github-pages`; ruleset on `main` (PR, status check,
code-owner review, no force push), `CODEOWNERS` for generated content and `.github/`, owner bypass for PRs
only; PR preview as an artifact; `dependabot.yml` weekly; later lychee, a Playwright smoke script and
`onBrokenAnchors: 'throw'`.

---

## C. Governed live AI generation (Agent C)

Repository facts the agent checked (read-only): `prototype/ai/gemini_provider.py:47` calls
`:generateContent` with header `x-goog-api-key`; `prototype/ai/anthropic_provider.py:13` sends
`anthropic-version: 2023-06-01`; `prototype/ai/openai_provider.py:12` uses `/v1/chat/completions`; all four
live adapters forward `temperature` from `opts`, and none sends a structured-output field;
`prototype/schemas/interview.schema.json` uses `minLength`/`maxLength`/`pattern` and
`prototype/schemas/document.schema.json` uses `pattern`, `if/then` and `minimum`.

### C1. Structured JSON output over plain REST

| # | Claim | Source | Status | → DOCCAD |
|---|---|---|---|---|
| C1.1 | Gemini `POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent` remains fully supported; structured output via `generationConfig` (`responseMimeType` + `responseSchema` **or** `responseJsonSchema`, mutually exclusive) | https://ai.google.dev/api/generate-content | VERIFIED | Existing Gemini adapter endpoint stays valid; add `generationConfig` |
| C1.2 | Gemini's new **Interactions API** (`POST /v1beta/interactions`, `response_format` with `mime_type: application/json` + `schema`) is GA since June 2026 and recommended for new projects; `generateContent` is called "legacy" but not deprecated | https://ai.google.dev/gemini-api/docs/interactions ; https://ai.google.dev/gemini-api/docs/structured-output | VERIFIED | Keep `generateContent` behind one small request-builder function so a later switch is local to the adapter |
| C1.3 | Gemini schema subset (Interactions page): types, title, description, properties, required, additionalProperties, enum, format (date-time/date/time only), minimum/maximum, items, prefixItems, minItems/maxItems; large or deeply nested schemas may be rejected. No mention of `pattern`, `minLength`, `if/then` | https://ai.google.dev/gemini-api/docs/interactions | VERIFIED (list); keyword support on `generateContent` UNVERIFIED | Send a provider-facing schema, not the repo schema |
| C1.4 | Anthropic structured outputs are GA: `POST https://api.anthropic.com/v1/messages`, headers `anthropic-version: 2023-06-01`, `content-type: application/json`, body `output_config.format = {type: "json_schema", schema}`; older `output_format` is deprecated (beta header `structured-outputs-2025-11-13`) | https://platform.claude.com/docs/en/build-with-claude/structured-outputs | VERIFIED | Add `output_config.format` to the Anthropic adapter |
| C1.5 | Anthropic auth: `Authorization: Bearer` preferred, `x-api-key` still supported | https://platform.claude.com/docs/en/manage-claude/authentication | VERIFIED | Either works; keep keys env-only |
| C1.6 | Anthropic schema support: enum, const, anyOf, internal `$ref`/`$defs`, required, `additionalProperties: false` (required), string formats, `pattern` (no lookaheads/backrefs/`\b`), `minItems` 0 or 1 only. **Unsupported:** recursion, `minimum`/`maximum`/`multipleOf`, `minLength`/`maxLength`, `allOf` with `$ref`. Refusal → `stop_reason: "refusal"`; "Schema is too complex" error possible; grammars cached 24 h | same | VERIFIED | Interview schema's length/minimum keywords cannot be sent; enforce locally |
| C1.7 | Forced tool use (`tool_choice` any/tool) returns 400 on the newest Anthropic model families; strict tool `input_schema` is an alternative with `tool_choice: auto` | https://platform.claude.com/docs/en/api/errors ; structured-outputs page | VERIFIED | Prefer `output_config.format` over tool-use-for-JSON |
| C1.8 | OpenAI Responses API recommended for new projects; Chat Completions not deprecated. Responses: `POST /v1/responses`, `text.format = {type: "json_schema", …}`; Chat Completions: `response_format: {type: "json_schema", json_schema: {…}}` | https://developers.openai.com/api/docs/guides/migrate-to-responses | VERIFIED | Adapter may stay on Chat Completions; add `response_format` |
| C1.9 | OpenAI strict mode: `additionalProperties: false` on every object, every property in `required`, root must be an object; refusals in a `refusal` field; `minLength`, `pattern`, `format`, `minimum` unsupported | https://developers.openai.com/api/docs/guides/structured-outputs | PARTIALLY VERIFIED (keyword list from page excerpt; nesting/property limits UNVERIFIED) | Both repo schemas need a transformed provider schema |
| C1.10 | Newer OpenAI models may require `max_completion_tokens` instead of `max_tokens` | — | UNVERIFIED | First live call must test this; adapter currently sends `max_tokens` |
| C1.11 | Ollama native `POST /api/chat` accepts `format: "json"` or a JSON Schema object; `stream` defaults to `true` (set `false`); docs recommend also putting the schema in the prompt and temperature 0; structured outputs unsupported on Ollama Cloud | https://docs.ollama.com/api/chat ; https://docs.ollama.com/capabilities/structured-outputs | VERIFIED | Local adapter needs `stream: false` and a schema path |
| C1.12 | Ollama OpenAI-compatible `/v1/chat/completions` supports `response_format`, but the compatibility page confirms only JSON mode, not `json_schema`; `logprobs`, `tool_choice`, `logit_bias`, `n` unsupported; `/v1/responses` added in v0.13.3 | https://docs.ollama.com/api/openai-compatibility ; https://ollama.com/blog/structured-outputs (2024-12) | VERIFIED (page); `json_schema` enforcement UNVERIFIED | Test `json_schema` on the target Ollama version; fall back to native `/api/chat` `format` or JSON mode + local validation |
| C1.13 | Every provider's constrained decoding supports only a JSON-Schema subset | synthesis of C1.3, C1.6, C1.9, C1.11 | INFERRED | **The repo schemas stay the gate; re-validate every response locally with `jsonschema`. Provider-side enforcement is an optimization only.** |

### C2. Model IDs by environment variable; deprecation handling

| # | Claim | Source | Status | → DOCCAD |
|---|---|---|---|---|
| C2.1 | Anthropic lifecycle Active → Legacy → Deprecated → Retired; ≥60 days' notice; retired models fail; `claude-sonnet-4-5-20250929` deprecated 2026-09-30, retiring 2026-11-30 | https://platform.claude.com/docs/en/about-claude/model-deprecations | VERIFIED | Env-only model IDs (AD-5) are the right design; add a deprecation watch |
| C2.2 | Anthropic: non-default `temperature`/`top_p`/`top_k` return 400 on Opus 4.7 and later; prefill rejected on 4.6 and later | same | VERIFIED | Make sampling parameters opt-in per provider/model; the adapters forward `temperature` today |
| C2.3 | Gemini shutdown dates are "earliest possible"; preview models can be very short-lived | https://ai.google.dev/gemini-api/docs/deprecations | VERIFIED | Avoid preview models in CI |
| C2.4 | OpenAI: ≥6 months' notice for GA models, ≥3 months for specialized variants, ~2 weeks for previews; snapshots are pinned, aliases move | https://developers.openai.com/api/docs/deprecations | VERIFIED | Pin snapshots via env in CI |
| C2.5 | Record the model string the API *returns* in `generation.model`, not only the configured alias | inference from C2.4 | INFERRED | Provenance stamp change in `generate_page.py` |

### C3. Evaluating grounded, citation-faithful generation

| # | Claim | Source | Status | → DOCCAD |
|---|---|---|---|---|
| C3.1 | ALCE (Gao et al., EMNLP 2023) defines automatic citation-quality metrics; even the best models lacked complete citation support ~50% of the time on ELI5 | https://arxiv.org/abs/2305.14627 | VERIFIED | Citation support must be checked, not assumed |
| C3.2 | Post-hoc checks can test *support*, not whether the model derived the claim from the source | https://tianpan.co/blog/2026-04-23-rag-citations-post-hoc-rationalization (blog) | UNVERIFIED | Human review stays the final gate (AD-9) |
| C3.3 | Deterministic, stdlib-only eval methods: citation resolution against allowed evidence + recorded sha256; verbatim-quote containment (whitespace-normalized substring); coverage/orphan checks; number and proper-noun overlap flags; golden-set regression in `unittest` | agent design inference | INFERRED | Build a `check_grounding` validator next to `validate_docs.py`; golden set of (contract, expected cited sources) |
| C3.4 | promptfoo offers deterministic (`contains`, `is-json`, `regex`, `python`, `latency`, `cost`) and model-graded (`llm-rubric`, `context-faithfulness`, `factuality`) assertions in YAML; it is a Node tool | https://www.promptfoo.dev/docs/configuration/expected-outputs/ | VERIFIED | Optional; **new dependency — owner approval** |
| C3.5 | RAGAS, DeepEval, FActScore are heavier Python packages | search snippets | UNVERIFIED | Not recommended under the stdlib + PyYAML rule |

### C4. Prompt-injection defense for retrieved documents

| # | Claim | Source | Status | → DOCCAD |
|---|---|---|---|---|
| C4.1 | OWASP LLM01:2025 defines indirect injection via external content; mitigations: constrain behavior, deterministic output-format validation, input/output filtering, least privilege, human approval for high-risk actions, segregate and label external content, adversarial testing; "unclear if there are fool-proof methods of prevention" | https://genai.owasp.org/llmrisk/llm01-prompt-injection/ | VERIFIED | Matches AD-15 and T2 in the archive |
| C4.2 | Anthropic guidance: deliver untrusted content as labeled data (tool results), state an untrusted-content policy, JSON-encode untrusted strings, least privilege, optional classifier screen, red-team with injected documents | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks | VERIFIED | Add injection-bearing fixtures to the test suite |
| C4.3 | Design patterns that constrain the agent (e.g. CaMeL, the June 2025 "design patterns" paper) give real guarantees; delimiter spotlighting, sandwiching and instruction hierarchy do not and fail against adaptive attacks | https://simonwillison.net/2025/Jun/13/prompt-injection-design-patterns/ ; https://arxiv.org/abs/2503.18813 | UNVERIFIED (snippets) | Consistent with the archive's own residual-risk note (T2) |
| C4.4 | Keep the generator a no-tool, no-network, write-nothing text transform; the gate is deterministic (schema, allowed-evidence citations, no new URLs/paths outside the allowlist) plus human review | agent synthesis | INFERRED | Already DOCCAD's shape (ADR-004 "no agent loops"); keep it |

### C5. Rate limits, retries, budgets, caching

| # | Claim | Source | Status | → DOCCAD |
|---|---|---|---|---|
| C5.1 | Anthropic: RPM/ITPM/OTPM per model class, token bucket; 429 carries `retry-after`; spend-cap 429 has **no** `retry-after` and `error_code: "enforced_spend_limit_reached"` (retry futile); 529 overloaded; 500 retry with backoff; 504 → streaming or Batches; `request-id` header; cached-read tokens do not count toward ITPM on most models | https://platform.claude.com/docs/en/api/rate-limits ; https://platform.claude.com/docs/en/api/errors | VERIFIED | Stdlib retry helper that distinguishes retryable from terminal 429s |
| C5.2 | Anthropic prompt caching: `cache_control: {type: "ephemeral"}` (optional `ttl: "1h"`), default TTL 5 min; write 1.25× (5 min) / 2× (1 h), read ≈0.1×; minimum cacheable size 512–4,096 tokens by model; usage fields `cache_creation_input_tokens`, `cache_read_input_tokens` | https://platform.claude.com/docs/en/build-with-claude/prompt-caching | VERIFIED | Put the shared governance + evidence prefix first |
| C5.3 | OpenAI: RPM/RPD/TPM/TPD/IPM; exponential backoff + jitter; `Retry-After` is a minimum; `x-ratelimit-*` headers; 429 can mean quota exhaustion; Batch API has separate limits; prompt caching is automatic (`usage.input_tokens_details.cached_tokens`) | https://developers.openai.com/api/docs/guides/rate-limits ; https://developers.openai.com/api/docs/guides/prompt-caching | VERIFIED | Same retry helper |
| C5.4 | Gemini limits are per project (not per key): RPM, TPM, RPD, shown only in AI Studio; over-limit → 429 `RESOURCE_EXHAUSTED` | https://ai.google.dev/gemini-api/docs/rate-limits | VERIFIED | Same retry helper |
| C5.5 | Gemini context caching; Batch APIs for DOCCAD's scale | — | UNVERIFIED (not researched) | Optional later |
| C5.6 | Adapters today use bare `urlopen` with 120–300 s timeouts and no retry | agent repo read | EXPLICIT (repo) | Add retry: 429/500/502/503/504/529 with backoff + jitter honoring `Retry-After`; fail fast on 400/401/403 and quota/spend-cap 429; log `request-id` and usage; per-run token/cost ceiling with an abort switch |

### C6. Provider secrets in GitHub Actions

| # | Claim | Source | Status | → DOCCAD |
|---|---|---|---|---|
| C6.1 | Secrets are not passed to workflows triggered from forks (except a read-only `GITHUB_TOKEN`); first-time contributors may need approval to run workflows | https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions ; https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows | VERIFIED | Validation on PRs never needs provider keys |
| C6.2 | `pull_request_target` runs privileged with secrets: avoid it; never check out untrusted code under it; use `workflow_run` for privilege separation; pin actions to full SHAs; default `GITHUB_TOKEN` read-only; pass untrusted values through `env:` not inline `${{ }}` | https://docs.github.com/en/actions/reference/security/secure-use | VERIFIED | Confirms archive T8 policy verbatim |
| C6.3 | Environments: up to 6 required reviewers (one approval suffices; optional prevent-self-review), wait timers, branch/tag restrictions; environment secrets released only after rules pass; **free plans get environments on public repos only** | https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments | VERIFIED | Repo visibility decision affects the `generation` environment design |
| C6.4 | GitHub OIDC: `id-token: write` → JWT exchanged for short-lived cloud credentials (AWS, Azure, GCP, Vault); GCP needs an attribute condition | https://docs.github.com/en/actions/concepts/security/openid-connect | VERIFIED | Pages deploy via OIDC as designed |
| C6.5 | **Anthropic supports Workload Identity Federation**: a GitHub Actions JWT is exchanged at `POST /v1/oauth/token` for a short-lived Claude API token; requires a service account, federation issuer and federation rule | https://platform.claude.com/docs/en/manage-claude/authentication | VERIFIED | **Conflicts with the archive** (see D-conflicts) — static Anthropic key can be replaced |
| C6.6 | Vertex AI access via GitHub OIDC; OpenAI workload identity federation | — | UNVERIFIED | Keep static keys + environment protection + spend caps for these |

### C7. Ingesting external Git repositories (Phase 3)

| # | Claim | Source | Status | → DOCCAD |
|---|---|---|---|---|
| C7.1 | `actions/checkout` (README says latest major is v7): multi-repo via separate steps with `repository`, `ref` (SHA allowed), `path`; `sparse-checkout` (cone mode default); `persist-credentials` defaults to `true` (set `false`); `fetch-depth` 1; default token limited to the current repo — private external repos need a PAT, GitHub App token or deploy key | https://github.com/actions/checkout | VERIFIED | Pinned sparse checkout per external source |
| C7.2 | Submodules store a gitlink to an exact commit SHA; updating is explicit | https://git-scm.com/book/en/v2/Git-Tools-Submodules | VERIFIED | Built-in pinning, but adds clone friction |
| C7.3 | REST contents API accepts `ref=<SHA>`; files ≤1 MB returned inline, 1–100 MB via raw media type; directory listings capped at 1,000 entries (use Git Trees API beyond) | https://docs.github.com/en/rest/repos/contents | VERIFIED | Viable stdlib path (`urllib`) |
| C7.4 | Subtree copies content in and loses clean provenance unless the origin SHA is recorded | — | UNVERIFIED | Not recommended |
| C7.5 | `repository_dispatch` runs on the default branch; `client_payload` ≤10 top-level properties and 65,535 chars; `workflow_dispatch` ≤25 inputs; `GITHUB_TOKEN` cannot trigger other workflow runs — cross-repo dispatch needs an App or PAT | https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows ; https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow | VERIFIED (token scopes UNVERIFIED) | Cross-repo triggers need a human-provisioned token |
| C7.6 | A repo without a license is all-rights-reserved by default | https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository | VERIFIED | License check before ingest; unlicensed → block |
| C7.7 | GitHub secret scanning covers the repo's own history; nothing about scanning ingested third-party content | https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning | VERIFIED | Pre-ingest secret scan needed |
| C7.8 | External provenance record = `{repo, commit SHA, path, sha256}`, never a branch name; ingested content is untrusted (C4) | agent synthesis | INFERRED | Extends `generation.source_documents` for Phase 3 |

**Agent C recommended design (condensed):** fixture stays default and live runs are opt-in only; one
provider-facing schema per adapter derived from the repo schema, with local `jsonschema` validation as the
gate; native structured output per provider; sampling parameters opt-in per model; stdlib retry helper and
per-call usage logging; per-run token/cost ceiling and cache-friendly prompt ordering; a deterministic
grounding gate before any page is written; generator without tools or network, injection fixtures in
tests; live jobs only on `workflow_dispatch`/`schedule` in a protected environment, results as a PR;
Phase 3 sources pinned to SHAs with secret and license checks.

**New dependencies (owner approval):** none required. `jsonschema` + `referencing` become effectively
required for the local gate. Optional: promptfoo (Node), RAGAS/DeepEval (Python), a provider SDK, gitleaks
or trufflehog.

---

## D. Conflicts between research, archive decisions and the prototype

Each conflict names both sides, then a proposed resolution. No archive file is changed by this pack. Where a
resolution would change an accepted decision, it is written as a **supersede proposal** (`NV-SUP-n`) for the
owner to accept or reject; accepting one means recording a new DEC (next free: DEC-011) and marking the old
one SUPERSEDED in `docs/primary-inputs/00_PROJECT_CONTROL/ENTITY_REGISTER.md`, per
`docs/primary-inputs/CONTRIBUTING.md`.

| # | Archive / prototype says | Research says | Proposed resolution | Type |
|---|---|---|---|---|
| D1 | Model providers authenticate only with static API keys; OIDC applies to Pages only (`PI/04_ARCHITECTURE/SAD/security_architecture.md:296-303`) | Anthropic now supports Workload Identity Federation from GitHub Actions (C6.5, VERIFIED); OpenAI/Vertex still UNVERIFIED (C6.6) | **No supersede needed**: the same paragraph says "If a provider ships OIDC/WIF for its inference API, adopt it and delete the corresponding key". Phase 2 offers Anthropic WIF as an owner-optional item; other providers keep static keys + `generation` environment + spend caps | Follow existing rule |
| D2 | ADR-002 / DEC-003: Node ≥24.14 (`adr-002-docusaurus-framework.md:18`); prototype `engines.node >=20.0` (`prototype/package.json:38`) | Node 20 EOL 2026-04-30; 24 is Active LTS (B2) | Align the prototype **to the ADR**: `engines.node >=24.14`, `.nvmrc` 24, CI on Node 24. The prototype was the deviation, not the decision | Prototype fix |
| D3 | ADR-002 adopts `future.faster` (Rspack, SSG workers); prototype has no `future` block | Faster is stable in 3.10 but needs the optional `@docusaurus/faster` package (B1.5); `future.v4` flags should be enabled one at a time (B1.4) | Keep DEC-003; implement `future.faster` only after the owner approves the new dependency; enable `future.v4` flags individually with CI green after each | Deferred implementation (owner approval) |
| D4 | ADR-007 / DEC-008: CI compiles every diagram with mermaid-cli; compile failure blocks merge | mermaid-cli 12 bundles Mermaid 12 (new default ELK layout) while the site pins Mermaid 11.17.2 (B1.9, B5.3); client-side rendering may not fail the build (B5.4, UNVERIFIED) | Preferred: pin a mermaid-cli release whose bundled Mermaid matches the site's 11.x (availability UNVERIFIED — check first). Fallback **NV-SUP-1**: replace "mermaid-cli" with "headless-browser render of every diagram page in the smoke test, failing on render errors" if no matching CLI exists. Either is a new dev dependency (owner approval) | Supersede proposal (only if fallback is taken) |
| D5 | ADR-005 / DEC-006: branch protection requires human approval; bot cannot approve its own PRs | Authors cannot approve their own PRs (B4.3); PRs and pushes made with `GITHUB_TOKEN` do not trigger other workflow runs (C7.5) | INFERRED: bot-authored generation PRs **can** be approved by the owner (owner is not the author), so ADR-005 holds for them. Two consequences: (a) the owner's own PRs touching gated paths need a ruleset bypass "for pull requests only"; (b) a generation PR opened with `GITHUB_TOKEN` gets no `pull_request` CI run, so its required checks never report. Resolution: the generation workflow authenticates with a **GitHub App installation token** (owner creates the App — human action); fallback: the generation job runs the full gate itself and attaches the report, and the owner closes and reopens the PR to trigger CI (UNVERIFIED workaround) | Design detail within DEC-006 |
| D6 | `approved` "is set by merge automation" (`PI/05_DOCUMENTATION_DESIGN/information-architecture/content_architecture.md:100`; KB `pr-gated-generation.md:32`); prototype: no producer of `approved`, and `build_filter.py:85-88` publishes any page whose frontmatter says `approved` | Rulesets + CODEOWNERS give a recorded human approval on the PR (B4.1–B4.2) | INFERRED design for Phase 1: an `approval_record` block (PR number, approver login, timestamp) is written by a human-triggered command on the PR branch before merge; CI on `main` rejects `approval_status: approved` without a complete `approval_record`; the production filter publishes only such pages. Schema change ⇒ bump `document.schema.json` and the three contract versions. Owner confirms the semantics before Phase 1 starts (open question E3) | Design within DEC-006 (owner confirmation) |
| D7 | T12: content classification `visibility: public\|private`, **defaulting to `private` when absent** (`security_architecture.md:259-269`); prototype has no field and an expected-failure test | — | Implement T12 as written. Consequence: every currently public page must declare `visibility: public`, or it disappears from the production build. This touches canonical frontmatter (a metadata migration, done once, listed in the PR) | Implement archive design |
| D8 | Non-goal: "multi-repo knowledge federation" (`PI/04_ARCHITECTURE/SAD/solution_architecture.md:53-57`) | External repos can be pinned by SHA with sparse checkout and provenance `{repo, sha, path, sha256}` (C7) | **NV-SUP-2** (owner decision before Phase 3): allow *pinned external evidence* — read-only snapshots of other repositories, fetched at a recorded commit SHA into the generation job, never served and never canonical — while keeping federation (live multi-repo sources of truth) a non-goal. If rejected, Phase 3 is dropped | Supersede proposal |
| D9 | Archive secret name `GOOGLE_API_KEY` (`security_architecture.md:290`) | Prototype and `.env.example` use `GEMINI_API_KEY` | Keep the prototype's name (it is what the code reads); note the difference in the plan | Naming only |
| D10 | ADR-004: adapters call `generateContent`, chat completions, Messages over plain HTTP | Gemini calls `generateContent` "legacy" (still supported) in favour of the Interactions API (C1.2); OpenAI recommends Responses (C1.8) | Keep current endpoints (supported, smaller change); isolate each request shape in one function per adapter so a later switch stays local. No decision change | Within DEC-005 |
| D11 | HU fallback: `flow_publishing.mmd:15` says "EN fallback"; Docusaurus runbook says untranslated pages 404 | Fallback behaviour UNVERIFIED (B6.2) | Phase 0 acceptance test: build with a page missing from `i18n/hu/` and record the actual behaviour in `VALIDATION.md` | Test, then document |
| D12 | `AGENTS.md` delegates detailed conventions to `.claude/rules/*.md` | Antigravity reads `AGENTS.md`, `GEMINI.md`, `.agents/rules/*.md` — not `.claude/rules/` (A3.1, A3.2) | The Antigravity prompt instructs the run to read `.claude/rules/README.md` and the matching rule files by hand (which `AGENTS.md` already asks of agents without path-glob loading). Do not add `GEMINI.md`. Optional owner step: copy rule content into flat `.agents/rules/` after a canary confirms git-ignored `.agents/` loads | Prompt instruction |
| D13 | T3: generated MDX must contain no `import`/`export`; components come from global MDXComponents (`security_architecture.md:160-170`) | — | Prototype generated pages import `EvidenceLink`, `InterviewPrep` and JSON datasets today. Phase 0: register components globally (`src/theme/MDXComponents.tsx` exists), load interview data without an MDX import, and add the T3 gate to `validate_docs.py` | Implement archive design |
| D14 | MkDocs is the constraint-adjusted fallback "with a dated exit decision before 2026-11-05" (`decision_matrix.md:52-55`); re-evaluation checkpoint 2026-10-15 (`PI/02_RESEARCH/documentation-platforms/mkdocs/` ADR-001) | — | No action unless DEC-001 is revisited; record in the plan that the fallback expires 2026-11-05 and Zensical (1.0 + plugin API + multi-language) is the designated re-evaluation target | Record only |
| D15 | Prototype canonical pages claim a link allowlist (`docs/source/security/prompt-injection-defense.md:45`) and a mermaid-cli CI gate (`docs/source/decisions/adr-007-mermaid-as-code.md:30`); fixture output claims a context secret scan (`prototype/ai/fixture_provider.py:384-389`) | — | Implement the gates in Phase 0–1; until each exists, the page states it as planned. Re-seed generated views after the fixture text changes | Prototype fix |

---

## E. Open questions

### E-owner. Decisions only the owner can make (needed before or during the run)

| # | Question | Why it matters | Default if unanswered |
|---|---|---|---|
| E1 | Public or private GitHub repository? | Free-plan Pages and environments need a public repo (B3.6, C6.3) | Plan assumes **public** (the `.gitignore` states "This repository is intended to be public") |
| E2 | Repository name and owner, or a custom domain? | Sets `url` / `baseUrl` (B3.5) | Phase 1 stops at this step until answered |
| E3 | Approval semantics: confirm D6 (human-triggered `approval_record`, CI-enforced) | Defines what "approved" means in production | Phase 1 implements D6 as proposed |
| E4 | Second human reviewer, or solo owner? | Solo approval is a deliberate recorded act, not independent review (B4.3) | Solo; documentation must say so |
| E5 | Which live provider first, which model (via `AI_MODEL_*`), and what spend cap per run and per month? | Phase 2 cost and safety | Phase 2 stops before any live call until keys, model env values and caps exist |
| E6 | Approve new dependencies? `jsonschema` + `referencing` as declared requirements; optional `@playwright/test` (smoke), `@mermaid-js/mermaid-cli` (diagram gate), `@docusaurus/faster`, lychee (CI-only) | `AGENTS.md`: "Do not add packages without asking" | Only `jsonschema` + `referencing` assumed (already optional dependencies); others not added |
| E7 | Create a GitHub App for generation PRs (D5)? | Required checks on bot PRs | Fallback workaround documented; generation PRs stay manual |
| E8 | Accept NV-SUP-2 (pinned external evidence) for Phase 3? Which licenses are acceptable? | Phase 3 scope | Phase 3 stays specification-only |
| E9 | What to do with `PI/02_RESEARCH/ai-models/`: register it (new RES/REF IDs, manifest entry, dated COLLECTION_REPORT section), move it out of the archive, or leave it | Archive integrity rule | Leave as is; recorded as an archive task for a separate session |
| E10 | Antigravity setup: permission allow/deny rules, a PreToolUse hook protecting the archive, browser allowlist | The run stalls or is unprotected otherwise (A2.4, A3.4, A4.2) | See the pre-run checklist in `03_NEXT_VERSION_PLAN.md` |

### E-research. Unresolved research questions (verify during the run)

- Antigravity: does it load git-ignored `.agents/`? glob-rule frontmatter syntax? context-overflow behaviour?
  does `/goal` keep an approved-plan gate? Stop-hook blocking? quota numbers and thinking level? is the
  raw-string tool-call bug present on Linux / fixed? (A3.3, A5.3, A5.6, A6.1)
- Does `/browser` need a Chrome extension? (A4.3)
- Gemini `responseJsonSchema` keyword support on `generateContent` (C1.3); Ollama `json_schema` enforcement on
  `/v1` (C1.12); OpenAI `max_completion_tokens` (C1.10).
- OpenAI / Vertex workload identity federation (C6.6); cross-repo dispatch token scopes (C7.5).
- Docusaurus untranslated-doc fallback (B6.2, D11); Mermaid syntax errors failing the build (B5.4); whether a
  mermaid-cli 11.x matching Mermaid 11.17.2 exists (D4); Dependabot bumping SHA-pinned actions (B5.8);
  `deploy-pages` v5 `actions: read` (B3.4); rulesets on private Free repos (B4.1).
