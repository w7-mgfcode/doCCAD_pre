---
id: security-trust-boundaries
slug: /security/trust-boundaries
title: Security Architecture & Trust Boundaries
type: canonical
audience: [architect, operator, developer]
owners: [security]
sources: [ai/router.py, scripts/validate_docs.py]
related: [security-prompt-injection-defense, architecture-ai-generation-plane]
ai_generation:
  allowed: true
  derived_pages: [interview]
last_validated: 2026-09-21
---

# Security Architecture & Trust Boundaries

<!-- Archive mapping: Adapted from 04_ARCHITECTURE/SAD/security_architecture.md -->

DOCCAD's security model is designed around a fundamental premise: **the published documentation is a static build artifact with zero runtime server footprint**. Attack vectors targeting live application servers, database injection, or serving-time LLM jailbreaking are eliminated by construction.

## The Six Trust Zones

DOCCAD divides the documentation lifecycle into six distinct trust zones:

```mermaid
flowchart TB
  subgraph Z0["Zone 0: Untrusted Input"]
    UQ[User special questions]
    XPR[External PRs]
    DEP[Third-party packages]
  end

  subgraph Z1["Zone 1: Repository"]
    SRC[Canonical docs source]
    GEN[Generated docs plane]
    CFG[Contracts, prompts, ai config]
  end

  subgraph Z2["Zone 2: CI Generation Plane"]
    CTX[Context assembly as delimited data]
    RTR[Provider router]
    GATE[Schema & link gates]
    SECRETS[Actions secrets]
  end

  subgraph Z3["Zone 3: Cloud Model Providers"]
    ANT[Anthropic API]
    GGL[Google API]
    OAI[OpenAI API]
  end

  subgraph Z4["Zone 4: Local Model"]
    LOC[Local OpenAI-compatible endpoint]
  end

  subgraph Z5["Zone 5: Build & Publish"]
    BLD[Docusaurus build]
    PAGES[Static Site / GitHub Pages]
  end

  UQ -->|Data only, never instructions| CTX
  XPR -->|Human review & branch protection| SRC
  DEP -->|Pinned SHAs & lockfiles| BLD
  CTX -->|Allowed public evidence| RTR
  RTR -->|Public tasks| Z3
  RTR -->|Private tasks hard-pinned| Z4
  Z3 -->|Candidate output| GATE
  Z4 -->|Candidate output| GATE
  GATE -->|Bot PR| GEN
  SRC --> BLD
  GEN --> BLD
  BLD --> PAGES
```

## Boundary Crossing Invariants

1. **Z0 -> Z2 (Input to Context)**: User questions enter prompts purely as delimited string data (`<<<EVIDENCE-DATA`).
2. **Z2 -> Z3 (CI to Cloud)**: Only content explicitly classified as public may be transmitted to cloud providers.
3. **Z2 -> Z4 (Private Tasks)**: Tasks marked `privacy: private` are hard-pinned to local execution. Cloud fallback is prohibited.
4. **Z3/Z4 -> Z1 (Model Output to Repo)**: Generated text must pass schema validation and is persisted only through PR branches requiring human review.
