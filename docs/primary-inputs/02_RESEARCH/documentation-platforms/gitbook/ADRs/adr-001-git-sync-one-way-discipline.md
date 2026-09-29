# ADR-001: Operate Git Sync in one-way Git→GitBook discipline

## Status
Proposed (adoption-blocking decision)

## Context
GitBook Git Sync is bidirectional: merged GitBook change requests commit to the synced GitHub branch
(`GITBOOK-{n}` commits), and repo commits import into GitBook [VERIFIED-OFFICIAL]. The target
ecosystem mandates GitHub as the single canonical source with all changes flowing through PR review.
GitBook's internal block model is the operational source of truth; export re-serializes Markdown,
may create new files instead of reusing existing ones, and duplicates README files created in the UI
[VERIFIED-OFFICIAL]. App-side merges land on the branch without GitHub PR review. GitHub PRs do not
create GitBook change requests, so review remains GitHub-side anyway.

## Decision
Enable Git Sync with initial direction "GitHub → GitBook" and enforce a one-way authoring policy:
every human member holds Reader role (or no membership) in the GitBook app; no change requests are
ever created app-side; all content changes — human and AI-generated — enter via GitHub PRs to the
synced branch. Branch protection alerts on any commit whose message matches `GITBOOK-*`.

## Consequences
- Git remains effectively canonical; diffs stay reviewable and deterministic (modulo initial
  normalization, which is verified once during adoption).
- The GitBook editor, live collaboration, and app-side change requests — a large part of the paid
  value — are deliberately unused.
- A single leaked Editor+ credential can still violate the policy; monitoring for `GITBOOK-*`
  commits is the compensating control.
- Non-technical contributors must use GitHub (or file issues) instead of the WYSIWYG editor.

## Alternatives
- **Full bidirectional use**: accepted GitBook normalization and unreviewed `GITBOOK-n` commits;
  rejected — breaks the canonical-Git and PR-review invariants.
- **No Git Sync, API-only pushes**: rejected — loses PR previews and makes GitBook the only store.
- **Different platform (pure SSG)**: viable; retained as rehearsed exit (see ADR-004).
