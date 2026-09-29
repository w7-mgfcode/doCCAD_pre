# ADR-004: Exact version pinning and a standing exit strategy

## Status
Accepted (2026-08-12)

## Context
Zensical is alpha software (PyPI "Development Status :: 3 - Alpha" [VERIFIED-REPO: pyproject.toml]) releasing several times per month (v0.0.48→v0.0.53 between 2026-07-07 and 2026-08-04 [VERIFIED-REPO: git log]). The core team is effectively two people (last-50-commit shortlog: Martin Donath, Timothée Mazzucotelli dominate [VERIFIED-REPO: git shortlog]). Only the latest version receives security fixes [VERIFIED-REPO: SECURITY.md]. Material for MkDocs remains maintained "at least 12 months" from 2025-11-05 [VERIFIED-OFFICIAL: FAQ] — a window that is nearly exhausted, with continuation unconfirmed [UNKNOWN].

## Decision
1. Pin `zensical==<exact>` in a lockfile/requirements with hash checking; CI never floats.
2. A monthly 30-minute upgrade ritual: read changelog, bump in a branch, rely on `--strict` build + link validation + HTML diff spot-check before merge.
3. Maintain a tested fallback CI job (`mkdocs build` with mkdocs-material pinned) as long as upstream maintains it; smoke-test the fallback quarterly.
4. Adoption of any Zensical-only feature that breaks mkdocs.yml compatibility requires a new ADR.

## Consequences
- Positive: reproducible builds; security-fix policy satisfied by the monthly bump; controlled exposure to breaking changes; a rehearsed exit in hours, not weeks.
- Negative: monthly maintenance overhead; fallback job costs CI minutes; the fallback decays once Material's maintenance window closes — at that point the exit becomes "pin last-good Zensical" or community fork (MIT permits) [VERIFIED-REPO: LICENSE.md].

## Alternatives
- Track latest automatically (Renovate auto-merge): too risky pre-1.0.
- Freeze on one version for a year: violates the latest-only security-fix policy.
- Vendor the wheel: unnecessary; PyPI + attestations suffice [VERIFIED-REPO: .github/workflows/build.yml attestation step].
