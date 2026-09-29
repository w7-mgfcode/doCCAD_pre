# AI Model Documentation Suite — Conventions & Chapter Template

Date basis: 2026-08. HARD RULES for every author (human or agent):

1. **Web-verified currency.** The commissioning directive lists historical model names (GPT-4.1/4o,
   Gemini 2.0/1.5, Claude 3.5/3). Those are EXAMPLES from an earlier landscape. Document what is CURRENT
   per the provider's official docs at access time. List legacy/deprecated families in a "Legacy &
   migration" subsection only.
2. **Citations with access dates.** Every factual block (model list, pricing, limits, regions) cites the
   official doc URL + access date. End each chapter with a Sources list.
3. **No invention.** Pricing, rate limits, SLAs, region availability: official numbers or `[UNVERIFIED —
   not published / not found]`. Never guess. Third-party figures are labeled as such.
4. **Volatility warning.** Each chapter opens with: "Model lineups and pricing change frequently.
   Verified against official documentation on <date>. Re-verify before production decisions."
5. **Code that would run.** SDK/REST examples must match current official API shapes; mark any example you
   could not verify against docs. Placeholders like `$API_KEY` only — never realistic-looking keys.
6. **Terminology.** "Context window" (tokens), "output limit", "input/output pricing per 1M tokens",
   "modalities in/out", "structured output" (JSON schema), "tool use" (function calling), "batch API".

## Mandatory chapter structure (every provider)

```
# <N>. <Provider>
> Volatility warning + access date
N.1 Platform overview & positioning
N.2 Current model catalog        ← table: model id, family, context, output limit, modalities in/out,
                                    tool use, structured output, fine-tuning, price in/out per 1M
N.3 Model details & limitations  ← per family: capabilities, limits, known constraints
N.4 Embedding / audio / vision / video models
N.5 Pricing model & cost notes   ← incl. caching/batch discounts if offered
N.6 Authentication & environment ← keys/env vars; OAuth/IAM where applicable
N.7 API endpoints & schemas      ← base URLs, main endpoints, request/response JSON schema, versioning
N.8 SDK integration              ← Python + JavaScript minimal-complete examples; curl
N.9 Streaming, tool use, structured output examples
N.10 Error handling & retry      ← error codes table, retry/backoff pattern
N.11 Rate limits & quotas
N.12 Fine-tuning & customization
N.13 RAG & embedding pipeline notes
N.14 Agent support               ← official agent SDKs/frameworks, MCP support
N.15 Deployment patterns         ← serverless / container / managed; provider-specific notes
N.16 Region availability & data residency
N.17 Security, compliance & SLA  ← only documented certifications/SLAs
N.18 Legacy models & migration notes
N.19 Task-suitability verdict    ← what this provider's models are best/worst at (evidence-based)
N.20 Sources
```

## Structured sidecar (mandatory)

Each chapter emits `providers/<provider>.models.json`:
```json
{"provider":"...","accessed":"2026-08-14","models":[
 {"id":"...","family":"...","tier":"frontier|mid|small|embedding|audio|vision|video",
  "context_tokens":0,"max_output_tokens":0,"modalities_in":[],"modalities_out":[],
  "tool_use":true,"structured_output":true,"fine_tuning":false,
  "price_in_per_1m":0.0,"price_out_per_1m":0.0,"price_notes":"","currency":"USD",
  "open_weights":false,"local_capable":false,"regions_note":"","best_for":[],"avoid_for":[],
  "source_url":"","confidence":"HIGH|MEDIUM|LOW"}]}
```
Prices `null` when unpublished — never 0 for unknown.

## Style
Extremely technical, no marketing language, tables for enumerable facts, code blocks for integration,
ASCII diagrams where structure helps. Consistent heading depth. English.
