# ADR-005: The repository is public-equivalent; the protect element is never used as access control

## Status
Proposed (2026-08-12)

## Context
Hyperbook's `protect` directive gates content behind a password client-side: the password ships base64-encoded in a `data-toast` attribute and the "protected" content is present in the HTML in a hidden div (verified: packages/markdown/src/remarkDirectiveProtect.ts). It is a pedagogical pacing device, not security. The target ecosystem may hold recruiter-sensitive or candidate-specific material, and a static host serves everything it is given. There is no server-side auth anywhere in the static platform (Hyperbook Cloud is a separate student-data backend, out of scope).

## Decision
Treat the content repository and the published site as public-equivalent. Policy, enforced in contributor docs and PR checklist: no credentials, no personal data beyond what is deliberately published, no confidential company information, in canonical or derived content. `protect` may be used only for presentation purposes (e.g., "spoiler" hiding of interview answers) with the explicit understanding that the content is fully visible in page source. If genuinely restricted views are ever required, they are served from a separate access-controlled host (e.g., Pages behind an auth proxy or a private deployment), not by the `protect` element. CI runs a secret scanner (e.g., gitleaks) on every PR including AI-generated ones.

## Consequences
- Eliminates the most likely human-error security incident class for this platform.
- Interview-answer hiding remains available as UX (protect/collapsible) without security claims.
- A future "private recruiter view" requirement triggers an explicit architecture change (auth proxy or second private site) rather than silent misuse.
- Secret scanning adds negligible CI time and also guards AI output.

## Alternatives
- Rely on protect passwords for sensitive sections: rejected — verifiably not security.
- Encrypt sensitive pages client-side (e.g., staticrypt-style): rejected for now — added complexity contradicts the anti-overengineering rule and the current content model has no confirmed private-content requirement.
