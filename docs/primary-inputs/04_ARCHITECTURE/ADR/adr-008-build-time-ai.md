# ADR-008: Build-Time / CI-Time AI over Runtime AI

Status: Accepted · 2026-08-12

## Context
Derived views could be produced at build/CI time (committed artifacts) or at request time (runtime service
calling models). Mission constraint: approved documentation must remain available when every provider is
down; AI must not sit in the read path.

## Decision
All AI output is produced in CI or local CLI and committed via PR before it is ever served. The published
site is static; no server-side or client-side model call exists in the serving path. Special questions are
CI jobs producing preview PRs, not a chat endpoint.

## Consequences
+ Availability and cost decouple from providers; every served word was reviewable; caching/scaling are
  trivial (static). - No real-time personalization or chat (explicit non-goal; a future chat feature would
  be an isolated service, per spine Deferred).

## Alternatives
Runtime generation rejected (availability coupling, unreviewed output, injection surface at serve time).
Hybrid per-page runtime hydration rejected (two lifecycles, worst of both).
