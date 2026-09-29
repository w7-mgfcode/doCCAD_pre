# GitHub-Native AI Documentation System — PoC

This proof-of-concept demonstrates a docs-as-code system where AI generates derived
views in CI, but only through pull requests, and never sits in the serving path.

- [Canonical documentation](/docs/overview) — human-owned, route `/docs`
- [Generated views](/views/recruiter/project-overview) — AI-derived, route `/views`
- [Interview prep view](/views/interview/architecture-system-overview) — rendered from generated JSON
