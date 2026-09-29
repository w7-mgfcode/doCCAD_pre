# ADR-005: Represent AI-derived views with a restricted native-block palette, no custom components

## Status
Proposed

## Context
The ecosystem produces derived views (recruiter pages, interview-prep sections, role-specific docs)
from canonical docs and wants a reusable presentation component (e.g., "InterviewPrep"). GitBook has
no MDX or author-defined components; its extension mechanism is platform-hosted integrations whose
ContentKit blocks render inside docs [VERIFIED-OFFICIAL] (renderer dependency
`@gitbook/react-contentkit` confirms the mechanism [VERIFIED-REPO]). Native blocks available via
Markdown include hints (`{% hint %}`), tabs, expandables, steppers, cards, code blocks, and fenced
`mermaid` diagrams [VERIFIED-OFFICIAL]. New files sync only when listed in `SUMMARY.md`
[VERIFIED-OFFICIAL].

## Decision
The generation pipeline emits derived pages using a fixed, versioned template library that maps each
logical component to a deterministic arrangement of native GitBook blocks (e.g., InterviewPrep =
intro paragraph + tabs per role + expandable Q&A items + hint for sources). Derived pages live in
dedicated `SUMMARY.md` groups ("AI-derived") and carry a `tags: [ai-derived]` frontmatter marker.
Every generation PR updates page files and `SUMMARY.md` atomically. Building a ContentKit
integration is explicitly deferred until a real rendering need cannot be met with native blocks.

## Consequences
- Zero platform extension code to maintain; templates are plain text transformations, testable in CI.
- Visual sophistication is capped at GitBook's native palette; acceptable for the target audience.
- Template versioning enables incremental regeneration (regenerate only pages whose template or
  source changed).
- The restricted palette keeps the ADR-004 exit converter small.

## Alternatives
- **ContentKit integration with a custom block**: richer UI, but adds a hosted-app dependency,
  GitBook-specific code, and review overhead — rejected for MVP (revisit if templates prove
  insufficient).
- **Pre-rendered HTML/images embedded in pages**: opaque to search and to the Markdown exit path;
  rejected.
- **Fork the GPLv3 renderer to add components**: heavy maintenance + copyleft implications, and only
  affects self-hosted rendering, not gitbook.io hosting; rejected.
