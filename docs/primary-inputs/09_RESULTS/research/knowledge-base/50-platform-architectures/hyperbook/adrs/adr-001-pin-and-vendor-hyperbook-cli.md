# ADR-001: Pin and vendor the Hyperbook CLI version

## Status
Proposed (2026-08-12)

## Context
Hyperbook is pre-1.0 (0.104.0 as of 2026-08-11) with a very fast release cadence (11 npm releases between mid-July and mid-August 2026) and effectively a single human maintainer (~90%+ of human commits by Mike Barkmin; two external contributors with one commit each — verified via git shortlog of openpatch/hyperbook). Directive behavior, config schema, and output structure can change between minor versions without semver guarantees. The target ecosystem must be operable by one engineer and must not break because an unattended CI run pulled a newer generator.

## Decision
CI installs an exact, pinned version of the `hyperbook` npm package (no `^`/`~` ranges, lockfile committed). Additionally, the exact tarball (`npm pack hyperbook@X.Y.Z`) is vendored into repository storage (or a private registry mirror) so builds succeed even if the package is unpublished or the maintainer account is compromised. Upgrades happen deliberately, at most quarterly, via a PR that rebuilds a smoke-test book exercising every directive and config feature in use, with a visual diff review.

## Consequences
- Builds are reproducible and immune to upstream churn and npm supply-chain events.
- Security or bug fixes arrive only at upgrade windows; an out-of-band upgrade path must exist for critical fixes.
- The smoke-test book is a small permanent maintenance artifact but doubles as living documentation of used features.
- Vendored tarballs plus a mirror of the source monorepo constitute step one of fork readiness (see ADR-004).

## Alternatives
- Track `latest` in CI: rejected — unattended breakage risk with a 0.x package.
- Build from a forked source immediately: rejected as premature — adds monorepo (pnpm/changesets) maintenance cost before it is needed.
