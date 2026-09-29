# AI Model Documentation Suite — Table of Contents

Multi-vendor, developer-ready reference. Verified against official documentation 2026-08-14; model
lineups and pricing change frequently — re-verify before production decisions. Scope: currently
available, practically usable models only; legacy families appear only in per-chapter migration notes.

## Part I — Foundations
0. Conventions, evidence rules, terminology (00_CONVENTIONS.md)
1. This table of contents
2. How to read the catalogs: pricing units, context vs output limits, modality notation

## Part II — Provider Chapters (each follows the 20-section template in 00_CONVENTIONS.md)
3. OpenAI — platform, current model catalog, embeddings/audio/vision, API + SDKs, limits, deployment
4. Google Gemini (AI Studio / Gemini API) — incl. Gemma open models
5. Anthropic Claude — Messages API, tool use, agent SDK/MCP
6. AWS Bedrock — multi-vendor managed models (Anthropic, Meta, Mistral, Cohere, Amazon own-brand …)
7. Azure AI Foundry — OpenAI models on Azure + model catalog (Phi, Llama, Mistral …)
8. OpenRouter — aggregation layer: routing, unified API, pricing model, dynamic model catalog
9. Ollama — local inference: hardware realities, quantization, current usable open-weight lineup
10. Hugging Face — Inference API/Endpoints, Transformers, TGI, Spaces

Each provider chapter contains: current model catalog table · capabilities & limitations · pricing ·
context/output limits · multimodal support · fine-tuning · embedding/audio/vision models · agent support ·
RAG notes · deployment options · authentication · endpoints & schemas · Python/JS/curl examples ·
streaming · tool use / structured output · error handling & retry · rate limits · region availability ·
security/compliance/SLA (documented only) · legacy & migration · task-suitability verdict · sources.

## Part III — Cross-Provider Integration Blueprints
11. Provider-agnostic client patterns: env config, thin adapters, fallback chains
12. Retry, timeout, and streaming patterns (Python + JS)
13. Tool use / function calling across providers — schema differences table
14. RAG pipeline blueprint (embeddings → store → retrieve → ground) with per-provider slots
15. Agent patterns and MCP: what each provider officially supports
16. Vision & audio pipelines
17. Local inference setup (Ollama, HF TGI) incl. Docker
18. Deployment: containers, serverless (Lambda / Cloud Run), managed endpoints
19. Monitoring, logging, cost optimization (caching, batching, routing by tier)
20. Security & compliance across providers: keys, data-usage policies, residency

## Part IV — Unified Model Selection Guide
21. Master comparison matrix (all providers, from structured model data)
22. Task-type suitability map: classification · summarization · reasoning · coding · agents ·
    multimodal · RAG · embeddings · speech · vision
23. Price/performance ranking by tier (budget / mid / premium reasoning)
24. Selection dimensions: latency · context window · accuracy · local vs cloud · compliance · region ·
    open-source vs frontier
25. Decision trees ("If your use case is X, choose Y") — ASCII
26. Avoid-lists ("Avoid these models for X") — evidence-based warnings
27. Scorecards & tradeoff analysis (incl. ASCII spider profiles)
28. Migration & versioning strategy across providers

## Part V — Appendices
A. Structured model data (providers/*.models.json — machine-readable)
B. Master source register with access dates
C. Glossary


---


# 2. How to Read the Catalogs

Pricing is quoted in USD per 1M tokens (input/output separately) as published on the access date; `n/p` /
`null` means not published — never assume free. "Context window" = maximum input tokens; "output limit" =
maximum generated tokens per request; some providers meter long-context surcharges above thresholds (noted
per chapter). Modality notation: `in: text,image,audio` / `out: text` describes what a model accepts and
produces. Every factual block carries an official-source citation with access date 2026-08-14; items the
authors could not verify are marked `[UNVERIFIED]`, third-party figures are labeled, and each chapter opens
with a volatility warning. The machine-readable catalog behind all comparison tables is
`providers/*.models.json` (195 models); regenerate the master tables with `scripts/build_matrix.py`.


---

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


---

# 3. OpenAI

> **Volatility warning.** Model lineups and pricing change frequently. Verified against official
> documentation on **2026-08-14**. Re-verify before production decisions.
>
> Note on doc URLs: `platform.openai.com/docs/...` now 302-redirects to `developers.openai.com/api/docs/...`
> (observed 2026-08-14). Citations below use the post-redirect host.

## 3.1 Platform overview & positioning

OpenAI's API platform (api.openai.com) centers on the **GPT-5.6 family** — three tiers named
**Sol** (frontier), **Terra** (balanced), **Luna** (small/high-volume) — launched July 9, 2026, all with a
~1.05M-token context window and unified reasoning-effort control. The **Responses API** is the primary
interface ("recommended for all new projects"); Chat Completions remains supported; the Assistants API
shuts down **2026-08-26**. Adjacent products: Agents SDK (Python/TS), Realtime API (GA), gpt-image-2,
Batch API, and a specialized cybersecurity line (gpt-5.6-cyber, Daybreak). Notable 2026 strategic shifts:
the self-serve **fine-tuning platform is winding down** (closed to new users), and the **Sora/video API is
being shut down** (2026-09-24) with no announced replacement.
Sources: https://developers.openai.com/api/docs/models (2026-08-14);
https://openai.com/index/gpt-5-6/ (2026-08-14);
https://developers.openai.com/api/docs/guides/migrate-to-responses (2026-08-14);
https://developers.openai.com/api/docs/deprecations (2026-08-14).

## 3.2 Current model catalog

Prices = USD per 1M tokens, standard tier, **short-context** rate (≤272K input tokens; above that: 2× input,
1.5× output for the GPT-5.6 trio). Pricing page accessed 2026-08-14. See §3.5 for the pricing-page vs
model-page discrepancy on the 5.6 trio (July 2026 price drop; model detail pages still showed pre-drop
figures at access time — flagged MEDIUM confidence).

| Model id | Family/tier | Context | Max out | Modalities in→out | Tools | Struct. out | FT | $ in / out per 1M |
|---|---|---|---|---|---|---|---|---|
| `gpt-5.6-sol` (alias `gpt-5.6`) | GPT-5.6 frontier | 1,050,000 | 128,000 | text+image→text | yes | yes | no | 2.50 / 15.00 |
| `gpt-5.6-terra` | GPT-5.6 mid | 1,050,000 | 128,000 | text+image→text | yes | yes | no | 1.00 / 6.00 |
| `gpt-5.6-luna` | GPT-5.6 small ("nano-tier") | 1,050,000 | 128,000 | text+image→text | yes | yes | no | 0.10 / 0.60 |
| `gpt-5.6-cyber` | cybersecurity | [UNVERIFIED] | [UNVERIFIED] | text→text | yes | yes | no | 12.50 / 75.00 |
| `daybreak-red-latest` / `daybreak-blue-latest` | cybersecurity (offense/defense) | [UNVERIFIED — limited access] | — | text→text | — | — | — | [UNVERIFIED — not published] |
| `gpt-5.3-codex` | agentic coding | 400,000 | 128,000 | text+image→text | yes | yes | no | 1.75 / 14.00 |
| `chat-latest` | ChatGPT-parity chat | [UNVERIFIED] | — | text→text | — | — | no | 5.00 / 30.00 |
| `text-embedding-3-large` | embedding | 8,192 in | 3,072 dims | text→vector | n/a | n/a | no | 0.13 / n/a |
| `text-embedding-3-small` | embedding | 8,192 in | 1,536 dims | text→vector | n/a | n/a | no | 0.02 / n/a |
| `gpt-realtime-2.1` | realtime speech | [UNVERIFIED] | — | audio+text→audio+text | yes | — | no | audio 32 / 64; text 4 / 24 |
| `gpt-realtime-2.1-mini` | realtime speech mini | [UNVERIFIED] | — | audio+text→audio+text | yes | — | no | audio 10 / 20; text 0.60 / 2.40 |
| `gpt-realtime-translate` | realtime translation | — | — | audio→audio/text | — | — | no | $0.034 / min |
| `gpt-live-transcribe` | streaming STT | — | — | audio→text | — | — | no | $0.017 / min |
| `gpt-realtime-whisper` | realtime STT | — | — | audio→text | — | — | no | $0.017 / min |
| `gpt-transcribe` | batch STT | — | — | audio→text | — | — | no | $0.0045 / min |
| `gpt-4o-transcribe` / `-mini-transcribe` | STT (token-priced) | — | — | audio→text | — | — | no | 2.50/10.00 ; 1.25/5.00 |
| `gpt-4o-mini-tts` | TTS | — | — | text→audio | — | — | no | [UNVERIFIED — not on current pricing page] |
| `gpt-audio-1.5` | audio chat (replaces gpt-audio/gpt-4o-audio) | [UNVERIFIED] | — | audio+text→audio+text | — | — | no | [UNVERIFIED] |
| `gpt-image-2` (snapshot `gpt-image-2-2026-04-21`) | image gen/edit | n/a | n/a | text+image→image | no | no | no | text in 5.00; image in 8.00; image out 30.00 |
| `sora-2` / `sora-2-pro` | video (SUNSET 2026-09-24) | n/a | n/a | text→video | no | no | no | $0.10–0.70 / sec by res. |
| `omni-moderation-latest` | moderation | n/a | n/a | text+image→scores | n/a | n/a | no | free |
| `o4-mini-2025-04-16` | RFT fine-tuning base only | 200,000* | — | text→text | yes | yes | RFT | 4.00 / 16.00 (+$100/hr training) |

\* o4-mini context from prior-generation docs, not re-verified 2026-08-14.
Sources: https://developers.openai.com/api/docs/models, /models/gpt-5.6-sol, /models/gpt-5.6-terra,
/models/gpt-5.6-luna, /models/gpt-5.3-codex, /models/gpt-image-2, /api/docs/pricing,
/api/docs/guides/embeddings, /api/docs/guides/moderation, /api/docs/guides/fine-tuning (all 2026-08-14).

## 3.3 Model details & limitations

### GPT-5.6 family (Sol / Terra / Luna)
- Context **1,050,000 tokens**, max output **128,000**, knowledge cutoff **2026-02-16** (all three).
- Input: text + image. Output: text only. **No audio/video I/O** in these models (use Realtime/audio models).
- Reasoning effort levels: `none, low, medium (default), high, xhigh, max`.
- Long-context surcharge: requests **>272K input tokens** bill at 2× input / 1.5× output.
- **Fast mode** (Sol): 2× standard rates for lower latency (pricing page, 2026-08-14; announced with the
  July 2026 Terra/Luna price drop — https://community.openai.com/t/1388484).
- Fine-tuning **not supported** on any 5.6 model.
- Positioning per docs: Sol = "strongest capability for complex coding, computer use, research, and
  cybersecurity"; Terra = "balances intelligence and cost", "performance competitive with GPT-5.5 at a
  lower cost"; Luna = "cost-sensitive, high-volume workloads", nano-tier successor.
  Sources: model pages above + https://learn.chatgpt.com/docs/models (Codex models page, 2026-08-14).

### gpt-5.3-codex
Agentic coding model ("most capable agentic coding model to date"); 400K context, 128K out, cutoff
2025-08-31; reasoning `low..xhigh`; requires ≥ Tier 1 (not on free tier). A `gpt-5.3-codex-spark`
research preview exists in the Codex product (ChatGPT Pro only, not general API).
Sources: https://developers.openai.com/api/docs/models/gpt-5.3-codex; https://learn.chatgpt.com/docs/models (2026-08-14).

### Cybersecurity line
`gpt-5.6-cyber` (API, $12.50/$75.00, short-context only) plus `daybreak-red-latest` /
`daybreak-blue-latest` (offensive/defensive security). Access conditions and specs beyond the catalog
listing: [UNVERIFIED — gated/limited documentation]. Source: https://developers.openai.com/api/docs/models (2026-08-14).

### chat-latest
ChatGPT-parity conversational model exposed to the API ($5.00/$30.00). Family/version binding and specs:
[UNVERIFIED — pricing page listing only]. Source: https://developers.openai.com/api/docs/pricing (2026-08-14).

## 3.4 Embedding / audio / vision / video models

- **Embeddings**: `text-embedding-3-small` (1536 dims default) and `-large` (3072 dims); max input 8,192
  tokens; native Matryoshka-style `dimensions` parameter (docs recommend it over manual truncation +
  L2-norm). No newer embedding generation documented as of 2026-08-14.
  Source: https://developers.openai.com/api/docs/guides/embeddings (2026-08-14).
- **Vision**: no standalone vision models; image input is native to GPT-5.6 trio and gpt-5.3-codex.
- **Audio/Realtime**: see §3.2 table; `gpt-realtime-2.1` is the recommended voice-agent model;
  `gpt-audio-1.5` replaces `gpt-audio`/`gpt-4o-audio` (legacy shut down 2027-01-20).
  Sources: /api/docs/guides/realtime; /api/docs/deprecations (2026-08-14).
- **Image**: `gpt-image-2` (gen + edit, token-priced; per-image effective cost varies by size/quality).
- **Video**: `sora-2`/`sora-2-pro` still billed per-second but the **Videos API shuts down 2026-09-24 with
  no replacement listed** — do not build on it.
  Sources: /api/docs/deprecations (2026-08-14); corroboration https://pixo.video/blog/sora-api-still-available (third-party, 2026-08-14).

## 3.5 Pricing model & cost notes

Canonical: https://developers.openai.com/api/docs/pricing (2026-08-14).

- **Short vs long context**: ≤272K input tokens = base rate; above = 2× input / 1.5× output (5.6 trio).
- **Prompt caching**: cached input billed at **0.1× input rate**. GPT-5.6+: cache **writes billed at
  1.25× input rate** (total, not additive), fixed **30-min TTL** (`prompt_cache_options.ttl`), min
  cacheable prefix 1,024 tokens; older models (gpt-5.5/5.4/5.1/4.1): no write charge documented,
  optional retention up to **24 h** (`prompt_cache_retention`), `prompt_cache_key` for cache routing
  (keep ≤~15 req/min per key). Source: /api/docs/guides/prompt-caching (2026-08-14).
- **Batch API**: flat **50% discount**, 24 h window (see §3.7).
- **Fast mode** (Sol): 2× standard rates.
- **Regional processing**: +10% uplift for data-residency-eligible models released on/after 2026-03-05.
- **Tool billing** (Responses built-ins): web search $10/1k calls (+model tokens); web search preview
  $25/1k calls; file search $2.50/1k calls + $0.10/GB-day storage; containers (code interpreter/shell)
  $0.03–$1.92 per 20-min session; ChatKit storage $0.10/GB-day (1 GB free).
- **Discrepancy flag**: model detail pages (Sol $5/$30, Terra $2/$12, Luna $0.20/$1.20) did not reflect
  the July 2026 price drop shown on the pricing page (Sol $2.50/$15, Terra $1/$6, Luna $0.10/$0.60
  short-context) at access time. Treat exact 5.6 pricing as MEDIUM confidence; re-verify.

## 3.6 Authentication & environment

- API key header: `Authorization: Bearer $OPENAI_API_KEY`; official SDKs read env var `OPENAI_API_KEY`.
- Optional scoping headers: `OpenAI-Organization`, `OpenAI-Project`; project-scoped keys (`sk-proj-...`
  format) are the default key type. Admin/service-account keys managed in the dashboard.
- No OAuth/IAM for the core API; SSO/SCIM exist at the org-management level (enterprise).
  Source: https://developers.openai.com/api/reference (auth section, 2026-08-14). [Key-format detail:
  carried from prior docs, not re-verified 2026-08-14.]

## 3.7 API endpoints & schemas

Base URL `https://api.openai.com/v1`. No date-based API versioning; models are versioned via snapshots.

| Endpoint | Purpose | Status |
|---|---|---|
| `POST /v1/responses` | Primary text/multimodal generation, tools, agents | **Recommended** |
| `POST /v1/chat/completions` | Legacy-style chat generation | Supported, not deprecated |
| `POST /v1/embeddings` | Embeddings | Current |
| `POST /v1/images/generations`, `/v1/images/edits` | gpt-image-2 | Current |
| `GET/POST /v1/conversations` | Server-side conversation state | Current (Assistants successor) |
| `POST /v1/realtime/client_secrets` + WebRTC/WS/SIP `/v1/realtime` | Realtime API (GA; no more `OpenAI-Beta: realtime=v1`) | Current |
| `POST /v1/audio/transcriptions`, `/v1/audio/speech` | STT / TTS | Current |
| `POST /v1/moderations` | omni-moderation-latest (free) | Current |
| `POST /v1/batches` + `/v1/files` | Batch API (JSONL) | Current |
| `POST /v1/fine_tuning/jobs` | Fine-tuning | **Winding down** (closed to new users) |
| `/v1/assistants`, `/v1/threads` | Assistants API | **Shutdown 2026-08-26** |
| `/v1/videos` | Sora video | **Shutdown 2026-09-24** |

Responses request (minimal): `{"model": "...", "input": "<string or item array>", "instructions": "...",
"reasoning": {"effort": "none|low|medium|high|xhigh|max"}, "store": true|false, "previous_response_id": "..."}`.
Response carries a typed `output` array of items (`message`, `reasoning`, `function_call`,
`function_call_output`, tool items); SDKs expose the convenience field `output_text`. Responses are
**stored by default** — set `"store": false` for stateless/ZDR operation.
Batch JSONL line: `{"custom_id": "...", "method": "POST", "url": "/v1/responses", "body": {...}}`; ≤50,000
requests/batch, ≤200 MB input file, output retained 30 days, separate token pool.
Sources: /api/docs/guides/migrate-to-responses; /api/docs/guides/batch; /api/docs/guides/realtime (2026-08-14).

## 3.8 SDK integration

Python (`pip install openai`):
```python
from openai import OpenAI

client = OpenAI()  # reads OPENAI_API_KEY
resp = client.responses.create(
    model="gpt-5.6-terra",
    instructions="You are a terse technical assistant.",
    input="Summarize RFC 9110 section 9 in 3 bullets.",
    reasoning={"effort": "low"},
)
print(resp.output_text)
```

JavaScript (`npm install openai`):
```js
import OpenAI from "openai";
const client = new OpenAI();
const resp = await client.responses.create({
  model: "gpt-5.6-luna",
  input: "Give me one haiku about TCP retransmission.",
});
console.log(resp.output_text);
```

curl:
```bash
curl https://api.openai.com/v1/responses \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-5.6-terra", "input": "ping"}'
```
Shapes match /api/docs/guides/migrate-to-responses and /api/docs/guides/structured-outputs (2026-08-14).
`reasoning.effort` value set verified on model pages; exact wire name carried from GPT-5-era Responses
reference [not re-verified 2026-08-14].

## 3.9 Streaming, tool use, structured output examples

Streaming (SSE; semantic events, e.g. `response.output_text.delta`, `response.completed`):
```python
with client.responses.stream(model="gpt-5.6-terra", input="Count to 5.") as stream:
    for event in stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="")
```

Tool use (function calling; note top-level `name` on Responses tools, `strict` schemas):
```python
tools = [{
    "type": "function",
    "name": "get_weather",
    "description": "Get current weather for a city",
    "parameters": {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"],
        "additionalProperties": False,
    },
    "strict": True,
}]
r1 = client.responses.create(model="gpt-5.6-sol", input="Weather in Oslo?", tools=tools)
call = next(i for i in r1.output if i.type == "function_call")
r2 = client.responses.create(
    model="gpt-5.6-sol",
    previous_response_id=r1.id,
    input=[{"type": "function_call_output", "call_id": call.call_id, "output": '{"temp_c": 14}'}],
    tools=tools,
)
```
Built-in tools (no user execution loop): `web_search`, `file_search`, `code_interpreter`, `computer_use`,
`image_generation`, hosted shell, apply_patch, skills, MCP (`{"type": "mcp", ...}`).

Structured output (Responses API — schema lives under `text.format`, NOT `response_format`):
```python
resp = client.responses.create(
    model="gpt-5.6-terra",
    input=[{"role": "user", "content": "solve 8x + 7 = -23"}],
    text={"format": {
        "type": "json_schema",
        "name": "math_response",
        "schema": MathResponse.model_json_schema(),
        "strict": True,
    }},
)
```
Sources: /api/docs/guides/structured-outputs; /api/docs/guides/migrate-to-responses (2026-08-14).
Streaming event names cross-checked against Realtime GA naming (`response.output_text.delta`); full event
list [not exhaustively re-verified].

## 3.10 Error handling & retry

| HTTP | Meaning | Action |
|---|---|---|
| 400 | invalid_request_error (bad schema/params) | Fix request; no retry |
| 401 | invalid API key / org | Fix credentials |
| 403 | unsupported region / permission | No retry |
| 404 | model or object not found | Check model id vs §3.2 |
| 409 / 429 | conflict / `rate_limit_exceeded`, `insufficient_quota` | Backoff per `Retry-After` header |
| 500 / 503 | server error / overloaded | Exponential backoff + jitter, idempotent retry |

Rate-limit headers: `x-ratelimit-{limit,remaining,reset}-{requests,tokens}` (+ project-scoped variants),
`Retry-After`. SDK default: automatic retries (2) with backoff; set `max_retries` on client. Distinguish
`rate_limit_exceeded` (transient) from `insufficient_quota` (billing — do not retry).
Source: /api/docs/guides/rate-limits (2026-08-14). [Error-code table shape carried from API reference;
codes not individually re-verified.]

## 3.11 Rate limits & quotas

Automatic spend-based tiers (org-level; limits are per model per org, RPM/TPM/RPD/TPD/IPM — first
exhausted metric blocks):

| Tier | Qualification | Monthly usage cap |
|---|---|---|
| Free | eligible geography | $100 |
| Tier 1 | $5 paid | $100 |
| Tier 2 | $50 paid | $500 |
| Tier 3 | $100 paid | $1,000 |
| Tier 4 | $250 paid | $5,000 |
| Tier 5 | $1,000 paid | $200,000 |

Per-model RPM/TPM matrices for GPT-5.6 per tier: shown per-model in dashboard/model pages
[UNVERIFIED — not captured here; check platform limits page]. Batch API has a separate queued-token pool
(active batches count; completed do not). gpt-5.3-codex requires ≥Tier 1.
Source: https://developers.openai.com/api/docs/guides/rate-limits (2026-08-14).

## 3.12 Fine-tuning & customization

**Status change (major): OpenAI is winding down the self-serve fine-tuning platform** — "no longer
accessible to new users"; existing users retain access "for the coming months". No GPT-5.x model is
fine-tunable. Remaining documented options (existing users):

| Method | Base models | Price |
|---|---|---|
| SFT / DPO | `gpt-4.1-2025-04-14`, `gpt-4.1-mini-...`, `gpt-4.1-nano-...` | [UNVERIFIED — removed from current pricing page] |
| Vision SFT | `gpt-4o-2024-08-06` | [UNVERIFIED] |
| RFT (reasoning) | `o4-mini-2025-04-16` | $100/hr training; usage $4/$16 per 1M ($2/$8 with data sharing) |

Alternative customization path per docs: prompt engineering + Responses `instructions`, structured
outputs, retrieval (file search), and (enterprise) custom-model programs.
Sources: /api/docs/guides/fine-tuning; /api/docs/pricing (2026-08-14).

## 3.13 RAG & embedding pipeline notes

- `text-embedding-3-large` with `dimensions` (e.g. 1024/256) is the documented cost/recall dial;
  shortened-large outperforms full ada-002. Normalize (L2) only if truncating manually.
- Max 8,192 tokens per embedding input; batch via array `input`; Batch API supports `/v1/embeddings`
  (≤50,000 inputs per batch) at the 50% discount.
- Managed alternative: Responses **file_search** tool (vector stores, $0.10/GB-day + $2.50/1k calls)
  removes the self-hosted vector DB but note vector stores are **ZDR-ineligible** (§3.16).
Sources: /api/docs/guides/embeddings; /api/docs/pricing; /api/docs/guides/your-data (2026-08-14).

## 3.14 Agent support

- **Agents SDK**: Python `openai-agents` (github.com/openai/openai-agents-python) and TypeScript
  (`openai/openai-agents-js`). Concepts: agent definitions, runner loop with streaming, **handoffs**
  (multi-agent), **guardrails** (I/O validation, human-approval/resumable flows), **sessions** (state),
  **tracing** (model/tool/agent spans), sandboxed execution.
- **MCP**: first-class — remote MCP servers attachable as tools in the Responses API and Agents SDK.
- **Hosted tools**: web search, file search, computer use, code interpreter, hosted shell, apply_patch,
  skills, image generation.
- **AgentKit/ChatKit**: ChatKit = embeddable chat UI + widgets ($0.10/GB-day storage); Agent Builder is
  legacy with migration guides.
Source: https://developers.openai.com/api/docs/guides/agents (2026-08-14).

## 3.15 Deployment patterns

- API-only (no self-hosted current models; `gpt-oss` open-weight line from 2025 not present in the current
  catalog page — status [UNVERIFIED]). Standard pattern: server-side proxy holding the key; never ship
  keys to clients. Realtime uses **ephemeral client secrets** (`POST /v1/realtime/client_secrets`) so
  browsers/mobile connect via WebRTC without the master key; SIP for telephony.
- Throughput classes: standard, **fast mode** (2×, Sol), **Batch** (50%, 24 h), **Scale Tier** (reserved
  TPM units, 30-day minimum) and priority processing for latency-critical workloads.
- Azure: the GPT-5.6 family is also deployable via **Microsoft Foundry (Azure)** with Azure-side SLA/quota
  mechanics — see the Azure chapter for detail.
  (https://azure.microsoft.com/en-us/blog/gpt-5-6-now-available-in-microsoft-foundry/, 2026-08-14).
Sources: /api/docs/guides/realtime; /api/docs/pricing; https://openai.com/api-scale-tier/ (2026-08-14).

## 3.16 Region availability & data residency

- Single global API endpoint; no self-selectable serving regions in the standard tier.
- **Data residency** (approved customers): storage/processing configurable for US, Europe, UK, Canada,
  Australia, Japan, India, Singapore, South Korea, UAE. Most non-US regions require approval and a
  Modified Retention amendment. Regional processing endpoints: +10% price uplift (models released ≥
  2026-03-05 that are residency-eligible).
Sources: /api/docs/guides/your-data; /api/docs/pricing (2026-08-14).

## 3.17 Security, compliance & SLA

- **Data usage**: API data is **not used for training by default** (opt-in only).
- **Retention**: abuse-monitoring logs ≤30 days (longer if legally required). Stateless-by-default
  endpoints: chat completions (`store:false`), responses (`store:false`), images, embeddings. Stored-until-
  deleted: conversations, files, vector stores. **ZDR** (approval required): forces `store:false`;
  assistants/threads/vector stores/video endpoints ineligible. Middle option: **Modified Abuse
  Monitoring**. Source: /api/docs/guides/your-data (2026-08-14).
- **SLA**: no published uptime SLA for the standard pay-as-you-go API (status page: status.openai.com).
  **Scale Tier** (reserved capacity) carries a **99.9% uptime SLA** plus latency commitments
  (e.g. "99% > 50 tok/s" older large models, "99% > 100 tok/s" smaller models) — note the Scale Tier page
  still listed pre-5.6 models at access time. Source: https://openai.com/api-scale-tier/ (2026-08-14).
- **Certifications**: SOC 2 Type 2, CSA STAR, ISO 27001 historically claimed at trust.openai.com
  [UNVERIFIED on 2026-08-14 — re-check trust portal].

## 3.18 Legacy models & migration notes

| Legacy | Shutdown | Migrate to |
|---|---|---|
| Assistants API | **2026-08-26** | Responses + Conversations APIs |
| `sora-2` / Videos API | 2026-09-24 | none listed |
| `gpt-3.5-turbo` | 2026-10-23 | `gpt-5.6-terra` |
| `gpt-4-0613` | 2026-10-23 | `gpt-5.6-sol` |
| `o1-2024-12-17` | 2026-10-23 | `gpt-5.6-sol` |
| `gpt-5-2025-08-07` | 2026-12-11 | `gpt-5.6-sol` |
| `gpt-5-mini-2025-08-07` | 2026-12-11 | `gpt-5.6-terra` |
| `gpt-5-nano-2025-08-07` | 2026-12-11 | `gpt-5.6-luna` |
| `o3-2025-04-16` | 2026-12-11 | `gpt-5.6-sol` |
| `gpt-realtime`, `gpt-audio`, `gpt-4o-audio` | 2027-01-20 | `gpt-realtime-2.1` / `gpt-audio-1.5` |
| DALL-E 2/3 | done (2026-05-12) | `gpt-image-2` |
| `gpt-4.5-preview`, `o1-preview` | done (2025) | — |

Still serving but superseded (no announced API shutdown as of 2026-08-14): `gpt-5.5`, `gpt-5.4`,
`gpt-5.4-mini`, `gpt-5.2`, `gpt-5.1`, `gpt-4.1` family, `gpt-4o` snapshots, `o4-mini` (evidence:
prompt-caching guide, Scale Tier page, fine-tuning guide, Codex product page — the Codex *product*
retires GPT-5.4 models 2026-08-31). Migration mechanics: Chat Completions → Responses (§3.7);
`response_format` → `text.format`; Assistants threads → Conversations.
Source: https://developers.openai.com/api/docs/deprecations (2026-08-14).

## 3.19 Task-suitability verdict

- **Best**: agentic coding & computer use (Sol, gpt-5.3-codex — Responses hosted shell/apply_patch);
  long-context work (1.05M window across all price tiers — unusual: even the $0.10 Luna tier);
  voice agents (Realtime GA, WebRTC/SIP, dedicated translate/transcribe models); high-volume cheap
  inference (Luna + batch + caching ⇒ $0.05/1M batched input); image gen/edit (gpt-image-2).
- **Weak / avoid**: fine-tuning-dependent products (platform winding down, no 5.6 FT); video generation
  (API shutting down); audio output from flagship text models (not supported — separate audio models);
  strict on-prem/self-hosting (no current open-weight in catalog); uptime-SLA-required workloads without
  Scale Tier spend; anything on Assistants API (12 days to shutdown at access date).
- Cost watch-outs: >272K-input requests silently cost 2×/1.5×; Sol fast mode 2×; GPT-5.6 cache writes 1.25×.

## 3.20 Sources

All accessed **2026-08-14**:
1. https://developers.openai.com/api/docs/models (+ /gpt-5.6-sol, /gpt-5.6-terra, /gpt-5.6-luna, /gpt-5.3-codex, /gpt-image-2)
2. https://developers.openai.com/api/docs/pricing
3. https://developers.openai.com/api/docs/deprecations
4. https://developers.openai.com/api/docs/guides/rate-limits
5. https://developers.openai.com/api/docs/guides/migrate-to-responses
6. https://developers.openai.com/api/docs/guides/structured-outputs
7. https://developers.openai.com/api/docs/guides/prompt-caching
8. https://developers.openai.com/api/docs/guides/batch
9. https://developers.openai.com/api/docs/guides/fine-tuning
10. https://developers.openai.com/api/docs/guides/realtime
11. https://developers.openai.com/api/docs/guides/moderation
12. https://developers.openai.com/api/docs/guides/embeddings
13. https://developers.openai.com/api/docs/guides/agents
14. https://developers.openai.com/api/docs/guides/your-data
15. https://openai.com/index/gpt-5-6/ ; https://openai.com/api-scale-tier/
16. https://learn.chatgpt.com/docs/models (Codex models)
17. https://azure.microsoft.com/en-us/blog/gpt-5-6-now-available-in-microsoft-foundry/
18. Third-party corroboration (labeled): community.openai.com/t/1384931 & /t/1388484 (launch, price drop);
    venturebeat.com (GPT-5.6 preview); pixo.video (Sora API sunset).


---

# 4. Google Gemini API / AI Studio

> **Volatility warning.** Model lineups and pricing change frequently. Everything below was verified
> against official documentation at https://ai.google.dev/gemini-api/docs on **2026-08-14**. Several
> promotional prices expire 2026-12-31. Re-verify before production decisions.

## 4.1 Platform overview & positioning

The Gemini API (a.k.a. "Gemini Developer API") is Google's direct, API-key-based access path to the
Gemini model family, managed through **Google AI Studio** (https://aistudio.google.com). It exposes
first-party frontier models (Gemini 3.x), the previous 2.5 generation, native image generation
("Nano Banana" line), video generation (Veo), TTS/Live audio models, music (Lyria), embeddings, and
hosted **Gemma 4** open-weight models — all behind one key and one base URL
(`https://generativelanguage.googleapis.com`). Two request surfaces coexist in 2026: the classic
`models/*:generateContent` REST family and the newer **Interactions API** (`POST /v1beta/interactions`),
which is GA and is what Google now recommends "for access to all the latest features and models"
(https://ai.google.dev/gemini-api/docs/text-generation, accessed 2026-08-14). An OpenAI-compatibility
endpoint is also offered (beta).

**AI Studio vs Vertex AI (one paragraph).** The same Gemini models are separately available on
**Vertex AI**, Google Cloud's enterprise ML platform. Vertex is the enterprise path: IAM/service-account
auth instead of API keys, GCP project/region selection, VPC-SC, CMEK, provisioned throughput, enterprise
data-governance contracts, and model tuning/deployment tooling. The Gemini API/AI Studio path documented
in this chapter is the lightweight developer path (API key, generativelanguage.googleapis.com, free
tier). Endpoints, auth, quotas and some feature timing differ between the two; this chapter documents
only the AI Studio / Gemini API surface. (https://ai.google.dev/gemini-api/docs, accessed 2026-08-14.)

## 4.2 Current model catalog

Source: https://ai.google.dev/gemini-api/docs/models and per-model subpages; pricing:
https://ai.google.dev/gemini-api/docs/pricing (all accessed 2026-08-14). Prices are USD per 1M tokens,
standard (non-batch) tier, text input unless noted. "1M" context = 1,048,576 tokens; "64K" output =
65,536 tokens. FC = function calling, SO = structured output. Fine-tuning is **not available for any
model** on the Gemini API (see 4.12).

### Text / multimodal reasoning models

| Model ID | Family/status | Context | Max out | Modalities in→out | FC | SO | $ in / $ out per 1M |
|---|---|---|---|---|---|---|---|
| `gemini-3.7-flash` | Flash, stable, latest (2026-08) | 1,048,576 | 65,536 | text,image,video,audio,PDF → text | ✓ | ✓ | 0.75 / 3.75 (promo to 2026-12-31; 1.50 / 7.50 after) |
| `gemini-3.6-flash` | Flash, stable (2026-07) | 1,048,576 | 65,536 | text,image,video,audio,PDF → text | ✓ | ✓ | 0.75 / 3.75 (same promo terms as 3.7) |
| `gemini-3.5-flash` | Flash, stable (2026-05) | 1,048,576 | 65,536 | text,image,video,audio,PDF → text | ✓ | ✓ | 1.50 / 9.00 |
| `gemini-3.5-flash-lite` | Flash-Lite, stable (2026-07) | 1,048,576 | 65,536 | text,image,video,audio,PDF → text | ✓ | ✓ | 0.30 / 2.50 |
| `gemini-3.1-flash-lite` | Flash-Lite, stable (2026-05) | 1,048,576 | 65,536 | text,image,video,audio,PDF → text | ✓ | ✓ | 0.25 (0.50 audio) / 1.50 |
| `gemini-3.1-pro-preview` | Pro flagship, **preview** (2026-02) | 1,048,576 | 65,536 | text,image,video,audio,PDF → text | ✓ | ✓ | ≤200K: 2.00 / 12.00 · >200K: 4.00 / 18.00 |
| `gemini-3-flash-preview` | Flash, preview (2025-12) | 1,048,576 | 65,536 | text,image,video,audio,PDF → text | ✓ | ✓ | [UNVERIFIED — not found on pricing page] |
| `gemini-2.5-pro` | Pro, stable, prior gen | 1,048,576 | 65,536 | text,image,video,audio,PDF → text | ✓ | ✓ | ≤200K: 1.25 / 10.00 · >200K: 2.50 / 15.00 |
| `gemini-2.5-flash` | Flash, stable, prior gen | 1,048,576 | 65,536 | text,image,video,audio → text | ✓ | ✓ | 0.30 (1.00 audio) / 2.50 |
| `gemini-2.5-flash-lite` | Flash-Lite, stable, prior gen | 1,048,576 | 65,536 | text,image,video,audio → text | ✓ | ✓ | 0.10 (0.30 audio) / 0.40 |

Variant: `gemini-3.1-pro-preview-customtools` — same model tuned for custom-tool/bash agent workflows
(https://ai.google.dev/gemini-api/docs/models/gemini-3.1-pro-preview, accessed 2026-08-14).

### Image generation (Gemini-native; Imagen is legacy, see 4.18)

| Model ID | Alias | Context in/out | Modalities | Image price (standard) |
|---|---|---|---|---|
| `gemini-3-pro-image` | Nano Banana Pro | 65,536 / 32,768 | text,image → text,image | $0.134 per 1K/2K img; $0.24 per 4K; text: 2.00 in / 12.00 out |
| `gemini-3.1-flash-image` | Nano Banana 2 | 131,072 / 32,768 | text,image,PDF → text,image | $0.045 (0.5K) / $0.067 (1K) / $0.101 (2K) / $0.151 (4K); text: 0.50 in / 3.00 out |
| `gemini-3.1-flash-lite-image` | Nano Banana 2 Lite | [UNVERIFIED] | text,image,video → text,image | $0.0336 per 1K img; text: 0.25 in / 1.50 out |
| `gemini-2.5-flash-image` | Nano Banana (prior gen; Imagen migration target) | [UNVERIFIED] | text,image → text,image | [UNVERIFIED — not on fetched pricing page] |

### Video, audio, music, embeddings, agents — see 4.4.

### Gemma open-weight models hosted on the Gemini API (brief — see Ollama/HF chapters for local detail)

| Model ID | Notes |
|---|---|
| `gemma-4-31b-it` | Gemma 4, 256K context; text, audio, image input; system instructions, function calling, Google Search, thinking (`high`/`minimal`) |
| `gemma-4-26b-a4b-it` | Gemma 4 sparse/MoE-style variant (a4b = active-params designation per ID; architecture detail [UNVERIFIED]); same feature set |

Source: https://ai.google.dev/gemma/docs/core/gemma_on_gemini_api (accessed 2026-08-14). Pricing/rate
limits for hosted Gemma: [UNVERIFIED — not published on fetched pages]. Wider Gemma 4 family (Apache
2.0 per docs): EmbeddingGemma, ShieldGemma 2, FunctionGemma, DiffusionGemma, PaliGemma, Gemma 3n —
https://ai.google.dev/gemma/docs (accessed 2026-08-14).

## 4.3 Model details & limitations

**Gemini 3.x Flash line (3.5 → 3.7).** All are 1M-context, 64K-output, text-out-only multimodal models.
Docs position 3.7 Flash for "complex coding and agentic workflows"; 3.6 Flash for code generation,
agentic execution and spatial reasoning; 3.5 Flash-Lite for "high-throughput, low-cost execution for
subagent tasks and document parsing"; 3.1 Flash-Lite for "high-frequency, lightweight tasks"
(translation, extraction, routing). All support thinking, FC, SO, caching, code execution, Google
Search + Maps grounding, file search, URL context, Batch/Flex/Priority inference; computer use is
preview on 3.5+/3.6/3.7. None support audio/image generation or the Live API. Thinking levels:
3.7-flash = low/medium/high (**no `minimal`**); 3.6-flash and 3.5-flash-lite add `minimal`.
Knowledge cutoffs for 3.x: [UNVERIFIED — not stated on model pages]. Sources: per-model pages under
https://ai.google.dev/gemini-api/docs/models/… and https://ai.google.dev/gemini-api/docs/thinking
(accessed 2026-08-14).

**Gemini 3.1 Pro (preview).** Current flagship intelligence tier; still `-preview` — no stable Pro-class
Gemini 3 model exists as of 2026-08 (the earlier `gemini-3-pro-preview` was shut down). Optimized for
software engineering and multi-step tool execution; tiered pricing above/below 200K prompt tokens.

**Gemini 2.5 family.** Still fully supported (stable), knowledge cutoff January 2025, last updated
June 2025. Cheapest text path on the API is `gemini-2.5-flash-lite` ($0.10/$0.40). 2.5 is also the only
generation with the computer-use model and native-audio Live model. Expect eventual deprecation;
prefer 3.x for new builds.

**Image models.** `gemini-3-pro-image` (Nano Banana Pro) is reasoning-driven ("thinking" supported) but
does **not** support function calling, structured outputs, or caching. `gemini-3.1-flash-image`
supports 0.5K–4K outputs, aspect ratios up to 1:8/8:1, image search grounding, improved multilingual
text rendering. Image output is billed per image (token-equivalent rates also published).

**Known constraints (documented):** text-only output for all reasoning models (no audio/image gen);
very large or deeply nested JSON schemas may be rejected (structured output docs); Gemini 3 requires
thought-signature round-tripping in stateless mode (see 4.9); image models lack FC/SO.

## 4.4 Embedding / audio / vision / video models

**Embeddings** (https://ai.google.dev/gemini-api/docs/embeddings, accessed 2026-08-14):

| Model | Input limit | Dimensions | Modalities | Price in per 1M |
|---|---|---|---|---|
| `gemini-embedding-2` (models page lists it as `gemini-embedding-2-preview`; docs body uses `gemini-embedding-2` — ID discrepancy noted) | 8,192 tok | 128–3072 flexible (MRL; rec. 768/1536/3072) | text, image, video, audio, PDF | [UNVERIFIED] |
| `gemini-embedding-001` | 2,048 tok | 128–3072 flexible (MRL) | text only | $0.15 (official launch blog, 2025-07-14 — may be stale) |

Task steering differs: `gemini-embedding-001` takes a `task_type` parameter
(`SEMANTIC_SIMILARITY`, `RETRIEVAL_DOCUMENT`, `RETRIEVAL_QUERY`, `CLASSIFICATION`, `CLUSTERING`);
`gemini-embedding-2` instead uses inline task instructions, e.g.
`"task: search result | query: {content}"`.

**TTS** (https://ai.google.dev/gemini-api/docs/speech-generation, accessed 2026-08-14):
`gemini-3.1-flash-tts-preview` ($1.00 text in / $20.00 audio out per 1M; ~25 audio tokens/sec),
`gemini-2.5-flash-preview-tts`, `gemini-2.5-pro-preview-tts` (2.5 TTS prices [UNVERIFIED]). 30 named
voices (Kore, Puck, Charon, Fenrir, Enceladus, …), 100+ languages auto-detected, single- and
multi-speaker (up to 2). Output: base64 PCM, 24 kHz, 16-bit mono. TTS session context limit: 32K tokens.

**Live API / realtime audio** (https://ai.google.dev/gemini-api/docs/live, accessed 2026-08-14):
stateful WebSocket (WSS); input raw 16-bit PCM 16 kHz LE, output 24 kHz; barge-in interruption;
function calling + Google Search inside sessions; 70 languages. Models: `gemini-3.1-flash-live-preview`
(text 0.75 in / 4.50 out; audio 3.00 in / 12.00 out per 1M, ≈ $0.005/min in, $0.018/min out),
`gemini-2.5-flash-native-audio-preview-12-2025` (price [UNVERIFIED]), and
`gemini-3.5-live-translate-preview` (speech translation, 70+ languages; 3.50 in / 21.00 out per 1M,
≈ $0.0053/$0.0315 per minute).

**Video generation — Veo** (https://ai.google.dev/gemini-api/docs/veo, accessed 2026-08-14):
`veo-3.1-generate-preview` (latest), `veo-3.1-fast-generate-preview`, `veo-3.1-lite-generate-preview`
(+ older `veo-3-generate-preview`, `veo-2-generate-preview` still listed). Veo 3.1: 8 s clips, 720p/
1080p/4K (4K at 8 s only), native audio always on, video extension up to +7 s (extended max 141 s,
720p), up to 3 reference images, 16:9/9:16. Generation latency 11 s–6 min; generated videos retained
2 days server-side. Per-second pricing: [UNVERIFIED — absent from fetched pricing page].
`gemini-omni-flash-preview`: conversational video generation/editing via generateContent-style calls;
$1.50 in / $9.00 text + $17.50 video out per 1M (≈$0.10 per second of 720p at 5,792 tokens/s).

**Music — Lyria:** `lyria-3-pro-preview` (full songs), `lyria-3-clip-preview` (≤30 s),
`lyria-realtime-exp` (streaming). Pricing [UNVERIFIED]. (Models page, accessed 2026-08-14.)

**Agentic/specialized:** `gemini-2.5-computer-use-preview-10-2025` (UI automation),
`deep-research-preview-04-2026` / `deep-research-max-preview-04-2026` (managed multi-step research
agents), `antigravity-preview-05-2026` (managed general agent with code execution + browsing),
`gemini-robotics-er-2-preview` / `-er-1.6-preview` (embodied reasoning). Specs/pricing for these:
[UNVERIFIED — models page listing only]. Vision understanding is native to all Gemini reasoning models
(image/video/PDF input); there is no separate vision model.

## 4.5 Pricing model & cost notes

Source: https://ai.google.dev/gemini-api/docs/pricing (accessed 2026-08-14).

- **Unit:** USD per 1M tokens, split by modality for some models (text/image/video vs audio input);
  image output billed per image; audio out ~25 tokens/s; video out 5,792 tokens/s (omni-flash).
- **Prompt-length tiers:** Pro-class models price higher above 200K prompt tokens (see 4.2).
- **Promotional pricing:** 3.7/3.6 Flash at $0.75/$3.75 **through 2026-12-31**, then $1.50/$7.50.
- **Batch API: 50% off** standard rates for all listed models (see 4.7).
- **Context caching:** cached input tokens billed at ~10% of input rate + storage per token-hour.
  Examples (per 1M cached tokens + storage per 1M tok/hr): 3.7-flash $0.075 + $0.50; 3.5-flash $0.15 +
  $1.00; 3.1-pro-preview $0.20–0.40 + $4.50; 2.5-pro $0.125–0.25 + $4.50; 2.5-flash $0.03 ($0.10 audio)
  + $1.00; 2.5-flash-lite $0.01 ($0.03 audio) + $1.00. Implicit-cache hits are discounted automatically
  with no storage fee.
- **Grounding with Google Search:** Gemini 3.x — 5,000 free search requests/month shared across all
  3.x models, then **$14 per 1,000 requests**, billed **per search query the model executes** (multiple
  queries in one request each count). Gemini 2.5 — 1,500 requests/day free (free tier: 500 RPD), then
  **$35 per 1,000 grounded prompts** (billed per prompt). Google Maps grounding: 5,000 free req/month
  then $14 per 1,000.
- **Priority tier:** ~1.8× standard for guaranteed capacity (e.g. 3.7-flash Priority $1.35/$6.75).
  Flex inference offered as a cheaper/looser alternative tier ([UNVERIFIED multiplier]).
- **Free tier:** $0 for listed models (3.7/3.6/3.5 Flash, Flash-Lite, 2.5 family, TTS, Live) at
  reduced rate limits; free-tier data is used for product improvement (see 4.17).

## 4.6 Authentication & environment

- API key from AI Studio: https://aistudio.google.com/apikey
- Env var: `GEMINI_API_KEY` (SDKs auto-read it; `GOOGLE_API_KEY` also honored by google-genai SDKs —
  the docs' canonical name is `GEMINI_API_KEY`).
- Header for REST: `x-goog-api-key: $GEMINI_API_KEY` (query param `?key=` also accepted historically;
  header form is what current docs show).
- OpenAI-compat endpoint uses the same key as the OpenAI-SDK `api_key`.
- No OAuth needed for the core API. Billing is linked to a Google Cloud billing account to leave the
  free tier (tier upgrades, see 4.11). Vertex AI uses IAM/ADC instead — out of scope here.
  (https://ai.google.dev/gemini-api/docs/quickstart, accessed 2026-08-14.)

## 4.7 API endpoints & schemas

Base URL: `https://generativelanguage.googleapis.com`. Version prefix `v1beta` is the documented
default.

| Surface | Endpoint | Notes |
|---|---|---|
| **Interactions API (GA, recommended)** | `POST /v1beta/interactions` | Unified: text, chat, tools, structured output, TTS; returns step history + usage |
| generateContent (supported, no deprecation notice) | `POST /v1beta/models/{model}:generateContent` | Classic surface; **required for explicit caching** |
| Streaming (classic) | `POST /v1beta/models/{model}:streamGenerateContent?alt=sse` | SSE chunks |
| Embeddings | `POST /v1beta/models/{model}:embedContent` | |
| Batch | `client.batches.*` / `POST /v1beta/batches` (SDK-first; JSONL via File API) | 50% discount |
| Files | `/v1beta/files` | uploads for multimodal + batch JSONL |
| Cached content (explicit) | `/v1beta/cachedContents` | generateContent-only |
| Video gen (Veo) | long-running operations via SDK `generate_videos` + `operations.get` | poll `done` |
| Live API | WSS endpoint (WebSocket) | realtime audio/video |
| **OpenAI-compat (beta)** | `https://generativelanguage.googleapis.com/v1beta/openai/` | chat completions, embeddings, images, `/v1/videos` (Sora-compatible), audio, batch (create/monitor/results only), models list |

**Interactions request (REST) minimal shape:**

```json
POST https://generativelanguage.googleapis.com/v1beta/interactions
x-goog-api-key: $GEMINI_API_KEY
Content-Type: application/json

{
  "model": "gemini-3.6-flash",
  "input": "Explain how AI works in a few words",
  "generation_config": { "thinking_level": "low" },
  "tools": [ { "type": "google_search" } ],
  "response_format": { "type": "text", "mime_type": "application/json", "schema": { } }
}
```

Response carries `output_text`, a `steps` array (e.g. `google_search_call`, `google_search_result`,
`model_output` with `url_citation` annotations: `url`, `title`, `start_index`, `end_index`), and
`usage` (incl. `total_cached_tokens`).

**generateContent request top-level fields** (https://ai.google.dev/api/generate-content, accessed
2026-08-14): `contents[]` (required), `systemInstruction`, `tools[]`, `toolConfig`,
`generationConfig`, `safetySettings[]`, `cachedContent`, `serviceTier`, `store`. Response:
`candidates[]`, `promptFeedback`, `usageMetadata`, `modelVersion`.

## 4.8 SDK integration

Packages: Python `google-genai` (`pip install -U google-genai`), JavaScript `@google/genai`
(`npm install @google/genai`). Both auto-read `GEMINI_API_KEY`.
(https://ai.google.dev/gemini-api/docs/quickstart, accessed 2026-08-14.)

**Python (Interactions API — canonical):**

```python
from google import genai

client = genai.Client()  # reads GEMINI_API_KEY

interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input="Explain how AI works in a few words",
)
print(interaction.output_text)
```

**JavaScript:**

```javascript
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});           // reads GEMINI_API_KEY
const interaction = await ai.interactions.create({
  model: "gemini-3.6-flash",
  input: "Explain how AI works in a few words",
});
console.log(interaction.output_text);
```

**curl:**

```bash
curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "gemini-3.6-flash", "input": "Explain how AI works in a few words"}'
```

**OpenAI-compat (Python, beta):**

```python
from openai import OpenAI

client = OpenAI(
    api_key="$GEMINI_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
resp = client.chat.completions.create(
    model="gemini-3.6-flash",
    messages=[{"role": "user", "content": "Explain how AI works"}],
)
```

**Embeddings (Python):**

```python
from google import genai
from google.genai import types

client = genai.Client()
result = client.models.embed_content(
    model="gemini-embedding-2",
    contents="What is the meaning of life?",
    config=types.EmbedContentConfig(output_dimensionality=768),
)
```

## 4.9 Streaming, tool use, structured output examples

**Streaming.** The Interactions API supports streaming (documented, exact snippet not captured —
example below uses the verified classic surface). Classic SSE:

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:streamGenerateContent?alt=sse" \
  -H "x-goog-api-key: $GEMINI_API_KEY" -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Write a haiku about latency."}]}]}'
```

Python classic streaming: `client.models.generate_content_stream(model=..., contents=...)`
[example shape from SDK, not re-verified verbatim against docs on access date].

**Function calling** (https://ai.google.dev/gemini-api/docs/function-calling, accessed 2026-08-14).
Declarations now use `"type": "function"`; mode is set via `tool_choice` in `generation_config`
(`auto` default, `any`, `none`, `validated`). Parallel and compositional calling supported; Gemini 3
models use internal reasoning to improve call accuracy.

```json
{
  "model": "gemini-3.6-flash",
  "input": "What is the weather in Zurich?",
  "tools": [{
    "type": "function",
    "name": "get_weather",
    "description": "Get current weather for a city.",
    "parameters": {
      "type": "object",
      "properties": { "location": { "type": "string", "description": "City name" } },
      "required": ["location"]
    }
  }],
  "generation_config": { "tool_choice": "auto" }
}
```

Loop: model emits a function call step → execute locally → send result back → model formats answer.
**Gemini 3 thought signatures:** in stateless usage you MUST resend all `thought` blocks exactly as
received (`missing_thought_signature` error otherwise); stateful Interactions mode handles this
server-side (https://ai.google.dev/gemini-api/docs/thinking, accessed 2026-08-14).

**Structured output** (https://ai.google.dev/gemini-api/docs/structured-output, accessed 2026-08-14):

```python
from google import genai
from pydantic import BaseModel
from typing import List

class Ingredient(BaseModel):
    name: str
    quantity: str

class Recipe(BaseModel):
    recipe_name: str
    ingredients: List[Ingredient]
    instructions: List[str]

client = genai.Client()
interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input="Extract the recipe from this text...",
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": Recipe.model_json_schema(),
    },
)
recipe = Recipe.model_validate_json(interaction.output_text)
```

Supported JSON-Schema subset: string/number/integer/boolean/object/array/null; `properties`,
`required`, `additionalProperties`; `enum`, `format` (date-time/date/time); `minimum`/`maximum`;
`items`, `prefixItems`, `minItems`/`maxItems`; `title`, `description`. Structured output **combined
with built-in tools** (Search, URL context, code execution) is Gemini-3-series-only. Oversized/deeply
nested schemas may be rejected.

**Grounding with Google Search:** `tools=[{"type": "google_search"}]` (older models used
`google_search_retrieval`). Response `steps` include executed queries and `url_citation` annotations
(https://ai.google.dev/gemini-api/docs/google-search, accessed 2026-08-14).

## 4.10 Error handling & retry

Source: https://ai.google.dev/gemini-api/docs/api-errors and …/docs/troubleshooting (accessed
2026-08-14).

| HTTP | error code | Meaning / action |
|---|---|---|
| 400 | `invalid_request` | Malformed payload/params — fix request |
| 400 | `failed_precondition` | e.g. billing not enabled — fix project setup |
| 400 | `parameter_unknown` | Remove unrecognized parameter |
| 401 | `authentication` | API key missing/invalid/expired |
| 403 | `permission_denied` | Key lacks permission for resource |
| 404 | `not_found` / `model_not_found` | Bad path / model unavailable |
| 409 | `already_exists` / `aborted` | Conflict; retry `aborted` at app level |
| 429 | `rate_limit_exceeded` | Per-minute/second limit — exponential backoff |
| 429 | `quota_exceeded` | Daily quota — wait for reset or upgrade tier |
| 500 | `api_error` | Server error — retry |
| 501 | `unimplemented` | Feature unsupported |
| 503 | `service_unavailable` | Overloaded — backoff retry |
| 504 | `deadline_exceeded` | Raise/remove client deadline |

Generation-blocked codes: `safety`, `recitation`, `language`, `prohibited_content`, `spii`,
`blocklist`, `image_safety`, `image_prohibited_content`, `image_recitation`, `image_other`.
Generation errors: `malformed_function_call`, `malformed_tool_call`, `unexpected_tool_call`,
`no_image`, `too_many_tool_calls`, `missing_thought_signature`.

Retry policy (documented guidance): retry only transient errors (429, 408, 5xx); never 400/403;
exponential backoff 1s → 2s → 4s → 8s with jitter and a max-attempt cap. The Python SDK auto-retries
transient errors up to 4 times (initial delay ≈1 s, max 60 s).

## 4.11 Rate limits & quotas

Source: https://ai.google.dev/gemini-api/docs/rate-limits (accessed 2026-08-14). Limits are measured
in RPM, TPM, RPD. **Per-model RPM/TPM/RPD tables are no longer published on the docs page** — active
limits are shown per-project in AI Studio (https://aistudio.google.com/rate-limit). Published tier
structure:

| Tier | Qualification | Billing cap | Spend-based limit |
|---|---|---|---|
| Free | active project, no billing | — | — (fixed low model limits) |
| Tier 1 | linked active billing account | $250 | $10 / 10 min |
| Tier 2 | ≥$100 paid + ≥3 days since first payment | $2,000 | $200 / 10 min |
| Tier 3 | ≥$1,000 paid + ≥30 days | $20,000–$100,000+ | $200 / 10 min |

Free→Tier 1 activates ~instantly after billing setup; later upgrades within ~10 minutes. Batch API has
separate limits: 100 concurrent batch requests, 2 GB max input file, 20 GB file storage; enqueued-token
caps scale from millions (Tier 1) to billions (Tier 3) per model. Per-model interactive numbers:
[UNVERIFIED — consult AI Studio console].

## 4.12 Fine-tuning & customization

**Not available.** Official statement: "With the deprecation of Gemini 1.5 Flash-001 in May 2025, we no
longer have a model available which supports fine-tuning in the Gemini API or AI Studio." Google states
no immediate plans to restore it; tuning "is supported in Gemini Enterprise Agent Platform" (and model
tuning generally lives on the Vertex AI side). Customization on this API = system instructions, few-shot
prompting, context caching, structured output, and tools.
(https://ai.google.dev/gemini-api/docs/model-tuning, accessed 2026-08-14.)

## 4.13 RAG & embedding pipeline notes

- Embed with `gemini-embedding-2` (multimodal, 8,192-token inputs) or `gemini-embedding-001` (text,
  2,048); MRL lets you truncate to 768/1536 dims to cut vector-store cost with little quality loss.
  Use asymmetric task steering (query vs document) — `task_type` on 001, inline `task:` prefixes on 2.
- Alternative to DIY RAG: the built-in **file search** tool (managed retrieval over uploaded files,
  supported by 2.5 and 3.x reasoning models) and **URL context** tool; **grounding with Google Search**
  covers web-fresh knowledge with citations (billing per query on 3.x — cost-model this for agent loops).
- 1M-token contexts + implicit caching (≥4,096 tokens prefix on 3.x) make "stuff the corpus in the
  prompt, cache the prefix" viable for mid-size corpora: cached tokens bill at ~10% of input rate.
- Batch API (50% off) is the right lane for offline corpus embedding/summarization; note embeddings are
  also exposed through the OpenAI-compat `/embeddings` endpoint for drop-in pipelines.

## 4.14 Agent support

- **Interactions API** is itself agent-oriented: server-side state (stateful mode), step history,
  automatic thought-signature handling, multi-tool (built-ins + custom functions in one request).
- Built-in tools: Google Search, Google Maps grounding, code execution, URL context, file search,
  computer use (preview; plus dedicated `gemini-2.5-computer-use-preview-10-2025`).
- Managed agent models: `deep-research[-max]-preview-04-2026`, `antigravity-preview-05-2026`
  (code execution + web browsing) — models-page listing; API details [UNVERIFIED].
- `gemini-3.1-pro-preview-customtools` targets bash/custom-tool agent harnesses.
- MCP: not documented on the pages fetched for this chapter [UNVERIFIED — check current SDK docs];
  function-calling docs describe SDK-side automatic tool-execution loops.
- Official SDKs (`google-genai` Python / `@google/genai` JS) are the supported client layer; the
  OpenAI-compat endpoint lets OpenAI-ecosystem agent frameworks target Gemini with a base_url swap.

## 4.15 Deployment patterns

The Gemini API is fully managed (serverless from the caller's perspective); you deploy only clients.
Patterns: (a) server-side proxy holding `GEMINI_API_KEY` (never ship keys to browsers/mobile);
(b) Cloud Run/Lambda functions calling the REST endpoints — SSE streaming pass-through works on both;
(c) Live API needs a WebSocket-capable backend (server-to-server) or ephemeral client tokens for
client-to-server [token mechanism [UNVERIFIED on fetched pages]]; (d) Batch jobs driven by a scheduler
+ File API for JSONL in/out; (e) enterprise controls (VPC-SC, CMEK, provisioned throughput, regional
pinning) require moving to Vertex AI, not this API. Priority/Flex service tiers select capacity class
per request (`serviceTier` field on generateContent).

## 4.16 Region availability & data residency

Available-regions list is published at https://ai.google.dev/gemini-api/docs/available-regions
[UNVERIFIED — page contents not re-fetched on access date]. The Gemini API is a global endpoint;
no data-residency selection is offered on this API (region pinning is a Vertex AI feature). EU/UK/CH
users are served under the same published terms; check the regions page before compliance decisions.

## 4.17 Security, compliance & SLA

Data usage (https://ai.google.dev/gemini-api/terms, accessed 2026-08-14):

- **Unpaid/free tier:** "Google uses the content you submit to the Services and any generated
  responses to provide, improve, and develop Google products" — including machine-learning
  technologies; human reviewers "may read, annotate, and process your API input and output"
  (disconnected from account/key/project first). Terms warn: "Do not submit sensitive, confidential,
  or personal information to the Unpaid Services."
- **Paid tier:** "Google doesn't use your prompts or responses to improve our products." Prompts and
  responses are logged only "for a limited period of time, solely for detecting and preventing
  violations" of the Prohibited Use Policy and legal compliance.
- Pricing page mirrors this: free tier = "used to improve", paid = "not used to improve".
- SLA: none documented for the Gemini API/AI Studio path [UNVERIFIED — no published SLA found];
  contractual SLAs are a Vertex AI matter. Certifications (SOC/ISO/HIPAA) for this API path:
  [UNVERIFIED — not documented on fetched pages].

## 4.18 Legacy models & migration notes

| Legacy | Status (2026-08-14) | Migration |
|---|---|---|
| Gemini 1.5 Pro/Flash/Flash-8B | Retired; no longer on models page | → Gemini 3.x Flash / 3.1 Pro |
| `gemini-2.0-flash`, `gemini-2.0-flash-lite` | **Shut down** (listed as deprecated/shut down) | → `gemini-3.1-flash-lite` / `gemini-2.5-flash-lite` |
| `gemini-3-pro-preview`, `gemini-3.1-flash-lite-preview` | Shut down | → `gemini-3.1-pro-preview`, `gemini-3.1-flash-lite` |
| Imagen 4 (`imagen-4.0-generate-001`, `-ultra-`, `-fast-`) | Deprecated; **shutdown 2026-08-17** | → `gemini-2.5-flash-image` (Nano Banana) or 3.x image models; `generate_images` → `generate_content`, image comes back as content part |
| Veo 2 / Veo 3 previews | Still listed; superseded | → `veo-3.1-*` |
| `google_search_retrieval` tool | Old-model tool name | → `{"type": "google_search"}` |
| Fine-tuned 1.5 Flash-001 tunes | Gone since 2025-05 | No replacement on this API (see 4.12) |
| `generateContent` surface | Supported, no deprecation notice, but docs steer to Interactions API | New code: Interactions; keep generateContent where explicit caching is needed |

Sources: https://ai.google.dev/gemini-api/docs/models, …/docs/imagen, …/docs/model-tuning (accessed
2026-08-14).

## 4.19 Task-suitability verdict

**Strong:** (a) long-context multimodal work — every reasoning model takes 1M tokens of text+image+
video+audio+PDF; (b) price/performance at the flash tier — $0.75/$3.75 promo on 3.7-flash and
$0.10/$0.40 on 2.5-flash-lite undercut comparable tiers, with 50% batch and ~90% cache discounts
stacking; (c) agentic/tool workloads — Interactions API step model, built-in Search/Maps/code-exec/
computer-use, thought-signature handling; (d) integrated media generation — image (Nano Banana line),
video (Veo 3.1 with native audio), TTS, realtime Live audio, music — one key for all; (e) grounded
answers with citations via Google Search tool; (f) generous free tier for prototyping.

**Weak / avoid:** (a) anything requiring fine-tuning — not available on this API at all; (b) flagship
stability — the top intelligence tier (`gemini-3.1-pro-preview`) is still preview-only, and preview IDs
churn (two 3.x IDs already shut down); (c) strict data-residency / SLA-bound workloads — no residency
control or published SLA here (use Vertex AI); (d) free-tier processing of sensitive data — inputs are
used for product improvement and may be human-reviewed; (e) capacity planning — per-model rate limits
are no longer published, only visible per-project in AI Studio; (f) image-model agents — image models
lack function calling/structured output; (g) reproducible pricing beyond 2026-12-31 (promo expiry).

## 4.20 Sources

All accessed **2026-08-14**:

1. Models catalog — https://ai.google.dev/gemini-api/docs/models
2. Per-model pages — https://ai.google.dev/gemini-api/docs/models/gemini-3.7-flash, …/gemini-3.6-flash,
   …/gemini-3.5-flash, …/gemini-3.5-flash-lite, …/gemini-3.1-flash-lite, …/gemini-3.1-pro-preview,
   …/gemini-3-flash-preview, …/gemini-3-pro-image, …/gemini-3.1-flash-image, …/gemini-2.5-pro,
   …/gemini-2.5-flash
3. Pricing — https://ai.google.dev/gemini-api/docs/pricing
4. Rate limits — https://ai.google.dev/gemini-api/docs/rate-limits
5. Quickstart — https://ai.google.dev/gemini-api/docs/quickstart
6. Text generation (Interactions API) — https://ai.google.dev/gemini-api/docs/text-generation
7. Structured output — https://ai.google.dev/gemini-api/docs/structured-output
8. Function calling — https://ai.google.dev/gemini-api/docs/function-calling
9. Thinking — https://ai.google.dev/gemini-api/docs/thinking
10. Context caching — https://ai.google.dev/gemini-api/docs/caching
11. Batch API — https://ai.google.dev/gemini-api/docs/batch-api
12. Google Search grounding — https://ai.google.dev/gemini-api/docs/google-search
13. OpenAI compatibility — https://ai.google.dev/gemini-api/docs/openai
14. Embeddings — https://ai.google.dev/gemini-api/docs/embeddings
15. Speech generation (TTS) — https://ai.google.dev/gemini-api/docs/speech-generation
16. Live API — https://ai.google.dev/gemini-api/docs/live
17. Veo — https://ai.google.dev/gemini-api/docs/veo (and …/docs/video)
18. Imagen deprecation — https://ai.google.dev/gemini-api/docs/imagen
19. generateContent API reference — https://ai.google.dev/api/generate-content
20. API errors — https://ai.google.dev/gemini-api/docs/api-errors; troubleshooting —
    https://ai.google.dev/gemini-api/docs/troubleshooting
21. Model tuning status — https://ai.google.dev/gemini-api/docs/model-tuning
22. Terms (data usage) — https://ai.google.dev/gemini-api/terms
23. Gemma on Gemini API — https://ai.google.dev/gemma/docs/core/gemma_on_gemini_api; Gemma family —
    https://ai.google.dev/gemma/docs
24. Gemini Embedding GA announcement (price) — https://developers.googleblog.com/gemini-embedding-available-gemini-api/
    (published 2025-07-14; price may be stale)


---

# 5. Anthropic Claude

> **Model lineups and pricing change frequently. Verified against official documentation on 2026-08-14. Re-verify before production decisions.**
>
> Official docs have consolidated at **platform.claude.com/docs** (docs.claude.com and docs.anthropic.com now 302-redirect there). Agent SDK docs live at **code.claude.com/docs**; MCP spec at **modelcontextprotocol.io**.

## 5.1 Platform overview & positioning

Anthropic exposes Claude models through a single first-party REST API (`https://api.anthropic.com`, primary endpoint `POST /v1/messages`), the Claude Console (`platform.claude.com`), and partner platforms (Amazon Bedrock, Google Cloud Vertex AI, Claude Platform on AWS, Microsoft Foundry). Positioning is agentic/coding/enterprise-first: no embedding, audio, image-generation, or video models; instead deep investment in tool use, structured outputs, prompt caching, the Files API, server-side tools (web search, code execution), computer use, hosted Managed Agents, the Claude Agent SDK, and the Model Context Protocol (MCP), which Anthropic originated.

The 2026-08 lineup is a 5-era lineup (Fable 5 / Opus 5 / Sonnet 5 at 1M context) plus Haiku 4.5 as the small tier. The 3.x families are retired; Claude 4.0/4.1 are retired; 4.5–4.8 models remain served but superseded (§5.18).

Source: https://platform.claude.com/docs/en/about-claude/models/overview (accessed 2026-08-14).

## 5.2 Current model catalog

Per models overview (https://platform.claude.com/docs/en/about-claude/models/overview, accessed 2026-08-14) and pricing (https://platform.claude.com/docs/en/about-claude/pricing, accessed 2026-08-14):

| Model | API id (pinned) | Family/tier | Context | Output limit | Modalities in/out | Tool use | Structured output | Fine-tuning | $ in / $ out per 1M |
|---|---|---|---|---|---|---|---|---|---|
| Claude Fable 5 | `claude-fable-5` | Fable / frontier | 1M | 128k | text+image / text | Yes | Yes | No | 10.00 / 50.00 |
| Claude Opus 5 | `claude-opus-5` | Opus / frontier | 1M | 128k | text+image / text | Yes | Yes | No | 5.00 / 25.00 |
| Claude Sonnet 5 | `claude-sonnet-5` | Sonnet / mid | 1M | 128k | text+image / text | Yes | Yes | No | 2.00 / 10.00 |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` (alias `claude-haiku-4-5`) | Haiku / small | 200k | 64k | text+image / text | Yes | Yes | No | 1.00 / 5.00 |

Notes:
- **Claude Mythos 5** (`claude-mythos-5`): invitation-only, defensive-cybersecurity workflows ("Project Glasswing"); same specs/pricing as Fable 5. Not generally available.
- Still served but superseded (migration targets in §5.18): Opus 4.8 / 4.7 / 4.6 ($5/$25), Sonnet 4.6 ($3/$15), Opus 4.5 and Sonnet 4.5 (pricing no longer on the current pricing page — [UNVERIFIED]).
- Model ids are **pinned snapshots**, not evergreen. Training/knowledge cutoffs: Fable 5 Jan 2026; Opus 5 May 2026; Sonnet 5 Jan 2026; Haiku 4.5 trained Jul 2025 / knowledge Feb 2025.
- Sonnet 5 $2/$10 is introductory pricing extended through 2026-08-31 per the pricing page; re-verify after that date.

## 5.3 Model details & limitations

### Fable 5 (`claude-fable-5`)
Top-priced frontier model. **Adaptive thinking is always on** (models overview lists extended thinking "No — adaptive thinking always on"): reasoning depth is model-controlled; there is no manual `budget_tokens` mode. Pricing page groups it under "Newer Models (Limited Availability)" while the overview lists it on all platforms — treat regional/tier availability as account-dependent. 1M context, 128k output.

### Opus 5 (`claude-opus-5`)
Frontier workhorse. Adaptive thinking (`thinking: {"type": "adaptive"}`) with `output_config.effort` control. Supports **Fast Mode** (Opus 5 and 4.8 only) at $10/$50 per 1M — faster output, not combinable with Batch API, stacks with caching and data-residency multipliers.

### Sonnet 5 (`claude-sonnet-5`)
Mid-tier default. Adaptive thinking. 1M context at flat pricing (no long-context tier surcharge per pricing page).

### Haiku 4.5 (`claude-haiku-4-5-20251001`)
Small/fast tier, last 4.5-era model in the main catalog. 200k context, 64k output. Uses **manual extended thinking** (`thinking: {"type": "enabled", "budget_tokens": N}`), not adaptive.

### Cross-cutting constraints (all per official docs, accessed 2026-08-14)
- **Sampling parameters deprecated on 4.7+ era models**: `temperature`, `top_p`, `top_k` set to non-default values return **400** on Claude 4.7+ (and Mythos Preview). Source: https://platform.claude.com/docs/en/about-claude/model-deprecations.
- Extended thinking (`type: "enabled"`) is **rejected with 400 on Opus 4.6+ / Sonnet 4.7+**; deprecated on Sonnet 4.6. Source: extended-thinking doc (§5.9).
- `stop_reason` values now include `pause_turn` (long-running turn paused), `refusal`, and `model_context_window_exceeded`; refusals carry `stop_details` with `category` (`cyber`, `bio`, `frontier_llm`, `reasoning_extraction`, `general_harms`).
- Tokenizer change: "Claude 4.7+ tokenizer: ~30% more tokens than earlier versions" (pricing page) — token-count assumptions from 4.5-era do not transfer.
- Tool-use system-prompt overhead (tool-use overview): Opus 5 286 tokens (`auto`/`none`) / 406 (`any`/`tool`); Sonnet 5 354/474; Haiku 4.5 496/588.

## 5.4 Embedding / audio / vision / video models

- **Embeddings: none.** Anthropic explicitly does not offer an embedding model and recommends third-party providers, primarily **Voyage AI** (`voyage-4-large`, `voyage-4`, `voyage-4-lite`, open-weight `voyage-4-nano`, plus code/finance/law/multimodal/context variants; up to 32k-token inputs; 256–2048 dims). Source: https://platform.claude.com/docs/en/docs/build-with-claude/embeddings (accessed 2026-08-14).
- **Vision:** image *input* only (JPEG/PNG/GIF/WebP via base64, URL, or `file_id`); no image generation.
- **Audio/video:** no audio or video modalities in or out. [Not offered per current docs.]

## 5.5 Pricing model & cost notes

All prices USD per 1M tokens; source: https://platform.claude.com/docs/en/about-claude/pricing (accessed 2026-08-14).

| Model | Input | Output | Batch in/out (−50%) | 5m cache write (1.25×) | 1h cache write (2×) | Cache read (0.1×) |
|---|---|---|---|---|---|---|
| Fable 5 | 10.00 | 50.00 | 5.00 / 25.00 | 12.50 | 20.00 | 1.00 |
| Opus 5 | 5.00 | 25.00 | 2.50 / 12.50 | 6.25 | 10.00 | 0.50 |
| Opus 4.8 / 4.7 / 4.6 | 5.00 | 25.00 | 2.50 / 12.50 | 6.25 | 10.00 | 0.50 |
| Sonnet 5 | 2.00 | 10.00 | 1.00 / 5.00 | 2.50 | 4.00 | 0.20 |
| Sonnet 4.6 | 3.00 | 15.00 | 1.50 / 7.50 | 3.75 | 6.00 | 0.30 |
| Haiku 4.5 | 1.00 | 5.00 | 0.50 / 2.50 | 1.25 | 2.00 | 0.10 |

- **Batch API:** 50% off input and output; not combinable with Fast Mode.
- **Fast Mode** (Opus 5/4.8 only): $10/$50.
- **Data residency:** `inference_geo: "us"` applies a **1.1× multiplier** to all token categories; default global routing at standard price.
- **Long context:** full 1M window at standard pricing (no tiered surcharge).
- **Thinking tokens billed as output tokens** (both adaptive and manual modes); tracked in `usage.output_tokens_details.thinking_tokens`.
- **Server tools:** web search $10 per 1,000 searches (+tokens); web fetch free beyond tokens; code execution free with web search/fetch, otherwise $0.05/hour (5-min minimum) after 1,550 free hours/month/org.
- **Managed Agents:** tokens at standard rates + **$0.08 per session-hour** while status is `running`.
- **Claude Platform on AWS / Microsoft Foundry** bill in Claude Consumption Units (100 CCU = $1). Bedrock/Google Cloud regional or multi-region endpoints carry a 10% premium over global endpoints.

## 5.6 Authentication & environment

- Header auth: `x-api-key: $ANTHROPIC_API_KEY` plus required `anthropic-version: 2023-06-01` and `content-type: application/json`.
- SDK convention: environment variable `ANTHROPIC_API_KEY`; base URL override at client construction.
- Keys are created in the Claude Console and scoped to workspaces (Files are workspace-scoped to the uploading key's workspace).
- Beta features are opted into via `anthropic-beta: <flag>` headers (e.g. `files-api-2025-04-14`, `mcp-client-2025-11-20`, `computer-use-2025-11-24`).
- OAuth/IAM: not used on the first-party API; Bedrock uses AWS credentials/IAM, Vertex uses Google Cloud IAM.

Source: https://platform.claude.com/docs/en/api/messages.md and /docs/en/api/client-sdks (accessed 2026-08-14).

## 5.7 API endpoints & schemas

Base URL `https://api.anthropic.com`; versioning via the `anthropic-version` header (current documented value still `2023-06-01`; new behavior ships behind beta headers).

| Endpoint | Purpose |
|---|---|
| `POST /v1/messages` | Create a message (streaming or not) |
| `POST /v1/messages/count_tokens` | Count input tokens (no `stream`/`inference_geo`) |
| `POST /v1/messages/batches` (+ `GET`, `/{id}`, `/{id}/results`, `/{id}/cancel`, `DELETE /{id}`) | Message Batches API |
| `POST /v1/files` (+ `GET`, `/{id}`, `/{id}/content`, `DELETE /{id}`) | Files API (beta) |

Request body (Messages, key fields): required `model`, `max_tokens`, `messages`; optional `system` (string or text-block array), `tools` (custom + server tools: `code_execution`, `bash`, `web_search`, `web_fetch`, `text_editor`, `memory`, `tool_search`), `tool_choice` (`auto` | `any` | `tool` | `none`), `thinking` (`enabled` | `disabled` | `adaptive`), `output_config` (structured-output format + `effort`), `metadata.user_id`, `stop_sequences`, `stream`, top-level `cache_control`, `container`, `inference_geo`, `service_tier` (`auto` | `standard_only`), and legacy sampling params (`temperature`/`top_p`/`top_k` — 400 on 4.7+ models when non-default).

Response shape:

```json
{
  "id": "msg_...", "type": "message", "role": "assistant", "model": "claude-opus-5",
  "content": [ {"type": "thinking", "thinking": "...", "signature": "..."},
               {"type": "text", "text": "...", "citations": []} ],
  "stop_reason": "end_turn | max_tokens | stop_sequence | tool_use | pause_turn | refusal | model_context_window_exceeded",
  "stop_sequence": null,
  "stop_details": {"type": "refusal", "category": "cyber|bio|frontier_llm|reasoning_extraction|general_harms", "explanation": null},
  "usage": {
    "input_tokens": 0, "output_tokens": 0,
    "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0,
    "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0},
    "output_tokens_details": {"thinking_tokens": 0},
    "server_tool_use": {"web_search_requests": 0, "web_fetch_requests": 0},
    "service_tier": "standard", "inference_geo": null
  },
  "container": null
}
```

Content block types: `text`, `thinking`, `redacted_thinking`, `tool_use` (with `caller` field), `server_tool_use`, `web_search_tool_result`, `web_fetch_tool_result`, `code_execution_tool_result`, `bash_code_execution_tool_result`, `text_editor_code_execution_tool_result`, `tool_search_tool_result`, `container_upload`. Input blocks additionally: `image` (base64/url/file), `document` (base64/text/url/file + optional `citations`), `tool_result`.

Request size limits: Messages and count_tokens 32 MB; Batches 256 MB; Files 500 MB.

Source: https://platform.claude.com/docs/en/api/messages.md, /docs/en/api/errors (accessed 2026-08-14).

## 5.8 SDK integration

Official SDKs: Python (`pip install anthropic`), TypeScript (`npm install @anthropic-ai/sdk`), Java, Go, Ruby, C#, PHP. Source: https://platform.claude.com/docs/en/api/client-sdks (accessed 2026-08-14).

Python:

```python
import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY

msg = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    system="You are a terse technical assistant.",
    thinking={"type": "adaptive"},
    output_config={"effort": "medium"},
    messages=[{"role": "user", "content": "Explain token bucket rate limiting."}],
)
print(msg.content[-1].text, msg.usage.output_tokens)
```

TypeScript:

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic(); // reads ANTHROPIC_API_KEY
const msg = await client.messages.create({
  model: "claude-sonnet-5",
  max_tokens: 1024,
  thinking: { type: "adaptive" },
  messages: [{ role: "user", content: "Explain token bucket rate limiting." }],
});
console.log(msg.content.at(-1));
```

curl:

```bash
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "anthropic-version: 2023-06-01" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -d '{
    "model": "claude-haiku-4-5",
    "max_tokens": 512,
    "messages": [{"role": "user", "content": "Hello, Claude"}]
  }'
```

## 5.9 Streaming, tool use, structured output examples

**Streaming** (`"stream": true`, SSE): event order `message_start` → per block (`content_block_start` → `content_block_delta`* → `content_block_stop`) → `message_delta` (cumulative usage) → `message_stop`; interleaved `ping` and possible `error` events (e.g. `overloaded_error`). Delta types: `text_delta`, `input_json_delta` (partial JSON strings for tool input), `thinking_delta`, `signature_delta`. With `thinking.display: "omitted"`, only `signature_delta` is sent for thinking blocks. Per-tool `eager_input_streaming` enables fine-grained tool-parameter streaming. Source: https://platform.claude.com/docs/en/docs/build-with-claude/streaming (accessed 2026-08-14).

**Tool use** (custom tool + result round trip):

```json
{
  "model": "claude-opus-5",
  "max_tokens": 1024,
  "tools": [{
    "name": "get_weather",
    "description": "Get current weather for a location.",
    "strict": true,
    "input_schema": {
      "type": "object",
      "properties": {"location": {"type": "string"}},
      "required": ["location"],
      "additionalProperties": false
    }
  }],
  "tool_choice": {"type": "auto"},
  "messages": [{"role": "user", "content": "Weather in Osaka?"}]
}
```

The model returns `stop_reason: "tool_use"` with a `tool_use` block (`id`, `name`, `input`); you append the assistant content plus a user turn containing `{"type": "tool_result", "tool_use_id": "...", "content": "..."}` and call again. Parallel tool calls are default; disable via `tool_choice: {"type": "any", "disable_parallel_tool_use": true}`. Source: https://platform.claude.com/docs/en/docs/agents-and-tools/tool-use/overview (accessed 2026-08-14).

**Structured outputs** — two mechanisms, combinable (source: https://platform.claude.com/docs/en/docs/build-with-claude/structured-outputs, accessed 2026-08-14):

1. JSON output via `output_config.format` (the older top-level `output_format` still works but is deprecated):

```json
{
  "model": "claude-sonnet-5",
  "max_tokens": 1024,
  "messages": [{"role": "user", "content": "Extract: John Smith wants an Enterprise demo Tuesday 2pm"}],
  "output_config": {
    "format": {
      "type": "json_schema",
      "schema": {
        "type": "object",
        "properties": {"name": {"type": "string"}, "plan": {"type": "string"}, "demo": {"type": "boolean"}},
        "required": ["name", "plan", "demo"],
        "additionalProperties": false
      }
    }
  }
}
```

2. Strict tool use: `"strict": true` in a tool definition guarantees schema-conformant `input`.

Limits: ≤20 strict tools/request; ≤24 optional parameters across strict schemas; ≤16 union-typed parameters; `minimum`/`maximum`/`minLength`/`maxLength` unsupported; incompatible with citations and message prefill; first request pays grammar-compilation latency (cached 24h). Thinking is not constrained by the grammar — only final output.

## 5.10 Error handling & retry

| HTTP | `error.type` | Meaning |
|---|---|---|
| 400 | `invalid_request_error` | Malformed request (incl. deprecated params on 4.7+) |
| 401 | `authentication_error` | Bad/revoked key |
| 402 | `billing_error` | Billing problem |
| 403 | `permission_error` | Key lacks access |
| 404 | `not_found_error` | Resource missing |
| 409 | `conflict_error` | State conflict |
| 413 | `request_too_large` | Over byte limit |
| 429 | `rate_limit_error` | Rate limited (`retry-after` header) |
| 500 | `api_error` | Internal error |
| 504 | `timeout_error` | Request timed out |
| 529 | `overloaded_error` | Capacity; also arrives as SSE `error` event |

Error body: `{"type":"error","error":{"type":"...","message":"..."},"request_id":"req_..."}`; every response carries a `request-id` header. SDKs raise typed exceptions and auto-retry transient failures (connection errors, 429, 5xx) with exponential backoff (2× default). For turns >10 minutes use streaming or the Batch API; keep TCP keep-alive on. Source: https://platform.claude.com/docs/en/api/errors (accessed 2026-08-14).

## 5.11 Rate limits & quotas

Source: https://platform.claude.com/docs/en/api/rate-limits (accessed 2026-08-14). The old numbered tiers (1–4) are replaced by named tiers:

| Tier | Monthly spend cap |
|---|---|
| Start | $500 |
| Build | $1,000 |
| Scale | $200,000 |
| Custom | none (account team) |

Advancement is based on usage history/account standing (exact thresholds not published — [UNVERIFIED]); new orgs may begin in a lower-limit Evaluation tier. Documented per-model limits (Start tier; Build/Scale same per docs): Opus 5 / Sonnet 5 / Haiku 4.5 each **1,000 RPM, 2,000,000 input TPM, 400,000 output TPM**.

- **Cache-aware ITPM:** only *uncached* input tokens count toward ITPM (billed at 0.1× when read) — with 80% cache hits, ~10M effective input tokens/min on a 2M ITPM limit.
- **Token bucket** algorithm: continuous replenishment, no fixed reset windows.
- **Batches:** separate 1,000 RPM (all models combined); ≤100,000 requests/batch; ≤200,000 requests in the processing queue.
- Headers: `anthropic-ratelimit-requests-remaining`, `anthropic-ratelimit-input-tokens-remaining`, `anthropic-ratelimit-output-tokens-remaining`, `retry-after`.

## 5.12 Fine-tuning & customization

No self-serve fine-tuning on the first-party Claude API; no fine-tuning docs exist for current models (accessed 2026-08-14). Customization levers instead: system prompts, prompt caching, structured outputs, tools/skills, and MCP servers. Historical Bedrock fine-tuning applied only to retired Claude 3 Haiku. Any current partner-platform fine-tuning: [UNVERIFIED — not published].

## 5.13 RAG & embedding pipeline notes

Anthropic ships no embedder; the documented pattern is external embeddings (Voyage AI recommended; see §5.4) + your vector store, with Claude as the generator. Platform features relevant to RAG:

- **Citations**: enable per `document` block (`"citations": {"enabled": true}`) — responses return `text` blocks with citation locations (`char_location`, `page_location`, `content_block_location`, `search_result_location`).
- **Files API** for reusable corpora (upload once, reference by `file_id`; PDFs and text as `document` blocks).
- **Server-side web search / web fetch** tools for retrieval without your own pipeline.
- **Prompt caching** (up to 4 breakpoints, 5m/1h TTL) to amortize large static context; 1M context windows reduce chunking pressure but input cost still scales linearly.

## 5.14 Agent support

- **Claude Agent SDK** (Python + TypeScript; repos `anthropics/claude-agent-sdk-python` and `anthropics/claude-agent-sdk-typescript`): the Claude Code agent loop as a library — built-in file/command/web tools, hooks, subagents, permissions, sessions (resume/fork), skills/commands/memory loaded from `.claude/`, plugins, MCP. Docs: https://code.claude.com/docs/en/agent-sdk/overview (accessed 2026-08-14). Note: third-party products may not offer claude.ai login/rate limits; API keys required.
- **Managed Agents**: hosted REST product — Anthropic runs the agent and sandbox; billed tokens + $0.08/session-hour (§5.5).
- **Server tools in Messages**: `web_search_20250305`, `web_fetch`, `code_execution` (sandboxed containers, `container` reuse, `container_upload` blocks), `text_editor`, `bash`, `memory`, and `tool_search` (regex/BM25 on-demand tool discovery for large tool sets).
- **Computer use** (beta): tool `computer_20251124` (predecessor `computer_20250124`), header `anthropic-beta: computer-use-2025-11-24`; models: Opus 5, Sonnet 5, Opus 4.5–4.8, Sonnet 4.6. Actions include screenshot/click/type/scroll/drag plus new `zoom` (`enable_zoom: true`). Prompt-injection classifiers enabled by default. Source: https://platform.claude.com/docs/en/docs/agents-and-tools/tool-use/computer-use-tool (accessed 2026-08-14).

### MCP (Model Context Protocol)

Anthropic originated and open-sourced MCP (Nov 2024) as a standard for connecting AI applications to external tools/data; it is now cross-vendor (Claude, ChatGPT, VS Code, Cursor, etc.). Current spec revision: **2026-07-28** at https://modelcontextprotocol.io (accessed 2026-08-14). Primitives: tools, resources, prompts; transports: stdio and HTTP (Streamable HTTP/SSE). In the Messages API, the **MCP connector** (beta header `mcp-client-2025-11-20`; `mcp-client-2025-04-04` deprecated) takes an `mcp_servers` array (`{"type":"url","url":"https://…","name":"…","authorization_token":"…"}`); remote HTTP servers only (no stdio), tool-calls-only (no MCP resources/prompts server-side), OAuth tokens obtained by the caller. The Agent SDK and Claude Code support full MCP including local stdio servers. Sources: https://platform.claude.com/docs/en/docs/agents-and-tools/mcp-connector; https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro.md (accessed 2026-08-14).

## 5.15 Deployment patterns

- First-party API: fully managed/serverless; `service_tier` (`auto`/`standard_only`); Batch API for offline bulk (≤100k requests, most <1h, 24h expiry, results 29 days, JSONL).
- **Amazon Bedrock**: all four current models available via AWS IAM/SDKs — see https://platform.claude.com/docs/en/api/claude-on-amazon-bedrock (one-line cross-ref; regional endpoints +10%).
- **Google Cloud Vertex AI**: all four current models via GCP — see https://platform.claude.com/docs/en/api/claude-on-vertex-ai (one-line cross-ref; regional endpoints +10%).
- **Claude Platform on AWS** and **Microsoft Foundry**: CCU-billed (100 CCU = $1).
- Managed Agents for hosted long-running agents; Agent SDK for self-hosted agent loops in your own infra.

## 5.16 Region availability & data residency

- Default: global routing at standard pricing. **US-only inference**: `inference_geo: "us"` at 1.1× on all token categories (Claude API and Claude Platform on AWS); `usage.inference_geo` echoes routing. Source: pricing page (accessed 2026-08-14).
- Per-region availability matrices for Bedrock/Vertex are maintained by those platforms; not enumerated here — [UNVERIFIED in this pass].

## 5.17 Security, compliance & SLA

Documented data handling (https://privacy.claude.com/en/articles/7996866, /7996868, accessed 2026-08-14):

- **No training on commercial/API data by default** ("By default, we will not use your inputs or outputs from our commercial products … to train our models"); explicit feedback or opt-in may be used.
- **Retention:** API inputs/outputs auto-deleted from backend within **30 days**, except usage-policy violations (up to 2 years; trust-and-safety scores 7 years), feedback (5 years), legal holds.
- **Zero Data Retention (ZDR)** available by agreement; Files API content is *not* ZDR-eligible; computer use is ZDR-eligible (client-side screenshots). Structured-output schemas are cached 24h (docs advise no PHI in schemas for HIPAA).
- Certifications (SOC 2, ISO, HIPAA BAA availability) and uptime SLAs: not verified in this pass — [UNVERIFIED — see Anthropic Trust Center].

## 5.18 Legacy models & migration notes

Policy: ≥60 days' notice before retiring publicly released models; email to active deployments; Anthropic has published model-weight preservation commitments. Bedrock/Vertex set their own retirement schedules. Source: https://platform.claude.com/docs/en/about-claude/model-deprecations (accessed 2026-08-14).

Retired (requests fail):

| Model | Retired | Replacement |
|---|---|---|
| `claude-opus-4-1-20250805` | 2026-08-05 | `claude-opus-4-8` (now → Opus 5) |
| `claude-opus-4-20250514` | 2026-06-15 | `claude-opus-4-8` |
| `claude-sonnet-4-20250514` | 2026-06-15 | `claude-sonnet-4-6` |
| `claude-3-7-sonnet-20250219` | 2026-02-19 | `claude-sonnet-4-6` |
| `claude-3-5-haiku-20241022` | 2026-02-19 | `claude-haiku-4-5-20251001` |
| `claude-3-haiku-20240307` | 2026-04-20 | `claude-haiku-4-5-20251001` |

Active-but-superseded, with earliest retirement dates: `claude-opus-4-8` (≥2027-05-28), `claude-opus-4-7` (≥2027-04-16), `claude-opus-4-6` (≥2027-02-05), `claude-opus-4-5-20251101` (≥2026-11-24), `claude-sonnet-4-6` (≥2027-02-17), `claude-sonnet-4-5-20250929` (≥2026-09-29 — imminent), `claude-haiku-4-5-20251001` (≥2026-10-15). Current 5-era floors: Fable 5 ≥2027-06-09, Opus 5 ≥2027-07-24, Sonnet 5 ≥2027-06-30.

API-surface migrations:
- `thinking: {"type":"enabled","budget_tokens":N}` → `thinking: {"type":"adaptive"}` + `output_config.effort` (`low|medium|high`); manual mode 400s on Opus 4.6+/Sonnet 4.7+; adaptive may skip thinking on easy inputs. Interleaved-thinking beta header (`interleaved-thinking-2025-05-14`) only needed for manual mode on 4.5-era.
- `output_format` → `output_config.format` (old form deprecated).
- Drop non-default `temperature`/`top_p`/`top_k` before moving to 4.7+/5-era models (400).
- Budget/effort changes invalidate prompt-cache breakpoints; hold them stable in cached conversations.
- Re-baseline token budgets: 4.7+ tokenizer yields ~30% more tokens.

## 5.19 Task-suitability verdict

**Best at (evidence-based):** agentic tool-use workloads (richest server-tool set, parallel + strict tools, tool search, computer use, Agent SDK/MCP origin); long-context work (1M standard-priced); cost-engineered high-volume serving (cache-aware rate limits + 0.1× cache reads + 50% batch); schema-guaranteed extraction (grammar-backed structured outputs). Sonnet 5 at $2/$10 is the price-performance anchor; Haiku 4.5 for latency/cost-sensitive routing; Opus 5/Fable 5 for frontier reasoning.

**Worst at / avoid:** anything needing embeddings, audio, image/video generation, or speech (none offered — pair with Voyage AI etc.); self-serve fine-tuning (none); strict determinism knobs (sampling params removed on 4.7+; adaptive thinking is nondeterministic in depth); Fable 5 for budget workloads ($10/$50, limited availability). Structured outputs exclude citations and prefill — pick one per request.

## 5.20 Sources

All accessed 2026-08-14:

1. Models overview — https://platform.claude.com/docs/en/about-claude/models/overview
2. Pricing — https://platform.claude.com/docs/en/about-claude/pricing
3. Messages API reference — https://platform.claude.com/docs/en/api/messages.md
4. Rate limits — https://platform.claude.com/docs/en/api/rate-limits
5. Errors — https://platform.claude.com/docs/en/api/errors
6. Client SDKs — https://platform.claude.com/docs/en/api/client-sdks
7. Extended/adaptive thinking — https://platform.claude.com/docs/en/docs/build-with-claude/extended-thinking
8. Structured outputs — https://platform.claude.com/docs/en/docs/build-with-claude/structured-outputs
9. Streaming — https://platform.claude.com/docs/en/docs/build-with-claude/streaming
10. Prompt caching — https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching
11. Batch processing — https://platform.claude.com/docs/en/docs/build-with-claude/batch-processing
12. Files API — https://platform.claude.com/docs/en/docs/build-with-claude/files
13. Tool use overview — https://platform.claude.com/docs/en/docs/agents-and-tools/tool-use/overview
14. Computer use — https://platform.claude.com/docs/en/docs/agents-and-tools/tool-use/computer-use-tool
15. MCP connector — https://platform.claude.com/docs/en/docs/agents-and-tools/mcp-connector
16. MCP spec/intro — https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro.md
17. Embeddings guidance — https://platform.claude.com/docs/en/docs/build-with-claude/embeddings
18. Model deprecations — https://platform.claude.com/docs/en/about-claude/model-deprecations
19. Agent SDK overview — https://code.claude.com/docs/en/agent-sdk/overview
20. Data retention — https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data
21. Training-data policy — https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training


---

# 6. AWS Bedrock

> **Volatility warning.** Model lineups and pricing change frequently. Verified against official
> documentation on **2026-08-14**. Re-verify before production decisions.

## 6.1 Platform overview & positioning

Amazon Bedrock is AWS's managed multi-vendor foundation-model service: a single control plane and
inference plane over models from **Anthropic, OpenAI, Amazon (Nova), Meta, Mistral AI, Cohere,
DeepSeek, Qwen, Google (Gemma), Z.AI, Moonshot AI, MiniMax, NVIDIA, xAI, AI21 Labs, Writer,
Stability AI, TwelveLabs, Luma AI** (docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html,
accessed 2026-08-14). It is not a model vendor competing on a single frontier model; it competes on
procurement (one AWS bill, one IAM boundary), data governance (prompts/outputs not used for training,
VPC endpoints, CloudTrail), and breadth.

Architecturally, Bedrock in 2026 has **two inference planes**:

```
                +--------------------------------------------+
  AWS SDK       |  bedrock-runtime.{region}.amazonaws.com    |  Converse / ConverseStream /
  (SigV4) ----->|  "classic" runtime, SigV4                  |  InvokeModel (+ stream)
                +--------------------------------------------+
                +--------------------------------------------+
  OpenAI /      |  bedrock-mantle.{region}.api.aws           |  OpenAI Responses & Chat Completions,
  Anthropic --->|  API-key or SigV4                          |  Anthropic Messages API
  SDKs          +--------------------------------------------+
```

The `bedrock-mantle` endpoint (GA 2026; console redesigned around it June 2026) exposes
**OpenAI-compatible and Anthropic-native APIs** so first-party SDKs (`openai`, `anthropic`) work
against Bedrock with a base-URL swap
(docs.aws.amazon.com/bedrock/latest/userguide/endpoints.html;
aws.amazon.com/about-aws/whats-new/2026/06/amazon-bedrock-redesigned-console-optimized-openai-anthropic-compatible-apis/,
accessed 2026-08-14). Some models are mantle-only: OpenAI's proprietary GPT-5.x line is served
**only** via the Responses API on `bedrock-mantle`, not via Converse/InvokeModel
(docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-56-sol.html, accessed 2026-08-14).

## 6.2 Current model catalog

The authoritative, continuously updated catalog is **"Models at a glance"**
(docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html) with one model-card page per model
(pattern: `.../model-card-<provider>-<model>.html`). The table below is the **notable, practically
usable subset** as of 2026-08-14 — not exhaustive (the full catalog is 110+ models across 19
providers). Prices are US-region on-demand per 1M tokens from aws.amazon.com/bedrock/pricing/ and
model cards (accessed 2026-08-14); rows marked ³ are third-party-sourced pending official
confirmation.

| Model (Bedrock ID) | Family | Context | Max out | Modalities in/out | Tool use | Structured out | FT | $ in / $ out per 1M |
|---|---|---|---|---|---|---|---|---|
| `anthropic.claude-opus-5` | Claude 5 | 1M | 128K | text+image / text | Y | Y (runtime) | N | 5.00 / 25.00 |
| `anthropic.claude-sonnet-5` | Claude 5 | 1M | 128K | text+image / text | Y | N¹ | N | 2.00 / 10.00 |
| `anthropic.claude-fable-5` | Claude 5 | [UNVERIFIED] | [UNVERIFIED] | text+image / text | Y | [UNVERIFIED] | N | 10.00 / 50.00 |
| `anthropic.claude-opus-4-8` | Claude 4 | [UNVERIFIED] | [UNVERIFIED] | text+image / text | Y | Y | N | 5.00 / 25.00 |
| `anthropic.claude-sonnet-4-6-v1` | Claude 4 | 200K | 64K³ | text+image / text | Y | Y | N | 3.00 / 15.00 |
| `anthropic.claude-haiku-4-5` | Claude 4 | 200K | 64K³ | text+image / text | Y | Y | N | 1.00 / 5.00 |
| `amazon.nova-2-lite-v1:0` | Nova 2 | 1M | 64K | text+image+video / text | Y | N | N | 0.33 / 2.75³ |
| `amazon.nova-2-sonic-v1:0` | Nova 2 | — | — | speech / speech (bidir) | Y | N | N | [UNVERIFIED] |
| `amazon.nova-pro-v1:0` | Nova 1 | 300K | 5K | text+image+video / text | Y | Y | Y | 0.80 / 3.20 |
| `amazon.nova-micro-v1:0` | Nova 1 | 128K | 5K | text / text | Y | Y | Y | 0.035 / 0.14 |
| `openai.gpt-5.6-sol` | GPT-5.6 | 1M | [UNVERIFIED] | text+image / text | Y (server-side) | N² | N | 5.50 / 33.00 (short-ctx tier) |
| `openai.gpt-5.5` | GPT-5.5 | [UNVERIFIED] | [UNVERIFIED] | text+image / text | Y | [UNVERIFIED] | N | [UNVERIFIED] |
| `openai.gpt-oss-120b-1:0` | gpt-oss | 128K³ | [UNVERIFIED] | text / text | Y | Y | Y (RFT) | [UNVERIFIED] |
| `meta.llama4-maverick-17b-instruct-v1:0` | Llama 4 | 1M | [UNVERIFIED] | text+image / text | Y | Y | N | 0.50 / 0.80³ |
| `meta.llama4-scout-17b-instruct-v1:0` | Llama 4 | 1M³ | [UNVERIFIED] | text+image / text | Y | Y | N | 0.17 / 0.36³ |
| `meta.llama3-3-70b-instruct-v1:0` | Llama 3.3 | 128K | [UNVERIFIED] | text / text | Y | Y | Y | 0.99 / 3.96⁴ |
| `mistral.mistral-large-3-v1:0` | Mistral Large 3 | 128K³ | [UNVERIFIED] | text / text | Y | Y | N | 0.50 / 1.50 |
| `mistral.pixtral-large-2502-v1:0` | Pixtral | 128K³ | [UNVERIFIED] | text+image / text | Y | Y | N | [UNVERIFIED] |
| `deepseek.v3.2` | DeepSeek | 128K³ | [UNVERIFIED] | text / text | Y | [UNVERIFIED] | N | 0.62 / 1.85 |
| `deepseek.r1-v1:0` | DeepSeek R1 | 128K | 32K³ | text / text | N³ | N³ | N | [UNVERIFIED] |
| `qwen.qwen3-32b-v1:0` | Qwen3 | [UNVERIFIED] | [UNVERIFIED] | text / text | Y | Y | N | 0.20 / 0.78 |
| `cohere.embed-v4` | Embed v4 | — | — | text+image / embedding | — | — | N | [UNVERIFIED] |
| `cohere.rerank-v3-5:0` | Rerank | — | — | text / scores | — | — | N | $2.00 per 1K queries |
| `amazon.titan-embed-text-v2:0` | Titan Embed | 8K in | — | text / embedding (256/512/1024d) | — | — | N | 0.02 / — |
| `amazon.nova-multimodal-embeddings` | Nova Embed | — | — | text+image+video / embedding | — | — | N | [UNVERIFIED] |
| `ai21.jamba-1-5-large-v1:0` | Jamba 1.5 | 256K | [UNVERIFIED] | text / text | Y | Y | N | [UNVERIFIED] |

¹ Sonnet 5 model card lists "Structured outputs: not supported" on bedrock-runtime (accessed 2026-08-14).
² GPT-5.6 Sol card: structured outputs not supported via Bedrock Responses API.
³ Third-party source (cloudprice.net / cloudzero.com / hidekazu-konishi.com catalog, accessed 2026-08-14) — verify on the official pricing page.
⁴ Fetched from aws.amazon.com/bedrock/pricing/ 2026-08-14; anomalous vs earlier published Llama 3.3 pricing — re-verify.

Also currently listed but not cataloged here: Google Gemma 4/3, NVIDIA Nemotron 3, Z.AI GLM 5/4.7,
Moonshot Kimi K2.5, MiniMax M2.x, xAI Grok 4.3, Writer Palmyra X5, TwelveLabs Marengo/Pegasus
(video understanding), Stability AI image suite, Luma AI Ray v2 (video gen), Amazon Nova
Canvas/Reel (image/video gen, gen-1 Legacy). Source: model-cards.html, accessed 2026-08-14.

## 6.3 Model details & limitations

**Anthropic Claude (flagship line on Bedrock).** Claude 5 generation (Opus 5, Sonnet 5, plus
specialty Mythos 5 / Fable 5 at $10/$50) is Active alongside a long Claude 4.x tail (Opus
4.5–4.8, Sonnet 4/4.5/4.6, Haiku 4.5). Opus 5: 1M context / 128K output, launched 2026-07-24;
Sonnet 5: 1M/128K, launched 2026-06-30. Both support prompt caching (5-min and 1-h TTL, 4
checkpoints), batch, computer use, Guardrails, Knowledge Bases, Agents; neither supports
fine-tuning on Bedrock. Claude pricing on Bedrock is **identical to Anthropic first-party list
prices**, with a **10% premium on regional/cross-region endpoints** per Anthropic's pricing page
(platform.claude.com/docs/en/about-claude/pricing, accessed 2026-08-14). Sources:
model-card-anthropic-claude-opus-5.html, model-card-anthropic-claude-sonnet-5.html (2026-08-14).

**OpenAI (new since 2025-08, proprietary line since 2026-06).** Open-weight `gpt-oss-120b/20b`
arrived 2025-08; proprietary **GPT-5.5, GPT-5.4 and Codex went GA on Bedrock 2026-06**, and the
**GPT-5.6 family (Sol/Terra/Luna)** launched 2026-07 (Sol: 2026-07-13, 1M context, us-east-1/2
in-region only, no cross-region profiles, no batch/streaming-via-Responses caveats apply). GPT-5.x
is **bedrock-mantle only** (OpenAI Responses API; Converse/InvokeModel rejected). AWS cut Luna
prices 80% and Terra 20% effective 2026-07-30 to track OpenAI first-party pricing. Sources:
aws.amazon.com/about-aws/whats-new/2026/06/amazon-bedrock-openai-models-codex-generally-available/;
.../2026/07/openai-gpt-terra-luna-pricing-bedrock/; model-card-openai-gpt-56-sol.html (2026-08-14).

**Amazon own-brand: Nova 2 is current; Titan text generation is gone.** The Titan-era text models
(Titan Text Express/Lite) no longer appear in the catalog; only **Titan embeddings and Titan Image
Generator v2** remain Active. Nova gen-1 (Micro/Lite/Pro/Premier/Canvas/Reel/Sonic) is being
sunset: Nova Premier EOL 2026-09-14, Canvas/Reel/Sonic-gen1 EOL 2026-09-30 (third-party catalog,
hidekazu-konishi.com, 2026-05 — verify per model card). Current line: **Nova 2 Lite** (1M ctx, 64K
out, text+image+video in, launched 2025-12-02, geo/global profiles only — no single-region
deployment), **Nova 2 Sonic** (bidirectional speech-to-speech), **Nova Multimodal Embeddings**.
Nova 2 Lite supports the new **Priority/Flex service tiers** (see 6.5). Source:
model-card-amazon-nova-2-lite.html (2026-08-14).

**Meta Llama.** Llama 4 Maverick/Scout (17B-active MoE, 1M context, multimodal) are current;
Llama 3.3 70B remains the dense workhorse; Llama 3.2 and 3.1 405B are Legacy-tier. Llama models
support fine-tuning on Bedrock (3.1/3.3 families).

**Mistral AI.** Mistral Large 3 (aggressively priced at $0.50/$1.50 in US regions), Pixtral Large
(vision), Ministral 3B/8B/14B edge line, Devstral 2 (code), Magistral (reasoning), Voxtral
(speech-in). One of the broadest non-US lineups on Bedrock (14 models).

**Cohere.** Pivoted on Bedrock to retrieval infrastructure: **Embed v4** (multimodal) and **Rerank
3.5** are the current models; Command R/R+ still listed but Legacy per third-party catalog.

**DeepSeek / Qwen / GLM / Kimi / MiniMax.** Bedrock added six open-weights models on 2026-02-10
(DeepSeek V3.2, MiniMax M2.1, GLM 4.7, GLM 4.7 Flash, Kimi K2.5, Qwen3 Coder Next), served through
OpenAI-compatible endpoints on mantle
(aws.amazon.com/about-aws/whats-new/2026/02/amazon-bedrock-adds-support-six-open-weights-models,
accessed 2026-08-14). DeepSeek-R1 (reasoning) has been serverless on Bedrock since 2025-03.

**AI21.** Jamba 1.5 Large/Mini (256K context hybrid SSM-transformer) — unchanged since 2024;
treat as maintenance-mode.

Known platform constraints: per-model feature matrices differ sharply (e.g., Sonnet 5 lacks
structured outputs on runtime; Nova 2 Lite lacks batch; GPT-5.6 lacks cross-region profiles) —
always read the model card before committing to a feature.

## 6.4 Embedding / audio / vision / video models

| Type | Models | Notes |
|---|---|---|
| Text embedding | `amazon.titan-embed-text-v2:0` (1024/512/256d, 8K in, $0.02/1M), Cohere Embed English/Multilingual v3 | Titan V2 is the KB default |
| Multimodal embedding | Amazon Nova Multimodal Embeddings (text/image/video), Cohere Embed v4, Titan Multimodal Embeddings G1, TwelveLabs Marengo 3.0 (video) | prices largely [UNVERIFIED] |
| Rerank | Cohere Rerank 3.5 ($2.00/1K queries), Amazon Rerank | used by KB reranking API |
| Speech | Nova 2 Sonic (speech↔speech), Voxtral Small/Mini (speech→text reasoning) | |
| Image gen/edit | Stability: SD 3.5 Large, Stable Image Core/Ultra + 13 editing primitives; Titan Image Generator v2; Nova Canvas (Legacy) | |
| Video gen | Luma AI Ray v2 (us-west-2), Nova Reel (Legacy) | |
| Video understanding | TwelveLabs Pegasus 1.2 | |

Source: model-cards.html + pricing page, accessed 2026-08-14.

## 6.5 Pricing model & cost notes

Five purchase modes (aws.amazon.com/bedrock/pricing/, accessed 2026-08-14):

1. **On-demand (Standard tier)** — per-token, per-region price lists; per-image/video for media
   models; per-query for rerank.
2. **Batch** — async JSONL jobs via S3; **50% of on-demand** across most supported text models.
3. **Provisioned Throughput** — hourly "model units" with 1-/6-month commitments; required for
   some customized models (e.g., Cohere Embed 3 listed at $7.12/h/unit). Not usable with
   cross-region inference profiles.
4. **Service tiers (new, 2026)** — per-request `serviceTier`: **Priority** (~1.75x, latency-SLO
   traffic), **Standard**, **Flex** (~50%, latency-tolerant), **Reserved** — supported model-by-model
   (e.g., Nova 2 Lite: Priority/Flex; Claude Opus 5: Standard+Batch only). Tier prices per model
   card / pricing page; third-party example for Nova 2 Lite global: 0.33/2.75 std, 0.165/1.38
   flex-batch, 0.578/4.81 priority (cloudprice.net, 2026-08-14).
5. **Prompt caching** — cache reads ≈10% of input price (Claude: writes 1.25x/2x for 5m/1h TTL,
   reads 0.1x; Nova: cache-read 0.25x [UNVERIFIED on current page]).

Cross-region pricing: geographic profiles bill at the **source-region price** (no routing
surcharge); **global profiles run ~10% cheaper** than geographic per AWS cross-region docs, while
Anthropic's page frames Bedrock regional/cross-region endpoints as a **10% premium over global**
— same delta, two framings. Guardrails billed separately: content filters $0.15/1K text units,
sensitive-info filters $0.10/1K text units, image filters $0.00075/image. Knowledge Bases: you pay
for embeddings + your vector store + retrieval-time model tokens; the KB orchestration itself has
no separate meter [structured-retrieval and reranking have their own line items — see pricing page].

## 6.6 Authentication & environment

Bedrock's default auth is **AWS IAM + SigV4 request signing** — the fundamental contrast with
API-key providers (OpenAI/Anthropic first-party):

- No static bearer key in the request; every call is signed with rotating credentials resolved
  from the standard AWS chain (env vars `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`/
  `AWS_SESSION_TOKEN`, `~/.aws/credentials` profiles, or — preferred in production — **IAM roles**
  (EC2 instance profile, ECS/EKS task role via IRSA/Pod Identity, Lambda execution role) with zero
  stored secrets.
- Authorization is IAM policy on actions (`bedrock:InvokeModel`, `bedrock:InvokeModelWithResponseStream`,
  `bedrock:Converse*`) and resources (model ARNs, inference-profile ARNs — a cross-region profile
  requires permission on the profile **and** the underlying regional model ARNs; SCPs must allow
  destination regions, or `"aws:RequestedRegion": "unspecified"` for global profiles).
- Model access must be **enabled per model per account** in the console/API before first use
  (`AccessDeniedException` otherwise).

Since 2025-07 Bedrock also issues **Bedrock API keys** (short-term ~12h, and long-term IAM-user
backed) for the mantle endpoint and SDK compatibility: `x-api-key: $AWS_BEARER_TOKEN_BEDROCK` /
`OPENAI_API_KEY=<bedrock-api-key>` — lowering the onboarding gap with API-key providers
(docs.aws.amazon.com/bedrock/latest/userguide/inference-messages-api.html, accessed 2026-08-14).
Minimal IAM policy:

```json
{"Version":"2012-10-17","Statement":[{"Effect":"Allow",
  "Action":["bedrock:InvokeModel","bedrock:InvokeModelWithResponseStream"],
  "Resource":["arn:aws:bedrock:*::foundation-model/anthropic.claude-sonnet-5",
              "arn:aws:bedrock:*:123456789012:inference-profile/global.anthropic.claude-sonnet-5"]}]}
```

## 6.7 API endpoints & schemas

| Endpoint | Purpose |
|---|---|
| `bedrock.{region}.amazonaws.com` | control plane: model access, customization jobs, provisioned throughput, Guardrails config |
| `bedrock-runtime.{region}.amazonaws.com` | inference: `Converse`, `ConverseStream`, `InvokeModel`, `InvokeModelWithResponseStream`, `StartAsyncInvoke` (video) |
| `bedrock-mantle.{region}.api.aws` | OpenAI Responses + Chat Completions (`/openai/v1`), Anthropic Messages (`/anthropic/v1/messages`); API-key or SigV4 |
| `bedrock-agent` / `bedrock-agent-runtime` | Knowledge Bases + classic Agents build/runtime (incl. `Retrieve`, `RetrieveAndGenerate`) |
| AgentCore endpoints | AgentCore Runtime/Gateway/Memory (separate service surface) |

**Converse vs InvokeModel (bedrock-runtime):**

- **`Converse`/`ConverseStream`** — uniform, model-agnostic JSON schema (`messages[].content[]`
  blocks, `system`, `inferenceConfig{maxTokens,temperature,topP,stopSequences}`, `toolConfig`,
  `guardrailConfig`, `additionalModelRequestFields` for vendor extras). Swap `modelId`, keep code.
  Recommended default for text/chat.
- **`InvokeModel`** — passes an opaque `body` in each **vendor's native schema** (e.g., Anthropic
  body requires `"anthropic_version": "bedrock-2023-05-31"`). Required for models/features Converse
  doesn't cover (embeddings, image/video gen, some vendor-specific params).

`modelId` accepts a base model ID, an **inference-profile ID** (`us.`/`eu.`/`apac.`/`jp.`/`au.`/
`global.` prefix), a provisioned-throughput ARN, or a custom-model deployment ARN. Versioning is
in the model ID itself (`-v1:0` suffixes; newest Anthropic IDs drop it, e.g.
`anthropic.claude-opus-5`), not an API version header.

## 6.8 SDK integration

Python (boto3 ≥ 1.34; Converse):

```python
import boto3
client = boto3.client("bedrock-runtime", region_name="us-east-1")
resp = client.converse(
    modelId="global.anthropic.claude-sonnet-5",
    system=[{"text": "You are a terse assistant."}],
    messages=[{"role": "user", "content": [{"text": "Three uses of SQS?"}]}],
    inferenceConfig={"maxTokens": 512, "temperature": 0.3},
)
print(resp["output"]["message"]["content"][0]["text"])
print(resp["usage"])   # {'inputTokens':..,'outputTokens':..,'totalTokens':..}
```

JavaScript (`@aws-sdk/client-bedrock-runtime` v3):

```javascript
import { BedrockRuntimeClient, ConverseCommand } from "@aws-sdk/client-bedrock-runtime";
const client = new BedrockRuntimeClient({ region: "us-east-1" });
const resp = await client.send(new ConverseCommand({
  modelId: "global.anthropic.claude-sonnet-5",
  messages: [{ role: "user", content: [{ text: "Three uses of SQS?" }] }],
  inferenceConfig: { maxTokens: 512 },
}));
console.log(resp.output.message.content[0].text);
```

curl against mantle (Anthropic Messages, API key):

```bash
curl -X POST https://bedrock-mantle.us-east-1.api.aws/anthropic/v1/messages \
  -H "x-api-key: $BEDROCK_API_KEY" -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{"model":"anthropic.claude-sonnet-5","max_tokens":512,
       "messages":[{"role":"user","content":"Three uses of SQS?"}]}'
```

OpenAI SDK against mantle (only way to reach GPT-5.x on Bedrock):

```python
from openai import OpenAI  # OPENAI_API_KEY=<bedrock key>, OPENAI_BASE_URL=https://bedrock-mantle.us-east-1.api.aws/openai/v1
client = OpenAI()
r = client.responses.create(model="openai.gpt-5.6-sol", input="Summarize SigV4 in two sentences.")
```

All verified against model-card sample code / inference-messages-api docs, accessed 2026-08-14.

## 6.9 Streaming, tool use, structured output

Streaming (boto3):

```python
stream = client.converse_stream(modelId="global.anthropic.claude-sonnet-5",
    messages=[{"role":"user","content":[{"text":"Stream a haiku."}]}])
for ev in stream["stream"]:
    if "contentBlockDelta" in ev:
        print(ev["contentBlockDelta"]["delta"].get("text",""), end="")
    elif "metadata" in ev:
        usage = ev["metadata"]["usage"]
```

Tool use (Converse `toolConfig`; loop: request → `stopReason=="tool_use"` → run tool → append
`toolResult` block → re-call):

```python
tool_cfg = {"tools":[{"toolSpec":{"name":"get_weather",
  "inputSchema":{"json":{"type":"object","properties":{"city":{"type":"string"}},
                  "required":["city"]}}}}]}
resp = client.converse(modelId="global.anthropic.claude-sonnet-5",
                       messages=msgs, toolConfig=tool_cfg)
if resp["stopReason"] == "tool_use":
    tu = next(b["toolUse"] for b in resp["output"]["message"]["content"] if "toolUse" in b)
    msgs += [resp["output"]["message"],
             {"role":"user","content":[{"toolResult":{"toolUseId":tu["toolUseId"],
               "content":[{"json":{"temp_c":21}}]}}]}]
    resp = client.converse(modelId="global.anthropic.claude-sonnet-5",
                           messages=msgs, toolConfig=tool_cfg)
```

Structured output: support is **per model** (model-card flag "Structured outputs"). Where absent
(e.g. Sonnet 5 on runtime, GPT-5.6 via Responses), use the standard workaround: a single required
tool whose `inputSchema` is your JSON schema, plus `toolChoice: {"tool": {"name": ...}}`.

## 6.10 Error handling & retry

| Exception (runtime) | HTTP | Meaning / action |
|---|---|---|
| `ThrottlingException` | 429 | RPM/TPM quota exceeded — exponential backoff + jitter; consider cross-region profile or Priority tier |
| `ValidationException` | 400 | bad schema, unsupported feature for model, context overflow |
| `AccessDeniedException` | 403 | IAM denied or **model access not enabled** in account/region |
| `ResourceNotFoundException` | 404 | wrong modelId/region combination |
| `ModelNotReadyException` | 429 | custom/marketplace model still loading — retry |
| `ModelTimeoutException` | 408 | model took too long — retry |
| `ModelErrorException` | 424 | model returned error |
| `ServiceQuotaExceededException` | 400 | hard quota — request increase |
| `ServiceUnavailableException` / `InternalServerException` | 503/500 | retry with backoff |

Source: Bedrock Runtime API reference (docs.aws.amazon.com/bedrock/latest/APIReference/), accessed
2026-08-14. boto3 pattern — raise both retry ceiling and read timeout (long generations exceed the
60 s default):

```python
from botocore.config import Config
cfg = Config(retries={"max_attempts": 10, "mode": "adaptive"},
             read_timeout=3600, connect_timeout=10)
client = boto3.client("bedrock-runtime", config=cfg)
```

## 6.11 Rate limits & quotas

Quotas are **per account, per region, per model** in requests/min and tokens/min, listed in
Service Quotas (`docs.aws.amazon.com/general/latest/gr/bedrock.html` + console); many are
adjustable by request. Exact numbers vary widely by model/region and change often —
[UNVERIFIED — see Service Quotas console for current values]. Levers when throttled: cross-region
inference profiles (spreads load across regions; AWS states higher effective throughput),
Priority service tier, provisioned throughput, batch for offline work. Mantle endpoint advertises
"higher initial throughput with fair-share distribution" (endpoints.html, accessed 2026-08-14).

## 6.12 Fine-tuning & customization

Customization jobs run from the control plane (console/`bedrock` API), output a custom model
invoked via provisioned throughput or on-demand custom-model deployment:

- **Fine-tuning (SFT, incl. LoRA/PEFT)** — Amazon Nova gen-1 (Micro/Lite/Pro), Meta Llama
  3.1/3.3, Titan-era models; per-model support flag on each model card. Current-generation
  frontier models (Claude 4.5+/5, GPT-5.x, Nova 2 Lite) do **not** support fine-tuning on Bedrock.
- **Reinforcement fine-tuning (RFT)** — GA since 2025-12 (AWS claims avg +66% accuracy over base);
  extended 2026-02 to **open-weight models via OpenAI-compatible APIs** (gpt-oss etc.); Nova RFT
  jobs documented at rft-nova-models.html.
- **Distillation** — teacher→student (e.g., Claude/Llama teacher into Nova/Llama student).
- **Continued pre-training** — Titan/Nova text models.
- Also: import of custom weights (Custom Model Import, Llama/Mistral architectures).

Sources: docs.aws.amazon.com/bedrock/latest/userguide/reinforcement-fine-tuning.html;
aws.amazon.com/about-aws/whats-new/2025/12/bedrock-reinforcement-fine-tuning-66-base-models;
.../2026/02/amazon-bedrock-reinforcement-fine-tuning-openai (accessed 2026-08-14).

## 6.13 RAG & embedding pipeline notes (Knowledge Bases)

**Bedrock Knowledge Bases** is the managed RAG layer: point it at data sources (S3, web crawler,
Confluence/Salesforce/SharePoint connectors), pick an embedding model (default Titan Text
Embeddings V2; Cohere Embed also supported) and a vector store (OpenSearch Serverless default;
Aurora PostgreSQL/pgvector, Pinecone, Redis Enterprise, MongoDB Atlas, **S3 Vectors** — the 2025
low-cost native option), and it handles chunking (fixed/semantic/hierarchical/custom-Lambda),
embedding, sync, retrieval, reranking (Cohere Rerank 3.5 / Amazon Rerank), and citation-bearing
generation. Runtime APIs: `Retrieve` (chunks only) and `RetrieveAndGenerate` (grounded answer)
on `bedrock-agent-runtime`; KBs also attach to Agents and to Converse via `guardrail`/agent
integration. Structured data retrieval (natural-language→SQL over Redshift) and GraphRAG
(Neptune) are additional KB modes. Source:
docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html, accessed 2026-08-14.

## 6.14 Agent support

Two distinct offerings — naming matters in 2026:

- **Amazon Bedrock Agents ("classic")** — the older fully-managed declarative agent (action
  groups from OpenAPI/Lambda, KB attachment, memory, `InvokeAgent` runtime). Still available and
  documented, but AWS's strategic push has moved to AgentCore.
- **Amazon Bedrock AgentCore** — GA since 2025-10 (aws.amazon.com/about-aws/whats-new/2025/10/
  amazon-bedrock-agentcore-available, accessed 2026-08-14). Framework- and model-agnostic
  production platform ("any framework, any model" — LangChain/LangGraph, CrewAI, OpenAI Agents
  SDK, Claude Agent SDK, Strands Agents, custom): modular services — **Runtime** (serverless agent
  hosting, session isolation, up to 8h executions), **Gateway** (turns APIs/Lambda into MCP tools),
  **Memory** (short/long-term), **Identity** (OAuth/agent identity), **Code Interpreter**,
  **Browser**, **Observability** (OTel-based). Consumption-priced (no per-agent fee);
  aws.amazon.com/bedrock/agentcore/pricing/ for meters. MCP is a first-class protocol in Gateway
  and Runtime.
- Related: Strands Agents (AWS's open-source agent framework) commonly deployed onto AgentCore.

New builds should target AgentCore (or a framework on AgentCore Runtime); classic Agents remain
supported for existing declarative deployments. Source: aws.amazon.com/bedrock/agentcore/,
accessed 2026-08-14.

## 6.15 Deployment patterns

- **Serverless on-demand** is the default: no capacity management; scale governed by quotas.
- **Cross-region inference profiles** for resilience/throughput: geographic (`us.`, `eu.`,
  `apac.`, `jp.`, `au.` — data stays in-geo) vs **global** (`global.` — any commercial region,
  ~10% cheaper, requires SCP allowance for unspecified region). Provisioned throughput is NOT
  compatible with inference profiles. Source: cross-region-inference.html, accessed 2026-08-14.
- **Provisioned throughput** for guaranteed capacity / customized models.
- **Batch** (S3-in/S3-out JSONL) for offline at 50%.
- **PrivateLink** VPC interface endpoints for private connectivity; CloudWatch metrics +
  CloudTrail + model-invocation logging (S3/CloudWatch) for ops; mantle gained CloudWatch metrics
  2026-06.
- **Guardrails** apply at Converse/InvokeModel via `guardrailConfig`, standalone via `ApplyGuardrail`
  (works even on non-Bedrock models), and include content/topic/word/PII filters, contextual
  grounding checks, and Automated Reasoning checks. Not available on mantle endpoint (endpoints.html).

## 6.16 Region availability & data residency

Bedrock is live in 30+ commercial regions plus GovCloud, but **model availability is strictly
model-by-region**. Do not assume any model exists in your region: consult the per-model
"Regional availability" section of each model card (docs.aws.amazon.com/bedrock/latest/userguide/
model-cards.html → model page), which distinguishes *in-region*, *geo cross-region*, and *global*
access. Patterns observed 2026-08-14: newest Anthropic models keep small in-region footprints
(us-east-1, eu-north-1, eu-west-1, ap-southeast-4, us-gov-west-1 for Sonnet 5) and rely on
profiles; Nova 2 Lite is **profile-only** (no in-region deployment); GPT-5.6 is US-only with no
profiles. Data residency: in-region invocation keeps inference in-region; geographic profiles keep
it in-geography; global profiles process anywhere on AWS's network (encrypted in transit;
processing region logged in CloudTrail `additionalEventData.inferenceRegion`). AWS states prompts
and outputs are not stored for or shared with model providers and not used to train.

## 6.17 Security, compliance & SLA

- **SLA** (aws.amazon.com/bedrock/sla/, last updated 2023-10-04, accessed 2026-08-14): monthly
  uptime commitment **99.9%** [UNVERIFIED — commitment tier inferred from credit table; page
  sections rendered partially]; service credits: 10% (<99.9%), 25% (<99.0%), 100% (<95.0%),
  claims within two billing cycles.
- Compliance: Bedrock is in scope for SOC 1/2/3, ISO 27001/27017/27018/9001, PCI DSS, HIPAA
  eligibility, FedRAMP High (GovCloud) per AWS Services in Scope
  (aws.amazon.com/compliance/services-in-scope/, accessed 2026-08-14 — verify per certification).
- Encryption at rest (KMS, incl. customer-managed keys for customizations/KBs), TLS in transit,
  IAM/SCP governance, PrivateLink, CloudTrail audit.

## 6.18 Legacy models & migration notes

| Legacy | Status | Migrate to |
|---|---|---|
| Titan Text Express/Lite | removed from catalog | Nova 2 Lite / Nova Micro |
| Nova gen-1 Premier | EOL 2026-09-14³ | Nova 2 Lite / Claude |
| Nova Canvas/Reel/Sonic gen-1 | EOL 2026-09-30³ / Legacy | Stability / Luma Ray v2 / Nova 2 Sonic |
| Claude 3.x (3.5 Haiku, 3 Haiku) | listed, Legacy-tier | Haiku 4.5 |
| Claude Sonnet 4 / Opus 4.1 / 4.5 | superseded, still Active | Sonnet 5 / Opus 5 |
| Llama 3.2 / 3.1 405B | Legacy³ | Llama 4 Scout/Maverick |
| Cohere Command R/R+ | Legacy³ | (Cohere on Bedrock is now Embed/Rerank) |
| AI21 Jamba 1.5 | stale (2024) | — |
| Bedrock Agents (classic) | supported, de-emphasized | AgentCore |

³ = third-party catalog (hidekazu-konishi.com, 2026-05) — confirm dates on model cards. Migration
mechanics: model IDs are immutable; upgrades are explicit ID swaps. Converse-based code migrates
across vendors with minimal change; InvokeModel bodies do not. Anthropic model IDs dropped the
date/version suffix in the 5.x generation.

## 6.19 Task-suitability verdict

**Best for:** organizations already on AWS wanting frontier models (Claude 5, GPT-5.6, Llama 4,
Nova 2) under existing IAM/VPC/CloudTrail governance; multi-vendor A/B via one Converse schema;
regulated workloads needing data-residency-aware routing (geo profiles) and HIPAA/FedRAMP scope;
cost-tiered serving (batch 50%, Flex, caching, global profiles); production agents (AgentCore is
among the most complete managed agent runtimes as of 2026-08).

**Worst for:** day-zero access to vendor features (structured outputs, newest API features often
lag or are absent per model card — e.g. no structured outputs on Sonnet 5 runtime or GPT-5.6);
fine-tuning frontier models (not offered — only Nova/Llama/open-weights customization); simple
projects where SigV4/IAM setup is overhead (mitigated by Bedrock API keys + mantle); GPT-5.x
outside US regions. The per-model feature matrix is the recurring operational hazard: every
capability must be checked per model card, per region.

## 6.20 Sources

All accessed 2026-08-14.

Official (AWS/Anthropic):
- https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html (catalog)
- https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-anthropic-claude-sonnet-5.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-anthropic-claude-opus-5.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-amazon-nova-2-lite.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-56-sol.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/endpoints.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/inference-messages-api.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/reinforcement-fine-tuning.html
- https://aws.amazon.com/bedrock/pricing/
- https://aws.amazon.com/bedrock/sla/
- https://aws.amazon.com/bedrock/agentcore/
- https://aws.amazon.com/about-aws/whats-new/2025/10/amazon-bedrock-agentcore-available
- https://aws.amazon.com/about-aws/whats-new/2026/02/amazon-bedrock-adds-support-six-open-weights-models
- https://aws.amazon.com/about-aws/whats-new/2026/06/amazon-bedrock-openai-models-codex-generally-available/
- https://aws.amazon.com/about-aws/whats-new/2026/07/openai-gpt-terra-luna-pricing-bedrock/
- https://aws.amazon.com/about-aws/whats-new/2026/06/amazon-bedrock-redesigned-console-optimized-openai-anthropic-compatible-apis/
- https://platform.claude.com/docs/en/about-claude/pricing (Claude price parity + Bedrock premium note)

Third-party (labeled where used):
- https://hidekazu-konishi.com/entry/amazon_bedrock_model_catalog_2026.html (catalog snapshot 2026-05)
- https://www.cloudzero.com/blog/amazon-bedrock-pricing/ (2026-07 price roundup)
- https://cloudprice.net/models/global.amazon.nova-2-lite-v1:0 (Nova 2 Lite tier prices)


---

# 7. Azure AI Foundry (Microsoft Foundry)

> **Volatility warning.** Model lineups and pricing change frequently. Verified against official
> documentation on **2026-08-14**. Re-verify before production decisions.

## 7.1 Platform overview & positioning

**Naming (verify-first, per directive):** At Ignite (November 2025) Microsoft renamed **Azure AI
Foundry → Microsoft Foundry**. As of 2026-08 official docs use both names interchangeably; the doc
tree moved to `learn.microsoft.com/azure/foundry` with the older portal documented under
`learn.microsoft.com/azure/foundry-classic` ("Microsoft Foundry (classic) portal"). The portal is
`ai.azure.com`. Product-Terms entries were updated January 2026
(learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure;
schneider.im/microsoft-foundry-the-new-name-for-azure-ai-foundry/; samexpert.com
/microsoft-product-terms-january-2026/, accessed 2026-08-14). "Azure OpenAI Service" survives as
the name of the OpenAI-model subset ("Azure OpenAI in Microsoft Foundry Models") and of the
pricing page.

Foundry is Microsoft's managed multi-vendor model platform. Its catalog splits into two legally
distinct groups (models-sold-directly-by-azure + models-from-partners docs, accessed 2026-08-14):

```
Microsoft Foundry
├── Foundry Models SOLD DIRECTLY BY AZURE   ← Microsoft's own product terms, Azure billing,
│    Azure OpenAI (GPT-5.x era, audio,        Azure data-privacy commitments apply.
│    image, video), Microsoft Phi/MAI,        "Models do NOT interact with services operated
│    DeepSeek, Meta Llama, xAI Grok,          by the model's provider."
│    Mistral (subset), FLUX (BFL), Cohere
├── Models from PARTNERS & COMMUNITY        ← "Non-Microsoft Products"; Azure Marketplace
│    Anthropic Claude 5/4.x, Mistral,         billing; provider sets license + price.
│    Cohere, NTT tsuzumi, Stability, ...      Serverless (Global Standard / Data Zone) or
│                                             managed compute.
└── Foundry Local / managed compute / Foundry Labs (edge + BYO-GPU + research)
```

Differentiation vs OpenAI direct (the sibling chapter): same OpenAI model weights and (since the
v1 API) near-identical wire format, but **Azure-side deployment model** (you create named
*deployments* of a model version inside a Foundry/Azure OpenAI resource), Azure quotas per
subscription, Entra ID auth/RBAC, data-zone/regional data-processing options, Azure Marketplace
procurement, an uptime **and** PTU latency SLA, and Azure compliance scope. Azure-specific prices
can lag OpenAI's (see 7.5).

## 7.2 Current model catalog

Authoritative list: **"Foundry Models sold directly by Azure"**
(learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure,
last updated 2026-07-23, accessed 2026-08-14) plus **"Models from partners and community"**. The
table is the notable, practically usable subset (catalog is 100+ IDs). Prices: USD per 1M tokens,
**Global Standard** deployment; sources in 7.5. FT = fine-tuning on Azure.

| Model (deployment name) | Family | Context | Max out | Modalities in/out | Tools | Struct. out | FT | $ in / $ out per 1M |
|---|---|---|---|---|---|---|---|---|
| `gpt-5.6-sol` | GPT-5.6 | 1,050,000 (922K in) | 128K | text+image / text | Y | Y | N | 5.50 / 33.00¹ |
| `gpt-5.6-terra` | GPT-5.6 | 1,050,000 | 128K | text+image / text | Y | Y | N | 2.75 / 16.50¹ |
| `gpt-5.6-luna` | GPT-5.6 | 1,050,000 | 128K | text+image / text | Y | Y | N | 1.10 / 6.60¹ |
| `gpt-chat-latest` (preview) | GPT-chat | 128K | 16,384 | text / text | Y | Y | N | [UNVERIFIED] |
| `gpt-5.5` | GPT-5.5 | 1,050,000 | 128K | text+image / text | Y | Y | N | [UNVERIFIED] |
| `gpt-5.4` | GPT-5.4 | 1,050,000 | 128K | text+image / text | Y | Y | N | 2.50 / 15.00 (ext-ctx 5.00 / 22.50) |
| `gpt-5.4-pro` | GPT-5.4 | 1,050,000 | 128K | text+image / text | Y | Y | N | 30.00 / 180.00 |
| `gpt-5.4-mini` | GPT-5.4 | 400K (272K in) | 128K | text+image / text | Y | Y | N | [UNVERIFIED] |
| `gpt-5.4-nano` | GPT-5.4 | 400K | 128K | text / text | Y | Y | N | [UNVERIFIED] |
| `gpt-5.3-codex` / `gpt-5.2-codex` | Codex | 400K | — | text+image / text | Y | Y | N | [UNVERIFIED] |
| `gpt-5` (2025-08-07) | GPT-5 | 400K | 128K | text+image / text | Y | Y | Y (RFT, gated) | [UNVERIFIED] |
| `gpt-oss-120b` / `-20b` (preview) | gpt-oss | 131,072 | — | text / text | Y | Y | Y (20b SFT) | [UNVERIFIED] |
| `model-router` | Router | routes | routes | text(+image) / text | Y | Y | N | billed at routed model's rate |
| `o4-mini` / `o3` / `o3-pro` | o-series | 200K in/100K out | 100K | text(+image) / text | Y | Y | o4-mini RFT | [UNVERIFIED] |
| `gpt-4.1` / `-mini` / `-nano` | GPT-4.1 | 1,047,576 | 32,768 | text+image / text | Y | Y | Y (SFT/DPO) | [UNVERIFIED] |
| `computer-use-preview` | CUA | 8,192 | 1,024 | screen+text / actions | Y | N | N | [UNVERIFIED]; gated |
| `text-embedding-3-large` | Embeddings | 8,192 in | 3,072-d | text / vector | — | — | N | [UNVERIFIED] |
| `text-embedding-3-small` | Embeddings | 8,192 in | 1,536-d | text / vector | — | — | N | [UNVERIFIED] |
| `gpt-realtime-2.1` / `-mini` (2026-07-07) | Audio | 32K in/4K out | 4K | speech+text / speech+text | Y | N | N | token-billed, [UNVERIFIED] |
| `gpt-live-transcribe` (2026-07-29) | Audio | 32K in | — | speech / text | — | — | N | duration-billed, [UNVERIFIED] |
| `gpt-image-2`, `gpt-image-1.5` | Image | 4,000 chars | image | text+image / image | — | — | N | [UNVERIFIED]; 1.5 gated |
| `sora-2`, `sora` | Video | 4,000 chars | video | text/image/video / video | — | — | N | [UNVERIFIED] |
| `Phi-4` family (see 7.3) | Phi | 16K–128K | — | text(+image+audio) / text | varies | varies | N | MIT open weights; MaaS PAYG [UNVERIFIED] |
| `Phi-4-Reasoning-Vision` (15B) | Phi | [UNVERIFIED] | — | text+image / text | [UNVERIFIED] | — | N | [UNVERIFIED] |
| `DeepSeek-V4-Pro` | DeepSeek | 1,000,000 | 384K | text / text (reasoning) | Y | JSON | N | 2.00 / 8.00³ |
| `DeepSeek-V4-Flash` | DeepSeek | 1,000,000 | 384K | text / text (reasoning) | Y | JSON | N | 0.20 / 0.80³ |
| `DeepSeek-V3.2` / `-Speciale` | DeepSeek | 128K | 128K | text / text | Y | JSON | N | [UNVERIFIED] |
| `Llama-4-Maverick-17B-128E-Instruct-FP8` | Llama 4 | 1,000,000 | 1,000,000² | text+image / text | Y | Y | N | [UNVERIFIED] |
| `Llama-3.3-70B-Instruct` | Llama 3.3 | 128K | 8,192 | text / text | Y | Y | Y (SFT) | [UNVERIFIED] |
| Grok 4.2 (GA 2026-03-30) | xAI Grok | [UNVERIFIED] | — | text / text | Y | [UNVERIFIED] | N | [UNVERIFIED]³ |
| `Mistral-medium-2505`, `Codestral-2501`, `Ministral-3B` | Mistral | 128K / 262K / — | — | text / text | Y | Y | Ministral-3B SFT | [UNVERIFIED] |
| `claude-opus-5`, `claude-sonnet-5`, `claude-haiku-4-5` (partner) | Claude | up to 1M | up to 128K | text+image / text | Y | varies | N | [UNVERIFIED on Azure] |
| `Cohere-embed-v-4-0` | Embeddings | 512 tok + 2MP img | 256–1536-d | text+image / vector | — | — | N | [UNVERIFIED] |
| `FLUX.2-pro`, `FLUX.2-flex` (BFL) | Image | 32K prompt | image | text+image / image | — | — | N | [UNVERIFIED] |

¹ Rates actually billed on Azure as of 2026-08 per a Microsoft Q&A thread; OpenAI announced cuts
2026-07-30 (Luna −80%, Terra −20%) and Microsoft stated parity "effective August 1st", but
customers reported still being billed at the rates above mid-August
(learn.microsoft.com/en-us/answers/questions/5962521/, accessed 2026-08-14). A third-party tracker
already lists the reduced rates (Sol 5.00/30.00, Terra 2.00/12.00, Luna 0.20/1.20;
nops.io/blog/azure-ai-foundry-pricing/, accessed 2026-08-14). Re-verify at billing time.
² 1M max output as printed in the official model table — anomalous; re-verify.
³ Third-party (nops.io) figures; nops lists "Grok 4.5" and "DeepSeek-V4" prices — Grok 4.5 not yet
confirmed in Microsoft docs (Grok 4.2 GA per devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-mar-2026/).

Also in catalog, not tabled: GPT-5.1/5.2/5.3 series tail, GPT-4o line, `codex-mini`, whisper/tts,
`gpt-4o-transcribe-diarize`, `gpt-realtime-translate`/`-whisper` (duration-billed), MAI-Image /
MAI-Thinking / MAI-Voice (via Speech), healthcare models, NVIDIA Nemotron (GA 2026-03), Fireworks
AI collection (DeepSeek V3.2, Kimi K2.5, MiniMax M2.5, preview), NTT `tsuzumi-7b`, Cohere
Command A / rerank v4.0. Sources: models-sold-directly-by-azure, models-from-partners, Foundry
March-2026 blog (accessed 2026-08-14).

## 7.3 Model details & limitations

**GPT-5.6 (sol / terra / luna)** — current flagship trio (training data June 2026): 1,050,000
context (922K input cap), 128K output, reasoning, Responses + Chat Completions, structured
outputs, computer use, and "multi-agent" orchestration capability. Token budget is shared: input +
reasoning + output all draw on the same window; e.g. on the 5.5/5.6-class Responses API a
921,549-token prompt leaves only ~451 tokens of generation (formula: available_generation =
922,000 − prompt_tokens). Default quota only for tenants in quota Tiers 5–6; others must request
(models-sold-directly-by-azure, accessed 2026-08-14).

**gpt-chat-latest (preview)** — continuously updated consumer-style chat alias (snapshots
2026-06-24 etc.), 128K/16,384. Preview: auto-upgrades, not for production pinning.

**GPT-5.5 / GPT-5.4 line** — GPT-5.5 (2026-04-24): 1.05M/128K. GPT-5.4 GA 2026-03-05 with
integrated computer use; `-pro` for maximum analysis depth; `-mini`/`-nano` at 400K (272K input)
for classification/extraction (Foundry Mar-2026 blog, accessed 2026-08-14).

**Codex line** (`gpt-5.3-codex`, `gpt-5.2-codex`, `gpt-5.1-codex[-mini|-max]`, `gpt-5-codex`) —
Responses-API-only coding models for Codex CLI / VS Code; `gpt-5.1-codex-max` supports
`reasoning_effort: xhigh`. **Reasoning gotcha:** `gpt-5.1`+ default `reasoning_effort` is `none`
— set it explicitly; reasoning models reject `temperature`/`top_p`.

**GPT-4.1 known issue** — documented failure with tool definitions >300K tokens even inside the
1M window (`context_length_exceeded` / `string_above_max_length` on Chat Completions; HTTP 500 on
Responses). Provisioned GPT-4.1 deployments cap context at 128K (spillover available).

**gpt-oss-120b/20b** — OpenAI open-weight (Apache-2.0), preview on Foundry; 20b runs on managed
compute and **Foundry Local** (on-device); 20b is SFT-fine-tunable (preview).

**model-router** — GA 2025-08; a deployable meta-model that auto-selects the underlying chat
model (supports GPT-5 series); you pay the routed model's price.

**Microsoft Phi (current state)** — Phi-4 generation is current: `Phi-4` (14B-class reasoning/math
SLM), `Phi-4-mini-instruct`, `Phi-4-multimodal-instruct` (text+image+audio in), `Phi-4-reasoning`,
`Phi-4-mini-reasoning`, and **Phi-4-Reasoning-Vision 15B** (announced 2026-03-04, multimodal
chain-of-thought). MIT-licensed open weights; run serverless (MaaS PAYG), on managed compute, via
Hugging Face/Ollama, or on-device via Foundry Local. No Phi-5 announced as of 2026-08-14
[UNVERIFIED beyond absence in docs]. Microsoft first-party **MAI** models (MAI-Image,
MAI-Thinking; MAI-Voice-1/MAI-Transcribe via Speech) now sit alongside Phi
(azure.microsoft.com/en-us/products/phi; techcommunity.microsoft.com Phi-4-Reasoning-Vision post;
models-sold-directly-by-azure, accessed 2026-08-14).

**Third-party highlights** — DeepSeek-V4-Pro/Flash: 1M context, 384K output reasoning models sold
directly by Azure (Azure privacy terms apply; weights never talk to DeepSeek). Llama-4-Maverick
17B-128E FP8: 1M-context multimodal. Grok 4.2 GA 2026-03-30. Mistral: Medium 2505 / Codestral
2501 / Ministral-3B (partner, Marketplace-billed). **Anthropic Claude** (opus-5, sonnet-5,
fable-5/mythos-5, 4.x tail) is listed as a partner model, hosted "on Azure or Anthropic
infrastructure" — different privacy posture than Azure-direct models; check terms
(models-from-partners, accessed 2026-08-14).

## 7.4 Embedding / audio / vision / video models

- **Embeddings**: `text-embedding-3-large` (3,072-d), `-small` (1,536-d), both 8,192-token input,
  `dimensions` parameter supported; `text-embedding-ada-002` legacy. Limits: 2,048 array items and
  300K tokens per request. Cohere `embed-v-4-0` (Matryoshka 256–1536-d, text+image) as
  alternative. (models-sold-directly-by-azure; quotas-limits, accessed 2026-08-14.)
- **Audio**: current recommended stack is `gpt-realtime-2.1`/`-2.1-mini` (2026-07-07,
  speech-to-speech, improved silence/noise handling), `gpt-audio-1.5` (2026-02-23, audio gen),
  `gpt-live-transcribe` (2026-07-29, recommended streaming STT), `gpt-realtime-translate` and
  `gpt-realtime-whisper` (2026-05-06). Billing split: translate/whisper/live-transcribe are
  **duration-billed**, the rest token-billed. File STT: `whisper`, `gpt-transcribe`,
  `gpt-4o-transcribe(-diarize)` (25 MB cap). TTS: `tts(-hd)`, `gpt-4o-mini-tts`. Realtime API has
  WebRTC (2025-04) and SIP telephony (2025-10) transports.
- **Image**: `gpt-image-2`, `gpt-image-1.5` (limited access, high input-fidelity editing, ≤
  1024×1536), `gpt-image-1(-mini)`; BFL `FLUX.2-pro`/`FLUX.2-flex`/`FLUX.1-Kontext-pro` via
  `/images/generations` + `/images/edits`; MAI-Image.
- **Video**: `sora-2` (new) and `sora` (preview): text-, image- (2025-08) and video-to-video
  (2025-09) generation.

## 7.5 Pricing model & cost notes

Official price source: azure.microsoft.com/en-us/pricing/details/azure-openai/ — the page is
calculator-driven and rendered "$-" without region selection at access time (2026-08-14), so most
per-model numbers above come from Microsoft blog/Q&A posts or are [UNVERIFIED]. Structure
(verified from the pricing page + deployment-types doc):

- **Three price tiers by deployment type**: Global (cheapest) < Data Zone < Regional Standard.
  Provisioned (PTU) is capacity-priced; Batch is token-priced at **50% of Standard** with 24-h
  target turnaround. A **Priority Processing** lane (preview, 2026-03) adds a premium
  latency-sensitive tier.
- **Prompt caching**: cached input discounted (per-model %). **Note:** "Cache write charges are
  not active yet"; billing for cache writes starts **on or after 2026-08-21** — a live pricing
  change (pricing page, accessed 2026-08-14).
- **PTU (Provisioned Throughput Units)**: you buy model-agnostic PTU capacity per deployment
  (Global/Data Zone/Regional Provisioned SKUs), billed hourly, with **monthly and annual Azure
  Reservations** at substantial discounts (rates [UNVERIFIED — calculator only]). Each model has
  a minimum PTU size and tokens-per-PTU throughput table; capacity calculator in the Foundry
  portal. **Spillover** (GA 2025-08) routes overflow from a provisioned deployment to a standard
  deployment automatically.
- **GPT-5.6 parity lag**: OpenAI's 2026-07-30 cuts (Luna −80%, Terra −20%, Sol "Fast Mode")
  announced for Azure "effective August 1st" but billing still at old rates mid-August per
  customer reports — budget at old rates until invoices confirm (MS Q&A 5962521, accessed
  2026-08-14).
- **Partner models** (Claude, Mistral, Cohere, …): billed via **Azure Marketplace** at
  provider-set prices; unavailable on free/student/CSP subscriptions.
- **Fine-tuned model hosting** is charged per-hour while deployed (≈$120/day per third-party
  estimate, [UNVERIFIED official rate]); Developer-tier deployments avoid hosting cost but
  expire after 24 h.
- Agent Service: prompt agents = inference + tool usage; hosted agents add container compute
  (agents/overview, accessed 2026-08-14).

## 7.6 Authentication & environment

Two mechanisms on every Foundry/Azure OpenAI resource:

1. **API keys** — two rotatable keys per resource; sent as `api-key: $AZURE_OPENAI_API_KEY`
   header (legacy dated API) or as bearer/`api_key` in the v1 API.
2. **Microsoft Entra ID (recommended)** — RBAC roles (`Cognitive Services OpenAI User`/
   `Contributor`, `Azure AI User`) on the resource; tokens via `azure-identity`
   `DefaultAzureCredential` (supports managed identity, workload identity, CLI login). Token
   scope for the v1 API: `https://ai.azure.com/.default` (older docs:
   `https://cognitiveservices.azure.com/.default`). Keys can be disabled resource-wide for
   Entra-only posture (api-version-lifecycle doc, accessed 2026-08-14).

```bash
export AZURE_OPENAI_API_KEY="$API_KEY"            # if using keys
export OPENAI_BASE_URL="https://YOUR-RESOURCE.openai.azure.com/openai/v1/"
export OPENAI_API_KEY="$AZURE_OPENAI_API_KEY"     # lets plain OpenAI() client work unchanged
```

Agent-side auth adds Entra **Agent Identity**, managed identity, and OAuth identity passthrough
for MCP tools (Foundry Mar-2026 blog).

## 7.7 API endpoints & schemas

**Current scheme — v1 API (GA since 2025-08):** no `api-version` parameter; continuous feature
delivery; plain `openai` clients work.

```
Base URLs (both valid):
  https://<resource>.openai.azure.com/openai/v1/
  https://<resource>.services.ai.azure.com/openai/v1/

Main endpoints under the base:
  POST /responses               ← primary (Responses API; agents build on it)
  POST /chat/completions
  POST /embeddings
  POST /images/generations | /images/edits
  POST /audio/transcriptions | /audio/speech ; WS/WebRTC /realtime
  POST /batches ; /files ; /fine_tuning/jobs ; /evals
```

Key Azure difference vs OpenAI direct: `model` refers to your **deployment name** (which you
chose at deployment time), not necessarily the upstream model id. Preview features are opted into
via headers (e.g. `"aoai-evals": "preview"` historically) or `/alpha/` path segments instead of
dated api-versions. **Legacy scheme** (still supported): `https://<resource>.openai.azure.com/
openai/deployments/<deployment>/chat/completions?api-version=2024-10-21` with `AzureOpenAI()`
clients — migrate off it. OpenAPI 3.0 spec: github.com/Azure/azure-rest-api-specs
`.../OpenAI.v1/azure-v1-v1-generated.json`. (api-version-lifecycle, accessed 2026-08-14.)
Request/response JSON bodies are wire-identical to OpenAI's Responses/Chat Completions schemas
plus Azure extensions (`content_filter_results`, On Your Data `data_sources`).

## 7.8 SDK integration

**Python (openai ≥1.x, v1 API):**

```python
import os
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default")

client = OpenAI(
    base_url="https://YOUR-RESOURCE.openai.azure.com/openai/v1/",
    api_key=token_provider)                    # or api_key=os.environ["AZURE_OPENAI_API_KEY"]

resp = client.responses.create(model="gpt-5.4",          # deployment name
                               input="Summarize RFC 9110 in 3 bullets.")
print(resp.output_text)
```

**JavaScript/TypeScript (openai pkg):**

```javascript
import OpenAI from "openai";
const client = new OpenAI({
  baseURL: "https://YOUR-RESOURCE.openai.azure.com/openai/v1/",
  apiKey: process.env.AZURE_OPENAI_API_KEY,   // or Entra bearer via @azure/identity
});
const r = await client.responses.create({ model: "gpt-5.4", input: "Hello" });
console.log(r.output_text);
```

**curl:**

```bash
curl "https://YOUR-RESOURCE.openai.azure.com/openai/v1/responses" \
  -H "Authorization: Bearer $AZURE_OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-5.4","input":"ping"}'
```

**Azure-native SDKs:** `azure-ai-projects` 2.0.x (Python, 2026-03; bundles `openai` +
`azure-identity`, constructor-level `allow_preview=True`, agents unified under
`AIProjectClient`), `@azure/ai-projects` 2.0.x (JS), `Azure.AI.Projects` 2.0 (.NET, GA
2026-04-01), `azure-ai-projects` 2.0 Java (first stable, 2026-03-27). Use these for
projects/agents/evals/connections; use the `openai` client for raw inference. (Foundry Mar-2026
blog, accessed 2026-08-14.)

## 7.9 Streaming, tool use, structured output

```python
# Streaming (Responses API)
with client.responses.stream(model="gpt-5.4", input="Write a haiku") as stream:
    for event in stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="")

# Tool use
tools = [{"type": "function", "name": "get_weather",
          "parameters": {"type": "object",
                         "properties": {"city": {"type": "string"}},
                         "required": ["city"]}}]
r = client.responses.create(model="gpt-5.4", input="Weather in Oslo?", tools=tools)
# → r.output contains a function_call item; execute, then send
#   {"type":"function_call_output","call_id":..., "output":...} in a follow-up call.

# Structured output (JSON schema)
r = client.responses.create(
    model="gpt-5.4", input="Extract: 'Ada, 36, Oslo'",
    text={"format": {"type": "json_schema", "name": "person", "strict": True,
          "schema": {"type": "object", "properties": {
              "name": {"type": "string"}, "age": {"type": "integer"},
              "city": {"type": "string"}},
              "required": ["name", "age", "city"], "additionalProperties": False}}})
```

Shapes match the OpenAI Responses API (wire-compatible per Foundry Agent Service docs); verified
against the v1 lifecycle doc's client pattern, not re-tested per-parameter — treat the
`text.format` block as OpenAI-current. Reasoning models: use `reasoning: {"effort": "high"}`
(Responses) / `reasoning_effort` (Chat Completions); remember `gpt-5.1`+ defaults to `none`.

## 7.10 Error handling & retry

| HTTP | Azure meaning | Action |
|---|---|---|
| 400 `content_filter` | Prompt blocked by content filter (see 7.17); details in `content_filter_results` | Don't retry unchanged; surface policy error |
| 401 | Bad key / missing token | Fix auth; check key not disabled |
| 403 | Entra RBAC denied / network (VNet, private endpoint) rules | Assign `Azure AI User` role; check firewall |
| 404 `DeploymentNotFound` | Deployment name wrong or not yet propagated | Verify deployment name (not model id) |
| 408/5xx | Transient | Retry with backoff |
| 429 | TPM/RPM exceeded, **or monthly usage-tier exceeded, or regional capacity strain** | Honor `Retry-After`; exponential backoff; consider PTU/spillover |

Streaming responses can terminate with `finish_reason: "content_filter"` mid-stream — always
check `finish_reason`. Filtered completions return `finish_reason:"content_filter"` instead of
`stop`. Retry pattern: exponential backoff w/ jitter (docs show `tenacity`), gradual ramp-up, and
quota-increase request at aka.ms/oai/stuquotarequest (quotas-limits; content-filter docs,
accessed 2026-08-14).

## 7.11 Rate limits & quotas

Model changed materially on **2026-05-07** (quotas-limits doc, accessed 2026-08-14):

- **Subscription-scoped pools**: Global Standard quota for a model/version is one pool across all
  regions per subscription; Data Zone Standard pools per data zone. Deployments share the pool
  (no per-deployment carve-out).
- **7 quota tiers** (Free, 1–6) assigned per subscription from usage, EA/MCA-E relationship, and
  payment history; **auto-upgrade** as you approach limits (opt-out via
  `quotaTiers` PATCH `tierUpgradePolicy: NoAutoUpgrade`,
  api-version `2025-10-01-preview`). GPT-5.6/5.5 default quota only at Tiers 5–6.
- Sample Tier-1 defaults: `gpt-5` Global Standard 10K RPM / 1M TPM; `gpt-4o-mini` 20K RPM / 2M
  TPM; `o3-mini` 5M TPM.
- **Usage tiers** (2026): per-tenant *monthly* token ceilings per model (e.g. gpt-5 32B,
  gpt-5.1 86B, gpt-5.4 50B, gpt-4o-mini 85B tokens/month); exceeding them brings latency
  variability and 429s even under TPM. Standard-family only (not Batch/PTU).
- **Batch quota** in enqueued tokens (e.g. gpt-5: 5B Enterprise / 200M default / 50M credit-card);
  file limits 200 MB (1 GB BYOS), 100K requests/file.
- Resource limits: 30 Azure OpenAI resources/subscription, 32 standard deployments/resource,
  embeddings ≤2,048 inputs & ≤300K tokens/request.

## 7.12 Fine-tuning & customization

Methods: **SFT**, **DPO**, **RFT** (fine-tuning table in models-sold-directly-by-azure, accessed
2026-08-14). Current matrix (GA unless noted): `gpt-4.1`/`-mini`/`-nano` (SFT+DPO), `gpt-4o`,
`gpt-4o-mini` (SFT[/DPO]), `o4-mini` (RFT), **`gpt-5` (RFT, invitation-gated)**; preview:
`Ministral-3B`, `Qwen-32B`, `Llama-3.3-70B-Instruct`, `gpt-oss-20b` (SFT, Global-only).
Training location options: **regional** (North Central US, Sweden Central, East US2 typical),
**Global Training** (cheaper, no residency guarantee), **Developer tier** (evaluation-only
deployments, 24-hour lifetime, no SLA). Limits: ≤720 h/job, ≤2B training tokens. Hosted
fine-tuned deployments: ≤10/resource, billed hourly while deployed. A Fine-Tuning CLI with cost
estimation shipped 2026-03. Stored Completions API captures production traffic for distillation/
eval sets. Prices per-model on the pricing calculator [UNVERIFIED here].

## 7.13 RAG & embedding pipeline notes

Canonical Azure pattern: `text-embedding-3-*` (or Cohere embed v4) → **Azure AI Search**
(vector + hybrid + semantic ranker) → grounded generation, either client-side, via the **On Your
Data** `data_sources` extension, or via Agent Service **File search** tool (managed chunking/
embedding/vector store). Groundedness detection content filter (streaming, select regions:
Central US, East US, France Central, Canada East) can flag ungrounded claims at generation time.
Batch API at 50% is well suited to corpus embedding; mind the 300K-token/request embeddings cap
and 2,048-item array cap. Third-party cost anchor for a typical production RAG stack: AI Search
$150–300/mo (nops.io, third-party, accessed 2026-08-14).

## 7.14 Agent support

**Microsoft Foundry Agent Service** (GA; formerly "Azure AI Agent Service") — built **on the
Responses API, wire-compatible with OpenAI agents** (agents/overview, updated 2026-06-02; Foundry
Mar-2026 blog, accessed 2026-08-14):

- **Prompt agents** (fully managed, declarative) and **hosted agents** (your code — Microsoft
  Agent Framework, LangGraph, OpenAI Agents SDK, Anthropic SDK — run in managed containers).
- Tools: web search (preview), file search, code interpreter, memory (preview), custom functions,
  **MCP servers** (remote + Azure Functions; centrally managed versioned "Toolbox"); MCP auth via
  key, Entra Agent Identity, managed identity, OAuth passthrough. **A2A protocol** in preview.
- Non-OpenAI models supported (DeepSeek, Llama, xAI, etc.). Each agent can get its own **Entra
  Agent Identity**; BYO-VNet end-to-end private networking (2026-03); tracing GA, Evaluations GA
  with continuous monitoring to Azure Monitor; guardrails incl. Task Adherence and tool-call/
  tool-response intervention points plus third-party (Prisma AIRS, Zenity) integrations.
- Distribution to Teams / M365 Copilot / Entra Agent Registry. Pricing: inference + tool usage
  (+ container compute for hosted).
- The old **Assistants API** remains preview-only for legacy gpt-4o versions in select regions —
  treat as legacy (see 7.18).

## 7.15 Deployment patterns

Deployment-type matrix (deployment-types doc, accessed 2026-08-14):

| Type (SKU) | Processing | Billing | Notes |
|---|---|---|---|
| Global Standard (`GlobalStandard`) | any Azure region | per-token | Default; new models land here first; biggest quota |
| Data Zone Standard (`DataZoneStandard`) | within US / EU / APAC zone | per-token | Residency middle ground |
| Standard (`Standard`) | single region | per-token | Regional compliance; fewer models |
| Global Provisioned (`GlobalProvisionedManaged`) | any region | PTU-hour / reservation | Guaranteed throughput + latency SLA |
| Data Zone Provisioned (`DataZoneProvisionedManaged`) | zone | PTU | |
| Regional Provisioned (`ProvisionedManaged`) | region | PTU | Limited regions |
| Global / Data Zone Batch (`GlobalBatch`/`DataZoneBatch`) | any / zone | −50% tokens | 24-h target, no realtime SLA |
| Developer (`DeveloperTier`) | any | per-token | FT evaluation only; 24-h life; no SLA |

Beyond serverless: **managed compute** (dedicated VMs for open/community models incl. BYO
weights via Fireworks collection), **Foundry Local** (on-device/edge runtime — e.g.
`gpt-oss-20b`, Phi), **spillover** PTU→Standard, **Model Router** for cost-routing, and
**Priority Processing** (preview). Control plane: Foundry Control Plane ARM API (2026-03) unifies
agents/models/tools management.

## 7.16 Region availability & data residency

Approach: availability is **per model × per deployment type**, enumerated in "Region availability
for Foundry Models sold by Azure" — always check that page, not marketing region lists. ~27+
regions carry Standard SKUs (Australia East … West US3); fine-tuning restricted to a handful
(North Central US, Sweden Central, East US2 + Global). Data zones: **US**, **EU** (and APAC per
deployment-types doc). Documented residency commitments (data-privacy legal doc, updated
2026-05-18, accessed 2026-08-14): **data at rest always stays in the customer-designated
geography** for every deployment type; *processing* location varies — Global = any Azure region,
Data Zone = within zone, Standard/Regional Provisioned = in-region. Abuse-monitoring stores are
kept in the resource's geography; EEA resources get EEA-located human reviewers. Azure Government
has separate docs/filters.

## 7.17 Security, compliance & SLA

- **Data privacy (documented commitments):** prompts/completions are not available to OpenAI or
  other model providers, not used to train foundation models, models are stateless;
  fine-tuning data never trains base models. Flagged content may be stored for human abuse
  review (geography-local, SAW + JIT access); **Modified Abuse Monitoring** opt-out removes
  storage/human review (automated review remains) — verify via the `ContentLogging:false`
  resource attribute. AES-256 at rest, CMK optional
  (learn.microsoft.com/en-us/legal/cognitive-services/openai/data-privacy, accessed 2026-08-14).
- **Content filtering / Responsible AI layer** (Azure AI Content Safety, on by default for
  Azure-direct models; Whisper exempt): hate/sexual/violence/self-harm at 4 severity levels
  (default blocks low+), Prompt Shields (jailbreak + indirect injection, incl. spotlighting),
  Protected Material text/code, PII detection (2025-10), Groundedness (streaming, select
  regions), blocklists; **modified/disabled filters require Microsoft approval**
  (ncv.microsoft.com form); request-level filter configs supported. 2026 UI: "Guardrails +
  controls" in the portal; agent-specific Task Adherence and tool-call guardrails
  (content-filter doc, accessed 2026-08-14). This filtering layer is a real behavioral delta vs
  OpenAI direct: identical models can refuse/400 differently on Azure.
- **SLA:** Microsoft publishes SLAs for online services at
  microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services. For Azure
  OpenAI/Foundry Models: **99.9% monthly availability**, credits 10%/25% below 99.9%/99%; plus a
  **latency SLA for Provisioned deployments** (99% of 5-min windows meeting per-model
  tokens-per-second floors, e.g. 25 t/s on gpt-4o) — figures corroborated via third-party SLA
  analysis (redresscompliance.com/azure-openai-sla-and-support, accessed 2026-08-14); confirm
  exact current text in the licensing document before contracting. Batch and Developer tiers:
  no SLA.
- **Compliance:** Azure platform certification portfolio (ISO 27001/27017/27018, SOC 1/2/3,
  HIPAA BAA, FedRAMP High for Azure Government, EU Data Boundary) applies per the Microsoft
  Trust Center / Service Trust Portal; per-service scope statements there [specific per-cert
  scope for Foundry not re-verified here].

## 7.18 Legacy models & migration notes

- **API**: dated `api-version` scheme + `AzureOpenAI()` clients → migrate to **v1** base URL +
  plain `OpenAI()` clients (7.7). Assistants API (preview, legacy gpt-4o/gpt-4/3.5 only, 11
  regions) → **Responses API / Agent Service**.
- **Models**: GPT-4o/4.1/o1/o3 generations remain deployable but are pre-GPT-5-era; GPT-4.5
  Preview, o1-preview, gpt-3.5-turbo, DALL-E 3, ada-002 are legacy — consult "model retirements"
  page for dates (not re-verified). Preview-tagged models auto-upgrade and are unfit for
  production pinning.
- **Platform**: Azure AI Studio → Azure AI Foundry (2024) → Microsoft Foundry (2025-11); classic
  portal/docs live under `/azure/foundry-classic`. **PromptFlow deprecated** (migrate to
  Framework Workflows by 2027-04-20); Azure ML "Import Data" connections and low-priority VMs
  deprecated 2026-03; new managed VNets lose default internet egress after 2026-03-31 (Foundry
  Mar-2026 blog, accessed 2026-08-14).

## 7.19 Task-suitability verdict

**Best when:** you want OpenAI's current frontier line (GPT-5.6 sol/terra/luna, Codex, realtime
audio, Sora 2) under Azure governance — Entra ID/RBAC, VNet privacy, data-zone processing,
uptime + PTU-latency SLA, Marketplace procurement; enterprise agent platforms (Agent Service is
the most complete managed agent runtime of the clouds surveyed: Responses-wire-compatible, MCP +
A2A, per-agent Entra identity, M365 distribution); regulated workloads needing EU/US data-zone
processing; hybrid/edge SLM deployment (Phi + Foundry Local); using DeepSeek/Grok-class models
under Microsoft's no-provider-access privacy terms.

**Worst when:** you need day-zero OpenAI price parity (documented 2-week+ lag on the 2026-07
cuts) or day-zero features (Azure trails OpenAI direct on some launches); ungated permissive
content generation (default filters + approval gates for modification add refusals and latency);
simple low-ops prototyping (resource/deployment/quota-tier machinery is heavyweight vs a single
OpenAI key); breadth of non-OpenAI frontier models (Anthropic presence is partner-tier —
Bedrock/Anthropic-direct are more natural Claude homes); predictable throughput without capacity
planning (usage tiers + tier-gated GPT-5.6 quota surprise teams at scale).

## 7.20 Sources (all accessed 2026-08-14)

1. learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure (updated 2026-07-23)
2. learn.microsoft.com/en-us/azure/ai-foundry/foundry-models/concepts/models-from-partners
3. learn.microsoft.com/en-us/azure/foundry-classic/openai/whats-new
4. learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/deployment-types
5. learn.microsoft.com/en-us/azure/ai-foundry/openai/api-version-lifecycle (updated 2026-05-13)
6. learn.microsoft.com/en-us/azure/ai-foundry/openai/quotas-limits
7. learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/content-filter
8. learn.microsoft.com/en-us/azure/ai-foundry/agents/overview (updated 2026-06-02)
9. learn.microsoft.com/en-us/legal/cognitive-services/openai/data-privacy (updated 2026-05-18)
10. learn.microsoft.com/en-us/answers/questions/5962521/pricing-of-openai-gpt-5-6-models-luna-terra (GPT-5.6 Azure pricing thread)
11. devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-mar-2026/
12. azure.microsoft.com/en-us/pricing/details/azure-openai/ (calculator-driven; cache-write billing note)
13. azure.microsoft.com/en-us/products/phi/
14. techcommunity.microsoft.com/blog/azure-ai-foundry-blog/introducing-phi-4-reasoning-vision-to-microsoft-foundry/4499154 (2026-03-04)
15. Third-party (labeled): nops.io/blog/azure-ai-foundry-pricing/; redresscompliance.com/azure-openai-sla-and-support; schneider.im/microsoft-foundry-the-new-name-for-azure-ai-foundry/; samexpert.com/microsoft-product-terms-january-2026/
16. microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services (SLA of record; exact current text not re-fetched)


---

# 8. OpenRouter

> **Volatility warning.** Model lineups and pricing change frequently — on OpenRouter *daily*, because the
> catalog is dynamic and pricing is set per underlying provider endpoint. Verified against official
> documentation and the live `GET /api/v1/models` response on **2026-08-14**. Re-verify before production
> decisions; prefer querying the models API (§8.7) over any static table, including the one in §8.2.

## 8.1 Platform overview & positioning

OpenRouter (https://openrouter.ai) is an **aggregation/routing layer**, not a model lab. It fronts
hundreds of models from many labs (OpenAI, Anthropic, Google, xAI, DeepSeek, Qwen/Alibaba, Moonshot,
Z.AI, MiniMax, Mistral, Meta, NVIDIA, and many smaller ones) behind **one OpenAI-compatible API and one
API key**, and routes each request to one of possibly several **provider endpoints** serving that model
(the lab's first-party API, or hosts like Together, Fireworks, Groq, DeepInfra, etc.).

```
your app ──> openrouter.ai/api/v1 ──router──> provider endpoint A (e.g. first-party)
             (one key, OpenAI schema)   ├────> provider endpoint B (e.g. Fireworks)
                                        └────> provider endpoint C (fallback)
```

What OpenRouter adds vs going direct:
- **One key, one schema** for every lab; switching models is a string change.
- **Fallback resilience**: multi-provider load balancing, automatic failover, model fallback arrays.
- **Live price/perf routing**: cheapest or fastest endpoint per request (`sort`, `:nitro`, `:floor`).
- **Pass-through inference pricing**: "no markup on inference pricing"; the platform monetizes via a fee
  on credit purchases and on BYOK usage (§8.5). (FAQ, https://openrouter.ai/docs/faq, accessed 2026-08-14.)
- Uniform surface for tool use, structured outputs, caching, and usage accounting across labs.

Tradeoffs (honest):
- **An added network hop** (edge-routed; adds latency vs calling the lab directly — magnitude not
  officially published, [UNVERIFIED]).
- **Feature lag / lowest-common-denominator risk** on provider-specific capabilities: OpenRouter exposes
  the OpenAI Chat Completions shape; lab-native APIs (Anthropic Messages beta headers, OpenAI Responses-API
  specifics, Gemini video-tuning knobs, realtime/audio sockets) arrive later or not at all.
- **Two operational dependencies** instead of one; OpenRouter outages affect all your models at once.
- Occasional **price-sync lag** between OpenRouter listings and lab list prices (observed at access date,
  §8.2 notes).

## 8.2 Current model catalog

**The real catalog is dynamic** — ~300+ models (100+ visible in the first page of the API response alone);
enumerate it live via `GET https://openrouter.ai/api/v1/models` (schema in §8.7). Below is a **curated
subset** of notable models by tier, exactly as listed by the live API and official model pages on
2026-08-14. Prices are USD per 1M tokens (OpenRouter returns per-token strings; converted here).
Variant suffixes: `:free`, `:batch`, `:nitro`, `:floor`, `:online` (§8.5, §8.7); `~author/…-latest` =
evergreen alias tracking a lab's newest model (observed in catalog; semantics per OpenRouter blog,
https://openrouter.ai/blog/tutorials/codex-cli-openrouter/, accessed 2026-08-14).

| OpenRouter model id | Lab / tier | Context | $ in / out per 1M | Notes |
|---|---|---|---|---|
| `openai/gpt-5.6-sol` | OpenAI frontier | 1,050,000 | 5.00 / 30.00 | ⚠ OpenAI direct lists 2.50/15.00 after a July 2026 price drop (see ch. 3); OpenRouter listing appears to lag — MEDIUM confidence |
| `openai/gpt-5.6-terra` | OpenAI mid | 1,050,000 | 1.00 / 6.00 | matches OpenAI direct |
| `openai/gpt-5.6-luna` | OpenAI small | 1,050,000 | 0.10 / 0.60 | matches OpenAI direct |
| `openai/gpt-5.3-codex` | OpenAI agentic coding | 400,000 | 1.75 / 14.00 | |
| `anthropic/claude-fable-5` | Anthropic frontier | 1,000,000 | 10.00 / 50.00 | `:batch` 5.00/25.00 |
| `anthropic/claude-opus-5` | Anthropic frontier | 1,000,000 | 5.00 / 25.00 | `claude-opus-5-fast` 10.00/50.00; `:batch` 2.50/12.50 |
| `anthropic/claude-sonnet-5` | Anthropic mid | 1,000,000 | 2.00 / 10.00 | model page 2.00/10.00 (Anthropic intro pricing to 2026-08-31); API response showed 3.00/15.00 at access — MEDIUM, re-verify |
| `anthropic/claude-haiku-4.5` | Anthropic small | 200,000 | 1.00 / 5.00 | |
| `google/gemini-3.1-pro-preview` | Google frontier (preview) | 1,048,576 | 2.00 / 12.00 | `:batch` 1.00/6.00 |
| `google/gemini-3.7-flash` | Google fast frontier | 1,048,576 | 0.375 / 1.875 | released 2026-08-13; Google direct lists 0.75/3.75 promo — OpenRouter listing is *lower*; MEDIUM |
| `google/gemini-3.5-flash-lite` | Google budget | 1,048,576 | 0.30 / 2.50 | |
| `x-ai/grok-4.6` | xAI frontier | 500,000 | 2.00 / 6.00 | `~x-ai/grok-latest` alias, same price |
| `deepseek/deepseek-v4-pro-0813` | DeepSeek frontier | 1,048,576 | 0.435 / 0.87 | released 2026-08-13 |
| `deepseek/deepseek-v4-flash-0731` | DeepSeek fast | 1,048,576 | 0.14 / 0.28 | `~deepseek/deepseek-v4-flash-latest` listed 0.08/0.252 at access — MEDIUM |
| `qwen/qwen3.8-max` | Alibaba frontier | 1,000,000 | 2.00 / 6.00 | multimodal reasoning |
| `qwen/qwen3.7-flash` | Alibaba budget | 1,000,000 | 0.03 / 0.13 | |
| `moonshotai/kimi-k3` | Moonshot frontier | 1,048,576 | 3.00 / 15.00 | |
| `z-ai/glm-5.2` | Z.AI frontier | 1,048,576 | 0.392 / 1.232 | long-horizon agent workflows |
| `minimax/minimax-m3` | MiniMax frontier | 1,048,576 | 0.23 / 0.96 | `:batch` 0.15/0.60 |
| `mistralai/mistral-large-2512` | Mistral flagship (open-weight lineage) | 262,144 | 0.50 / 1.50 | sparse MoE, 41B active |
| `mistralai/mistral-medium-3-5` | Mistral proprietary mid | 262,144 | 1.50 / 7.50 | |
| `meta/muse-spark-1.2` | Meta frontier | 1,048,576 | 1.25 / 4.25 | Muse family (2026); weight availability [UNVERIFIED] |
| `meta/muse-glimmer-30b` | Meta small | 131,072 | 0.35 / 1.50 | |
| `openai/gpt-oss-120b` | OpenAI open-weight | 131,072 | 0.03 / 0.17 | Apache-2.0-era open weights |
| `nvidia/nemotron-3.5-lightning` | NVIDIA open, budget | 1,000,000 | 0.10 / 0.25 | 1M ctx at budget price |
| `openrouter/auto` | meta-router | n/a (`auto-beta`: 2,000,000) | billed at routed model's rate | picks model per prompt; no extra fee (docs, model-routing) |
| `nvidia/nemotron-3.5-lightning:free` | free tier | 1,000,000 | 0 / 0 | free-variant limits apply (§8.11) |
| `openai/gpt-oss-20b:free` | free tier | 131,072 | 0 / 0 | |
| `google/gemma-4-31b-it:free` | free tier (open-weight) | 262,144 | 0 / 0 | paid variant 0.08/0.35 |
| `poolside/laguna-s-2.1:free` | free tier | 262,144 | 0 / 0 | paid variant 0.09/0.18 |

Sources: `GET https://openrouter.ai/api/v1/models` (live JSON), https://openrouter.ai/anthropic/,
https://openrouter.ai/openai/, https://openrouter.ai/google/, https://openrouter.ai/deepseek/,
https://openrouter.ai/qwen/, https://openrouter.ai/z-ai/, https://openrouter.ai/minimax/,
https://openrouter.ai/mistralai/ — all accessed 2026-08-14. Ultra-budget honorable mentions observed in
the live catalog: `upstage/solar-pro4` (0.03/0.12, 524K ctx), `inclusionai/ling-3.0-flash` (0.021/0.063).

## 8.3 Model details & limitations

- **Same model ≠ same behavior everywhere.** A model id can be served by several provider endpoints with
  different context lengths, quantizations (`int4/int8/fp8/bf16…`), feature support (structured outputs,
  tool use), and prices. `top_provider` in the models response describes only the primary endpoint;
  restrict/inspect with provider routing (§8.7) or per-endpoint data on the model's page.
- **Capability truth source** is the per-model `supported_parameters` array (e.g. `tools`, `tool_choice`,
  `response_format`, `structured_outputs`, `reasoning`, `reasoning_effort`, `seed`). Example: Gemini 3.7
  Flash lists mandatory reasoning (`reasoning: {"mandatory": true, "default_enabled": true, efforts
  high/medium/low}`) in the API response.
- **Reasoning models**: OpenRouter normalizes reasoning control via `reasoning`/`reasoning_effort`
  request fields and can return reasoning tokens; `pricing.internal_reasoning` prices them where billed
  separately (Gemini 3.7 Flash bills reasoning at output rate). (Models API, accessed 2026-08-14.)
- **Moderation**: endpoints flagged `is_moderated: true` apply upstream content filters; blocked inputs
  return 403 with moderation metadata (§8.10).
- **No lab-native betas**: features shipped only on a lab's native API (e.g. Anthropic beta headers,
  OpenAI realtime sockets) are generally unavailable until OpenRouter maps them.

## 8.4 Embedding / audio / vision / video models

- **Embeddings: none.** No embeddings endpoint is documented in the API reference at access date — pair
  OpenRouter with a direct embedding provider for RAG (§8.13). [Verified absent from docs 2026-08-14.]
- **Vision input**: broad — most frontier models list `image` (many also `file`/`video`/`audio`) in
  `architecture.input_modalities` (e.g. Gemini 3.7 Flash: `text+image+file+audio+video->text`).
- **Audio/video generation**: partner models appear in the catalog with non-token pricing — MiniMax
  `speech-2.8-hd` ($100/1M characters), `speech-2.8-turbo` ($60/1M chars), video models `hailuo-2.3`
  ($0.0817/sec), `hailuo-3` ($0.13/sec); the models schema includes a `supported_voices` field.
  (https://openrouter.ai/minimax/, accessed 2026-08-14.) End-to-end API workflow for these modalities:
  [UNVERIFIED — check each model page].
- Image *generation* models exist in the catalog (pricing fields include `image`); enumerate via the
  models API rather than assuming parity with labs' native image APIs.

## 8.5 Pricing model & cost notes

All figures from https://openrouter.ai/docs/faq and feature docs, accessed 2026-08-14.

- **Inference = pass-through**: OpenRouter "passes through the pricing of the underlying providers" with
  "no markup on inference pricing." (Observed exceptions/lags in §8.2 — always trust the live listing,
  which is what you are actually billed.)
- **Platform fee on credit purchases**: Stripe **5.5% ($0.80 minimum)**; crypto via Coinbase **5%**.
  Fees are non-refundable; unused credits refundable only within 24h of purchase; crypto never
  refundable; unused credits may expire after one year (per terms).
- **BYOK fee**: using your own provider key costs **5% of what the same usage would have cost on
  OpenRouter**, deducted from credits (§8.6). FAQ additionally cites monthly fee-free BYOK allowances
  (**$25,000** pay-as-you-go; **$200,000** enterprise) — re-verify tier applicability.
- **Batch discounts**: `:batch` variant slugs observed throughout the live catalog at roughly **50% of
  interactive price** (e.g. `claude-opus-5:batch` 2.50/12.50; `gemini-3.7-flash:batch` 0.1875/0.9375).
  Batch-API mechanics doc: [UNVERIFIED — see model pages].
- **Prompt caching** (https://openrouter.ai/docs/features/prompt-caching): supported and billed per
  provider — OpenAI GPT-5.6+: write 1.25×, read 0.25–0.5×; Anthropic: write 1.25× (5 min TTL) or 2×
  (1 h), read 0.1×; Gemini: implicit/explicit, read 0.25× + storage; DeepSeek: write 1×, read 0.1×;
  Grok: write free, read 0.25×. Anthropic-style breakpoints via `cache_control: {"type":"ephemeral"}` on
  content parts. **Sticky routing** keeps successive requests on the same endpoint to preserve cache hits
  (10-min inactivity expiry; steer with `session_id`, ≤256 chars). Usage reported in
  `prompt_tokens_details.cached_tokens` / `cache_write_tokens`.
- **Web search**: `:online` suffix or `plugins: [{"id":"web"}]` — **$4 per 1000 results**, default
  `max_results` 5 (≈$0.02/request) plus tokens for injected results. Per-model `pricing.web_search` also
  appears in the catalog (Gemini 3.7 Flash: $0.007). (https://openrouter.ai/docs/features/web-search.)
- **Logging discount**: opting in to prompt/completion logging gives a **1% discount** on usage (§8.16).
- **Cost accounting**: exact billed cost per request via `GET /api/v1/generation?id=<generation id>`
  (native token counts + actual charge), or `usage` accounting in responses.

## 8.6 Authentication & environment

- API key from the dashboard; send `Authorization: Bearer $OPENROUTER_API_KEY`. Conventional env var:
  `OPENROUTER_API_KEY`. Base URL `https://openrouter.ai/api/v1`.
  (https://openrouter.ai/docs/quickstart, accessed 2026-08-14.)
- Key/limit introspection: `GET /api/v1/auth/key` returns credit usage, limits, and rate-limit state
  (https://openrouter.ai/docs/api-reference/limits, accessed 2026-08-14). Credits endpoint
  (`/api/v1/credits`) is referenced in the API reference; programmatic key-provisioning API:
  [UNVERIFIED at access date].
- **BYOK** (https://openrouter.ai/docs/use-cases/byok): store per-provider keys ("securely encrypted") in
  account settings. Priority is configurable: use your key first with OpenRouter credits as fallback, or
  credits first and your key as fallback on rate limits/failures. Fee: 5% of OpenRouter-equivalent cost
  (§8.5). Azure/Bedrock/Vertex BYOK specifics: [UNVERIFIED — not on the fetched page].
- **App attribution headers** (optional but required for app rankings/analytics;
  https://openrouter.ai/docs/app-attribution, accessed 2026-08-14):
  - `HTTP-Referer: <your app URL>` — primary app identifier;
  - `X-OpenRouter-Title: <display name>` (preferred; `X-Title` is the backwards-compatible legacy form);
  - `X-OpenRouter-Categories: <cat1,cat2>` — ≤2 per request, ≤10 total per app.

## 8.7 API endpoints & schemas

Base: `https://openrouter.ai/api/v1` (path-versioned; v1 current). OpenAI Chat Completions-compatible.
(https://openrouter.ai/docs/api-reference/overview, accessed 2026-08-14.)

| Endpoint | Method | Purpose |
|---|---|---|
| `/chat/completions` | POST | main inference (messages) |
| `/completions` | POST | legacy prompt-string inference |
| `/models` | GET | **dynamic catalog + live pricing** (schema below) |
| `/generation?id=` | GET | post-hoc native token counts + exact cost |
| `/auth/key` | GET | current key's credits/limits |
| `/credits` | GET | credit balance (referenced in API reference) |
| `/models/{author}/{slug}/endpoints` | GET | per-provider endpoints for one model [UNVERIFIED at access date] |

### `GET /api/v1/models` response schema (verbatim example object, accessed 2026-08-14)

`{"data": [ <model>, … ]}` where each `<model>` is:

```json
{
  "id": "google/gemini-3.7-flash",
  "canonical_slug": "google/gemini-3.7-flash-20260813",
  "hugging_face_id": null,
  "name": "Google: Gemini 3.7 Flash",
  "created": 1786640581,
  "description": "…",
  "context_length": 1048576,
  "architecture": {
    "modality": "text+image+file+audio+video->text",
    "input_modalities": ["text", "image", "video", "file", "audio"],
    "output_modalities": ["text"],
    "tokenizer": "Gemini",
    "instruct_type": null
  },
  "pricing": {
    "prompt": "0.000000375",          // USD per TOKEN (string) → ×1e6 = $/1M
    "completion": "0.000001875",
    "image": "0.000000375",
    "audio": "0.000000375",
    "web_search": "0.007",
    "internal_reasoning": "0.000001875",
    "input_cache_read": "0.0000000375",
    "input_cache_write": "0.0000000208333333333333"
  },
  "top_provider": { "context_length": 1048576, "max_completion_tokens": 65536, "is_moderated": false },
  "per_request_limits": null,
  "supported_parameters": ["include_reasoning","max_tokens","reasoning","reasoning_effort",
    "response_format","seed","stop","structured_outputs","temperature","tool_choice","tools","top_p"],
  "default_parameters": {},
  "supported_voices": null,
  "knowledge_cutoff": null,
  "expiration_date": null,
  "reasoning": { "mandatory": true, "default_enabled": true,
                 "supported_efforts": ["high","medium","low"], "default_effort": "medium" }
}
```

Readers should query this endpoint for live pricing instead of trusting any printed table. Note: prices
are **per-token strings**; `:free` variants have `"0"`; `openrouter/auto*` uses `-1` sentinels.

### Request-body extensions beyond OpenAI schema

- `models: ["primary","fallback1",…]` and `route` — model-fallback chains (§8.7 routing; API overview).
- `provider: {…}` — provider preferences (https://openrouter.ai/docs/features/provider-routing, accessed
  2026-08-14): `order` (slugs in priority order), `allow_fallbacks` (default `true`),
  `require_parameters` (default `false` — only route to endpoints supporting all request params),
  `data_collection` (`"allow"`(default)/`"deny"`), `only`, `ignore`, `zdr` (ZDR-only endpoints),
  `quantizations` (e.g. `["fp8"]`), `sort` (`"price" | "throughput" | "latency"`, object form supports
  `partition: "model"|"none"`), `preferred_min_throughput` (tok/s), `preferred_max_latency` (s),
  `max_price` (per-token caps).
- **Default routing** (no preferences): among providers with no significant outage in the last 30 s,
  choose low-cost candidates "weighted by inverse square of the price."
- **Suffix shortcuts**: `:nitro` ≡ `sort:"throughput"`, `:floor` ≡ `sort:"price"`; `:free`, `:batch`,
  `:online` variants; `~author/…-latest` evergreen aliases track a lab's newest model — pin exact slugs
  in production.
- `openrouter/auto` — prompt-based model selection; "you pay the standard rate for whichever model is
  selected. There is no additional fee." (https://openrouter.ai/docs/features/model-routing.)
- Other: `transforms`, `reasoning`/`reasoning_effort`, `plugins`, `session_id`, usage accounting.

## 8.8 SDK integration

Official SDKs per quickstart (accessed 2026-08-14): TypeScript `@openrouter/sdk`, Python `openrouter`;
plus full compatibility with the OpenAI SDKs via `base_url`.

```python
# Python — OpenAI SDK pointed at OpenRouter
from openai import OpenAI
import os

client = OpenAI(base_url="https://openrouter.ai/api/v1",
                api_key=os.environ["OPENROUTER_API_KEY"])

resp = client.chat.completions.create(
    model="anthropic/claude-sonnet-5",
    extra_headers={"HTTP-Referer": "https://yourapp.example",
                   "X-OpenRouter-Title": "YourApp"},
    extra_body={"models": ["anthropic/claude-sonnet-5", "google/gemini-3.7-flash"],  # fallback chain
                "provider": {"sort": "price", "data_collection": "deny"}},
    messages=[{"role": "user", "content": "Hello"}],
)
print(resp.choices[0].message.content)
```

```javascript
// JavaScript — plain fetch (shape per quickstart)
const r = await fetch("https://openrouter.ai/api/v1/chat/completions", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.OPENROUTER_API_KEY}`,
    "Content-Type": "application/json",
    "HTTP-Referer": "https://yourapp.example",
    "X-OpenRouter-Title": "YourApp",
  },
  body: JSON.stringify({
    model: "deepseek/deepseek-v4-pro-0813",
    messages: [{ role: "user", content: "Hello" }],
  }),
});
const data = await r.json();
```

```bash
# curl — live catalog with pricing (no auth required at access date)
curl -s https://openrouter.ai/api/v1/models | jq '.data[] | {id, pricing, context_length}'

curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "openai/gpt-5.6-terra", "messages": [{"role":"user","content":"Hello"}]}'
```

## 8.9 Streaming, tool use, structured output examples

**Streaming** (https://openrouter.ai/docs/api-reference/streaming, accessed 2026-08-14): `stream: true`
→ SSE chunks. Keep-alive **comment lines** like `: OPENROUTER PROCESSING` are interleaved — skip them
before `JSON.parse` ("unhandled it will crash your stream loop"). Terminates with `data: [DONE]`; the
final chunk carries usage stats. Mid-stream **cancellation** (`AbortController`) stops billing only on
supporting providers (OpenAI, Anthropic, Cohere, Together, …); **not** on AWS Bedrock, Groq, Google,
Mistral — there the model completes and you pay in full.

**Tool use** (https://openrouter.ai/docs/features/tool-calling): OpenAI `tools`/`tool_choice` format
passed through and normalized across labs; responses use `finish_reason: "tool_calls"`, results return as
`role:"tool"` messages with `tool_call_id`. Guarantee support by routing with
`provider: {"require_parameters": true}` and by checking `supported_parameters` for `tools`.

**Structured output** (https://openrouter.ai/docs/features/structured-outputs):

```json
{
  "model": "openai/gpt-5.6-terra",
  "messages": [{"role": "user", "content": "Weather in London as JSON"}],
  "provider": {"require_parameters": true},
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "weather", "strict": true,
      "schema": {"type": "object",
                 "properties": {"city": {"type": "string"}, "temp_c": {"type": "number"}},
                 "required": ["city", "temp_c"], "additionalProperties": false}
    }
  }
}
```

Caveats: "the same model may be served by multiple providers, and only some of those providers may
support structured outputs"; strict-mode schema-feature limits are provider-dependent and "exact
compliance is not guaranteed on every endpoint." Filter models by the `structured_outputs` supported
parameter.

## 8.10 Error handling & retry

Source: https://openrouter.ai/docs/api-reference/errors, accessed 2026-08-14.

| HTTP | Meaning |
|---|---|
| 400 | Bad request (invalid/missing params, CORS) |
| 401 | Invalid credentials (expired OAuth session, disabled/invalid key) |
| 402 | Insufficient credits (also fires on **negative balance — including for free models**) |
| 403 | Forbidden: permissions, guardrail block, or **moderation flag** |
| 408 | Request timed out |
| 429 | Rate limited |
| 502 | Chosen model down / invalid upstream response |
| 503 | **No provider meets your routing requirements** (over-constrained `provider` prefs) |

Error shape: `{"error": {"code": <number>, "message": <string>, "metadata?": {…}}}`. Moderation metadata:
`reasons[]`, `flagged_input` (truncated to 100 chars), `provider_name`, `model_slug`. Upstream provider
error codes surface in `error.metadata.provider_code` for non-500s; masked on 500s. Note: errors after a
stream has begun arrive as SSE events with HTTP 200. Warm-up edge case: a generation can return no
content yet still incur upstream prompt-processing cost.

Retry pattern: exponential backoff on 408/429/502; on 503 **loosen routing constraints** rather than
retrying blindly; on 402 stop and refill credits. OpenRouter's own fallback machinery (multi-provider +
`models` array) already absorbs most transient upstream failures before you see them.

## 8.11 Rate limits & quotas

Source: https://openrouter.ai/docs/api-reference/limits, accessed 2026-08-14.

- **Free variants (`:free`)**: **20 requests/min and 200 requests/day** per account.
- **Paid**: limits scale with credit balance — **1 request/sec per credit**, floor ~0.5 credits → 1 rps,
  up to a surge limit (typically **500 rps**); >1000 credits → contact support. No fixed TPM quotas —
  upstream capacity is load-balanced across providers.
- Negative balances → 402s until topped up. Cloudflare DDoS protection blocks extreme bursts.
- Inspect your own limits: `GET /api/v1/auth/key`.
- Historical "$10 credits unlocks 1000 free requests/day" rule: **no longer present** in current docs
  (checked 2026-08-14).

## 8.12 Fine-tuning & customization

None. OpenRouter is inference-only aggregation — no fine-tuning, training, or model-hosting API is
documented (verified absent 2026-08-14). Customization levers instead: provider routing, presets/system
prompts client-side, BYOK to reach your own fine-tuned deployments on the underlying lab where that lab
supports serving them under your key ([UNVERIFIED] per-lab — check BYOK docs for your provider).

## 8.13 RAG & embedding pipeline notes

- No embeddings endpoint (§8.4) → hybrid architecture: embed via a direct provider (OpenAI, Google,
  Voyage, etc.), retrieve, then generate through OpenRouter. This keeps generation portable across labs
  with one key while pinning the embedding space to one vendor (embedding vectors are not portable).
- `:online`/web plugin ($4/1000 results) is a zero-infra alternative for freshness-style grounding.
- Long-context RAG is a strength: many catalog models offer ≥1M context (§8.2) — but per-endpoint context
  can be lower than the model's headline number; check `top_provider.context_length` or restrict
  providers.

## 8.14 Agent support

- **MCP**: no native hosting; docs show converting MCP (Anthropic-format) tool definitions to OpenAI tool
  format for use through OpenRouter, and the official **`@openrouter/mcp`** TypeScript package "connects
  to a remote MCP server, authenticates once, and returns tools you spread directly into `callModel`."
  (https://openrouter.ai/docs/use-cases/mcp-servers, accessed 2026-08-14.)
- Standard OpenAI-compatible tool loop works with all major agent frameworks (LangChain, Vercel AI SDK,
  OpenAI Agents SDK via base-URL override, Codex CLI per OpenRouter's own tutorial).
- Agent-relevant platform features: fallback `models` arrays, sticky sessions for cache-friendly
  multi-turn tool loops, `reasoning_effort` normalization, `openrouter/auto` for per-prompt model choice.

## 8.15 Deployment patterns

- Pure HTTPS API — deploys anywhere (serverless, containers, edge); no VPC/private-link offering
  documented ([UNVERIFIED] for enterprise). Keep the key server-side; for user-keyed apps OpenRouter
  supports OAuth-style user connections ([UNVERIFIED at access date — historical PKCE flow; re-verify]).
- Common pattern: OpenRouter as the **resilience/routing tier** — primary traffic direct to a lab for
  lowest latency, OpenRouter as fallback; or OpenRouter primary with `provider.order` pinned and
  `allow_fallbacks: true` for automatic failover.
- Streaming through proxies/edge runtimes: handle SSE comments (§8.9).

## 8.16 Region availability & data residency

- Service is globally reachable; inference location is **provider-dependent** by default.
- **Enterprise regional routing**: EU or US regional endpoints where "your prompts and completions are
  processed within the selected region." (https://openrouter.ai/docs/features/privacy-and-logging,
  accessed 2026-08-14.)
- Per-request control: constrain to specific providers (`provider.only/order`) whose residency you have
  verified upstream. Fine-grained residency guarantees per provider: [UNVERIFIED — consult each
  provider's terms surfaced on the model page].

## 8.17 Security, compliance & SLA

Documented (accessed 2026-08-14):
- **Default privacy**: "Prompt and completion are not logged" by OpenRouter; opt-in logging earns a 1%
  usage discount. "OpenRouter itself has a ZDR policy; your prompts are not retained unless you
  specifically opt in to prompt logging." (FAQ + https://openrouter.ai/docs/features/zdr.)
- **ZDR routing**: account-level ZDR per model group (Anthropic/OpenAI/Google/non-frontier) and
  per-request `provider: {"zdr": true}`; OR-logic — a request cannot loosen an account-wide restriction.
  In-memory prompt caching does not disqualify an endpoint from ZDR.
- **Training controls**: account settings gate routing to providers that may train on data (separate
  toggles for paid vs free models); per-request `data_collection: "deny"`.
- BYOK keys "securely encrypted."
- Certifications (SOC 2 etc.) and uptime SLA: **[UNVERIFIED — not found in fetched docs]**; enterprise
  agreements exist (fee allowances, regional routing) — contact sales.
- Note: `:free` models are typically served under provider terms allowing data use — check each
  endpoint's data policy before sending sensitive content.

## 8.18 Legacy models & migration notes

- The catalog retains long tails of superseded slugs (e.g. `anthropic/claude-3.5-sonnet`,
  `claude-opus-4.1`, `deepseek/deepseek-r1`, `qwen/qwq-32b`) — useful for reproducibility, often worse
  price/perf than current tiers. The models schema's `expiration_date` field signals scheduled removals;
  deprecations otherwise mirror upstream labs.
- Migration is OpenRouter's core convenience: change the model string (or use `models` fallback arrays to
  A/B old→new). Avoid `~…-latest` evergreen aliases and `openrouter/auto` where output stability matters;
  pin `canonical_slug`-style dated variants (e.g. `deepseek-v4-pro-0813`) for reproducibility.
- Migrating *to* direct lab APIs later is low-cost by design (OpenAI-compatible schema), except where you
  depend on OpenRouter-specific fields (`provider`, `models`, plugins, `session_id`).

## 8.19 Task-suitability verdict

**Best for**: multi-model products and evals (one key, hot-swappable strings); resilience-critical
workloads (multi-provider fallback beats any single lab's uptime); cost-optimized routing across the
open-weight ecosystem (`:floor`, `sort:"price"`, quantization filters); rapid access to new lab releases
(same-day listings, e.g. two models above released 2026-08-13); prototyping on `:free` tiers; agent stacks
needing uniform tool/reasoning semantics across labs.

**Worst for / avoid**: latency-critical paths where the extra hop matters — measure vs direct;
lab-bleeding-edge features (realtime audio sockets, provider beta APIs, native batch/file APIs) — go
direct; embeddings (none — §8.4); strict compliance programs needing certifications OpenRouter has not
published; sub-cent price determinism (listings can lag lab price changes both directions — §8.2
observed gpt-5.6-sol high and gemini-3.7-flash low vs lab list; billed price follows the listing).

## 8.20 Sources

All accessed **2026-08-14**:

1. Quickstart — https://openrouter.ai/docs/quickstart
2. Live catalog + schema — https://openrouter.ai/api/v1/models
3. API overview — https://openrouter.ai/docs/api-reference/overview
4. Provider routing — https://openrouter.ai/docs/features/provider-routing
5. Model routing / auto router — https://openrouter.ai/docs/features/model-routing
6. Rate limits — https://openrouter.ai/docs/api-reference/limits
7. Errors — https://openrouter.ai/docs/api-reference/errors
8. Streaming — https://openrouter.ai/docs/api-reference/streaming
9. Structured outputs — https://openrouter.ai/docs/features/structured-outputs
10. Tool calling — https://openrouter.ai/docs/features/tool-calling
11. Prompt caching — https://openrouter.ai/docs/features/prompt-caching
12. Web search — https://openrouter.ai/docs/features/web-search
13. Privacy & logging — https://openrouter.ai/docs/features/privacy-and-logging
14. Zero data retention — https://openrouter.ai/docs/features/zdr
15. BYOK — https://openrouter.ai/docs/use-cases/byok
16. FAQ (fees, refunds, logging discount) — https://openrouter.ai/docs/faq
17. App attribution — https://openrouter.ai/docs/app-attribution
18. MCP servers — https://openrouter.ai/docs/use-cases/mcp-servers
19. Vendor catalog pages — https://openrouter.ai/openai/ · /anthropic/ · /google/ · /deepseek/ ·
    /qwen/ · /z-ai/ · /minimax/ · /mistralai/
20. Evergreen `~` aliases — https://openrouter.ai/blog/tutorials/codex-cli-openrouter/


---

# 9. Ollama (local open-weight inference)

> **Volatility warning.** Model lineups and pricing change frequently. Verified against official
> documentation on **2026-08-14** (ollama.com, docs.ollama.com, github.com/ollama/ollama).
> Re-verify before production decisions. Ollama is a *runtime*, not a model vendor: the catalog below
> is the currently well-usable open-weight lineup distributed through the Ollama library, and it moves
> even faster than hosted-API catalogs.

## 9.1 Platform overview & positioning

Ollama is an open-source (MIT-licensed) local inference server + CLI for running open-weight LLMs on
Linux, macOS and Windows. It wraps llama.cpp/GGML-based engines (plus an MLX engine on Apple Silicon
since the v0.32.x line) behind a single binary that handles model download, quantized storage,
GPU offload, an HTTP API on `localhost:11434`, and OpenAI- and Anthropic-compatible endpoints.

- Current release at access time: **v0.32.6** (2026-08-04). Recent release-line highlights: MLX engine
  for Apple GPUs (Qwen3.5 speedups), OpenAI-compatible streaming format fixes, CUDA on Windows ARM64
  and B200 support, an interactive CLI agent mode (v0.32.0), flash attention on older NVIDIA GPUs.
  (https://github.com/ollama/ollama/releases, accessed 2026-08-14)
- Distribution model: models are pulled from the Ollama registry (`ollama.com/library`) as layered
  blobs, typically 4-bit quantized by default; other quantizations are exposed as tags.
- Since 2025 Ollama also operates **Ollama Cloud** (formerly marketed as "Turbo"), a paid hosted
  tier for models too large for local hardware — see 9.5/9.15. Local use remains free.
- Positioning: the lowest-friction way to run open weights locally; not the highest-throughput server
  (vLLM/SGLang beat it for batch/multi-user serving), but the de-facto standard for developer
  workstations, edge boxes, and privacy-constrained single-tenant deployments.

## 9.2 Current model catalog

No per-token prices (local inference). "Disk" = default-quant download size as listed in the library.
Realistic memory need ≈ disk size + KV cache + overhead (see 9.5). All library pages accessed
2026-08-14 via ollama.com/library/<name>.

### Generalist / instruct / reasoning (local-capable)

| Model (tag) | Vendor | Params (tags) | Disk (default) | Context | Tool use | Thinking | Vision | Notes |
|---|---|---|---|---|---|---|---|---|
| `qwen3.6` | Alibaba | 27B, 35B | 17 / 24 GB | 256K | yes | yes | yes | Newest Qwen; agentic coding, reasoning-context retention; MLX tags |
| `qwen3.5` | Alibaba | 0.8B–122B (+397B cloud) | 1.0–81 GB | 256K | yes | yes | yes | Unified VL family, MoE + Gated Delta Nets, 201 languages |
| `gemma4` | Google | E2B, E4B, 12B, 26B (MoE, 3.8B act.), 31B | 7.2–20 GB | 128K (E2B/E4B) / 256K | yes | — | yes (all) | E-series is edge/on-device class; audio-in on E2B/E4B |
| `muse-glimmer` | Meta | 30B | 18 GB | 128K | yes | yes | yes | Apache 2.0; Meta's agent line (distilled from Muse Spark), tuned for tool use / failure recovery |
| `gpt-oss` | OpenAI | 20B, 120B | 14 / 65 GB | 128K | yes | yes (effort low/med/high) | no | MXFP4 native (~4.25 bit); Apache 2.0; 20b runs in ~16 GB RAM, 120b on one 80 GB GPU |
| `deepseek-r1` (distills) | DeepSeek | 1.5B–70B (+671B full) | 1.1–43 GB (671b: 404 GB) | 128K (671b: 160K) | yes | yes | no | Qwen2.5/Qwen3/Llama3.3 distills; older gen but still heavily pulled |
| `mistral-medium-3.5` | Mistral | 128B | — | — | yes | yes | yes | Current Mistral flagship on Ollama; needs multi-GPU class hardware |
| `mistral-small3.2` | Mistral | 24B | — | — | yes | no | yes | Best current single-GPU Mistral; 3.1/3.2 ~1 yr old |
| `nemotron-3.5-lightning` | NVIDIA | 30B MoE (3B active) | — | — | yes | yes | no | "Always-on agents" positioning; very fast per-token (low active params) |
| `phi4` / `phi4-mini` / `phi4-reasoning` | Microsoft | 14B / 3.8B / 14B | — | — | mini: yes | reasoning: yes | no | Aging (≥1 yr old); still good small-footprint STEM/chat |
| `llama3.1` / `llama3.2` / `llama3.3` | Meta | 8B–405B / 1B–3B / 70B | — | 128K | yes | no | no | Legacy but most-pulled family (118M+ pulls); see 9.18 |
| `qwen3` | Alibaba | 0.6B–235B | — | — | yes | yes | no | Prior Qwen gen; superseded by 3.5/3.6 |

### Coding

| Model | Params | Disk | Context | Notes |
|---|---|---|---|---|
| `qwen3-coder` | 30B (A3B), 480B | 19 GB / 290 GB | 256K native (1M extrapolated) | Agentic SWE focus; 480b also as `-cloud`; 30b is the practical local pick |
| `qwen3.6` (27B/35B) | see above | | 256K | Explicitly tuned for agentic/repo-level coding |
| `qwen2.5-coder`, `codellama`, `starcoder2` | various | | | Legacy; prefer qwen3-coder |

### Vision-language (see 9.4) and cloud-only

| Model | Params | Context | Notes |
|---|---|---|---|
| `qwen3-vl` | 2B–235B (1.9–143 GB) | 256K (→1M) | Strongest dedicated open VL family on Ollama; GUI-agent + OCR (32 langs); requires ≥0.12.7 |
| `deepseek-v4-flash` | 284B total / 13B active | 1M | **cloud tag** — preview, efficient reasoning; not practical locally |
| `glm-5.1`, `kimi-k2.6/2.7-code`, `minimax-m3`, `qwen3.5:397b`, `qwen3-coder:480b`, `gpt-oss:120b-cloud` | — | — | Library models carrying the `cloud` capability tag (run on Ollama Cloud, not local) |

Sources: ollama.com/library (popular + newest sort), individual model pages, all accessed 2026-08-14.
Params/sizes for rows marked "—" were listed on search/overview pages without full tag detail:
treat as MEDIUM confidence; per-tag detail in the sidecar JSON.

## 9.3 Model details & limitations

**Qwen 3.5 / 3.6 (Alibaba).** The current default recommendation for general local use. 3.5 spans
0.8B→122B with a unified early-fusion vision-language architecture, sparse MoE + Gated Delta Networks,
256K context, tools + thinking on every size; 3.6 (27B/35B) adds agentic-coding upgrades and
preservation of reasoning context across turns. MLX-optimized tags exist for Apple Silicon. Weak spots:
the smallest tags (0.8B/2B) hallucinate heavily on factual queries; 122B needs ~96+ GB of fast memory.
(ollama.com/library/qwen3.5, /qwen3.6, accessed 2026-08-14)

**Gemma 4 (Google).** Multimodal at every size; E2B/E4B are effective-parameter edge models
(2.3B/4.5B effective; audio input) at 128K context, 12B/26B-MoE/31B at 256K. Native function calling.
The 26B MoE (3.8B active) gives near-31B quality at much higher tokens/s. License is the Gemma license
(use restrictions), not Apache. (ollama.com/library/gemma4, accessed 2026-08-14)

**Muse Glimmer (Meta).** Meta's post-Llama agent line: 30B dense, Apache 2.0, 128K context,
multimodal-in, 100+ languages, controllable reasoning effort; distilled from the larger Muse Spark and
explicitly tuned for tool schemas, long tasks and failure recovery. Not a general-chat champion —
pick it for agent loops. (ollama.com/library/muse-glimmer, accessed 2026-08-14)

**gpt-oss (OpenAI).** 20B/120B MoE, MXFP4-native (≈4.25 bits/param), 128K context, Apache 2.0, full
chain-of-thought with selectable reasoning effort, strong function calling and structured output.
20b is the best "fits in 16 GB" reasoner; 120b needs ~80 GB GPU (or 64 GB+ unified memory Mac,
slowly). ~10 months old at access time; still current, no successor published.
(ollama.com/library/gpt-oss, accessed 2026-08-14)

**DeepSeek-R1 distills.** 1.5B–70B distills (Qwen2.5, Qwen3-8B, Llama3.3-70B bases), 128K context.
Still popular (91M pulls) and fine for offline math/logic, but ~1.5 generations old; verbose thinking
inflates latency and KV usage. The 671B full model (404 GB) is not realistically local; DeepSeek's
current V4 line appears on Ollama as cloud tags. (ollama.com/library/deepseek-r1, accessed 2026-08-14)

**Mistral.** Current: `mistral-medium-3.5` (128B, vision+tools+thinking) — needs workstation/server
class memory; `mistral-small3.2` (24B, vision+tools) remains the practical single-GPU option;
`mistral-nemo` (12B) and `mistral:7b` are legacy small options. `mistral-large-3` is cloud-tagged.
(ollama.com/search?q=mistral, accessed 2026-08-14)

**Phi (Microsoft).** Newest available generation is still Phi-4 (14B) / Phi-4-mini (3.8B, tools) /
Phi-4(-mini)-reasoning, all ≥1 year old. Good STEM density per parameter and permissive to run, but
short on tool-use robustness vs Qwen3.5-class peers; no Phi-5 on Ollama at access time.
(ollama.com/search?q=phi, accessed 2026-08-14)

**Llama 3.x / 4 (Meta).** llama3.1 is still the most-pulled model (118M) and llama3.2 1B/3B remains a
solid tiny-tools baseline, but the whole family is ≥1 year stale; Meta's new open work ships under the
Muse brand. Treat Llama as legacy (9.18). (ollama.com/search?q=llama, accessed 2026-08-14)

**General limitations of the platform.** Default context is **4096 tokens regardless of model
capability** — you must raise `num_ctx`/`OLLAMA_CONTEXT_LENGTH` explicitly (9.7); default quants are
~4-bit, which costs measurable accuracy on hard reasoning vs fp16/8-bit; scheduler is optimized for
1–few users, not high-QPS serving.

## 9.4 Embedding / vision / audio models

### Embeddings (all local, `/api/embed`)

| Model | Params | Notes |
|---|---|---|
| `qwen3-embedding` | 0.6B / 4B / 8B | Current best quality family on Ollama; multilingual |
| `embeddinggemma` | 300M | Google; small, strong for size; used in official docs examples |
| `nomic-embed-text-v2-moe` | MoE | Multilingual retrieval; successor to `nomic-embed-text` (82M pulls, 2 yrs old) |
| `mxbai-embed-large` | 335M | Solid English general-purpose; 2 yrs old |
| `bge-m3` | 567M | Multi-lingual/-granularity; 2 yrs old |
| `snowflake-arctic-embed2` | 568M | Multilingual frontier-class (1 yr old) |
| `all-minilm` | 22M/33M | Tiny/fast, quality floor |
| `granite-embedding` | 30M/278M | IBM, text-only dense |

(ollama.com/search?c=embedding, accessed 2026-08-14.) `dimensions` request field supports
Matryoshka-style truncation where the model allows it (docs.ollama.com/api/embed.md).

### Vision

Vision input is first-class in current generalist families (qwen3.5/3.6, gemma4, muse-glimmer,
mistral-small3.2/medium-3.5, llama4). Dedicated VL: **qwen3-vl** 2B–235B (GUI-agent use, OCR in 32
languages, 256K context, video understanding); legacy: `llama3.2-vision` (11B/90B), `llava`,
`minicpm-v`. Images are passed base64 in `messages[].images` (native API) or OpenAI-style
image_url-with-base64 (compat API); remote URLs are **not** fetched by the server.
(docs.ollama.com/capabilities/vision.md, ollama.com/library/qwen3-vl, accessed 2026-08-14)

### Audio / video generation

Gemma 4 E2B/E4B accept audio input. No general local audio-out/TTS or video model line is part of the
core library at access time; experimental image generation was **removed** in v0.32.6
(github.com/ollama/ollama/releases). Anything else: [UNVERIFIED].

## 9.5 Pricing model & cost notes (hardware instead of tokens)

Local inference has no per-token price; cost = hardware + power. Rules of thumb (estimates, not
official figures — actual need depends on quant, context length, and KV cache type):

- **Memory:** weights ≈ download size; add KV cache (grows linearly with `num_ctx` × layers; can be
  halved/quartered with `OLLAMA_KV_CACHE_TYPE=q8_0/q4_0`) plus ~1–2 GB runtime overhead. A 4-bit ~8B
  fits comfortably in 8 GB VRAM at moderate context; ~24–35B class (qwen3.6:35b 24 GB, qwen3-coder:30b
  19 GB, muse-glimmer 18 GB, gemma4:31b 20 GB) wants 24–32 GB VRAM or Apple unified memory;
  gpt-oss:120b / qwen3.5:122b (65–81 GB) need 80 GB-class GPUs or ≥96 GB unified-memory Macs.
- **Official anchors:** gpt-oss:20b "runs on 16 GB RAM systems"; gpt-oss:120b "fits a single 80 GB
  GPU" (ollama.com/library/gpt-oss). Everything else above is an estimate.
- **Quant tags:** default library tags are ~4-bit (K-quants; MXFP4/NVFP4 for natively-quantized
  releases); most families expose `q8_0`, `fp16`, and MLX tags. Higher-bit quants ≈ proportionally
  more memory, slightly better accuracy. [Tag-level quant naming varies per model — check the model's
  Tags page.]

**Ollama Cloud** (the current name; "Turbo" branding is gone) is the only priced product:
Free $0 (1 concurrent cloud model, light usage), **Pro $20/mo** ($200/yr, 3 concurrent, "50× more
usage than Free"), **Max $100/mo** (10 concurrent, 5× Pro — new signups paused at access time).
Usage metered in tokens (input/cached-input/output) weighted by model compute class (1–4); no public
per-token price sheet → per-token rates [UNVERIFIED — not published]. Hosted with NVIDIA cloud
partners, primarily US (possible EU/Singapore routing); "prompt or response data is never logged or
trained on" per Ollama. (ollama.com/cloud, docs.ollama.com/cloud.md, accessed 2026-08-14)

## 9.6 Authentication & environment

- **Local API: no authentication of any kind.** Anyone who can reach TCP 11434 can use models,
  pull/delete them, and read whatever you send. Binding defaults to `127.0.0.1:11434`; changing
  `OLLAMA_HOST` to `0.0.0.0` without a fronting proxy is the classic Ollama security mistake (9.17).
- **Ollama Cloud:** account on ollama.com; `ollama signin` for CLI/local-offload flows, or an API key
  from ollama.com/settings/keys sent as `Authorization: Bearer $OLLAMA_API_KEY` against
  `https://ollama.com/api/...`. (docs.ollama.com/cloud.md, /api/authentication.md, accessed 2026-08-14)

Key environment variables (server side; set via systemd override / launchd / Windows env):

| Variable | Default | Purpose |
|---|---|---|
| `OLLAMA_HOST` | `127.0.0.1:11434` | Bind address/port |
| `OLLAMA_MODELS` | per-OS (9.15) | Model blob store location |
| `OLLAMA_CONTEXT_LENGTH` | `4096` | Default context window (override per-request via `options.num_ctx`) |
| `OLLAMA_KEEP_ALIVE` | `5m` | How long a model stays loaded after last use |
| `OLLAMA_NUM_PARALLEL` | `1` | Parallel requests per loaded model (multiplies KV memory) |
| `OLLAMA_MAX_LOADED_MODELS` | 3×GPU count (3 on CPU) | Concurrently resident models |
| `OLLAMA_FLASH_ATTENTION` | on where supported | `0/1` toggle |
| `OLLAMA_KV_CACHE_TYPE` | `f16` | `f16` / `q8_0` / `q4_0` KV quantization |
| `OLLAMA_ORIGINS` | localhost origins | Extra allowed CORS origins |
| `CUDA_VISIBLE_DEVICES` / `ROCR_VISIBLE_DEVICES` / `GGML_VK_VISIBLE_DEVICES` | all | GPU selection (NVIDIA/AMD/Vulkan) |
| `OLLAMA_VULKAN` | `1` | Disable Vulkan backend with `0` |
| `HTTPS_PROXY` | — | Proxy for model downloads (do not use `HTTP_PROXY`) |

(docs.ollama.com/faq.md, /gpu.md, /docker.md, accessed 2026-08-14)

## 9.7 API endpoints & schemas

Base URL `http://localhost:11434`. Native API under `/api`, stable/backwards-compatible per docs.
Same schema served hosted at `https://ollama.com/api` (auth required). No URL versioning.

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/generate` | POST | Single-turn completion (`model`, `prompt`, optional `suffix`, `images`, `format`, `options`, `stream`, `keep_alive`, `think`) |
| `/api/chat` | POST | Chat with `messages[]`, `tools[]`, `format`, `options`, `stream`, `keep_alive`, `think`, `logprobs`/`top_logprobs` |
| `/api/embed` | POST | Embeddings: `input` (string or array), `truncate` (default true), `dimensions`, `options`, `keep_alive` |
| `/api/tags` | GET | List local models |
| `/api/show` | POST | Model metadata/capabilities |
| `/api/pull` · `/api/push` · `/api/delete` · `/api/copy` · `/api/create` | POST/DELETE | Registry + Modelfile operations |
| `/api/ps` | GET | Loaded models + VRAM residency |
| `/v1/...` | — | OpenAI-compatible surface (below) |

`/api/chat` request/response essentials (docs.ollama.com/api/chat.md, accessed 2026-08-14):

```jsonc
// POST /api/chat
{
  "model": "qwen3.5",
  "messages": [{"role": "user", "content": "why is the sky blue?"}],
  "tools": [ /* JSON-schema function defs */ ],
  "format": "json",            // or a JSON schema object
  "think": true,                // bool, or effort "low"|"medium"|"high"|"max" (model-dependent)
  "stream": true,               // DEFAULT true — NDJSON chunks
  "keep_alive": "5m",
  "options": {"temperature": 0.7, "num_ctx": 32768, "seed": 42}
}
// final (done:true) response object
{
  "model": "qwen3.5", "created_at": "...",
  "message": {"role": "assistant", "content": "...", "thinking": "...", "tool_calls": [ ... ]},
  "done": true, "done_reason": "stop",
  "total_duration": 174560334, "load_duration": 101397084,   // nanoseconds
  "prompt_eval_count": 11, "eval_count": 18                  // token counts
}
```

**Context caveat:** unless `options.num_ctx` (or `OLLAMA_CONTEXT_LENGTH`) is raised, requests run at a
4,096-token window even on 256K-capable models; excess prompt is truncated silently.
(docs.ollama.com/faq.md, /context-length.md, accessed 2026-08-14)

### OpenAI-compatible endpoint

`http://localhost:11434/v1` — API key required by clients but ignored (use `"ollama"`).
Supported: `/v1/chat/completions` (streaming, JSON mode/response_format, vision via base64, tools,
reasoning control, `seed`), `/v1/completions`, `/v1/models`, `/v1/embeddings` (string/array only, no
token arrays), `/v1/responses` (since v0.13.3; streaming + tools; stateful features not implemented).
Not supported: `logprobs`, `tool_choice`, `n` on chat; `best_of`/`echo` on completions; image URLs
(base64 only). `ollama cp model gpt-3.5-turbo` aliases a local model to a name a legacy tool expects.
An Anthropic-compatible endpoint also exists (docs.ollama.com/api/anthropic-compatibility.md).
(docs.ollama.com/api/openai-compatibility.md, accessed 2026-08-14)

## 9.8 SDK integration

Install + model management (CLI):

```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh          # installs binary + systemd service
# macOS / Windows: download app from ollama.com/download (Windows: OllamaSetup.exe, no admin needed)
# Docker (CPU):
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
ollama pull qwen3.5            # download
ollama run qwen3.5             # interactive; /set parameter num_ctx 32768
ollama ls && ollama ps         # installed / loaded
ollama rm mistral              # delete
```

**Python** (`pip install ollama`, github.com/ollama/ollama-python, accessed 2026-08-14):

```python
from ollama import chat, embed, Client, AsyncClient

resp = chat(model="qwen3.5",
            messages=[{"role": "user", "content": "Why is the sky blue?"}],
            options={"num_ctx": 32768})
print(resp.message.content)

emb = embed(model="qwen3-embedding", input=["doc one", "doc two"])
client = Client(host="http://gpubox.internal:11434")   # custom host; kwargs pass to httpx
```

**JavaScript** (`npm install ollama`):

```js
import ollama from "ollama";
const res = await ollama.chat({
  model: "qwen3.5",
  messages: [{ role: "user", content: "Why is the sky blue?" }],
});
console.log(res.message.content);
```

**curl** (native):

```bash
curl http://localhost:11434/api/generate -d '{"model":"gemma4","prompt":"Why is the sky blue?","stream":false}'
```

**OpenAI SDK against Ollama:**

```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
r = client.chat.completions.create(model="qwen3.5",
        messages=[{"role": "user", "content": "hi"}])
```

## 9.9 Streaming, tool use, structured output

**Streaming.** Native API streams by default: NDJSON, one JSON object per chunk with incremental
`message.content` (and `message.thinking`), terminated by a `done: true` object carrying timing/token
stats. `"stream": false` returns one object. OpenAI endpoint streams SSE `chat.completion.chunk`
(format aligned further in v0.32.6).

```python
for chunk in chat(model="qwen3.5", messages=msgs, stream=True):
    print(chunk.message.content or "", end="", flush=True)
```

**Tool use.** `tools[]` uses JSON-schema function definitions; model replies with
`message.tool_calls[{function:{name, arguments}}]`; you execute, append a `role:"tool"` message
(with results) and re-call — single, parallel, and agent-loop patterns are documented. Works with
streaming (accumulate content/thinking/tool_calls across chunks before responding). The Python SDK can
derive tool schemas directly from Python functions. Tool support is a per-model capability — filter
the library on the `tools` tag (qwen3.5/3.6, gemma4, muse-glimmer, gpt-oss, qwen3-coder,
mistral-small3.2/medium-3.5, llama3.x, phi4-mini, deepseek-r1, nemotron-3.5-lightning...).
(docs.ollama.com/capabilities/tool-calling.md, accessed 2026-08-14)

**Structured output.** `format: "json"` (free-form JSON) or `format: <JSON schema>` for constrained
decoding against a schema; works on `/api/generate`, `/api/chat`, and with vision inputs; exposed as
`response_format` on the OpenAI endpoint. Docs recommend temperature 0 and restating the schema in the
prompt. Note: docs state structured outputs are **not currently supported on Ollama Cloud**.

```python
from pydantic import BaseModel
class Country(BaseModel):
    name: str; capital: str; languages: list[str]
r = chat(model="qwen3.5", messages=[{"role":"user","content":"Tell me about Canada."}],
         format=Country.model_json_schema())
country = Country.model_validate_json(r.message.content)
```

(docs.ollama.com/capabilities/structured-outputs.md, accessed 2026-08-14)

**Thinking.** `think: true|false` or effort strings (`"low"|"medium"|"high"|"max"`) on supported
models; reasoning arrives separately in `message.thinking`. (docs.ollama.com/api/chat.md,
/capabilities/thinking.md, accessed 2026-08-14)

## 9.10 Error handling & retry

Plain HTTP + `{"error": "..."}` bodies; no error-code taxonomy like hosted APIs.

| HTTP | Typical cause | Handling |
|---|---|---|
| 400 | Malformed JSON, missing field, bad option, `truncate:false` overflow on embed | Fix request |
| 404 | Model not pulled / unknown endpoint | `ollama pull <model>` (or POST `/api/pull`), retry |
| 500 | Engine failure (OOM during load, crashed runner) | Reduce `num_ctx`/quant/parallel; check `journalctl -u ollama` |
| conn refused / timeout | Server not running, wrong bind, model-load latency | Health-check `GET /` or `/api/tags`; allow long first-token timeouts (cold load can take tens of seconds for big models) |

Retry pattern: retries with backoff are only useful for load-contention (queued requests when memory
is constrained — Ollama queues rather than 429s) and transient runner crashes; idempotent by nature.
Cold-start mitigation: pre-warm with an empty-prompt request or `keep_alive: -1`. (Behavioral notes
from docs.ollama.com/faq.md; no official error-code table exists → codes above are observed
conventions, [UNVERIFIED as an exhaustive list].)

## 9.11 Rate limits & quotas

Local: none — capacity is your hardware. Concurrency is governed by `OLLAMA_NUM_PARALLEL` (per-model
parallel slots; each slot reserves its own KV cache) and `OLLAMA_MAX_LOADED_MODELS`; excess requests
queue when memory is insufficient. Cloud: usage tiers per plan (9.5) with weekly/hourly-style caps
implied by "light usage" wording; exact numeric quotas [UNVERIFIED — not published]. Cloud model
retirements happen (e.g. minimax-m2.5 retired 2026-07-31 per docs.ollama.com/cloud.md).

## 9.12 Fine-tuning & customization

Ollama does **no training/fine-tuning**. Customization paths:

1. **Modelfile** — prompt-level derivation: `FROM <base>`, `SYSTEM`, `TEMPLATE`, `PARAMETER`
   (temperature, num_ctx, stop, ...), `ADAPTER` (apply a LoRA), `LICENSE`/`MESSAGE`. Build with
   `ollama create mymodel -f Modelfile`; push to a namespace on ollama.com with `ollama push`.
2. **Import external weights** — GGUF (and safetensors for supported architectures) via
   `FROM ./model.gguf` in a Modelfile (docs.ollama.com/import.md); this is how you run fine-tunes made
   with axolotl/unsloth/etc.
3. **Quantize on create** — `ollama create --quantize q4_K_M` from higher-precision imports.

```dockerfile
FROM qwen3.5:9b
SYSTEM "You are a terse SQL assistant. Output only SQL."
PARAMETER temperature 0.2
PARAMETER num_ctx 16384
```

(docs.ollama.com/modelfile.md, /import.md, /cli.md, accessed 2026-08-14)

## 9.13 RAG & embedding pipeline notes

- `/api/embed` batches (`input` array) and returns `embeddings[][]`; `truncate:false` to fail loudly
  instead of silently truncating long chunks; `dimensions` for reduced-dim output where supported.
- Model choice: `qwen3-embedding:0.6b` (quality/speed balance), `embeddinggemma` (smallest good
  multilingual), `bge-m3`/`nomic-embed-text-v2-moe` for multilingual retrieval; keep the *same* model
  for indexing and querying; embedding models are separate from chat models (a chat model stays loaded
  alongside — budget memory for both, cf. `OLLAMA_MAX_LOADED_MODELS`).
- Latency: local embedding of large corpora is CPU/GPU-bound; a 0.3–0.6B embedder on any modern GPU
  processes thousands of chunks/min (estimate).
- Integrations: LangChain/LlamaIndex ship Ollama classes for both LLM and embeddings; any vector DB
  works since output is plain float arrays. Ollama also exposes a built-in **web search API/tool**
  usable to ground agents (docs.ollama.com/capabilities/web-search.md — requires ollama.com API key).

## 9.14 Agent support

- **CLI agent**: v0.32.0 introduced an interactive agent experience in the CLI (task delegation,
  coding), extended in later 0.32.x releases (github.com/ollama/ollama/releases, accessed 2026-08-14).
- **Tool-calling API** (9.9) is the primitive; docs document full agent loops.
- **Ecosystem**: official integrations listed for agent tools (OpenClaw, Claude Code, Cline, Goose,
  Droid, ...), IDEs (VS Code, JetBrains, Xcode, Zed) and workflow platforms (n8n, marimo)
  (docs.ollama.com/integrations, accessed 2026-08-14). OpenAI-compat + Anthropic-compat endpoints make
  Ollama a drop-in local backend for most agent frameworks; MCP is consumed by the client frameworks
  rather than by Ollama itself — no first-party MCP server is documented [UNVERIFIED beyond docs
  index].
- Model guidance for agents: muse-glimmer (failure recovery), qwen3.6/qwen3-coder (repo-level coding),
  gpt-oss (reasoning-effort control), nemotron-3.5-lightning (low-latency always-on loops).

## 9.15 Deployment patterns

**Linux/systemd (default from install.sh):** service `ollama.service` running as user `ollama`,
models in `/usr/share/ollama/.ollama/models`. Configure via
`sudo systemctl edit ollama` → `[Service] Environment="OLLAMA_HOST=0.0.0.0:11434" ...`; logs via
`journalctl -e -u ollama`. Pin versions with `OLLAMA_VERSION=` on the install script.
(docs.ollama.com/linux.md, accessed 2026-08-14)

**macOS:** desktop app (menu bar) or `brew`-style CLI; models in `~/.ollama/models`; MLX engine tags
for Apple-GPU-optimized weights. **Windows:** `OllamaSetup.exe` (Win 10 22H2+, no admin), runs as
background GUI service; standalone `ollama-windows-amd64.zip` for CLI-only/NSSM-service embedding;
models under `%HOMEPATH%\.ollama`. (docs.ollama.com/macos.md, /windows.md, accessed 2026-08-14)

**Docker:** `ollama/ollama` (CPU/NVIDIA via `--gpus=all` + NVIDIA Container Toolkit),
`ollama/ollama:rocm` (AMD, `--device /dev/kfd --device /dev/dri`); volume `-v ollama:/root/.ollama`;
Vulkan on by default (`OLLAMA_VULKAN=0` to disable); Jetson via `JETSON_JETPACK=5|6`.
(docs.ollama.com/docker.md, accessed 2026-08-14)

**Reverse proxy / remote access:** put Nginx/Caddy/Traefik, ngrok, or Cloudflare Tunnel in front of
`localhost:11434`; terminate TLS and add auth at the proxy (Ollama has none); set `OLLAMA_ORIGINS` for
browser clients. **Concurrency sizing:** `OLLAMA_NUM_PARALLEL` multiplies KV memory per loaded model;
`OLLAMA_MAX_LOADED_MODELS` bounds resident models; overflow queues. For multi-user production
throughput beyond a handful of parallel streams, prefer vLLM/SGLang (third-party consensus, estimate).

**GPU support matrix** (docs.ollama.com/gpu.md, accessed 2026-08-14):

| Backend | Requirements / coverage |
|---|---|
| NVIDIA CUDA | Compute capability 5.0+ (GTX 750 Ti → RTX 50xx, A/H/B-series incl. B200); driver 550+ (570+ for CC 5.0–6.2); Windows ARM64 CUDA since v0.32.3 |
| AMD ROCm | Linux: ROCm v7 — RX 7000/9000, Radeon AI PRO/PRO W, Ryzen AI, Instinct MI100–MI350X; Windows: RX 7000 + PRO W only; `HSA_OVERRIDE_GFX_VERSION` escape hatch |
| Apple Silicon | Metal on all M-series; MLX engine for optimized tags (v0.32.x) |
| Vulkan | Windows/Linux fallback for Intel/AMD/others; on by default; Linux may need drivers + `render` group |
| CPU | Universal fallback (AVX-class x86-64, ARM64) |

**Performance realities (all ESTIMATES, third-party/community-derived — Ollama publishes no official
tokens/s figures):** ~8B @ 4-bit: ~80–140 tok/s on RTX 4090-class, ~30–60 tok/s on M-series
(Pro/Max), ~5–12 tok/s CPU-only. ~30B class (or MoE with ~3B active at near-small-model speed for the
MoE case): ~25–50 tok/s on a 24 GB GPU when fully offloaded; falls off a cliff if layers spill to
system RAM. gpt-oss:120b on one 80 GB GPU: ~30–50 tok/s. Long contexts slow prefill substantially;
flash attention + `q8_0` KV cache mitigate. Treat every number here as an order-of-magnitude estimate
to verify on your own hardware [UNVERIFIED — no official source].

## 9.16 Region availability & data residency

Local: fully offline-capable after model download — data never leaves the machine; this is the
platform's core residency story. Registry pulls come from ollama.com (proxy support via
`HTTPS_PROXY`; air-gapped installs possible by copying the models directory / using `ollama pull`
through a mirror [UNVERIFIED — no official air-gap doc]). Cloud: inference hosted with NVIDIA cloud
partners primarily in the US, with possible routing to Europe/Singapore for capacity; no
region-pinning control documented. (ollama.com/cloud, accessed 2026-08-14)

## 9.17 Security, compliance & SLA

- **No authentication on the local API** — by design. Defaults are safe (`127.0.0.1` bind), but any
  `OLLAMA_HOST=0.0.0.0` or Docker `-p 0.0.0.0:11434:11434` exposure hands out unauthenticated model
  execution, model deletion, and prompt visibility. Historically thousands of exposed instances have
  been indexed by Shodan-type scanners (third-party reports). Mitigate: keep localhost bind; front
  with authenticated reverse proxy/TLS; firewall 11434; network-segment GPU hosts; for containers,
  publish only to `127.0.0.1`.
- Past RCE/path-traversal CVEs in the pull/registry path (e.g. CVE-2024-37032 "Probllama",
  third-party disclosure) argue for keeping Ollama current and not pulling untrusted model names from
  hostile registries.
- Model supply chain: library blobs are content-addressed (SHA256 digests); still, community-uploaded
  namespaces are unvetted — pin digests for production.
- Compliance/SLA: none published for the open-source runtime; Ollama Cloud states no-logging /
  no-training / zero-data-retention requirements on partners but publishes no SOC 2 / ISO cert or
  uptime SLA at access time [UNVERIFIED — not published]. (ollama.com/cloud, accessed 2026-08-14)

## 9.18 Legacy models & migration notes

| Legacy | Migrate to | Why |
|---|---|---|
| llama2 / llama3 / llama3.1 / llama3.2(-vision) / llama3.3 / llama4 | muse-glimmer (agents), qwen3.5 / gemma4 (general, vision) | Meta's open line moved to Muse; Llama tags ≥1 yr stale |
| mistral:7b, mistral-small/-3.1, mistral-nemo | mistral-small3.2 or mistral-medium-3.5 | Superseded |
| qwen2.5(-coder), qwen3 | qwen3.5/3.6, qwen3-coder | Superseded |
| gemma3 / gemma3n | gemma4 (E-series replaces 3n edge role) | Superseded |
| phi2/3/3.5 | phi4(-mini) or qwen3.5 small tags | Superseded |
| llava, minicpm-v, llama3.2-vision | qwen3-vl, gemma4, qwen3.5 | VL folded into current generalists |
| deepseek-r1 distills | still usable; qwen3.6/gpt-oss for reasoning; deepseek-v4-* is cloud-only | Aging |
| nomic-embed-text, mxbai-embed-large, all-minilm | qwen3-embedding, embeddinggemma, snowflake-arctic-embed2 | Newer multilingual embedders |
| API: `/api/embeddings` (old single-input form) | `/api/embed` | Current docs only document `/api/embed` |

Old tags remain pullable indefinitely (registry keeps blobs), so "deprecation" is soft; cloud tags do
get hard-retired (9.11).

## 9.19 Task-suitability verdict

**Best at:** privacy-constrained and offline inference; zero-cost experimentation; single-tenant
agents/coding assistants on 16–32 GB machines (qwen3.6:27b, qwen3-coder:30b, muse-glimmer,
gpt-oss:20b); local RAG (qwen3-embedding + qwen3-vl/gemma4 for multimodal docs); edge/small-footprint
deployment (gemma4 E-series, llama3.2 1B/3B, phi4-mini); acting as a drop-in OpenAI/Anthropic-compat
backend for existing tooling.

**Worst at:** frontier-quality reasoning (even the best ~35B local models trail current hosted
frontier models); high-QPS multi-user serving (use vLLM/SGLang); anything needing >80 GB-class models
without Ollama Cloud; long-context work if you forget the 4096-token default; audio/video generation
(absent); compliance-certified hosting (no certifications).

**Sweet-spot picks (2026-08):** general = `qwen3.5:9b` (8 GB VRAM) / `qwen3.6:27b` (24 GB);
agents = `muse-glimmer`; coding = `qwen3-coder:30b`; reasoning-per-GB = `gpt-oss:20b`;
edge = `gemma4:e4b`; embeddings = `qwen3-embedding:0.6b`; vision = `qwen3-vl:8b`.

## 9.20 Sources

All accessed 2026-08-14:

- https://docs.ollama.com/llms.txt (doc index) · https://docs.ollama.com/api/introduction.md
- https://docs.ollama.com/api/chat.md · https://docs.ollama.com/api/embed.md
- https://docs.ollama.com/api/openai-compatibility.md · https://docs.ollama.com/api/authentication.md
- https://docs.ollama.com/faq.md · https://docs.ollama.com/gpu.md · https://docs.ollama.com/linux.md
- https://docs.ollama.com/windows.md · https://docs.ollama.com/docker.md · https://docs.ollama.com/cloud.md
- https://docs.ollama.com/capabilities/structured-outputs.md · https://docs.ollama.com/capabilities/tool-calling.md
- https://docs.ollama.com/modelfile.md · https://docs.ollama.com/import.md
- https://ollama.com/cloud (pricing) · https://ollama.com/library (popular + newest sorts)
- Model pages: https://ollama.com/library/gpt-oss · /gemma4 · /deepseek-r1 · /qwen3.5 · /qwen3.6 ·
  /muse-glimmer · /qwen3-coder · /qwen3-vl
- Search pages: https://ollama.com/search?q=mistral · ?q=phi · ?q=llama · ?c=embedding
- https://github.com/ollama/ollama/releases (v0.32.6, 2026-08-04)
- https://github.com/ollama/ollama-python
- Performance figures in 9.15 and security-scan claims in 9.17: third-party/community, labeled as
  estimates/[UNVERIFIED] respectively.


---

# 10. Hugging Face

> **Volatility warning.** Model lineups and pricing change frequently. Verified against official
> documentation on **2026-08-14**. Re-verify before production decisions.
>
> Hugging Face is a **hub + hosting platform**, not a model vendor: there is no per-token price list of
> "Hugging Face models". Costs are either (a) pass-through partner-provider rates (Inference Providers),
> (b) per-instance-hour (Inference Endpoints, Spaces), or (c) your own hardware (self-hosting). The
> sidecar JSON therefore carries `price_*: null` with the hosting cost model in `price_notes`.

## 10.1 Platform overview & positioning

Hugging Face (HF) operates the dominant open-weight model hub (models/datasets/Spaces git-based repos)
plus four inference/product surfaces relevant here:

```
                         ┌──────────────────────────────────────────────┐
                         │              Hugging Face Hub                │
                         │  model repos (safetensors) · gated access ·  │
                         │  tokens · orgs / Team / Enterprise           │
                         └───────┬───────────┬────────────┬────────────┘
   (1) Inference Providers      (2) Inference Endpoints  (3) Self-host       (4) Spaces
   router.huggingface.co/v1     dedicated containers,     transformers v5 +  Gradio/Docker demo
   → 18 partner providers       per-instance-hour, vLLM/  vLLM/SGLang (TGI   apps, CPU/GPU/
   (Groq, Cerebras, Together,   SGLang/TGI/TEI/llama.cpp  ARCHIVED 2026-03), ZeroGPU tiers
   Fireworks, Fal, …), pass-    engines                   TEI for embeddings
   through billing + credits
```

Key 2025–2026 state changes an integrator must know:

- The old "serverless Inference API" was replaced by **Inference Providers**: HF now routes requests to
  **18 partner providers** (Baseten, Cerebras, Cohere, DeepInfra, Featherless AI, Fireworks, Groq,
  **HF Inference** (HF's own compute, one provider among many), Novita, Nscale, OVHcloud, Public AI,
  Scaleway, Together, Z.ai for LLM/VLM; Fal AI, Replicate, WaveSpeedAI for image/video/STT), with an
  OpenAI-compatible router at `https://router.huggingface.co/v1`.
  Source: https://huggingface.co/docs/inference-providers/index (2026-08-14).
- **Text Generation Inference (TGI) is end-of-life**: the GitHub repo was **archived (read-only) on
  2026-03-21**. HF's stated direction: "Going forward, we contribute to and recommend using vllm,
  SGLang, as well as local engines with inter-compatibility such as llama.cpp or MLX."
  Source: https://github.com/huggingface/text-generation-inference (2026-08-14).
- The open-weight landscape shifted: Meta de-emphasized Llama (proprietary "Muse Spark" flagship) but
  released open **Muse Glimmer 30B** (Apache-2.0) in Aug 2026; Chinese labs (Qwen, DeepSeek, Moonshot,
  Z.ai) dominate hub activity per HF's own "State of Open Source: Spring 2026" post.
  Sources: https://huggingface.co/meta-models/Muse-Glimmer-30B (2026-08-14);
  https://huggingface.co/blog/huggingface/state-of-os-hf-spring-2026 (2026-08-14).

## 10.2 Current model catalog (curated — the hub hosts ~2M repos; this is NOT exhaustive)

Selection criteria: trending/most-downloaded open-weight families on the hub as of 2026-08-14 that are
servable via at least one of the four surfaces. "FT" = weights are open, so fine-tuning is always
possible on your own compute; column marks practical LoRA/full-FT feasibility on commodity hardware.
Prices: n/a — see §10.5 hosting cost models.

| Model id (hub) | Family | Params (total/active) | Context | Modalities in→out | Tools | Struct. out | FT feasible | License | Best surface |
|---|---|---|---|---|---|---|---|---|---|
| `Qwen/Qwen3.8-2.4T-A95B` | Qwen3.8 (frontier MoE) | 2.4T / 95B | 262K native → 1.01M ext. | text→text (thinking-only) | yes | yes | no (scale) | qwen3.8-max (custom) | Inference Providers |
| `Qwen/Qwen3.6-27B` | Qwen3.6 (dense) | 27B | 262K → 1.01M ext. | text+image+video→text | yes | yes | yes | Apache-2.0 | Endpoints / self-host |
| `Qwen/Qwen3.6-35B-A3B` | Qwen3.6 (MoE) | 35B / 3B | 262K | text→text | yes | yes | yes | Apache-2.0 [MEDIUM] | self-host |
| `deepseek-ai/DeepSeek-V4-Pro-0813` | DeepSeek V4 | 1.7T MoE | ~1M ("million-token") | text→text | yes | yes | no (scale) | MIT | Inference Providers |
| `deepseek-ai/DeepSeek-V4-Flash-0731` | DeepSeek V4 | 304B MoE | [UNVERIFIED] | text→text | yes | yes | limited | MIT | Providers / Endpoints |
| `moonshotai/Kimi-K3` | Kimi K3 | 2.8T / 104B MoE | 1M | text+image+video→text | yes | yes | no (scale) | Kimi K3 License (custom) | Inference Providers |
| `zai-org/GLM-5.2` (also GLM-5.1, GLM-5) | GLM-5 | 753B MoE | 1M | text→text | yes | yes | no (scale) | MIT | Inference Providers |
| `meta-models/Muse-Glimmer-30B` | Meta Muse (open distill) | 29.6B dense (incl. 1.8B ViT) | 131,072+ | text+image→text | yes | yes | yes | Apache-2.0 | Endpoints / self-host |
| `meta-llama/Llama-4-Scout-17B-16E-Instruct`, `-Maverick-…` | Llama 4 (legacy, §10.18) | 109B/17B; 400B/17B MoE | 10M / 1M (claimed) | text+image→text | yes | yes | yes | Llama 4 Community (gated) | Endpoints / self-host |
| `google/gemma-4-31B(-it)` | Gemma 4 | 31B dense | 256K | text+image→text | yes | yes | yes | Apache-2.0 | Endpoints / self-host |
| `google/gemma-4-26B-A4B(-it)` | Gemma 4 MoE | 26B / 4B | 256K | text+image→text | yes | yes | yes | Apache-2.0 | self-host |
| `google/gemma-4-E2B` / `-E4B` / `-12B` Unified | Gemma 4 on-device | 2.3B eff / 4.5B eff / 12B | 128K | text+image+audio→text | partial | yes | yes | Apache-2.0 | self-host / Spaces |
| `mistralai/Mistral-Medium-3.5-128B` | Mistral 3.x | 128B dense | 256K | text+image→text | yes | yes | costly | Modified MIT (revenue clause) | Providers / Endpoints |
| `openai/gpt-oss-120b` / `-20b` | gpt-oss (2025) | 117B/5.1B; 21B/3.6B MoE | 128K | text→text | yes | yes | yes | Apache-2.0 | Providers (Groq/Cerebras) |
| `microsoft/phi-4`, `microsoft/Phi-4-multimodal-instruct` | Phi-4 | 14B dense | 16K | text(/img/audio for -mm)→text | yes | yes | yes | MIT | self-host / Spaces |
| `nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B` | Nemotron 3.5 | 30B / 3B MoE | [UNVERIFIED] | text→text | [UNVERIFIED] | — | yes | [UNVERIFIED — NVIDIA open license expected] | self-host |
| `LiquidAI/LFM2.5-2.6B`, `LFM2.5-VL-3B` | LFM2.5 (edge) | 2.6–3B | [UNVERIFIED] | text(/image)→text | [UNVERIFIED] | — | yes | [UNVERIFIED — LFM license] | self-host / on-device |
| `Qwen/Qwen3-VL-*` (2B…235B-A22B) | Qwen3-VL | 2B–235B | 256K [MEDIUM] | text+image+video→text | yes | yes | yes (small sizes) | Apache-2.0 [MEDIUM] | Endpoints / self-host |
| `Qwen/Qwen3-Embedding-0.6B/-4B/-8B` | Qwen3-Embedding | 0.6–8B | 32K in [MEDIUM] | text→vector (≤1024–4096d, MRL) | n/a | n/a | yes | Apache-2.0 | TEI / Endpoints |
| `google/embeddinggemma-300m` | EmbeddingGemma | 0.3B | 2K in [MEDIUM] | text→vector (768d, truncatable) | n/a | n/a | yes | Gemma license [MEDIUM] | TEI / on-device |
| `BAAI/bge-m3` | BGE | 0.6B | 8,192 in | text→dense+sparse+colbert | n/a | n/a | yes | MIT | TEI |
| `Alibaba-NLP/gte-multilingual-base` | GTE | 0.305B | 8,192 in [MEDIUM] | text→vector (elastic) | n/a | n/a | yes | Apache-2.0 [MEDIUM] | TEI |
| `sentence-transformers/all-MiniLM-L6-v2`, `all-mpnet-base-v2` | sentence-transformers | 23M / 110M | 256–384 in | text→vector (384/768d) | n/a | n/a | yes | Apache-2.0 | TEI / anywhere |
| `openai/whisper-large-v3`, `-v3-turbo` | Whisper | 1.55B / 0.81B | 30s chunks | audio→text (99 langs) | n/a | n/a | yes | Apache-2.0 (HF card) | Providers (fal) / Endpoints |
| `black-forest-labs/FLUX.2-dev`, `FLUX.2-klein-4B/-9B` | FLUX.2 | 4–9B (klein) / [UNVERIFIED] dev | n/a | text(+image)→image | no | no | LoRA | dev: non-commercial [MEDIUM]; klein: see card | Providers (fal/Replicate) / Spaces |

Sources (all 2026-08-14): model pages fetched directly — Qwen3.8-2.4T-A95B, Qwen3.6-27B,
DeepSeek-V4-Pro-0813, moonshotai/Kimi-K3, zai-org/GLM-5.2, meta-models/Muse-Glimmer-30B,
mistralai/Mistral-Medium-3.5-128B; https://huggingface.co/blog/gemma4;
https://huggingface.co/models?sort=trending; embedding picks cross-checked against
https://www.bentoml.com/blog/a-guide-to-open-source-embedding-models (third-party). Rows tagged
[MEDIUM]/[UNVERIFIED] were not re-verified against their model card on the access date.

## 10.3 Model details & limitations

- **Qwen3.8 / Qwen3.6 (Alibaba).** Flagship `Qwen3.8-2.4T-A95B`: MoE "2.4T in total and 95B activated",
  hybrid "Gated DeltaNet → MoE / Gated Attention → MoE" blocks, 512 experts (11 active), context
  "262,144 natively and extensible up to 1,010,000 tokens"; text-only and **requires thinking mode for
  all interactions**. License is **custom (`qwen3.8-max`)**, unlike the Apache-2.0 mid-tier
  Qwen3.6-27B (dense, multimodal-in, Apr 2026). Check license per checkpoint — the family mixes terms.
  Source: https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B; https://huggingface.co/Qwen/Qwen3.6-27B (2026-08-14).
- **DeepSeek V4 (MIT).** `V4-Pro-0813` (1.7T MoE, "million-token context intelligence", supersedes the
  preview) and `V4-Flash-0731` (304B). Deployment guidance on the card is vLLM-first
  (`--enable-expert-parallel`, `--moe-backend deep_gemm_mega_moe`). Practically served via Inference
  Providers; self-hosting Pro requires multi-node H200-class clusters.
  Source: https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813 (2026-08-14).
- **Kimi K3 (Moonshot).** "2.8T total parameters", "104B activated per token", 93 layers
  ("69 KDA + 24 Gated MLA"), 1M-token window, **native multimodal** (text/images/video, MoonViT-V2
  401M encoder). Custom "Kimi K3 License". Source: https://huggingface.co/moonshotai/Kimi-K3 (2026-08-14).
- **GLM-5.2 (Z.ai).** 753B MoE, 1M context ("IndexShare" sparse-attention indexer reuse, claimed 2.9×
  per-token FLOP reduction at 1M), MIT, thinking-effort levels; vLLM/SGLang/transformers supported.
  Source: https://huggingface.co/zai-org/GLM-5.2 (2026-08-14).
- **Meta Muse Glimmer 30B.** "30-billion-parameter causal language model with a dedicated perception
  encoder, distilled from Muse Spark and purpose-built for autonomous agentic tasks on consumer
  hardware." Dense, 52 layers, ~1.8B ViT-G/14 encoder, 131K+ context, Apache-2.0, Aug 2026, knowledge
  cutoff 2026-01-04. The larger Muse Spark is **proprietary** — Glimmer is Meta's only current
  open-weight release. Source: https://huggingface.co/meta-models/Muse-Glimmer-30B (2026-08-14).
- **Gemma 4 (Google, Apr 2026).** Five sizes, all base+IT, **all Apache-2.0** (change from the bespoke
  Gemma license): E2B ("2.3B effective, 5.1B with embeddings"), E4B, 12B "Unified" (encoder-free
  multimodal), 31B dense, 26B-A4B MoE. 128K (E-series) / 256K context; images+text everywhere, audio-in
  on E2B/E4B/12B. Per-Layer Embeddings + shared-KV-cache for on-device memory.
  Source: https://huggingface.co/blog/gemma4 (2026-08-14).
- **Mistral Medium 3.5 (128B dense, 256K).** "First flagship merged model" (instruct+reasoning+coding
  in one set of weights, per-request reasoning effort); replaces Magistral/Devstral 2 in Mistral's own
  products. **Modified MIT**: free "commercial and non-commercial use with exceptions for companies
  with large revenue". Source: https://huggingface.co/mistralai/Mistral-Medium-3.5-128B (2026-08-14).
- **gpt-oss (OpenAI, Aug 2025).** Still the only OpenAI open weights; Apache-2.0, MXFP4-quantized MoE
  (120b fits one 80GB GPU; 20b fits 16GB). Heavily used in HF's own docs examples
  (`openai/gpt-oss-120b:groq`). No 2026 successor found. Sources:
  https://huggingface.co/blog/welcome-openai-gpt-oss; https://openai.com/index/introducing-gpt-oss (2026-08-14).
- **Phi-4 (Microsoft, MIT).** 14B dense reasoning SLM + `Phi-4-multimodal-instruct` (text/image/audio).
  A "Phi-5" is reported by third parties; `microsoft/phi-5` returned HTTP 401 (gated or nonexistent) at
  access time — [UNVERIFIED]. Source: https://huggingface.co/microsoft/phi-4 (2026-08-14).

Cross-cutting constraints: context figures are **native** values from model cards — partner providers
frequently serve reduced windows (check per-provider model page tab); quantized community variants
(`unsloth/*-GGUF`, FP8) differ in quality; MoE VRAM needs are set by **total**, not active, params.

## 10.4 Embedding / audio / vision / video models

- **Embeddings** (serve with TEI, §10.13): `Qwen3-Embedding` 0.6B/4B/8B (multilingual,
  instruction-aware, Matryoshka dims), `embeddinggemma-300m` (edge, "<200MB RAM", 768d truncatable to
  512/256/128), `BAAI/bge-m3` (dense+sparse+ColBERT multi-vector, 8K input), `gte-multilingual-base`,
  classic `sentence-transformers` baselines, `jinaai/jina-embeddings-v4` (multimodal, 2048d — note
  **CC-BY-NC-4.0**, not commercial-safe). Rerankers: `BAAI/bge-reranker-*` family served by TEI's
  sequence-classification path. Source: https://www.bentoml.com/blog/a-guide-to-open-source-embedding-models
  (third-party, 2026-08-14); model cards not individually re-verified.
- **Audio/ASR**: `openai/whisper-large-v3` and `-v3-turbo` remain the default open ASR (99 languages);
  served via Providers (`automatic-speech-recognition` task, e.g. fal) or Endpoints. Newer NVIDIA
  speech stacks (`NVIDIA-NemotronLabs-VoiceChat-11B`) are trending but [UNVERIFIED] in detail.
  Source: https://huggingface.co/openai/whisper-large-v3-turbo (2026-08-14, existence).
- **Vision-language**: Qwen3.6-27B, Kimi K3, Muse Glimmer, Gemma 4, Mistral Medium 3.5 are natively
  multimodal-in (see §10.2); dedicated VLM lines: Qwen3-VL (2B→235B-A22B), `LiquidAI/LFM2.5-VL-3B`.
- **Image/video generation**: FLUX.2 (`-dev` gated non-commercial [MEDIUM]; `-klein-4B/9B` small
  variants), `Lightricks/LTX-2.5` (video), `MiniMaxAI/MiniMax-H3` ecosystem (image; heavy
  ComfyUI/LoRA activity) — generation models are best consumed through Providers (fal, Replicate,
  WaveSpeedAI) or ZeroGPU Spaces. Trending observations: https://huggingface.co/models?sort=trending (2026-08-14).

## 10.5 Pricing model & cost notes

Four distinct cost models (all USD):

**(1) Inference Providers — pass-through per-token/per-request + included credits.**
"Hugging Face charges you the same rates as the provider, with no additional fees. We just pass through
the provider costs directly." Monthly included credits: **Free $0.10** ("subject to change), **PRO
$2.00**, **Team/Enterprise $2.00 per seat** (pooled org-wide). Beyond credits: pay-as-you-go on your HF
account (free users must pre-purchase credits). Alternative: register a **custom provider key** → billed
directly by that provider, HF credits do not apply. HF-Inference (HF's own provider) bills
compute-time × hardware rate (example given: 10s FLUX.1-dev on $0.00012/s GPU = $0.0012).
Org billing attribution: `X-HF-Bill-To` header / `InferenceClient(bill_to="org")`.
Per-model per-provider token prices are listed on each model page's "Inference Providers" widget, not in
a central table. Source: https://huggingface.co/docs/inference-providers/pricing (2026-08-14).

**(2) Inference Endpoints — per instance-hour, billed by the minute** (charged only in
initializing/running states). Representative rates (full matrix in docs):

| Instance | Cloud | HW | $/h |
|---|---|---|---|
| intel-spr x1 (1 vCPU/2GB) | AWS | CPU | 0.033 |
| nvidia-t4 x1 (14GB) | AWS | T4 | 0.50 |
| nvidia-l4 x1 (24GB) | AWS | L4 | 0.80 |
| nvidia-a10g x1 (24GB) | AWS | A10G | 1.00 |
| nvidia-l40s x1 (48GB) | AWS | L40S | 1.80 |
| nvidia-a100 x1 (80GB) | AWS | A100 | 2.50 |
| nvidia-h200 x1 (141GB) | AWS | H200 | 5.00 |
| nvidia-h100 x1 (80GB) | GCP | H100 | 10.00 |
| inf2 x1 | AWS | Inferentia2 | 0.75 |
| tpu 1x1 | GCP | TPU v5e | 1.20 |

Cost = rate × ((hours × min replicas) + (scale-up hours × extra replicas)). **Scale-to-zero** stops
compute billing but still consumes quota (pause to release). Source:
https://huggingface.co/docs/inference-endpoints/en/pricing (2026-08-14).

**(3) Spaces — per hardware-hour, by the minute** (only while Starting/Running): CPU Basic free
(2 vCPU/16GB; note: **creating Gradio/Docker Spaces now requires a paid plan** — static Spaces stay
free); CPU Upgrade $0.03/h; T4 small/medium $0.40/$0.60; L4 $0.80 (4×L4 $3.80); L40S $1.80
(4× $8.30, 8× $23.50); A10G small/large $1.00/$1.50 (2×/4× large $3.00/$5.00); A100 $2.50
(4× $10.00, 8× $20.00). **H100 tiers were removed from Spaces in Dec 2025.** Free Spaces auto-suspend
after 48h idle. Source: https://huggingface.co/docs/hub/en/spaces-gpus (2026-08-14).

**(4) ZeroGPU (dynamic shared GPU for Spaces)** — NVIDIA RTX Pro 6000 Blackwell slices: `large`
(48GB, 1× quota) / `xlarge` (96GB, 2× quota). Daily quotas: unauthenticated 2 min, free 5 min, PRO/Team
40 min, Enterprise 60 min; PRO = 8× free quota + highest queue priority; overage via prepaid credits at
**$1 per 10 GPU-minutes**. Source: https://huggingface.co/docs/hub/en/spaces-zerogpu (2026-08-14).

**Subscriptions** (https://huggingface.co/pricing, 2026-08-14): PRO **$9/mo** (20× inference credits,
8× ZeroGPU, 10× private storage, Dev Mode); Team **$20/user/mo**; Enterprise **from $50/user/mo**;
Enterprise Plus custom.

## 10.6 Authentication & environment

- **User access tokens** (`hf_…`), created at hf.co/settings/tokens; roles: **fine-grained** (scope to
  specific repos/orgs and permissions — includes an "Inference Providers" permission; recommended for
  production), **read**, **write**. "Create one access token per app or usage."
  Source: https://huggingface.co/docs/hub/en/security-tokens (2026-08-14).
- Standard env var: `HF_TOKEN` (used throughout Inference Providers docs). CLI login: `hf auth login`
  (Python: `huggingface_hub.login()`).
- One HF token authorizes **all partner providers** through the router — no per-provider keys needed
  unless you opt into custom-key billing (configured at hf.co/settings/inference-providers).
- Org auth (Team/Enterprise): SSO (SAML/OIDC), SCIM (Enterprise+), OAuth token exchange, centralized
  token policy/revocation. Source: https://huggingface.co/docs/hub/en/enterprise-hub (2026-08-14).
- Gated repos (Llama 4, FLUX.2-dev, …): user must accept terms on the model page; access is granted
  per-user (automatic or manual approval); token must belong to a granted user. Programmatic
  management: `/api/models/{repo_id}/user-access-request/{pending|accepted|handle|grant}`.
  Source: https://huggingface.co/docs/hub/en/models-gated (2026-08-14).

## 10.7 API endpoints & schemas

| Surface | Base URL | Notes |
|---|---|---|
| Inference Providers (OpenAI-compatible) | `https://router.huggingface.co/v1/chat/completions` | chat-completion only; `GET /v1/models` lists routable models |
| Inference Providers (task APIs) | via `huggingface_hub` / `@huggingface/inference` clients | text-to-image, ASR, feature-extraction, etc. |
| Inference Endpoints (dedicated) | per-endpoint URL from ui.endpoints.huggingface.co | engine-native API (vLLM/SGLang/TGI/TEI expose OpenAI-style routes) |
| Hub API | `https://huggingface.co/api/...` | search, repo CRUD, access requests |
| File download ("resolvers") | `https://huggingface.co/<repo>/resolve/<rev>/<file>` | highest rate limits |

Model naming on the router: `<org>/<model>` plus optional suffix — explicit provider
(`openai/gpt-oss-120b:groq`) or policy: `:fastest` (default; highest tokens/s), `:cheapest` (lowest
price per output token), `:preferred` (your settings order). `provider="auto"` fails over automatically
when a provider is flagged unavailable. Request schema = OpenAI chat completions: `messages*`, `tools`,
`response_format` (`text` | `json_object` | `json_schema`), `stream` (SSE), `temperature`,
`max_tokens`, `top_p`. No API versioning header; the `/v1` path is the contract.
Sources: https://huggingface.co/docs/inference-providers/index;
https://huggingface.co/docs/inference-providers/tasks/chat-completion (2026-08-14).

## 10.8 SDK integration

**Python — huggingface_hub `InferenceClient`** (v1.x; auto-handles 429 retry since v1.2.0):

```python
import os
from huggingface_hub import InferenceClient

client = InferenceClient(provider="auto", api_key=os.environ["HF_TOKEN"])  # bill_to="my-org" optional

resp = client.chat_completion(
    [{"role": "user", "content": "What is the capital of France?"}],
    model="deepseek-ai/DeepSeek-V4-Flash-0731",
    max_tokens=100,
)
print(resp.choices[0].message.content)

image = client.text_to_image("Astronaut riding a horse",
                             model="black-forest-labs/FLUX.1-schnell")   # PIL.Image
```

**Python — OpenAI SDK against the router:**

```python
from openai import OpenAI
client = OpenAI(base_url="https://router.huggingface.co/v1",
                api_key=os.environ["HF_TOKEN"])
out = client.chat.completions.create(
    model="openai/gpt-oss-120b:cerebras",
    messages=[{"role": "user", "content": "What is the capital of France?"}])
```

**JavaScript — `@huggingface/inference`:**

```typescript
import { InferenceClient } from "@huggingface/inference";
const hf = new InferenceClient(process.env.HF_TOKEN);

const out = await hf.chatCompletion({
  model: "Qwen/Qwen3-32B", provider: "cerebras",
  messages: [{ role: "user", content: "Hello, nice to meet you!" }],
  max_tokens: 512,
});

const vec = await hf.featureExtraction({
  model: "sentence-transformers/all-MiniLM-L6-v2",
  inputs: "That is a happy person",
});
```

**curl:**

```bash
curl https://router.huggingface.co/v1/chat/completions \
  -H "Authorization: Bearer $HF_TOKEN" -H 'Content-Type: application/json' \
  -d '{"model":"openai/gpt-oss-120b:fastest",
       "messages":[{"role":"user","content":"Hello"}],"stream":false}'
```

Sources: https://huggingface.co/docs/huggingface_hub/en/guides/inference;
https://huggingface.co/docs/huggingface.js/inference/README;
https://huggingface.co/docs/inference-providers/tasks/chat-completion (all 2026-08-14).

## 10.9 Streaming, tool use, structured output

- **Streaming**: `stream=True` → SSE chunks, OpenAI delta format (`chunk.choices[0].delta.content`);
  JS: `for await (const chunk of hf.chatCompletionStream({...}))`.
- **Tool use**: OpenAI-style `tools` array on the router/clients. Support is **model- and
  provider-dependent** — verify on the model page's provider widget before relying on it.
- **Structured output**: `response_format: {"type":"json_schema", ...}` (also `json_object`) on the
  chat-completion schema; again provider-dependent enforcement.
- Non-chat tasks (text-to-image, ASR, embeddings) are **not** on the OpenAI-compatible route — use the
  HF clients' task methods.
Source: https://huggingface.co/docs/inference-providers/tasks/chat-completion (2026-08-14).

## 10.10 Error handling & retry

| Code | Meaning (HF surfaces) | Handling |
|---|---|---|
| 401 | invalid/missing token; also returned on some gated/unreleased repos | check token + gated access |
| 402 | credits exhausted / payment required (Providers pay-as-you-go) [MEDIUM — behavior per billing docs, code not explicitly tabulated] | add credits / upgrade |
| 403 | gated repo without accepted terms; fine-grained token missing permission | request access; widen token scope |
| 404 | model not routable by any enabled provider | check model page provider list |
| 429 | rate limit (5-min windows, §10.11) — response carries `RateLimit` / `RateLimit-Policy` headers | wait per header; `huggingface_hub` ≥1.2.0 auto-retries |
| 5xx | provider-side failure | with `provider="auto"`, router fails over; otherwise retry with backoff |

Official docs publish the 429-header contract explicitly; the rest of the table reflects standard HTTP
semantics observed across HF docs, not a single published error table.
Source: https://huggingface.co/docs/hub/en/rate-limits (2026-08-14).

## 10.11 Rate limits & quotas

Hub-wide request limits, **5-minute fixed windows** (per Sept-2025 revision, current at access):

| Plan | Hub API | Resolvers (downloads) | Pages |
|---|---|---|---|
| Anonymous (per IP) | 500 | 3,000 | 100 |
| Free user | 1,000 | 5,000 | 200 |
| PRO | 2,500 | 12,000 | 400 |
| Team org | 3,000 | 20,000 | 400 |
| Enterprise org | 6,000 | 50,000 | 600 |
| Enterprise Plus | 10,000 | 100,000 | 1,000 |

Inference Providers has **no published request-rate table** — throughput limits are the underlying
provider's; HF-side constraint is billing (credits / pay-as-you-go, §10.5). ZeroGPU daily GPU-time
quotas: §10.5(4). Endpoints instance quotas: shown per-account at ui.endpoints.huggingface.co.
Source: https://huggingface.co/docs/hub/en/rate-limits (2026-08-14).

## 10.12 Fine-tuning & customization

No managed per-token fine-tuning API exists on any of the four surfaces. Options:
- **Self-managed training** with the open stack: `transformers` (v5.x) Trainer, TRL (SFT/DPO/GRPO),
  PEFT/LoRA — on your own GPUs or rented compute. This is the normal path for every open-weight model
  in §10.2 whose license permits derivatives.
- **AutoTrain (Advanced)**: HF's no-code training UI/library (runs in Spaces or locally); docs live at
  https://huggingface.co/docs/autotrain (2026-08-14; feature currency [MEDIUM]).
- Trained weights are then served via Endpoints (upload repo → deploy) or merged LoRAs via
  vLLM/SGLang self-hosting.
Licenses gate this: MIT/Apache families (DeepSeek V4, GLM-5.2, Gemma 4, Muse Glimmer, gpt-oss, Phi-4)
allow derivatives freely; custom licenses (qwen3.8-max, Kimi K3, Llama 4 Community, FLUX.2-dev) impose
conditions — read per repo.

## 10.13 RAG & embedding pipeline notes (TEI)

**Text Embeddings Inference (TEI)** — Rust/Candle server for embeddings + rerankers + classifiers;
actively maintained (latest **v1.9.x** at access; Qwen3-Embedding and Blackwell support landed in the
1.8–1.9 line). Features: token-based dynamic batching, Flash Attention/cuBLASLt, safetensors-only fast
boot, OTel + Prometheus. Sources: https://huggingface.co/docs/text-embeddings-inference/en/index;
https://github.com/huggingface/text-embeddings-inference/releases (2026-08-14).

```bash
docker run --gpus all -p 8080:80 -v $PWD/data:/data \
  ghcr.io/huggingface/text-embeddings-inference:1.9 \
  --model-id Qwen/Qwen3-Embedding-0.6B
# POST /embed {"inputs": "..."}  |  POST /rerank {"query": "...", "texts": [...]}
```
(Tag `1.9` per release line; pick the CPU/Turing/Ampere/Hopper-specific image per docs — exact tags not
re-verified 2026-08-14.)

Pipeline notes: serverless embeddings also available via `feature_extraction` on the HF-Inference
provider; for production RAG prefer dedicated TEI (Endpoints supports TEI as a managed engine, §10.15).
BGE-M3's hybrid dense+sparse output pairs well with reciprocal-rank fusion; Qwen3-Embedding/
EmbeddingGemma support dimension truncation (Matryoshka) to cut vector-store cost.

## 10.14 Agent support

- **HF MCP Server** (`https://huggingface.co/mcp`): official MCP server exposing hub search, Spaces
  tools, and (per docs) Inference Providers access to MCP clients.
  Docs: https://huggingface.co/docs/hub/hf-mcp-server (2026-08-14; existence verified, tool list not audited).
- **smolagents**: HF's minimal agent framework (code-executing agents, MCP tool import) —
  https://huggingface.co/docs/smolagents (2026-08-14).
- **tiny-agents** in `huggingface_hub`/`@huggingface/inference`: MCP-client agent loop over Inference
  Providers [MEDIUM — not re-verified].
- Tool calling via the OpenAI-compatible router works with any OpenAI-style agent framework by swapping
  `base_url`.

## 10.15 Deployment patterns

| Pattern | Surface | When |
|---|---|---|
| Serverless multi-provider | Inference Providers | spiky traffic, frontier open models (2.4T-class) you cannot host |
| Dedicated managed container | Inference Endpoints (engines: **vLLM, SGLang, TGI, TEI, llama.cpp, custom image**; "for most use cases, TGI, vLLM, and SGLang will be equivalently good options") | steady traffic, private models, autoscale 0..N |
| Self-host | vLLM / SGLang (HF-recommended post-TGI), TGI 3.3.x frozen, llama.cpp/MLX local | full control, data locality |
| Demo/prototype | Spaces (Gradio SDK, `@spaces.GPU` on ZeroGPU) | showcases, internal tools |

Self-host notes: `transformers` **v5.x** (v5.12.x at access) is the model-definition layer; vLLM/SGLang
consume hub checkpoints directly (`vllm serve <repo-id>`). TGI remains runnable
(`ghcr.io/huggingface/text-generation-inference:3.3.5`, README) but archived — treat as frozen; plan
migrations to vLLM (also the engine DeepSeek/GLM cards document first). Hardware rule-of-thumb: BF16
needs ≈2 bytes/param + KV cache (Muse Glimmer 30B ≈ 1×80GB; Gemma-4-26B-A4B still needs total-param
VRAM despite 4B active); FP8/MXFP4 checkpoints halve/quarter that (gpt-oss-120b on one 80GB GPU).
Sources: https://github.com/huggingface/text-generation-inference;
https://github.com/huggingface/transformers/releases;
https://huggingface.co/docs/inference-endpoints/en/engines/vllm (2026-08-14).

## 10.16 Region availability & data residency

- Inference Endpoints: AWS / Azure / GCP instances; region selected at endpoint creation (per-region
  instance availability varies; matrix in pricing docs).
- Inference Providers: requests route to partner infrastructure — **data residency is provider-dependent
  and not contractually pinned by HF**; providers can be disabled org-wide in settings.
- Hub storage: **Storage Regions** (data residency for repos) available on Team+ plans.
- Chinese-origin models are hub-hosted globally; the weights themselves carry no region lock (MIT/Apache
  where noted).
Sources: https://huggingface.co/docs/inference-endpoints/en/pricing;
https://huggingface.co/docs/hub/en/enterprise-hub (2026-08-14). Formal residency guarantees beyond
Storage Regions: [UNVERIFIED — not published].

## 10.17 Security, compliance & SLA

- **Serialization**: pickle (`pytorch_model.bin`) allows arbitrary code execution on load ("Do not
  unpickle data from untrusted sources"). Hub countermeasures: ClamAV scan + pickle-import scan on
  every upload (opcode-level via `pickletools.genops`, "not 100% foolproof"). **Prefer safetensors**
  — the ecosystem default; TEI loads safetensors only; pickle is scanned but not banned.
  Source: https://huggingface.co/docs/hub/en/security-pickle (2026-08-14).
- **`trust_remote_code=True`** (transformers) executes repository Python at load time — treat as
  running untrusted code: pin a revision (`revision="<commit-sha>"`), audit the repo, sandbox. Most
  §10.2 families are natively supported in transformers v5 and do **not** need it.
- **Gated models + fine-grained tokens** limit exfiltration blast radius (§10.6).
- Enterprise features: audit logs, resource groups, RBAC, 2FA enforcement, SCIM, network
  security/IP-range controls and managed users (Enterprise Plus), malware/secret scanning on repos.
  Source: https://huggingface.co/docs/hub/en/enterprise-hub (2026-08-14).
- Certifications/SLA: Enterprise gets "email support with SLA"; SOC 2 / ISO status:
  [UNVERIFIED — not found on accessed docs pages; check trust.huggingface.co before procurement].
  No uptime SLA is published for Inference Providers or Endpoints on accessed pages: [UNVERIFIED].

## 10.18 Legacy models & migration notes

- **TGI → vLLM/SGLang**: repo archived 2026-03-21; both alternatives expose OpenAI-compatible servers,
  so client migration is a base-URL change; server flags differ (`--model-id` → `vllm serve`).
- **"Inference API (serverless)" → Inference Providers**: old task-endpoint URLs
  (`api-inference.huggingface.co`) are superseded by the router + clients; HF-Inference persists as one
  provider.
- **Llama 4** (Scout/Maverick, 2025): still downloadable/gated but no longer Meta's active open line —
  new work should evaluate Muse Glimmer 30B or §10.2 alternatives.
- **DeepSeek-R1 / V3.x, Qwen3/3.5, GLM-4.x, Gemma 3, Phi-3.5, Mistral Small 3.x / Large 2**:
  superseded generations; repos remain live (hub never deletes), fine for existing pipelines.
- **Spaces H100 tiers** removed Dec 2025 → migrate GPU Spaces to L40S/A100 or ZeroGPU.

## 10.19 Task-suitability verdict

**Best at**: access to the entire open-weight frontier (2.4T Qwen, 1.7T DeepSeek, Kimi K3, GLM-5.2)
behind one token and one OpenAI-compatible URL with zero markup and provider failover; cheap dedicated
serving of small/mid models (L4 at $0.80/h); embeddings at scale via TEI; demos via ZeroGPU at
near-zero cost; full-control self-hosting with no vendor lock-in (weights are yours).
**Worst at / caveats**: no proprietary frontier models (no GPT-5.6/Claude/Gemini); Providers gives no
HF-side latency/uptime SLA and per-provider feature variance (tool use, JSON schema, context caps)
demands per-model verification; multi-thousand-param MoE flagships are effectively Providers-only
(self-hosting needs multi-node clusters); license heterogeneity (MIT ↔ custom Qwen/Kimi/Llama terms)
requires per-repo legal review; pickle/`trust_remote_code` risks require repo hygiene discipline.

## 10.20 Sources

All accessed 2026-08-14:
- https://huggingface.co/docs/inference-providers/index · /pricing · /tasks/chat-completion · /guides/first-api-call
- https://huggingface.co/docs/inference-endpoints/en/pricing · /engines/vllm
- https://huggingface.co/docs/hub/en/spaces-gpus · /spaces-zerogpu · /rate-limits · /security-tokens · /security-pickle · /models-gated · /enterprise-hub · /hf-mcp-server
- https://huggingface.co/docs/huggingface_hub/en/guides/inference · https://huggingface.co/docs/huggingface.js/inference/README
- https://huggingface.co/docs/text-embeddings-inference/en/index · https://github.com/huggingface/text-embeddings-inference/releases
- https://github.com/huggingface/text-generation-inference (archived) · https://github.com/huggingface/transformers/releases
- https://huggingface.co/pricing · https://huggingface.co/models?sort=trending
- Model cards: Qwen/Qwen3.8-2.4T-A95B · Qwen/Qwen3.6-27B · deepseek-ai/DeepSeek-V4-Pro-0813 · moonshotai/Kimi-K3 · zai-org/GLM-5.2 · meta-models/Muse-Glimmer-30B · mistralai/Mistral-Medium-3.5-128B · microsoft/phi-4
- https://huggingface.co/blog/gemma4 · https://huggingface.co/blog/huggingface/state-of-os-hf-spring-2026 · https://huggingface.co/blog/welcome-openai-gpt-oss
- Third-party (labeled): https://www.bentoml.com/blog/a-guide-to-open-source-embedding-models


---

# Part III — Cross-Provider Integration Blueprints (sections 11–20)

> **Volatility warning.** Everything provider-specific below is grounded in the Part II chapters,
> which were verified against official documentation on **2026-08-14**. Model lineups, prices, API
> shapes and limits change frequently — re-verify against the cited chapter (and its sources) before
> production decisions. Where a pattern is generic engineering knowledge rather than a chapter
> finding, it is labeled as such.

---

## 11. Provider-agnostic client patterns

### 11.1 Environment configuration — all 8 providers

| Provider | Key env var(s) | Auth mechanism | Base URL | Primary endpoint |
|---|---|---|---|---|
| OpenAI | `OPENAI_API_KEY` | `Authorization: Bearer` | `https://api.openai.com/v1` | `POST /responses` (recommended); `/chat/completions` supported (ch. 3 §3.6–3.7) |
| Google Gemini | `GEMINI_API_KEY` (`GOOGLE_API_KEY` also honored by SDKs) | `x-goog-api-key` header | `https://generativelanguage.googleapis.com` (`/v1beta`) | `POST /v1beta/interactions` (GA, recommended); `models/{m}:generateContent` classic (ch. 4 §4.6–4.7) |
| Anthropic | `ANTHROPIC_API_KEY` | `x-api-key` + required `anthropic-version: 2023-06-01` | `https://api.anthropic.com` | `POST /v1/messages` (ch. 5 §5.6–5.7) |
| AWS Bedrock | `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`/`AWS_SESSION_TOKEN` (or IAM roles — preferred); `AWS_BEARER_TOKEN_BEDROCK` for Bedrock API keys | SigV4 signing; API key on mantle | `bedrock-runtime.{region}.amazonaws.com`; `bedrock-mantle.{region}.api.aws` | `Converse`/`ConverseStream`; mantle: `/openai/v1`, `/anthropic/v1/messages` (ch. 6 §6.6–6.7) |
| Azure / Microsoft Foundry | `AZURE_OPENAI_API_KEY` (or Entra ID via `azure-identity`, recommended) | `api-key` header / Bearer token | `https://<resource>.openai.azure.com/openai/v1/` | `POST /responses`, `/chat/completions` — `model` = **deployment name** (ch. 7 §7.6–7.7) |
| OpenRouter | `OPENROUTER_API_KEY` | `Authorization: Bearer` | `https://openrouter.ai/api/v1` | `POST /chat/completions`; `GET /models` for live catalog (ch. 8 §8.6–8.7) |
| Ollama (local) | none — **no auth on local API**; `OLLAMA_API_KEY` for Ollama Cloud | none locally; Bearer for cloud | `http://localhost:11434` (`/api` native, `/v1` OpenAI-compat, `api_key="ollama"` placeholder) | `POST /api/chat`; `/v1/chat/completions` (ch. 9 §9.6–9.7) |
| Hugging Face | `HF_TOKEN` | `Authorization: Bearer` | `https://router.huggingface.co/v1` | `POST /chat/completions` (chat only; other tasks via HF clients) (ch. 10 §10.6–10.7) |

Suggested twelve-factor layout — one variable set per provider, plus one selector:

```bash
LLM_PROVIDER=openai            # openai|gemini|anthropic|bedrock|azure|openrouter|ollama|hf
LLM_MODEL=gpt-5.6-terra        # provider-native model id (Azure: deployment name)
OPENAI_API_KEY=...             # only the providers you actually use
ANTHROPIC_API_KEY=...
GEMINI_API_KEY=...
AWS_REGION=us-east-1           # Bedrock: credentials from the standard AWS chain, no static key
AZURE_OPENAI_BASE_URL=https://myres.openai.azure.com/openai/v1/
OPENROUTER_API_KEY=...
HF_TOKEN=...
OLLAMA_BASE_URL=http://localhost:11434/v1
```

### 11.2 The thin-adapter pattern

Many surfaces speak the **OpenAI wire format**, so one `OpenAI()` client with a swapped
`base_url`/`api_key` covers a surprising share of the matrix:

```
                    ┌───────────────────────────────────────────────┐
                    │        openai SDK (base_url override)         │
                    └───┬──────────┬──────────┬──────────┬──────┬───┘
                        │          │          │          │      │
   api.openai.com/v1   openrouter  localhost  generative  bedrock-mantle…/openai/v1
   (Responses + Chat)  .ai/api/v1  :11434/v1  language…   (Responses+Chat; ch. 6 §6.8)
                       (Chat only) (Chat +    /v1beta/    <resource>.openai.azure.com
                       (ch. 8)     partial    openai/     /openai/v1 (ch. 7 §7.7)
                                   Responses; (beta,      router.huggingface.co/v1
                                   ch. 9 §9.7) ch. 4 §4.7) (Chat only; ch. 10 §10.7)
```

OpenAI-compatible surfaces (per chapters): **OpenRouter** (Chat Completions + extensions),
**Ollama** `/v1` (Chat Completions, embeddings, partial `/v1/responses` since v0.13.3; no
`logprobs`/`tool_choice`/`n` — ch. 9 §9.7), **Gemini compat endpoint** (beta: chat, embeddings,
images, audio, partial batch — ch. 4 §4.7), **Azure v1 API** (wire-identical Responses/Chat plus
Azure extensions — ch. 7 §7.7), **Bedrock mantle** (`/openai/v1`, and the *only* path to GPT-5.x
on Bedrock — ch. 6 §6.1), **HF router** (chat-completion task only — ch. 10 §10.7).

**Where the thin adapter breaks:**

- **Anthropic Messages** (first-party): different envelope entirely — `x-api-key` +
  `anthropic-version` headers, required `max_tokens`, content-block arrays, `tool_use`/`tool_result`
  blocks, `output_config` for structured output, its own SSE event grammar (ch. 5 §5.7–5.9). Use the
  `anthropic` SDK (which itself re-targets Bedrock mantle `/anthropic/v1/messages` and Ollama's
  Anthropic-compat endpoint via base-URL swap — ch. 6 §6.8, ch. 9 §9.7).
- **Bedrock Converse** (classic runtime): AWS-native JSON (`messages[].content[]` blocks,
  `inferenceConfig`, `toolConfig`) over SigV4 — model-agnostic *within Bedrock* but not
  OpenAI-shaped; streaming is an AWS event stream, not SSE (ch. 6 §6.7, §6.9).
- **Responses vs Chat Completions divergence**: OpenAI's recommended surface (Responses) has
  different tool and structured-output shapes (`text.format`, top-level tool `name`) than the Chat
  Completions shape the compat providers implement (ch. 3 §3.7, §3.9). A "thin adapter" that
  assumes Chat Completions everywhere quietly forfeits Responses-only features (built-in tools,
  `previous_response_id`, conversations).
- **Feature depth varies per compat surface**: e.g. Gemini compat is beta and skips
  Interactions-only features; Ollama compat ignores the API key and lacks `tool_choice`; HF router
  exposes no non-chat tasks; the same OpenRouter model id may hit endpoints with different
  parameter support (`supported_parameters` is the truth source — ch. 8 §8.3).

Practical adapter design (generic guidance): keep an internal request type of
`{model, system, messages, tools, json_schema, max_tokens, stream}`; write one adapter per *wire
format* (OpenAI-chat, OpenAI-responses, Anthropic-messages, Bedrock-converse, Gemini-interactions),
not one per vendor — that is 5 adapters for 8 providers, and the OpenAI-chat adapter serves
OpenRouter, Ollama, HF, Gemini-compat, Azure and mantle with only base-URL/auth differences.

### 11.3 Fallback-chain pseudocode

```
chain = [
  (openrouter, "anthropic/claude-sonnet-5"),   # OpenRouter has its own provider fallback (ch. 8 §8.7)
  (openai,     "gpt-5.6-terra"),
  (ollama,     "qwen3.6:27b"),                 # local last resort: degraded quality, never down
]

function generate(request):
  for (provider, model) in chain:
    try:
      return provider.call(model, request, timeout=per_provider_timeout)
    except NonRetryable(e):          # 400 schema, 401/403 auth, content policy
      log(e); continue_or_raise      # config bug → raise; policy block → try next provider
    except Retryable(e):             # 429/5xx/529 after in-provider backoff (see §12)
      log(e); continue               # fail over
  raise AllProvidersExhausted
```

Notes grounded in the chapters: OpenRouter natively supports `models: [primary, fallback…]` arrays
and multi-provider routing, so one OpenRouter entry already is a fallback chain (ch. 8 §8.7);
prompt caches do not transfer across providers — a failover request pays full input price; strict
structured-output guarantees differ per provider (ch. 8 §8.9), so validate JSON after every hop
regardless of which provider answered.

---

## 12. Retry, timeout, and streaming patterns

### 12.1 What the providers actually signal (from chapters)

| Provider | Rate limit / overload signals | Retry guidance from chapter |
|---|---|---|
| OpenAI | 429 `rate_limit_exceeded` (retry) vs `insufficient_quota` (billing — **never retry**); 500/503; `Retry-After` + `x-ratelimit-*` headers | exponential backoff + jitter; SDK auto-retries 2× (ch. 3 §3.10) |
| Gemini | 429 `rate_limit_exceeded` (per-minute) vs `quota_exceeded` (daily — wait/upgrade); 500/503/504 | retry 429/408/5xx only, 1→2→4→8 s + jitter; Python SDK auto-retries 4× (ch. 4 §4.10) |
| Anthropic | 429 `rate_limit_error` (`retry-after` header); **529 `overloaded_error`** — also arrives as an SSE `error` event mid-stream | SDKs auto-retry 429/5xx/connection with 2× backoff (ch. 5 §5.10) |
| Bedrock | `ThrottlingException` (429), `ModelNotReadyException` (429 — model loading), `ServiceUnavailableException` (503), `ModelTimeoutException` (408) | boto3 `Config(retries={"max_attempts":10,"mode":"adaptive"}, read_timeout=3600)` (ch. 6 §6.10) |
| Azure | 429 = TPM/RPM **or** monthly usage tier **or** regional capacity; honor `Retry-After`; 400 `content_filter` is not transient | backoff + jitter; consider PTU/spillover (ch. 7 §7.10) |
| OpenRouter | 429 rate limit; **402 = credits exhausted (stop, don't retry)**; **503 = no provider matches your routing constraints (loosen constraints, don't blind-retry)**; 502 upstream down | its own multi-provider fallback absorbs most transient upstream failures first (ch. 8 §8.10) |
| Ollama | no 429 — requests **queue** locally; 500 = engine OOM/crash; conn-refused/cold-load latency | retries only help load contention; pre-warm with `keep_alive: -1`; allow long first-token timeouts (ch. 9 §9.10) |
| Hugging Face | 429 with `RateLimit`/`RateLimit-Policy` headers (5-min windows); 402 credits; 5xx provider-side | `provider="auto"` fails over across partners; `huggingface_hub` ≥1.2.0 auto-retries 429 (ch. 10 §10.10) |

Cross-provider rules that fall out of the table:
1. Retry **only** 408, 429 (when it means rate, not billing), 5xx, and Anthropic's 529.
2. Never retry 400/401/403, OpenAI `insufficient_quota`, OpenRouter 402, Azure `content_filter`.
3. Always honor `Retry-After`/`retry-after` when present (OpenAI, Anthropic, Azure document it).
4. Errors can arrive **inside an open stream** (Anthropic SSE `error` events, Azure
   `finish_reason:"content_filter"`, OpenRouter post-200 SSE errors) — a 200 status is not success.

### 12.2 Canonical retry-with-backoff

Python (stdlib only; wrap any provider call that raises an error carrying `status`,
optional `code`, and response `headers`):

```python
import random
import time

RETRYABLE_STATUS = {408, 429, 500, 502, 503, 504, 529}
NON_RETRYABLE_CODES = {"insufficient_quota", "quota_exceeded", "content_filter"}

def call_with_backoff(fn, max_attempts=5, base=1.0, cap=60.0):
    for attempt in range(max_attempts):
        try:
            return fn()
        except ProviderError as e:                      # your adapter's error type
            retryable = (e.status in RETRYABLE_STATUS
                         and e.code not in NON_RETRYABLE_CODES)
            if not retryable or attempt == max_attempts - 1:
                raise
            delay = min(cap, base * 2 ** attempt)
            ra = e.headers.get("retry-after")
            if ra is not None:
                delay = max(delay, float(ra))           # server knows best
            time.sleep(delay + random.uniform(0, delay))  # full jitter
```

JavaScript:

```js
const RETRYABLE = new Set([408, 429, 500, 502, 503, 504, 529]);
const NON_RETRYABLE_CODES = new Set(["insufficient_quota", "quota_exceeded", "content_filter"]);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function callWithBackoff(fn, { maxAttempts = 5, base = 1000, cap = 60000 } = {}) {
  for (let attempt = 0; ; attempt++) {
    try {
      return await fn();
    } catch (e) {
      const retryable = RETRYABLE.has(e.status) && !NON_RETRYABLE_CODES.has(e.code);
      if (!retryable || attempt >= maxAttempts - 1) throw e;
      let delay = Math.min(cap, base * 2 ** attempt);
      const ra = e.headers?.get?.("retry-after");
      if (ra) delay = Math.max(delay, Number(ra) * 1000);
      await sleep(delay + Math.random() * delay);
    }
  }
}
```

Prefer the official SDKs' built-in retries where you use them (OpenAI `max_retries`, Anthropic
SDK defaults, boto3 adaptive mode, `huggingface_hub` — all documented in the respective §N.10);
the code above is for raw-HTTP adapters and for the outer *cross-provider* failover layer, which
SDK retries do not cover.

**Timeouts** (chapter-grounded): set connect timeouts short (~10 s) and read timeouts long —
Bedrock's boto3 default of 60 s is too short for long generations (ch. 6 §6.10); Anthropic advises
streaming or Batch for turns over 10 minutes (ch. 5 §5.10); Ollama cold model loads can take tens
of seconds before the first token (ch. 9 §9.10). Streaming largely dissolves the read-timeout
problem: apply an idle (inter-chunk) timeout instead of a total one.

### 12.3 SSE consumption — the three main API shapes

**Shape A — OpenAI Chat Completions chunks** (used verbatim by OpenRouter, HF router, Ollama `/v1`,
Gemini compat, Azure, Bedrock mantle): `data:` lines of `chat.completion.chunk` JSON, terminated by
`data: [DONE]`. OpenRouter interleaves SSE **comment lines** (`: OPENROUTER PROCESSING`) that crash
naive `JSON.parse` loops — skip lines not starting with `data:` (ch. 8 §8.9).

```python
import httpx, json

with httpx.stream("POST", url, headers=headers, json={**body, "stream": True}) as r:
    for line in r.iter_lines():
        if not line.startswith("data: "):
            continue                       # skips comments/keep-alives
        payload = line[6:]
        if payload == "[DONE]":
            break
        chunk = json.loads(payload)
        delta = chunk["choices"][0]["delta"].get("content")
        if delta:
            print(delta, end="")
        # last chunk may carry usage (OpenRouter does; ch. 8 §8.9)
```

**Shape B — OpenAI Responses semantic events** (OpenAI direct, Azure v1, mantle Responses): typed
events, not bare deltas — filter on `response.output_text.delta`, finish on `response.completed`
(ch. 3 §3.9, ch. 7 §7.9):

```python
with client.responses.stream(model="gpt-5.6-terra", input="Count to 5.") as stream:
    for event in stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="")
```

**Shape C — Anthropic Messages events**: fixed grammar `message_start` → per block
(`content_block_start` → `content_block_delta`* → `content_block_stop`) → `message_delta`
(cumulative usage) → `message_stop`, with `ping` and possible `error` events interleaved
(`overloaded_error` can arrive mid-stream). Delta subtypes: `text_delta`, `input_json_delta`
(partial tool-input JSON), `thinking_delta`, `signature_delta` (ch. 5 §5.9):

```python
with client.messages.stream(model="claude-sonnet-5", max_tokens=512,
                            messages=[{"role": "user", "content": "Count to 5."}]) as stream:
    for text in stream.text_stream:
        print(text, end="")
    final = stream.get_final_message()     # usage lives here
```

Not SSE at all (do not pipe through an SSE parser): **Bedrock Converse** streams an AWS binary
event stream — iterate `converse_stream()["stream"]` for `contentBlockDelta`/`metadata` events
(ch. 6 §6.9); **Ollama native** `/api/chat` streams NDJSON, one JSON object per line, ending with a
`done: true` object carrying token counts (ch. 9 §9.9). **Gemini classic**
`:streamGenerateContent?alt=sse` is SSE with `candidates[].content` chunks; Interactions streaming
is documented but its event snippet was not captured in ch. 4 (§4.9) — verify before relying on
event names.

---

## 13. Tool use / function calling across providers

### 13.1 Schema-shape comparison

| Surface | Tool definition | Model's call appears as | You return the result as | Forcing a tool |
|---|---|---|---|---|
| OpenAI Responses (ch. 3 §3.9) | `{"type":"function","name","description","parameters":<JSON Schema>,"strict":true}` — **name at top level** | `output[]` item `type:"function_call"` with `call_id`, `name`, arguments | input item `{"type":"function_call_output","call_id","output"}` (+ `previous_response_id`) | `tool_choice` (per Responses reference); built-in tools (`web_search`, `mcp`, …) need no loop |
| OpenAI Chat Completions shape (as passed through by OpenRouter/HF/Ollama-compat; ch. 8 §8.9, ch. 10 §10.9) | `tools:[{"type":"function","function":{name,description,parameters}}]` | `finish_reason:"tool_calls"`, `message.tool_calls[]` | message with `role:"tool"`, `tool_call_id` | `tool_choice` (Ollama compat does **not** support it — ch. 9 §9.7) |
| Anthropic Messages (ch. 5 §5.9) | `{"name","description","input_schema":<JSON Schema>,"strict":true}` — note **`input_schema`**, no `type` wrapper | `stop_reason:"tool_use"` + content block `{"type":"tool_use","id","name","input"}` | user-turn block `{"type":"tool_result","tool_use_id","content"}` | `tool_choice: {"type":"auto"\|"any"\|"tool"\|"none"}`; parallel calls default |
| Gemini Interactions (ch. 4 §4.9) | `{"type":"function","name","description","parameters":<JSON Schema>}` in `tools[]` | function-call **step** in the `steps[]` history | send result back as next input (loop per docs) | `generation_config.tool_choice: auto\|any\|none\|validated`; **Gemini 3 stateless mode must round-trip thought signatures** or you get `missing_thought_signature` |
| Bedrock Converse (ch. 6 §6.9) | `toolConfig.tools[].toolSpec: {name, inputSchema: {"json": <JSON Schema>}}` | `stopReason:"tool_use"` + content block `{"toolUse":{toolUseId,name,input}}` | user message block `{"toolResult":{toolUseId, content:[{"json":…}]}}` | `toolChoice` (also the standard structured-output workaround: one required tool) |

Same JSON Schema everywhere; what moves is (a) the wrapper key (`parameters` vs `input_schema` vs
`inputSchema.json`), (b) where the call shows up (typed output item vs stop-reason + content block
vs step history), and (c) the result-return convention. Strictness guarantees also differ:
Anthropic strict tools are grammar-backed with documented limits (≤20 strict tools, no
`minLength`/`maximum`, ch. 5 §5.9); OpenRouter warns exact compliance "is not guaranteed on every
endpoint" (ch. 8 §8.9); on Bedrock, structured output is a per-model-card flag (ch. 6 §6.9).

### 13.2 One worked example, ported across three providers

Task: `get_weather(city) -> {"temp_c": …}`, two-step loop.

**OpenAI Responses:**

```python
from openai import OpenAI
client = OpenAI()

tools = [{"type": "function", "name": "get_weather",
          "description": "Get current weather for a city",
          "parameters": {"type": "object",
                         "properties": {"city": {"type": "string"}},
                         "required": ["city"], "additionalProperties": False},
          "strict": True}]

r1 = client.responses.create(model="gpt-5.6-terra", input="Weather in Oslo?", tools=tools)
call = next(i for i in r1.output if i.type == "function_call")
r2 = client.responses.create(
    model="gpt-5.6-terra", previous_response_id=r1.id, tools=tools,
    input=[{"type": "function_call_output", "call_id": call.call_id,
            "output": '{"temp_c": 14}'}])
print(r2.output_text)
```

**Anthropic Messages:**

```python
import anthropic
client = anthropic.Anthropic()

tools = [{"name": "get_weather",
          "description": "Get current weather for a city",
          "strict": True,
          "input_schema": {"type": "object",
                           "properties": {"city": {"type": "string"}},
                           "required": ["city"], "additionalProperties": False}}]

msgs = [{"role": "user", "content": "Weather in Oslo?"}]
m1 = client.messages.create(model="claude-sonnet-5", max_tokens=512,
                            tools=tools, messages=msgs)
tu = next(b for b in m1.content if b.type == "tool_use")
msgs += [{"role": "assistant", "content": m1.content},
         {"role": "user", "content": [{"type": "tool_result",
                                       "tool_use_id": tu.id,
                                       "content": '{"temp_c": 14}'}]}]
m2 = client.messages.create(model="claude-sonnet-5", max_tokens=512,
                            tools=tools, messages=msgs)
print(m2.content[-1].text)
```

**Bedrock Converse (same Claude model, AWS schema):**

```python
import boto3
client = boto3.client("bedrock-runtime", region_name="us-east-1")

tool_cfg = {"tools": [{"toolSpec": {
    "name": "get_weather",
    "description": "Get current weather for a city",
    "inputSchema": {"json": {"type": "object",
                             "properties": {"city": {"type": "string"}},
                             "required": ["city"]}}}}]}

msgs = [{"role": "user", "content": [{"text": "Weather in Oslo?"}]}]
r1 = client.converse(modelId="global.anthropic.claude-sonnet-5",
                     messages=msgs, toolConfig=tool_cfg)
tu = next(b["toolUse"] for b in r1["output"]["message"]["content"] if "toolUse" in b)
msgs += [r1["output"]["message"],
         {"role": "user", "content": [{"toolResult": {
             "toolUseId": tu["toolUseId"], "content": [{"json": {"temp_c": 14}}]}}]}]
r2 = client.converse(modelId="global.anthropic.claude-sonnet-5",
                     messages=msgs, toolConfig=tool_cfg)
print(r2["output"]["message"]["content"][0]["text"])
```

The loop skeleton is identical (define → detect call → execute → append result → re-call); a
portable agent core only needs the three translation functions visible above. Tool-definition
token overhead is real and provider-specific (e.g. Anthropic documents 286–588 system-prompt
tokens per model/choice mode — ch. 5 §5.3); prune unused tools.

---

## 14. RAG pipeline blueprint

```
docs ──chunk──▶ embed (pluggable) ──▶ store (numpy / vector DB) ──▶ retrieve top-k
                                                                        │
query ──embed(query-mode)──────────────────────────────────────────────┘
                                                                        ▼
                                                grounded prompt ──▶ generator (any §11 provider)
```

### 14.1 Embeddings choice (from the chapters)

| Embedder | Where | Dims / input limit | Cost | Notes |
|---|---|---|---|---|
| `text-embedding-3-large` / `-small` | OpenAI, Azure | 3072 / 1536 native; `dimensions` param (Matryoshka-style); 8,192-token input | $0.13 / $0.02 per 1M in (OpenAI list) | shortened-large beats full ada-002; Batch API −50% (ch. 3 §3.2, §3.13; ch. 7 §7.4) |
| `gemini-embedding-2` (preview-ID discrepancy noted) / `gemini-embedding-001` | Gemini API | 128–3072 flexible (MRL); 8,192 / 2,048-token input | 2: [UNVERIFIED]; 001: $0.15 (2025 blog, may be stale) | embedding-2 is multimodal (text/image/video/audio/PDF); task steering: `task_type` on 001, inline `task:` prefixes on 2 (ch. 4 §4.4, §4.13) |
| Cohere `embed-v4` / `amazon.titan-embed-text-v2:0` | Bedrock | Embed v4 multimodal, 256–1536d Matryoshka; Titan v2 256/512/1024d, 8K in | Embed v4 [UNVERIFIED]; Titan $0.02 per 1M | Titan v2 is the Knowledge Bases default (ch. 6 §6.2, §6.13); Cohere embed-v4 also on Azure (ch. 7 §7.4) |
| Voyage AI (`voyage-4-*`) | third party | up to 32K-token inputs, 256–2048d | see Voyage | Anthropic ships **no embedder** and recommends Voyage (ch. 5 §5.4) |
| `Qwen3-Embedding-0.6B/4B/8B`, `embeddinggemma-300m`, `BAAI/bge-m3`, `gte-multilingual-base` | local via **Ollama `/api/embed`** or **HF TEI** | bge-m3: 8,192 in, dense+sparse; MRL truncation on Qwen3/EmbeddingGemma | hardware only | current local picks per ch. 9 §9.4 and ch. 10 §10.13; serve with TEI for production batching/rerankers |

Rules that hold across chapters: (a) index and query with the **same model and dimension** —
vectors are not portable between embedders (explicitly noted for the OpenRouter hybrid pattern,
ch. 8 §8.13); (b) use asymmetric task steering where offered (Gemini task types, Qwen3
instruction-awareness); (c) Matryoshka truncation (768–1024d) is the documented cost dial on
OpenAI/Gemini/Cohere/Qwen — it shrinks vector-store cost with little recall loss.

### 14.2 Chunking guidance (generic engineering knowledge, not chapter-specific)

- Start with ~500–1,500 tokens per chunk, 10–20% overlap; align boundaries to structure
  (headings/paragraphs/functions) rather than fixed bytes.
- Keep chunks well under the embedder's input limit — silent truncation is a real failure mode
  (Ollama defaults `truncate: true`; set `truncate: false` to fail loudly — ch. 9 §9.13).
- Store the source text and metadata (doc id, position) beside each vector; retrieval quality
  problems are debugged by reading what was actually indexed.
- Managed alternatives exist at every hosted provider if you'd rather not own this: OpenAI
  `file_search` (vector stores; ZDR-ineligible — ch. 3 §3.13), Gemini file search / URL context
  (ch. 4 §4.13), Anthropic Files API + citations (ch. 5 §5.13), Bedrock Knowledge Bases with
  managed chunking modes (ch. 6 §6.13), Azure AI Search / On Your Data (ch. 7 §7.13).

### 14.3 Minimal end-to-end example with a pluggable embedder

```python
"""Minimal RAG: numpy store, pluggable embedder, any §11 chat adapter as generator."""
from typing import Protocol
import numpy as np

class Embedder(Protocol):
    def embed(self, texts: list[str]) -> np.ndarray: ...   # (n, d), L2-normalized

class OpenAIEmbedder:
    def __init__(self, model="text-embedding-3-small", dimensions=512):
        from openai import OpenAI
        self.client, self.model, self.dim = OpenAI(), model, dimensions
    def embed(self, texts):
        r = self.client.embeddings.create(model=self.model, input=texts,
                                          dimensions=self.dim)
        v = np.array([d.embedding for d in r.data])
        return v / np.linalg.norm(v, axis=1, keepdims=True)

class OllamaEmbedder:
    def __init__(self, model="qwen3-embedding:0.6b"):
        import ollama
        self.ollama, self.model = ollama, model
    def embed(self, texts):
        r = self.ollama.embed(model=self.model, input=texts)
        v = np.array(r.embeddings)
        return v / np.linalg.norm(v, axis=1, keepdims=True)

def chunk(text: str, size=1000, overlap=150) -> list[str]:
    return [text[i:i + size] for i in range(0, max(len(text) - overlap, 1), size - overlap)]

class Index:
    def __init__(self, embedder: Embedder):
        self.embedder, self.chunks, self.vecs = embedder, [], None
    def add(self, docs: list[str]):
        self.chunks = [c for d in docs for c in chunk(d)]
        self.vecs = self.embedder.embed(self.chunks)
    def search(self, query: str, k=5) -> list[str]:
        q = self.embedder.embed([query])[0]
        scores = self.vecs @ q                       # cosine (all normalized)
        return [self.chunks[i] for i in np.argsort(-scores)[:k]]

def answer(index: Index, chat_fn, question: str) -> str:
    ctx = "\n---\n".join(index.search(question))
    return chat_fn(system="Answer ONLY from the provided context. Say 'not found' otherwise.",
                   user=f"Context:\n{ctx}\n\nQuestion: {question}")
```

### 14.4 When you do / don't need a vector DB (honest note)

Brute-force numpy over normalized vectors is exact, dependency-free, and fast enough for
surprisingly large corpora — a matrix–vector product over hundreds of thousands of 512-d float32
vectors is milliseconds on a laptop (generic knowledge). Reach for a vector DB only when you need:
persistent multi-process access, incremental updates with deletes, metadata filtering at scale,
approximate search over many millions of vectors, or a managed service boundary. Two
chapter-documented alternatives also displace the DB entirely at small scale: (a) long context +
prompt caching — 1M-token windows with ~0.1× cached-input pricing make "stuff the corpus in the
prompt, cache the prefix" viable for mid-size corpora (ch. 4 §4.13, ch. 5 §5.13); (b) provider-
managed retrieval (§14.2 list) where its data-retention terms are acceptable (note OpenAI vector
stores are ZDR-ineligible — ch. 3 §3.16).

---

## 15. Agent patterns and MCP

### 15.1 What each provider officially ships (chapter-verified)

| Provider | Official agent offering | MCP status |
|---|---|---|
| OpenAI | **Agents SDK** (Python `openai-agents`, TS) — handoffs, guardrails, sessions, tracing; hosted tools (web search, computer use, shell, apply_patch); ChatKit UI (ch. 3 §3.14) | first-class: remote MCP servers as Responses/Agents-SDK tools |
| Anthropic | **Claude Agent SDK** (Py/TS; Claude Code loop as a library — subagents, hooks, sessions, skills); **Managed Agents** (hosted, $0.08/session-hr); server tools incl. computer use, `tool_search` (ch. 5 §5.14) | **originated MCP** (spec rev 2026-07-28); Messages-API MCP connector (remote HTTP, tools-only, beta header); Agent SDK supports full MCP incl. stdio |
| Gemini | **Interactions API** is itself agent-oriented (server-side state, step history, multi-tool); managed agent models (`deep-research-*`, `antigravity-preview`); computer-use model; `-customtools` variant (ch. 4 §4.14) | not documented on pages fetched for ch. 4 — [UNVERIFIED]; OpenAI-compat endpoint lets OpenAI-ecosystem agent frameworks target Gemini |
| Bedrock | **AgentCore** (GA 2025-10): Runtime (8-h serverless sessions), **Gateway (turns APIs/Lambda into MCP tools)**, Memory, Identity, Browser, Code Interpreter, OTel observability; classic Bedrock Agents de-emphasized; Strands Agents OSS (ch. 6 §6.14) | first-class protocol in Gateway and Runtime |
| Azure | **Foundry Agent Service** (GA; ex "Azure AI Agent Service") — prompt agents + hosted agents (your framework in managed containers), per-agent Entra identity, tracing/evals, M365 distribution (ch. 7 §7.14) | MCP servers as tools (managed "Toolbox", OAuth/Entra auth); **A2A protocol in preview** |
| OpenRouter | no agent runtime; uniform OpenAI tool loop + fallback arrays + `reasoning_effort` normalization work with any framework (ch. 8 §8.14) | `@openrouter/mcp` package converts MCP servers' tools for use through the API |
| Ollama | CLI agent mode (v0.32.0+); tool-calling API as the primitive; drop-in OpenAI/Anthropic-compat backend for agent frameworks (ch. 9 §9.14) | consumed by client frameworks, not by Ollama itself; no first-party MCP server documented |
| Hugging Face | **smolagents** (minimal code-executing agents); tiny-agents MCP-client loop [MEDIUM per ch. 10] (ch. 10 §10.14) | official **HF MCP Server** (`huggingface.co/mcp`): hub search, Spaces tools, Providers access |

### 15.2 MCP as the cross-provider tool protocol

MCP (Anthropic-originated, open spec at modelcontextprotocol.io, current revision 2026-07-28 per
ch. 5 §5.14) is the one tool-integration format that appears on **both sides of every major stack
surveyed**: consumable by OpenAI Responses/Agents SDK, Anthropic Messages/Agent SDK, Azure Agent
Service; producible by Bedrock AgentCore Gateway and the HF MCP Server; bridgeable into plain
OpenAI-format tools for OpenRouter/Ollama. Practical consequence: **write each tool once as an MCP
server**, and you get portability across providers that native `tools[]` arrays cannot give you —
the per-provider difference collapses to "how do I attach this server" (a config block) instead of
"how do I re-encode this schema".

Caveats from the chapters: the Anthropic Messages MCP connector is remote-HTTP + tools-only (no
resources/prompts, no stdio) — full MCP requires the Agent SDK/Claude Code side (ch. 5 §5.14);
Gemini's MCP position was unverified at access date (ch. 4 §4.14); MCP servers are third-party
code with tool-description injection risk — apply the same trust review as any dependency (generic
security guidance).

### 15.3 Keep-it-simple guidance

- **A loop with tools is usually enough.** Every provider's agent story reduces to §13's
  define→call→execute→append→re-call loop plus persistence. Adopt an agent framework when you
  need its specific machinery (handoffs, tracing, managed sandboxes), not by default.
- Prefer **workflow-shaped code** (fixed sequence of model calls with checked outputs) over
  open-ended autonomous loops for anything with correctness requirements; cap iterations and
  spend per task (generic guidance; token/session meters in §19).
- Managed runtimes (AgentCore Runtime, Foundry hosted agents, Anthropic Managed Agents) buy you
  sandboxing, identity and observability at the price of platform lock-in and per-session cost
  (e.g. $0.08/session-hour on Anthropic — ch. 5 §5.5). Self-host the loop first; graduate when
  isolation or scale demands it.
- Long-running agents amplify every cost lever in §19 — prompt caching and small-model routing for
  subagent tasks (explicitly what Gemini positions Flash-Lite for — ch. 4 §4.3) matter more here
  than anywhere else.

---

## 16. Vision & audio pipelines

### 16.1 Capability matrix (from chapters/sidecars, 2026-08-14)

| Provider | Image in | Image out | Audio in | Audio out (TTS/speech) | Video | PDF/file input |
|---|---|---|---|---|---|---|
| OpenAI | yes (GPT-5.6 trio, codex) | `gpt-image-2` | STT models (`gpt-transcribe`, realtime line) | `gpt-realtime-2.1`, `gpt-4o-mini-tts`, `gpt-audio-1.5` | Sora **shutting down 2026-09-24** | files via Files/file_search; flagship text models: no audio I/O (ch. 3 §3.2–3.4) |
| Gemini | yes (all reasoning models) | Nano Banana line (`gemini-3.1-flash-image`, `3-pro-image`) | yes (native input) | TTS models + Live API (WSS realtime) | in: yes; out: Veo 3.1, omni-flash | **native PDF input** on reasoning models (ch. 4 §4.2–4.4) |
| Anthropic | yes (input only) | **no** | **no** | **no** | **no** | `document` blocks (PDF/text, base64/URL/`file_id`) + citations (ch. 5 §5.4, §5.7) |
| Bedrock | per model (Claude, Nova, Llama 4, Pixtral) | Stability, Titan Image v2 | Voxtral, Nova 2 Sonic | Nova 2 Sonic (speech↔speech) | in: Nova, TwelveLabs; out: Luma Ray v2 | per model card — always check (ch. 6 §6.4) |
| Azure | yes (GPT lines, Phi-4-multimodal) | `gpt-image-2/-1.5`, FLUX.2, MAI-Image | whisper/gpt-transcribe/realtime; 25 MB file cap for file STT | `tts(-hd)`, `gpt-4o-mini-tts`, MAI-Voice | Sora-2 (preview lineage) | On Your Data / file search (ch. 7 §7.4) |
| OpenRouter | broad (per-model `input_modalities`) | catalog image models | some models list `audio` in | partner TTS (MiniMax, per-character pricing) | partner video models (per-second) | `file` modality on some models; workflows [UNVERIFIED] (ch. 8 §8.4) |
| Ollama | yes (qwen3.5/3.6, gemma4, qwen3-vl, …) — **base64 only, no remote URL fetch** | removed in v0.32.6 | gemma4 E2B/E4B audio-in only | **no** | no | no (feed extracted text) (ch. 9 §9.4) |
| Hugging Face | open VLMs (Qwen3-VL, Gemma 4, Muse Glimmer) | FLUX.2, LTX video via Providers | Whisper large-v3(-turbo) | open TTS models exist; not chapter-cataloged | LTX-2.5 etc. via Providers | n/a (self-managed) (ch. 10 §10.4) |

Structural takeaway: Anthropic is text+image-in/text-out only (pair with other providers for
media); Gemini is the widest single-key multimodal surface; on Bedrock and OpenRouter modality is
a **per-model** property you must check, not a platform property.

### 16.2 One vision example (portable OpenAI-chat shape)

The Chat Completions image form works across OpenAI-compat surfaces (OpenRouter, Ollama `/v1`,
Gemini compat, Azure, HF router) — base64 data URLs are the lowest common denominator, since
Ollama does not fetch remote URLs (ch. 9 §9.4):

```python
import base64
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")  # or any §11 base_url
b64 = base64.b64encode(open("chart.png", "rb").read()).decode()

r = client.chat.completions.create(
    model="qwen3-vl:8b",   # swap model per provider
    messages=[{"role": "user", "content": [
        {"type": "text", "text": "Summarize this chart in two sentences."},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
    ]}])
print(r.choices[0].message.content)
```

Anthropic-native equivalent uses an `image` content block (`{"type":"image","source":{"type":
"base64","media_type":"image/png","data":…}}`) inside the same user turn (ch. 5 §5.7).

### 16.3 One STT + TTS example (OpenAI audio endpoints; Azure exposes the same routes — ch. 7 §7.7)

```python
from openai import OpenAI
client = OpenAI()

# Speech-to-text (batch file STT)
with open("meeting.mp3", "rb") as f:
    text = client.audio.transcriptions.create(model="gpt-transcribe", file=f).text

# Text-to-speech
speech = client.audio.speech.create(model="gpt-4o-mini-tts", voice="alloy",
                                    input=text[:500])
open("summary.mp3", "wb").write(speech.read())
```

Alternatives per chapters: Gemini TTS returns base64 PCM 24 kHz/16-bit mono with 30 named voices
and up to 2 speakers (ch. 4 §4.4); realtime/conversational audio needs socket transports, not
HTTP — OpenAI Realtime (WebRTC/WS/SIP, ephemeral client secrets), Gemini Live (WSS, 16 kHz PCM in
/ 24 kHz out), Bedrock Nova 2 Sonic (ch. 3 §3.15, ch. 4 §4.4, ch. 6 §6.4). Open/self-hosted STT:
Whisper large-v3(-turbo) via HF Providers or Endpoints (ch. 10 §10.4).

### 16.4 File/PDF handling differences (recurring integration trap)

- **Gemini**: PDFs are a first-class input modality on reasoning models; File API for large
  uploads (ch. 4 §4.2, §4.7).
- **Anthropic**: PDFs go in `document` blocks (base64/URL/`file_id` via the beta Files API) and
  can drive citations; request-size cap 32 MB, files up to 500 MB (ch. 5 §5.7, §5.13).
- **OpenAI**: no PDF modality on the model itself — route documents through `file_search`
  vector stores or pre-extract text/images (ch. 3 §3.13).
- **Ollama / local**: no document type; extract text (or rasterize pages to images for a VLM)
  before the prompt (ch. 9 §9.4).
- **Azure/Bedrock**: per-model; Bedrock model cards and Azure model pages are the truth source
  (ch. 6 §6.3 "read the model card", ch. 7 §7.2).

---

## 17. Local inference setup (Ollama, HF stack) incl. Docker

### 17.1 Ollama recipes

Bare metal (ch. 9 §9.8, §9.15): `curl -fsSL https://ollama.com/install.sh | sh` (Linux/systemd),
desktop apps for macOS/Windows; configure via `systemctl edit ollama` environment overrides.

Docker Compose (GPU, from the chapter's docker/env documentation — ch. 9 §9.6, §9.15):

```yaml
services:
  ollama:
    image: ollama/ollama            # ollama/ollama:rocm for AMD
    ports:
      - "127.0.0.1:11434:11434"     # bind to localhost — the API has NO auth (ch. 9 §9.17)
    volumes:
      - ollama:/root/.ollama
    environment:
      OLLAMA_CONTEXT_LENGTH: "32768"   # default is 4096 regardless of model! (ch. 9 §9.3)
      OLLAMA_KEEP_ALIVE: "30m"
      OLLAMA_NUM_PARALLEL: "2"         # each slot reserves its own KV cache
      OLLAMA_KV_CACHE_TYPE: "q8_0"     # halves KV memory
    deploy:
      resources:
        reservations:
          devices: [{driver: nvidia, count: all, capabilities: [gpu]}]
volumes:
  ollama:
```

Then `docker exec -it <ctr> ollama pull qwen3.6:27b`. The two classic mistakes, both
chapter-documented: publishing 11434 on 0.0.0.0 without a fronting authenticated proxy (ch. 9
§9.17), and forgetting that the **default context is 4,096 tokens** with silent prompt truncation
(ch. 9 §9.3, §9.7).

### 17.2 HF stack: vLLM/SGLang for generation, TEI for embeddings (TGI is EOL)

**TGI was archived 2026-03-21**; HF's stated direction is vLLM/SGLang (+ llama.cpp/MLX locally)
(ch. 10 §10.1). Both expose OpenAI-compatible servers, so §11's thin adapter applies unchanged.

```yaml
services:
  vllm:                              # generation
    image: vllm/vllm-openai:latest   # pin a version in production
    command: ["--model", "meta-models/Muse-Glimmer-30B", "--max-model-len", "32768"]
    ports: ["127.0.0.1:8000:8000"]
    environment: {HF_TOKEN: "${HF_TOKEN}"}          # for gated repos (ch. 10 §10.6)
    volumes: ["hf-cache:/root/.cache/huggingface"]
    deploy:
      resources:
        reservations:
          devices: [{driver: nvidia, count: all, capabilities: [gpu]}]

  tei:                               # embeddings + rerankers (ch. 10 §10.13)
    image: ghcr.io/huggingface/text-embeddings-inference:1.9
    command: ["--model-id", "Qwen/Qwen3-Embedding-0.6B"]
    ports: ["127.0.0.1:8080:80"]
    volumes: ["tei-data:/data"]
volumes: {hf-cache: {}, tei-data: {}}
```

Clients: `base_url="http://localhost:8000/v1"` for vLLM chat; TEI serves `POST /embed` and
`POST /rerank` (ch. 10 §10.13). vLLM flags above are illustrative — the exact serving flags for
big MoE models come from each model card (DeepSeek/GLM cards document vLLM-first deployment,
ch. 10 §10.3). Managed middle ground: HF Inference Endpoints run vLLM/SGLang/TEI as managed
engines per instance-hour (ch. 10 §10.5).

### 17.3 Hardware sizing (consolidated from ch. 9 §9.5/§9.15 and ch. 10 §10.15 — **estimates**)

| Class (default ~4-bit quant unless noted) | Examples | Memory needed | Typical speed (community estimates, unverified) |
|---|---|---|---|
| Tiny (≤4B) | llama3.2 1B/3B, phi4-mini, gemma4 E-series | 2–6 GB | fast even on CPU |
| Small (7–9B) | qwen3.5:9b, gpt-oss-ish distills | ~8 GB VRAM | ~80–140 tok/s on RTX-4090-class; ~30–60 on M-series; 5–12 CPU-only |
| Mid (24–35B) | qwen3.6:27b (17 GB disk), qwen3-coder:30b (19 GB), muse-glimmer (18 GB), gemma4:31b (20 GB) | 24–32 GB VRAM or Apple unified memory | ~25–50 tok/s fully offloaded; "falls off a cliff" if layers spill to RAM |
| MoE low-active | gemma4:26b-a4b (3.8B act), nemotron-3.5-lightning (3B act) | total-param memory, **near-small-model speed** | MoE VRAM is set by total params, not active (ch. 10 §10.3) |
| Large (100–130B) | gpt-oss:120b (65 GB, MXFP4), qwen3.5:122b (81 GB) | one 80 GB GPU or ≥96 GB unified-memory Mac | ~30–50 tok/s (gpt-oss:120b/80 GB — estimate) |
| Frontier MoE (≥300B) | DeepSeek V4, GLM-5.2, Kimi K3 | multi-node H200-class clusters | not practical locally — use Providers/cloud tags (ch. 9 §9.2, ch. 10 §10.3) |

Add to weights: KV cache (linear in context length; halve/quarter with `q8_0`/`q4_0` KV) plus
~1–2 GB overhead; BF16 self-hosting needs ≈2 bytes/param + KV (ch. 10 §10.15). Official anchors
(the only non-estimates): gpt-oss:20b "runs on 16 GB RAM"; gpt-oss:120b "fits a single 80 GB GPU"
(ch. 9 §9.5).

### 17.4 When local wins (and when it doesn't)

**Wins:** privacy/residency — data never leaves the machine, fully offline after model download
(ch. 9 §9.16); zero marginal cost — sustained high-utilization workloads amortize hardware vs
per-token billing (break-even math is deployment-specific — generic guidance); latency — no
network hop and no rate-limit queueing for single-tenant loads; egress control is trivially
auditable (§20.3). **Loses:** frontier quality — "even the best ~35B local models trail current
hosted frontier models" (ch. 9 §9.19); high-QPS multi-user serving on Ollama (use vLLM/SGLang —
ch. 9 §9.15); compliance certifications (none published for the OSS runtime — ch. 9 §9.17);
anything needing >80 GB-class models without cluster hardware.

---

## 18. Deployment: containers, serverless, managed endpoints

### 18.1 Container pattern — proxy with key isolation

Never ship provider keys to browsers/mobile — the server-side-proxy pattern is the documented
baseline at every hosted provider (ch. 3 §3.15, ch. 4 §4.15, ch. 8 §8.15). Minimal FastAPI proxy
that injects the key, pins the model allowlist, and passes SSE through:

```python
# app.py — container-deployable proxy; the ONLY place the provider key exists
import os
import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse

UPSTREAM = "https://api.openai.com/v1/chat/completions"   # or any §11 base URL
ALLOWED_MODELS = {"gpt-5.6-terra", "gpt-5.6-luna"}
app = FastAPI()

@app.post("/v1/chat")
async def chat(req: Request):
    body = await req.json()
    if body.get("model") not in ALLOWED_MODELS:
        raise HTTPException(400, "model not allowed")
    headers = {"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"}
    client = httpx.AsyncClient(timeout=httpx.Timeout(10, read=600))

    async def relay():
        async with client.stream("POST", UPSTREAM, json=body, headers=headers) as r:
            async for chunk in r.aiter_bytes():
                yield chunk
        await client.aclose()

    return StreamingResponse(relay(), media_type="text/event-stream")
```

Express equivalent (sketch): read body → validate model → `fetch(UPSTREAM, {headers: {Authorization:
`Bearer ${process.env.OPENAI_API_KEY}`}, body})` → pipe `res.body` to the client with
`Content-Type: text/event-stream`. Add per-user authn, rate limiting and the §19 usage logging at
this choke point — it is the natural place for all three. For browser realtime audio specifically,
OpenAI's ephemeral client secrets (`POST /v1/realtime/client_secrets`) replace the proxy so
clients connect via WebRTC without the master key (ch. 3 §3.15).

### 18.2 Serverless notes — AWS Lambda and Cloud Run

Chapter-grounded: the Gemini chapter states SSE streaming pass-through works on both Cloud Run and
Lambda functions (ch. 4 §4.15); Bedrock from Lambda should use the **execution role** (no stored
secrets — ch. 6 §6.6). The rest is generic platform knowledge — kept qualitative, verify current
limits before contracting:

- **Cold start**: keep dependencies thin (raw `httpx`/`fetch` beats heavyweight SDK trees);
  provisioned concurrency (Lambda) / min-instances (Cloud Run) for latency-sensitive paths.
- **Streaming**: Lambda requires response streaming mode (Function URLs); classic
  API-Gateway-buffered Lambda breaks SSE. Cloud Run supports HTTP streaming natively. If you cannot
  stream, fall back to polling a job store.
- **Timeouts**: both platforms cap request duration well below the longest model generations
  (Lambda's ceiling is minutes, not hours). Long jobs belong in Batch APIs (50% cheaper anyway —
  §19.3) or async workers, with the function returning a job id.
- **Concurrency vs rate limits**: serverless scale-out can stampede a per-minute token quota;
  put a shared limiter (queue/semaphore) between wide fan-out and the provider.

### 18.3 Managed / reserved-capacity endpoints compared

| Offering | Unit | SLA / guarantee (as documented) | Chapter |
|---|---|---|---|
| OpenAI Scale Tier | reserved TPM units, 30-day min | 99.9% uptime + latency commitments (page listed pre-5.6 models at access) | ch. 3 §3.15, §3.17 |
| Azure Provisioned (PTU) | PTU-hour, monthly/annual reservations; spillover to Standard | 99.9% availability + per-model latency SLA on Provisioned | ch. 7 §7.15, §7.17 |
| Bedrock Provisioned Throughput | model units, 1-/6-month commitments (not combinable with inference profiles) | Bedrock SLA 99.9% [commitment tier partially verified] | ch. 6 §6.5, §6.17 |
| Gemini Priority tier | per-request `serviceTier`, ~1.8× standard | guaranteed capacity; no published SLA on this API path | ch. 4 §4.5, §4.17 |
| Anthropic | `service_tier` auto/standard_only; Fast Mode (Opus) | no published SLA verified in ch. 5 | ch. 5 §5.15, §5.17 |
| HF Inference Endpoints | instance-hour (L4 $0.80/h … H100 $10/h), autoscale 0..N | no published uptime SLA on accessed pages | ch. 10 §10.5, §10.17 |
| Ollama Cloud | subscription ($20/$100 per month) + weighted token metering | no published SLA/certs | ch. 9 §9.5, §9.17 |

Rule of thumb: pay-as-you-go until 429s or latency SLOs force the issue; then Priority-style
per-request tiers; reserved capacity (PTU/Scale Tier/Provisioned) only for sustained, predictable
load — every chapter's reserved option carries commitments measured in months.

---

## 19. Monitoring, logging, cost optimization

### 19.1 Token accounting — usage field names per provider

| Surface | Where | Input / output fields | Cache & extras |
|---|---|---|---|
| OpenAI-chat shape (OpenAI, OpenRouter, HF, Ollama `/v1`, Azure, Gemini-compat) | `usage` | `prompt_tokens` / `completion_tokens` | OpenRouter: `prompt_tokens_details.cached_tokens`, `cache_write_tokens`; exact billed cost via `GET /api/v1/generation?id=` (ch. 8 §8.5) |
| Anthropic Messages | `usage` | `input_tokens` / `output_tokens` | `cache_creation_input_tokens`, `cache_read_input_tokens`, `cache_creation.ephemeral_{5m,1h}_input_tokens`, `output_tokens_details.thinking_tokens`, `server_tool_use.*` (ch. 5 §5.7) |
| Gemini generateContent | `usageMetadata` | prompt/candidates token counts | Interactions responses carry `usage` incl. `total_cached_tokens` (ch. 4 §4.7) |
| Bedrock Converse | `usage` (in `metadata` event when streaming) | `inputTokens` / `outputTokens` / `totalTokens` | (ch. 6 §6.8–6.9) |
| Ollama native | final `done:true` object | `prompt_eval_count` / `eval_count` | durations in **nanoseconds** (`total_duration`, `load_duration`) (ch. 9 §9.7) |

Streaming caveat: usage arrives at the **end** (final chunk / `message_delta` / `metadata` event) —
a client that abandons a stream early may never see it; log at the proxy. Also note mid-stream
cancellation does not stop billing on all OpenRouter upstreams (Bedrock, Google, Groq, Mistral
complete and charge in full — ch. 8 §8.9).

### 19.2 Structured logging pattern (one JSON line per model call, at the §18 proxy)

```python
import json, time, uuid

def log_call(provider, model, usage, t0, status, request_id=None, cached_in=0):
    print(json.dumps({
        "evt": "llm_call", "id": str(uuid.uuid4()), "ts": time.time(),
        "provider": provider, "model": model, "status": status,
        "latency_ms": round((time.time() - t0) * 1000),
        "in_tokens": usage.get("in", 0), "out_tokens": usage.get("out", 0),
        "cached_in_tokens": cached_in,
        "provider_request_id": request_id,      # e.g. Anthropic request-id header (ch. 5 §5.10)
        "est_cost_usd": estimate_cost(provider, model, usage, cached_in),
    }))
```

Log prompts/completions separately (if at all) with retention and access controls matched to §20's
data policies; keep the metrics line free of content so it can flow to any log pipeline. Capture
the provider's request id — every chapter's support path starts from it. Platform-native options:
Bedrock model-invocation logging + CloudWatch/CloudTrail (ch. 6 §6.15), Azure Monitor + Agent
Service tracing (ch. 7 §7.14), AgentCore/TEI expose OTel (ch. 6 §6.14, ch. 10 §10.13).

### 19.3 Cost levers, ranked by typical impact (all multipliers chapter-verified)

1. **Prompt caching — up to ~90% off repeated input.** Cache reads ≈0.1× input across OpenAI,
   Anthropic, Gemini (0.25× on some via OpenRouter); writes cost extra on some (OpenAI 5.6 1.25×,
   Anthropic 1.25×/2× by TTL; Azure cache-write billing starts ~2026-08-21) (ch. 3 §3.5, ch. 5
   §5.5, ch. 4 §4.5, ch. 7 §7.5). Structure prompts as [stable prefix | variable tail]; hold
   breakpoints stable; on Anthropic, cache-aware rate limits also multiply effective throughput
   (ch. 5 §5.11). On OpenRouter, sticky `session_id` routing preserves hits (ch. 8 §8.5).
2. **Batching — flat 50% wherever offered.** OpenAI, Anthropic, Gemini, Bedrock, Azure Batch and
   OpenRouter `:batch` variants all document −50% for 24-h-window async work (ch. 3 §3.5, ch. 5
   §5.5, ch. 4 §4.5, ch. 6 §6.5, ch. 7 §7.5, ch. 8 §8.5). Anything not interactive belongs here.
3. **Tier routing — order-of-magnitude spread.** Route easy traffic to the small tier
   (Luna $0.10/$0.60 vs Sol $2.50/$15; Haiku $1/$5 vs Fable $10/$50; flash-lite $0.10/$0.40 —
   ch. 3/5/4 §N.2) with a cheap classifier or escalate-on-failure. Managed routers exist: Azure
   `model-router` (billed at routed model's rate — ch. 7 §7.3), `openrouter/auto` +
   `sort:"price"`/`:floor` (ch. 8 §8.7), Flex/Priority service tiers (Gemini, Bedrock).
4. **Context discipline.** Long context is where budgets die: OpenAI 5.6 bills 2×/1.5× above 272K
   input; Gemini Pro steps up above 200K; thinking tokens bill as output (Anthropic tracks them in
   `thinking_tokens`; effort knobs — `reasoning.effort`, `thinking_level`, `output_config.effort`
   — directly cut them); Anthropic's 4.7+ tokenizer yields ~30% more tokens than 4.5-era budgets
   assumed (ch. 3 §3.5, ch. 4 §4.5, ch. 5 §5.3–5.5). Trim history, cap `max_tokens`, retrieve
   instead of stuffing.

### 19.4 Simple cost-tracking snippet

```python
# $/1M tokens (input, output, cached-input) — seed from chapter §N.2/N.5 tables;
# re-verify before billing decisions (prices change; some were MEDIUM confidence).
PRICES = {
    ("openai", "gpt-5.6-terra"):     (1.00, 6.00, 0.10),
    ("openai", "gpt-5.6-luna"):      (0.10, 0.60, 0.01),
    ("anthropic", "claude-sonnet-5"): (2.00, 10.00, 0.20),
    ("anthropic", "claude-haiku-4-5"): (1.00, 5.00, 0.10),
    ("gemini", "gemini-3.7-flash"):  (0.75, 3.75, 0.075),   # promo to 2026-12-31
    ("ollama", "*"):                 (0.0, 0.0, 0.0),
}

def estimate_cost(provider, model, usage, cached_in=0):
    p_in, p_out, p_cache = PRICES.get((provider, model),
                                      PRICES.get((provider, "*"), (0, 0, 0)))
    fresh_in = max(usage.get("in", 0) - cached_in, 0)
    return (fresh_in * p_in + cached_in * p_cache + usage.get("out", 0) * p_out) / 1e6
```

For exact rather than estimated numbers: OpenRouter's `/generation` endpoint returns the actual
charge per request (ch. 8 §8.5); AWS/Azure billing exports are authoritative on those platforms
(and Azure showed a documented price-parity lag in 2026-08 — budget at billed rates, ch. 7 §7.5).

---

## 20. Security & compliance across providers

### 20.1 Key management

- **One key per app/environment, least scope**: OpenAI project-scoped keys, Anthropic
  workspace-scoped keys, HF fine-grained tokens ("create one access token per app"), Azure
  two rotatable keys per resource (ch. 3 §3.6, ch. 5 §5.6, ch. 10 §10.6, ch. 7 §7.6).
- **Prefer identity over static secrets where the platform offers it**: Bedrock IAM roles
  (instance/task/Lambda execution roles — "zero stored secrets", ch. 6 §6.6); Azure Entra ID with
  `DefaultAzureCredential`, and disable resource keys entirely for Entra-only posture (ch. 7 §7.6).
- Keys live only server-side (§18.1); browser/mobile realtime uses ephemeral client secrets
  (ch. 3 §3.15). OpenRouter BYOK concentrates all lab keys in one third party ("securely
  encrypted" per docs, 5% fee) — a convenience/blast-radius tradeoff to make consciously
  (ch. 8 §8.6).
- Rotate on schedule and on any suspected exposure; scope monitoring (§19.2) so anomalous spend
  surfaces fast — spend is usually the first leak indicator (generic guidance).

### 20.2 Data-usage policy summary (pointer table — the chapters' §17 are the record; do not rely on this summary alone)

| Provider | Documented default posture (as verified in chapter) | Detail |
|---|---|---|
| OpenAI | API data not used for training by default; abuse logs ≤30 days; Responses **stored by default** (`store:false` for stateless); ZDR by approval (vector stores/assistants ineligible) | ch. 3 §3.17, §3.7 |
| Gemini | **Free tier: inputs/outputs used for product improvement incl. human review — do not send sensitive data.** Paid tier: not used to improve products; limited abuse logging | ch. 4 §4.17 |
| Anthropic | No training on API data by default; 30-day backend deletion; ZDR by agreement (Files API not ZDR-eligible); schemas cached 24 h (no PHI in schemas) | ch. 5 §5.17 |
| Bedrock | Prompts/outputs not stored for or shared with model providers, not used to train; HIPAA-eligible/FedRAMP-High scope; global profiles process in any region (CloudTrail logs where) | ch. 6 §6.16–6.17 |
| Azure | Not available to OpenAI; not used to train; abuse-monitoring storage unless Modified Abuse Monitoring approved; content filters on by default (behavioral delta vs OpenAI direct); data at rest stays in designated geography | ch. 7 §7.16–7.17 |
| OpenRouter | No prompt logging by default (opt-in earns 1% discount); ZDR policy + per-request `zdr`/`data_collection:"deny"` routing; **`:free` endpoints often allow provider data use**; no published certifications | ch. 8 §8.17 |
| Ollama | Local: data never leaves the machine — but the local API is **unauthenticated by design**; Cloud claims no-logging/no-training, no published certs/SLA | ch. 9 §9.16–9.17 |
| Hugging Face | Providers route to partner infra — residency/retention are provider-dependent, not HF-pinned; pickle and `trust_remote_code` are code-execution risks; enterprise audit/RBAC/SSO tiers | ch. 10 §10.16–10.17 |

Certification claims (SOC 2/ISO/HIPAA) were verified only for AWS and Azure platform scopes in
the chapters; the rest were [UNVERIFIED] at access date — check each vendor's trust portal before
procurement (ch. 3/5/8/9/10 §N.17).

### 20.3 Egress control for local mode

Local inference's compliance story only holds if the box actually stays local:

- Bind Ollama to `127.0.0.1` (default) and never expose 11434 without an authenticating TLS proxy;
  firewall the port; in Docker publish `127.0.0.1:11434:11434` only (ch. 9 §9.17, §17.1 above).
- Legitimate egress is enumerable: registry pulls (`ollama.com`), hub downloads
  (`huggingface.co/...`/resolve). Route them through an egress proxy (`HTTPS_PROXY` is the
  supported knob for Ollama pulls — ch. 9 §9.6) and default-deny everything else; air-gapped
  operation works by pre-copying the models directory (ch. 9 §9.16, air-gap doc [UNVERIFIED]).
- Supply chain: pin model digests (Ollama blobs are SHA256 content-addressed but community
  namespaces are unvetted — ch. 9 §9.17); prefer safetensors, treat pickle checkpoints and
  `trust_remote_code=True` as arbitrary code execution and pin revisions (ch. 10 §10.17); keep
  the runtime patched (historical pull-path CVEs — ch. 9 §9.17).

### 20.4 Secrets-in-CI practices (generic engineering guidance)

- Use the CI system's secret store with environment/branch scoping; production keys reachable only
  from protected branches and required-review workflows. Never echo secrets; mask logs.
- Prefer **OIDC federation over static cloud keys** in CI: GitHub/GitLab OIDC → AWS IAM role
  (Bedrock) or Entra workload identity (Azure) issues short-lived credentials per job — this is
  the CI extension of the same no-static-secrets posture the chapters document for runtime
  (ch. 6 §6.6, ch. 7 §7.6).
- Tests should default to mocks or a local Ollama service container (free, no secret needed);
  gate real-API integration tests behind a manual/nightly job with a dedicated low-limit key,
  so a leaked CI key is a bounded blast radius.
- Scan for committed secrets (pre-commit hooks + repo scanning); provider key formats (`sk-proj-`,
  `hf_`, …) are pattern-matchable. Rotate immediately on any hit — assume published means
  compromised.

---

*End of Part III. Continue with Part IV (Unified Model Selection Guide, sections 21–28).*


---

# Part IV — Unified Model Selection Guide (Sections 21–28)

> Model lineups and pricing change frequently. Verified against official documentation on
> **2026-08-14**. Re-verify before production decisions.
>
> This part is derived from (a) the 8 machine-readable sidecars `providers/*.models.json`
> (195 model rows) and (b) the per-chapter evidence in Part II — chiefly each chapter's
> §N.3 (model details & limitations), §N.17 (compliance), §N.18 (legacy) and §N.19
> (task-suitability verdict). No benchmark numbers are introduced here; where a ranking is
> not backed by chapter evidence it is explicitly labeled **[judgment call]**.

---

## 21. Master comparison matrix

All tables in this section are **script-generated** from the sidecars by
`scripts/build_matrix.py`. Regenerate after any sidecar update:

```bash
python3 scripts/build_matrix.py            # tables to stdout
python3 scripts/build_matrix.py --check    # row counts only
```

Legend: context/output in tokens (`1.05M` = 1,050,000; `n/p` = not published in the
sidecar). Modalities: `T`=text, `I`=image, `A`=audio, `V`=video, `P`=pdf/document;
`TIVAP->T` = multimodal in, text out. Prices are USD per 1M tokens as recorded from the
provider's official pricing at access date; `n/p` = null in the sidecar (unpublished —
per 00_CONVENTIONS.md never coerced to 0), `0.00` = explicitly free listing. `Conf` is the
sidecar's own confidence grade for the row. Aggregator/platform rows (OpenRouter, Bedrock,
Azure) intentionally duplicate lab models — same weights, different platform contract and
sometimes different price (see §23).

<!-- generated by scripts/build_matrix.py from 195 sidecar rows; do not hand-edit tables -->

### Frontier tier (52 rows)

| Model id | Provider | Context | Max out | Modalities | Tools | $in/1M | $out/1M | Conf |
|---|---|---|---|---|---|---|---|---|
| `gpt-5.3-codex` | OpenAI | 400k | 128k | TI->T | Y | 1.75 | 14 | HIGH |
| `gpt-5.6-sol` | OpenAI | 1.05M | 128k | TI->T | Y | 2.5 | 15 | MEDIUM |
| `chat-latest` | OpenAI | n/p | n/p | T->T | n/p | 5 | 30 | MEDIUM |
| `gpt-5.6-cyber` | OpenAI | n/p | n/p | T->T | Y | 12.5 | 75 | MEDIUM |
| `daybreak-blue-latest` | OpenAI | n/p | n/p | T->T | n/p | n/p | n/p | LOW |
| `daybreak-red-latest` | OpenAI | n/p | n/p | T->T | n/p | n/p | n/p | LOW |
| `gemini-3.6-flash` | Gemini | 1.05M | 65.5k | TIVAP->T | Y | 0.75 | 3.75 | HIGH |
| `gemini-3.7-flash` | Gemini | 1.05M | 65.5k | TIVAP->T | Y | 0.75 | 3.75 | HIGH |
| `gemini-2.5-pro` | Gemini | 1.05M | 65.5k | TIVAP->T | Y | 1.25 | 10 | HIGH |
| `gemini-3.1-pro-preview` | Gemini | 1.05M | 65.5k | TIVAP->T | Y | 2 | 12 | HIGH |
| `antigravity-preview-05-2026` | Gemini | n/p | n/p | T->T | Y | n/p | n/p | LOW |
| `deep-research-max-preview-04-2026` | Gemini | n/p | n/p | T->T | Y | n/p | n/p | LOW |
| `deep-research-preview-04-2026` | Gemini | n/p | n/p | T->T | Y | n/p | n/p | LOW |
| `claude-opus-4-6` | Anthropic | n/p | n/p | TI->T | Y | 5 | 25 | MEDIUM |
| `claude-opus-4-7` | Anthropic | n/p | n/p | TI->T | Y | 5 | 25 | MEDIUM |
| `claude-opus-4-8` | Anthropic | n/p | n/p | TI->T | Y | 5 | 25 | MEDIUM |
| `claude-opus-5` | Anthropic | 1M | 128k | TI->T | Y | 5 | 25 | HIGH |
| `claude-fable-5` | Anthropic | 1M | 128k | TI->T | Y | 10 | 50 | HIGH |
| `claude-mythos-5` | Anthropic | 1M | 128k | TI->T | Y | 10 | 50 | MEDIUM |
| `claude-opus-4-5-20251101` | Anthropic | n/p | n/p | TI->T | Y | n/p | n/p | MEDIUM |
| `anthropic.claude-sonnet-5` | Bedrock | 1M | 128k | TI->T | Y | 2 | 10 | HIGH |
| `anthropic.claude-opus-4-8` | Bedrock | n/p | n/p | TI->T | Y | 5 | 25 | MEDIUM |
| `anthropic.claude-opus-5` | Bedrock | 1M | 128k | TI->T | Y | 5 | 25 | HIGH |
| `openai.gpt-5.6-sol` | Bedrock | 1M | n/p | TI->T | Y | 5.5 | 33 | HIGH |
| `anthropic.claude-fable-5` | Bedrock | n/p | n/p | TI->T | Y | 10 | 50 | MEDIUM |
| `openai.gpt-5.5` | Bedrock | n/p | n/p | TI->T | Y | n/p | n/p | MEDIUM |
| `DeepSeek-V4-Pro` | Azure | 1M | 384k | T->T | Y | 2 | 8 | MEDIUM |
| `gpt-5.4` | Azure | 1.05M | 128k | TI->T | Y | 2.5 | 15 | HIGH |
| `gpt-5.6-terra` | Azure | 1.05M | 128k | TI->T | Y | 2.75 | 16.5 | MEDIUM |
| `gpt-5.6-sol` | Azure | 1.05M | 128k | TI->T | Y | 5.5 | 33 | HIGH |
| `gpt-5.4-pro` | Azure | 1.05M | 128k | TI->T | Y | 30 | 180 | HIGH |
| `claude-sonnet-5 (partner)` | Azure | 1M | 128k | TI->T | Y | n/p | n/p | MEDIUM |
| `gpt-5` | Azure | 400k | 128k | TI->T | Y | n/p | n/p | HIGH |
| `gpt-5.5` | Azure | 1.05M | 128k | TI->T | Y | n/p | n/p | HIGH |
| `minimax/minimax-m3` | OpenRouter | 1.05M | n/p | T->T | Y | 0.23 | 0.96 | HIGH |
| `z-ai/glm-5.2` | OpenRouter | 1.05M | n/p | T->T | Y | 0.392 | 1.232 | MEDIUM |
| `deepseek/deepseek-v4-pro-0813` | OpenRouter | 1.05M | n/p | T->T | Y | 0.435 | 0.87 | HIGH |
| `mistralai/mistral-large-2512` | OpenRouter | 262.1k | n/p | T->T | Y | 0.5 | 1.5 | MEDIUM |
| `meta/muse-spark-1.2` | OpenRouter | 1.05M | n/p | T->T | Y | 1.25 | 4.25 | MEDIUM |
| `openai/gpt-5.3-codex` | OpenRouter | 400k | 128k | TI->T | Y | 1.75 | 14 | HIGH |
| `google/gemini-3.1-pro-preview` | OpenRouter | 1.05M | 65.5k | TIVAF->T | Y | 2 | 12 | HIGH |
| `qwen/qwen3.8-max` | OpenRouter | 1M | n/p | TI->T | Y | 2 | 6 | HIGH |
| `x-ai/grok-4.6` | OpenRouter | 500k | n/p | T->T | Y | 2 | 6 | HIGH |
| `moonshotai/kimi-k3` | OpenRouter | 1.05M | n/p | T->T | Y | 3 | 15 | HIGH |
| `anthropic/claude-opus-5` | OpenRouter | 1M | 128k | TI->T | Y | 5 | 25 | HIGH |
| `openai/gpt-5.6-sol` | OpenRouter | 1.05M | 128k | TI->T | Y | 5 | 30 | MEDIUM |
| `anthropic/claude-fable-5` | OpenRouter | 1M | 128k | TI->T | Y | 10 | 50 | HIGH |
| `deepseek-v4-flash` | Ollama | 1M | n/p | T->T | Y | n/p | n/p | MEDIUM |
| `Qwen/Qwen3.8-2.4T-A95B` | HF | 262.1k | n/p | T->T | Y | n/p | n/p | HIGH |
| `deepseek-ai/DeepSeek-V4-Pro-0813` | HF | 1M | n/p | T->T | Y | n/p | n/p | HIGH |
| `moonshotai/Kimi-K3` | HF | 1M | n/p | TIV->T | Y | n/p | n/p | HIGH |
| `zai-org/GLM-5.2` | HF | 1M | n/p | T->T | Y | n/p | n/p | HIGH |

Note: OpenRouter/Bedrock/Azure rows duplicate lab models by design (same model, different platform terms/prices); price divergence between rows for the same model is real observed listing data, not an error — see section 23.

### Mid / budget tier (86 rows)

| Model id | Provider | Context | Max out | Modalities | Tools | $in/1M | $out/1M | Conf |
|---|---|---|---|---|---|---|---|---|
| `omni-moderation-latest` | OpenAI | n/p | n/p | TI->T | N | 0.00 | 0.00 | HIGH |
| `gpt-5.6-luna` | OpenAI | 1.05M | 128k | TI->T | Y | 0.1 | 0.6 | MEDIUM |
| `gpt-5.6-terra` | OpenAI | 1.05M | 128k | TI->T | Y | 1 | 6 | MEDIUM |
| `o4-mini-2025-04-16` | OpenAI | n/p | n/p | T->T | Y | 4 | 16 | MEDIUM |
| `gemini-2.5-flash-lite` | Gemini | 1.05M | 65.5k | TIVA->T | Y | 0.1 | 0.4 | MEDIUM |
| `gemini-3.1-flash-lite` | Gemini | 1.05M | 65.5k | TIVAP->T | Y | 0.25 | 1.5 | HIGH |
| `gemini-2.5-flash` | Gemini | 1.05M | 65.5k | TIVA->T | Y | 0.3 | 2.5 | HIGH |
| `gemini-3.5-flash-lite` | Gemini | 1.05M | 65.5k | TIVAP->T | Y | 0.3 | 2.5 | HIGH |
| `gemini-3.5-flash` | Gemini | 1.05M | 65.5k | TIVAP->T | Y | 1.5 | 9 | HIGH |
| `gemini-2.5-computer-use-preview-10-2025` | Gemini | n/p | n/p | TI->T | Y | n/p | n/p | MEDIUM |
| `gemini-3-flash-preview` | Gemini | 1.05M | 65.5k | TIVAP->T | Y | n/p | n/p | MEDIUM |
| `gemini-robotics-er-2-preview` | Gemini | n/p | n/p | TI->T | Y | n/p | n/p | LOW |
| `gemma-4-26b-a4b-it` | Gemini | 262.1k | n/p | TIA->T | Y | n/p | n/p | MEDIUM |
| `gemma-4-31b-it` | Gemini | 262.1k | n/p | TIA->T | Y | n/p | n/p | MEDIUM |
| `claude-haiku-4-5-20251001` | Anthropic | 200k | 64k | TI->T | Y | 1 | 5 | HIGH |
| `claude-sonnet-5` | Anthropic | 1M | 128k | TI->T | Y | 2 | 10 | HIGH |
| `claude-sonnet-4-6` | Anthropic | n/p | n/p | TI->T | Y | 3 | 15 | MEDIUM |
| `claude-sonnet-4-5-20250929` | Anthropic | n/p | n/p | TI->T | Y | n/p | n/p | MEDIUM |
| `amazon.nova-micro-v1:0` | Bedrock | 128k | 5k | T->T | Y | 0.035 | 0.14 | MEDIUM |
| `meta.llama4-scout-17b-instruct-v1:0` | Bedrock | 1M | n/p | TI->T | Y | 0.17 | 0.36 | MEDIUM |
| `qwen.qwen3-32b-v1:0` | Bedrock | n/p | n/p | T->T | Y | 0.2 | 0.78 | MEDIUM |
| `amazon.nova-2-lite-v1:0` | Bedrock | 1M | 64k | TIV->T | Y | 0.33 | 2.75 | HIGH |
| `meta.llama4-maverick-17b-instruct-v1:0` | Bedrock | 1M | n/p | TI->T | Y | 0.5 | 0.8 | MEDIUM |
| `mistral.mistral-large-3-v1:0` | Bedrock | 128k | n/p | T->T | Y | 0.5 | 1.5 | MEDIUM |
| `deepseek.v3.2` | Bedrock | 128k | n/p | T->T | Y | 0.62 | 1.85 | MEDIUM |
| `amazon.nova-pro-v1:0` | Bedrock | 300k | 5k | TIV->T | Y | 0.8 | 3.2 | MEDIUM |
| `meta.llama3-3-70b-instruct-v1:0` | Bedrock | 128k | n/p | T->T | Y | 0.99 | 3.96 | LOW |
| `anthropic.claude-haiku-4-5` | Bedrock | 200k | 64k | TI->T | Y | 1 | 5 | HIGH |
| `anthropic.claude-sonnet-4-6-v1` | Bedrock | 200k | 64k | TI->T | Y | 3 | 15 | HIGH |
| `ai21.jamba-1-5-large-v1:0` | Bedrock | 256k | n/p | T->T | Y | n/p | n/p | MEDIUM |
| `deepseek.r1-v1:0` | Bedrock | 128k | n/p | T->T | N | n/p | n/p | MEDIUM |
| `mistral.pixtral-large-2502-v1:0` | Bedrock | 128k | n/p | TI->T | Y | n/p | n/p | MEDIUM |
| `openai.gpt-oss-120b-1:0` | Bedrock | 128k | n/p | T->T | Y | n/p | n/p | MEDIUM |
| `DeepSeek-V4-Flash` | Azure | 1M | 384k | T->T | Y | 0.2 | 0.8 | MEDIUM |
| `gpt-5.6-luna` | Azure | 1.05M | 128k | TI->T | Y | 1.1 | 6.6 | MEDIUM |
| `Llama-4-Maverick-17B-128E-Instruct-FP8` | Azure | 1M | 1M | TI->T | Y | n/p | n/p | MEDIUM |
| `Mistral-medium-2505` | Azure | 128k | n/p | T->T | Y | n/p | n/p | HIGH |
| `Phi-4` | Azure | 16k | n/p | T->T | N | n/p | n/p | MEDIUM |
| `Phi-4-Reasoning-Vision-15B` | Azure | n/p | n/p | TI->T | N | n/p | n/p | MEDIUM |
| `Phi-4-multimodal-instruct` | Azure | 128k | n/p | TIS->T | N | n/p | n/p | MEDIUM |
| `gpt-4.1` | Azure | 1.05M | 32.8k | TI->T | Y | n/p | n/p | HIGH |
| `gpt-5.4-mini` | Azure | 400k | 128k | TI->T | Y | n/p | n/p | HIGH |
| `gpt-chat-latest` | Azure | 128k | 16.4k | T->T | Y | n/p | n/p | HIGH |
| `gpt-oss-120b` | Azure | 131.1k | n/p | T->T | Y | n/p | n/p | HIGH |
| `grok-4.2` | Azure | n/p | n/p | T->T | Y | n/p | n/p | MEDIUM |
| `model-router` | Azure | n/p | n/p | TI->T | Y | n/p | n/p | HIGH |
| `o4-mini` | Azure | 200k | 100k | TI->T | Y | n/p | n/p | HIGH |
| `google/gemma-4-31b-it:free` | OpenRouter | 262.1k | n/p | T->T | Y | 0.00 | 0.00 | MEDIUM |
| `nvidia/nemotron-3.5-lightning:free` | OpenRouter | 1M | n/p | T->T | Y | 0.00 | 0.00 | HIGH |
| `openai/gpt-oss-20b:free` | OpenRouter | 131.1k | n/p | T->T | Y | 0.00 | 0.00 | HIGH |
| `poolside/laguna-s-2.1:free` | OpenRouter | 262.1k | n/p | T->T | Y | 0.00 | 0.00 | MEDIUM |
| `openai/gpt-oss-120b` | OpenRouter | 131.1k | n/p | T->T | Y | 0.03 | 0.17 | HIGH |
| `qwen/qwen3.7-flash` | OpenRouter | 1M | n/p | T->T | Y | 0.03 | 0.13 | HIGH |
| `nvidia/nemotron-3.5-lightning` | OpenRouter | 1M | n/p | T->T | Y | 0.1 | 0.25 | MEDIUM |
| `openai/gpt-5.6-luna` | OpenRouter | 1.05M | 128k | TI->T | Y | 0.1 | 0.6 | HIGH |
| `deepseek/deepseek-v4-flash-0731` | OpenRouter | 1.05M | n/p | T->T | Y | 0.14 | 0.28 | MEDIUM |
| `google/gemini-3.5-flash-lite` | OpenRouter | 1.05M | 65.5k | TIVAF->T | Y | 0.3 | 2.5 | HIGH |
| `meta/muse-glimmer-30b` | OpenRouter | 131.1k | n/p | T->T | Y | 0.35 | 1.5 | MEDIUM |
| `google/gemini-3.7-flash` | OpenRouter | 1.05M | 65.5k | TIVAF->T | Y | 0.375 | 1.875 | MEDIUM |
| `anthropic/claude-haiku-4.5` | OpenRouter | 200k | 64k | TI->T | Y | 1 | 5 | HIGH |
| `openai/gpt-5.6-terra` | OpenRouter | 1.05M | 128k | TI->T | Y | 1 | 6 | HIGH |
| `mistralai/mistral-medium-3-5` | OpenRouter | 262.1k | n/p | T->T | Y | 1.5 | 7.5 | MEDIUM |
| `anthropic/claude-sonnet-5` | OpenRouter | 1M | 128k | TI->T | Y | 2 | 10 | MEDIUM |
| `openrouter/auto` | OpenRouter | 2M | n/p | T->T | Y | n/p | n/p | HIGH |
| `deepseek-r1` | Ollama | 131.1k | n/p | T->T | Y | n/p | n/p | HIGH |
| `gemma4` | Ollama | 262.1k | n/p | TIA->T | Y | n/p | n/p | HIGH |
| `gpt-oss` | Ollama | 131.1k | n/p | T->T | Y | n/p | n/p | HIGH |
| `llama3.1 / llama3.2 / llama3.3 / llama4` | Ollama | 131.1k | n/p | TI->T | Y | n/p | n/p | MEDIUM |
| `mistral-medium-3.5` | Ollama | n/p | n/p | TI->T | Y | n/p | n/p | MEDIUM |
| `mistral-small3.2` | Ollama | n/p | n/p | TI->T | Y | n/p | n/p | MEDIUM |
| `muse-glimmer` | Ollama | 131.1k | n/p | TI->T | Y | n/p | n/p | HIGH |
| `nemotron-3.5-lightning` | Ollama | n/p | n/p | T->T | Y | n/p | n/p | MEDIUM |
| `phi4 / phi4-mini / phi4-reasoning` | Ollama | n/p | n/p | T->T | Y | n/p | n/p | MEDIUM |
| `qwen3-coder` | Ollama | 262.1k | n/p | T->T | Y | n/p | n/p | HIGH |
| `qwen3.5` | Ollama | 262.1k | n/p | TI->T | Y | n/p | n/p | HIGH |
| `qwen3.6` | Ollama | 262.1k | n/p | TI->T | Y | n/p | n/p | HIGH |
| `LiquidAI/LFM2.5-2.6B` | HF | n/p | n/p | T->T | n/p | n/p | n/p | LOW |
| `Qwen/Qwen3.6-27B` | HF | 262.1k | n/p | TIV->T | Y | n/p | n/p | HIGH |
| `deepseek-ai/DeepSeek-V4-Flash-0731` | HF | n/p | n/p | T->T | Y | n/p | n/p | MEDIUM |
| `google/gemma-4-31B-it` | HF | 262.1k | n/p | TI->T | Y | n/p | n/p | HIGH |
| `google/gemma-4-E4B-it` | HF | 131.1k | n/p | TIA->T | Y | n/p | n/p | HIGH |
| `meta-llama/Llama-4-Scout-17B-16E-Instruct` | HF | 10M | n/p | TI->T | Y | n/p | n/p | MEDIUM |
| `meta-models/Muse-Glimmer-30B` | HF | 131.1k | n/p | TI->T | Y | n/p | n/p | HIGH |
| `microsoft/phi-4` | HF | 16.4k | n/p | T->T | Y | n/p | n/p | MEDIUM |
| `mistralai/Mistral-Medium-3.5-128B` | HF | 262.1k | n/p | TI->T | Y | n/p | n/p | HIGH |
| `openai/gpt-oss-120b` | HF | 131.1k | n/p | T->T | Y | n/p | n/p | MEDIUM |

Note: `0.00` rows are explicitly free listings (OpenRouter `:free` variants, moderation endpoint); `n/p` means the sidecar records no published per-token price (open-weight or compute-billed models).

### Embedding models (18 rows)

| Model id | Provider | Context | Max out | Modalities | Tools | $in/1M | $out/1M | Conf |
|---|---|---|---|---|---|---|---|---|
| `text-embedding-3-small` | OpenAI | 8.2k | n/p | T->V | N | 0.02 | n/p | HIGH |
| `text-embedding-3-large` | OpenAI | 8.2k | n/p | T->V | N | 0.13 | n/p | HIGH |
| `gemini-embedding-001` | Gemini | 2k | n/p | T->E | N | 0.15 | n/p | MEDIUM |
| `gemini-embedding-2-preview` | Gemini | 8.2k | n/p | TIVAP->E | N | n/p | n/p | MEDIUM |
| `amazon.titan-embed-text-v2:0` | Bedrock | 8.2k | n/p | T->? | N | 0.02 | n/p | MEDIUM |
| `amazon.nova-multimodal-embeddings` | Bedrock | n/p | n/p | TIV->? | N | n/p | n/p | LOW |
| `cohere.embed-v4` | Bedrock | n/p | n/p | TI->? | N | n/p | n/p | LOW |
| `cohere.rerank-v3-5:0` | Bedrock | n/p | n/p | T->? | N | n/p | n/p | HIGH |
| `Cohere-embed-v-4-0` | Azure | 512 | n/p | TI->? | N | n/p | n/p | MEDIUM |
| `text-embedding-3-large` | Azure | 8.2k | n/p | T->? | N | n/p | n/p | HIGH |
| `text-embedding-3-small` | Azure | 8.2k | n/p | T->? | N | n/p | n/p | HIGH |
| `embeddinggemma` | Ollama | n/p | n/p | T->E | N | n/p | n/p | HIGH |
| `qwen3-embedding` | Ollama | n/p | n/p | T->E | N | n/p | n/p | MEDIUM |
| `Alibaba-NLP/gte-multilingual-base` | HF | 8.2k | n/p | T->V | N | n/p | n/p | MEDIUM |
| `BAAI/bge-m3` | HF | 8.2k | n/p | T->V | N | n/p | n/p | MEDIUM |
| `Qwen/Qwen3-Embedding-0.6B` | HF | 32k | n/p | T->V | N | n/p | n/p | MEDIUM |
| `google/embeddinggemma-300m` | HF | 2k | n/p | T->V | N | n/p | n/p | MEDIUM |
| `sentence-transformers/all-MiniLM-L6-v2` | HF | 256 | n/p | T->V | N | n/p | n/p | MEDIUM |

Note: embedding output price is `n/p` by nature (input-only billing) for most rows.

### Local-capable models (any tier) (50 rows)

| Model id | Provider | Context | Max out | Modalities | Tools | $in/1M | $out/1M | Conf |
|---|---|---|---|---|---|---|---|---|
| `gemma-4-26b-a4b-it` | Gemini | 262.1k | n/p | TIA->T | Y | n/p | n/p | MEDIUM |
| `gemma-4-31b-it` | Gemini | 262.1k | n/p | TIA->T | Y | n/p | n/p | MEDIUM |
| `meta.llama4-scout-17b-instruct-v1:0` | Bedrock | 1M | n/p | TI->T | Y | 0.17 | 0.36 | MEDIUM |
| `qwen.qwen3-32b-v1:0` | Bedrock | n/p | n/p | T->T | Y | 0.2 | 0.78 | MEDIUM |
| `meta.llama4-maverick-17b-instruct-v1:0` | Bedrock | 1M | n/p | TI->T | Y | 0.5 | 0.8 | MEDIUM |
| `deepseek.v3.2` | Bedrock | 128k | n/p | T->T | Y | 0.62 | 1.85 | MEDIUM |
| `meta.llama3-3-70b-instruct-v1:0` | Bedrock | 128k | n/p | T->T | Y | 0.99 | 3.96 | LOW |
| `deepseek.r1-v1:0` | Bedrock | 128k | n/p | T->T | N | n/p | n/p | MEDIUM |
| `openai.gpt-oss-120b-1:0` | Bedrock | 128k | n/p | T->T | Y | n/p | n/p | MEDIUM |
| `Llama-4-Maverick-17B-128E-Instruct-FP8` | Azure | 1M | 1M | TI->T | Y | n/p | n/p | MEDIUM |
| `Phi-4` | Azure | 16k | n/p | T->T | N | n/p | n/p | MEDIUM |
| `Phi-4-Reasoning-Vision-15B` | Azure | n/p | n/p | TI->T | N | n/p | n/p | MEDIUM |
| `Phi-4-multimodal-instruct` | Azure | 128k | n/p | TIS->T | N | n/p | n/p | MEDIUM |
| `gpt-oss-120b` | Azure | 131.1k | n/p | T->T | Y | n/p | n/p | HIGH |
| `google/gemma-4-31b-it:free` | OpenRouter | 262.1k | n/p | T->T | Y | 0.00 | 0.00 | MEDIUM |
| `openai/gpt-oss-20b:free` | OpenRouter | 131.1k | n/p | T->T | Y | 0.00 | 0.00 | HIGH |
| `openai/gpt-oss-120b` | OpenRouter | 131.1k | n/p | T->T | Y | 0.03 | 0.17 | HIGH |
| `deepseek-r1` | Ollama | 131.1k | n/p | T->T | Y | n/p | n/p | HIGH |
| `embeddinggemma` | Ollama | n/p | n/p | T->E | N | n/p | n/p | HIGH |
| `gemma4` | Ollama | 262.1k | n/p | TIA->T | Y | n/p | n/p | HIGH |
| `gpt-oss` | Ollama | 131.1k | n/p | T->T | Y | n/p | n/p | HIGH |
| `llama3.1 / llama3.2 / llama3.3 / llama4` | Ollama | 131.1k | n/p | TI->T | Y | n/p | n/p | MEDIUM |
| `mistral-medium-3.5` | Ollama | n/p | n/p | TI->T | Y | n/p | n/p | MEDIUM |
| `mistral-small3.2` | Ollama | n/p | n/p | TI->T | Y | n/p | n/p | MEDIUM |
| `muse-glimmer` | Ollama | 131.1k | n/p | TI->T | Y | n/p | n/p | HIGH |
| `nemotron-3.5-lightning` | Ollama | n/p | n/p | T->T | Y | n/p | n/p | MEDIUM |
| `phi4 / phi4-mini / phi4-reasoning` | Ollama | n/p | n/p | T->T | Y | n/p | n/p | MEDIUM |
| `qwen3-coder` | Ollama | 262.1k | n/p | T->T | Y | n/p | n/p | HIGH |
| `qwen3-embedding` | Ollama | n/p | n/p | T->E | N | n/p | n/p | MEDIUM |
| `qwen3-vl` | Ollama | 262.1k | n/p | TIV->T | Y | n/p | n/p | HIGH |
| `qwen3.5` | Ollama | 262.1k | n/p | TI->T | Y | n/p | n/p | HIGH |
| `qwen3.6` | Ollama | 262.1k | n/p | TI->T | Y | n/p | n/p | HIGH |
| `Alibaba-NLP/gte-multilingual-base` | HF | 8.2k | n/p | T->V | N | n/p | n/p | MEDIUM |
| `BAAI/bge-m3` | HF | 8.2k | n/p | T->V | N | n/p | n/p | MEDIUM |
| `Lightricks/LTX-2.5` | HF | n/p | n/p | TI->V | N | n/p | n/p | LOW |
| `LiquidAI/LFM2.5-2.6B` | HF | n/p | n/p | T->T | n/p | n/p | n/p | LOW |
| `Qwen/Qwen3-Embedding-0.6B` | HF | 32k | n/p | T->V | N | n/p | n/p | MEDIUM |
| `Qwen/Qwen3-VL-8B-Instruct` | HF | 262.1k | n/p | TIV->T | Y | n/p | n/p | MEDIUM |
| `Qwen/Qwen3.6-27B` | HF | 262.1k | n/p | TIV->T | Y | n/p | n/p | HIGH |
| `black-forest-labs/FLUX.2-dev` | HF | n/p | n/p | TI->I | N | n/p | n/p | LOW |
| `google/embeddinggemma-300m` | HF | 2k | n/p | T->V | N | n/p | n/p | MEDIUM |
| `google/gemma-4-31B-it` | HF | 262.1k | n/p | TI->T | Y | n/p | n/p | HIGH |
| `google/gemma-4-E4B-it` | HF | 131.1k | n/p | TIA->T | Y | n/p | n/p | HIGH |
| `meta-llama/Llama-4-Scout-17B-16E-Instruct` | HF | 10M | n/p | TI->T | Y | n/p | n/p | MEDIUM |
| `meta-models/Muse-Glimmer-30B` | HF | 131.1k | n/p | TI->T | Y | n/p | n/p | HIGH |
| `microsoft/phi-4` | HF | 16.4k | n/p | T->T | Y | n/p | n/p | MEDIUM |
| `mistralai/Mistral-Medium-3.5-128B` | HF | 262.1k | n/p | TI->T | Y | n/p | n/p | HIGH |
| `openai/gpt-oss-120b` | HF | 131.1k | n/p | T->T | Y | n/p | n/p | MEDIUM |
| `openai/whisper-large-v3-turbo` | HF | n/p | n/p | A->T | N | n/p | n/p | MEDIUM |
| `sentence-transformers/all-MiniLM-L6-v2` | HF | 256 | n/p | T->V | N | n/p | n/p | MEDIUM |

Note: rows overlap with the tier tables above; this view filters `local_capable: true`. Prices shown are hosted-endpoint prices where a hosted listing exists; local runs are compute-cost-only.

---

## 22. Task-type suitability map

Recommendations cite the Part II chapter verdicts (§N.19) and limitation sections (§N.3).
"Primary" = best evidence-backed default; "Budget" = cheapest credible option; "Local" =
best open-weight/on-prem option. Where the chapters give no direct evidence, the cell is a
**[judgment call]** from adjacent evidence (positioning statements, price, feature matrix).

### Classification / routing / short structured tasks
| Slot | Pick | Rationale (chapter evidence) |
|---|---|---|
| Primary | `gpt-5.6-luna` (OpenAI) | §3.19: "high-volume cheap inference (Luna + batch + caching => $0.05/1M batched input)"; docs position it for "cost-sensitive, high-volume workloads" (§3.3). |
| Alt primary | `claude-haiku-4-5` | §5.19: "Haiku 4.5 for latency/cost-sensitive routing". |
| Budget | `amazon.nova-micro-v1:0` ($0.035/$0.14) or `qwen/qwen3.7-flash` via OpenRouter ($0.03/$0.13) | Cheapest published per-token rates in the sidecars; OpenRouter row flags "avoid: hard reasoning". |
| Local | `llama3.2 1B/3B`, `gemma4:e4b`, `phi4-mini` | §9.19: "edge/small-footprint deployment (gemma4 E-series, llama3.2 1B/3B, phi4-mini)". |

### Summarization
| Slot | Pick | Rationale |
|---|---|---|
| Primary | `gemini-3.5-flash-lite` / `gemini-2.5-flash-lite` | §4.3: 3.5 Flash-Lite positioned for "high-throughput, low-cost execution … and document parsing"; 1M context covers whole documents; §4.19 flash-tier price/performance. |
| Alt primary | `gpt-5.6-terra` | §3.3: "balances intelligence and cost"; 1.05M window at $1/$6. |
| Budget | `gemini-2.5-flash-lite` ($0.10/$0.40) | §4.3: "cheapest text path on the API"; batch −50% stacks. |
| Local | `qwen3.5:9b` / `qwen3.6:27b` | §9.19 general-use sweet-spot picks; 256K context. Watch the 4096-token default context (§9.3). |

### Extraction (schema-bound output)
| Slot | Pick | Rationale |
|---|---|---|
| Primary | `claude-sonnet-5` | §5.19: "schema-guaranteed extraction (grammar-backed structured outputs)"; $2/$10 "price-performance anchor". Caveat §5.19: structured outputs exclude citations/prefill. |
| Budget | `gemini-3.1-flash-lite` | §4.3: positioned for "high-frequency, lightweight tasks (translation, extraction, routing)"; SO supported; $0.25/$1.50. |
| Local | `gpt-oss:20b` or `qwen3.5` | §9.3: gpt-oss has "strong function calling and structured output"; both Apache-2.0. |
| Avoid | Bedrock `anthropic.claude-sonnet-5` for SO | §6.3/§6.19: "no structured outputs on Sonnet 5 runtime" on Bedrock — feature lags the native API. |

### Reasoning (hardest problems)
| Slot | Pick | Rationale |
|---|---|---|
| Primary | `claude-opus-5` / `claude-fable-5`; `gpt-5.6-sol` | §5.19: "Opus 5/Fable 5 for frontier reasoning"; §3.3: Sol = "strongest capability for complex coding, computer use, research, and cybersecurity". |
| Mid | `gemini-3.1-pro-preview` ($2/$12) | §4.3 flagship intelligence tier — but **preview-only**; §4.19 flags flagship stability as a weakness. |
| Budget | `deepseek/deepseek-v4-pro-0813` via OpenRouter ($0.435/$0.87) or `DeepSeek-V4-Pro` on Azure ($2/$8) | Frontier-tier open-weight at budget prices per sidecars; capability vs closed frontier not benchmarked here — **[judgment call]**. |
| Local | `gpt-oss:20b`/`120b`, `qwen3.6:27b` | §9.19: "reasoning-per-GB = gpt-oss:20b"; same section warns "even the best ~35B local models trail current hosted frontier models". |

### Coding
| Slot | Pick | Rationale |
|---|---|---|
| Primary | `gpt-5.3-codex` | §3.3: "most capable agentic coding model to date" (400K ctx, $1.75/$14); §3.19 best-at list. |
| Alt primary | `claude-opus-5`/`claude-sonnet-5` | §5.19 agentic tool-use strengths; §6.3: Bedrock positions Claude as its flagship line. |
| Mid | `gemini-3.7-flash` | §4.3: positioned for "complex coding and agentic workflows" at $0.75/$3.75 promo. |
| Local | `qwen3-coder:30b` | §9.19: "coding = qwen3-coder:30b" sweet-spot pick. |

### Agents / tool use
| Slot | Pick | Rationale |
|---|---|---|
| Primary | Anthropic Claude (Opus 5 / Sonnet 5) | §5.19: "richest server-tool set, parallel + strict tools, tool search, computer use, Agent SDK/MCP origin". |
| Enterprise runtime | Azure Agent Service; AWS AgentCore | §7.19: "most complete managed agent runtime of the clouds surveyed"; §6.19: "AgentCore is among the most complete managed agent runtimes". |
| Budget | `gemini-3.7-flash` + built-in tools | §4.19: "agentic/tool workloads — Interactions API step model, built-in Search/Maps/code-exec/computer-use". |
| Local | `muse-glimmer` | §9.3: "explicitly tuned for tool schemas, long tasks and failure recovery. Not a general-chat champion — pick it for agent loops." |
| Avoid | Gemini image models in agents (§4.19: no FC/SO); small local tags for complex agent chains (§26). |

### Multimodal understanding (image/video/audio/PDF in)
| Slot | Pick | Rationale |
|---|---|---|
| Primary | Gemini reasoning models (3.7/3.6-flash, 3.1-pro) | §4.19: "every reasoning model takes 1M tokens of text+image+video+audio+PDF" — only provider with full A/V/PDF input across the line. |
| Frontier alt | `gpt-5.6-*`, `claude-*` (text+image only) | §3.3: "No audio/video I/O" on GPT-5.6; Claude rows are TI->T. |
| Budget | `gemini-2.5-flash` / `amazon.nova-2-lite` | Nova 2 Lite: text+image+video in, 1M ctx, $0.33/$2.75 (§6.3). |
| Local | `qwen3-vl:8b`, `gemma4` (audio-in on E-series/12B) | §9.19 vision pick; §10.3 Gemma 4 audio-in sizes. |

### Image / video generation
| Slot | Pick | Rationale |
|---|---|---|
| Image primary | `gpt-image-2` (OpenAI/Azure) or `gemini-3-pro-image` (Nano Banana Pro) | §3.19 best-at list includes "image gen/edit (gpt-image-2)"; §4.19 "integrated media generation". |
| Image budget | `gemini-3.1-flash-lite-image` ($0.0336/1K image, batch half) | Cheapest published per-image rate in the sidecars. |
| Video primary | `veo-3.1-*` (Gemini) | §4.19: "video (Veo 3.1 with native audio)". OpenAI `sora-2` API **shuts down 2026-09-24** (§3.18) — do not build on it; Azure `sora-2` remains listed but verify roadmap. |
| Local | `FLUX.2-dev` (image; gated, non-commercial license per §10.4), `LTX-2.5` (video, LOW conf) | Only open-weight options in the sidecars; license review required (§10.19). |
| Avoid | Imagen 4 (shutdown 2026-08-17, §4.18); Nova Canvas/Reel gen-1 (EOL 2026-09-30, §6.18). |

### RAG / embeddings
| Slot | Pick | Rationale |
|---|---|---|
| Primary | `text-embedding-3-large` ($0.13) + any 1M-context generator | Highest-confidence published embedding row; §3.13. |
| Retrieval stack | Cohere `embed-v4` + `rerank-3.5` on Bedrock | §6.3: Cohere "pivoted on Bedrock to retrieval infrastructure" — but embed-v4 row is LOW confidence (id/price unconfirmed). |
| Budget | `text-embedding-3-small` ($0.02) or `amazon.titan-embed-text-v2` ($0.02) | Cheapest published embedding rates. |
| Local | `qwen3-embedding`, `embeddinggemma`, `BAAI/bge-m3` | §9.19: "local RAG (qwen3-embedding …)"; §10.19: "embeddings at scale via TEI". |
| Note | Anthropic and OpenRouter offer **no embeddings** (§5.19, §8.19) — pair with another provider. |

### Speech (STT / TTS / realtime voice)
| Slot | Pick | Rationale |
|---|---|---|
| Primary (voice agents) | OpenAI Realtime (`gpt-realtime-2.1`, WebRTC/SIP) | §3.19: "voice agents (Realtime GA, WebRTC/SIP, dedicated translate/transcribe models)". |
| Alt realtime | Gemini Live (`gemini-3.1-flash-live-preview`), `amazon.nova-2-sonic` (bidirectional S2S, §6.3) | Both preview/platform-specific; Gemini also has TTS + translate lines (§4.4). |
| Budget STT | `gpt-transcribe` ($0.0045/min — cheapest published batch STT, §3.4). |
| Local | `whisper-large-v3-turbo` (Apache-2.0, §10.4) | Only local STT row; no local TTS in the sidecars. |
| Note | Anthropic has no speech models at all (§5.19). |

---

## 23. Price/performance ranking

Ranking below is **by published price only** (sidecar values, USD per 1M tokens);
capability ordering within a tier is *not* implied — see the caveat column. Tier
boundaries: budget ≤ ~$0.5 in; mid ~$0.5–$3 in; premium-reasoning > $3 in or flagship
positioning.

### Budget tier (published price, ascending by input rate)
| Rank | Model (platform) | $in/$out | Caveat |
|---|---|---|---|
| 1 | `qwen/qwen3.7-flash` (OpenRouter) | 0.03/0.13 | 1M ctx; sidecar: "avoid: hard reasoning". |
| 1= | `openai/gpt-oss-120b` (OpenRouter) | 0.03/0.17 | Open-weight; per-endpoint quantization varies (§8.3). |
| 3 | `amazon.nova-micro` (Bedrock) | 0.035/0.14 | 128K ctx, text-only. |
| 4 | `gpt-5.6-luna` (OpenAI direct) | 0.10/0.60 | Frontier-family small tier; batched input $0.05; long-context >272K bills 0.20/0.90. |
| 4= | `nvidia/nemotron-3.5-lightning` (OpenRouter) | 0.10/0.25 | 1M ctx open-weight. |
| 6 | `gemini-2.5-flash-lite` | 0.10/0.40 | Older generation; §4.3 expects eventual deprecation. |
| 7 | `deepseek/deepseek-v4-flash-0731` (OpenRouter) | 0.14/0.28 | Azure lists same model at 0.20/0.80 — platform delta. |
| 8 | `meta.llama4-scout` (Bedrock) | 0.17/0.36 | 1M ctx multimodal MoE. |
| 9 | `qwen.qwen3-32b` (Bedrock) | 0.20/0.78 | ctx n/p on card. |
| 10 | `gemini-3.1-flash-lite` | 0.25/1.50 | Current-gen lite; SO+FC supported. |
| 11 | `gemini-3.5-flash-lite` / `gemini-2.5-flash` | 0.30/2.50 | Output rate is the highest of the tier. |
| — | `:free` OpenRouter variants | 0.00 | Prototyping only — see §26 rate floors and data-policy warnings. |

### Mid tier
| Rank | Model (platform) | $in/$out | Caveat |
|---|---|---|---|
| 1 | `minimax/minimax-m3` (OpenRouter) | 0.23/0.96 | 1M ctx open-weight. |
| 2 | `amazon.nova-2-lite` (Bedrock) | 0.33/2.75 | 1M ctx, T+I+V in; **no batch**, geo/global profiles only (§6.3). |
| 3 | `z-ai/glm-5.2` (OpenRouter) | 0.392/1.232 | MEDIUM conf listing; MIT weights. |
| 4 | `mistral.mistral-large-3` (Bedrock) | 0.50/1.50 | §6.3: "aggressively priced" US-region rate. |
| 5 | `deepseek.v3.2` (Bedrock) | 0.62/1.85 | Superseded by V4 line. |
| 6 | `gemini-3.7-flash` / `3.6-flash` | 0.75/3.75 | **Promo until 2026-12-31; 1.50/7.50 after** (sidecar price_notes). |
| 7 | `gpt-5.6-terra` (OpenAI direct) | 1.00/6.00 | Azure still bills 2.75/16.5 pending the announced −20% cut. |
| 8 | `claude-haiku-4-5` | 1.00/5.00 | 200K ctx only; manual (not adaptive) thinking (§5.3). |
| 9 | `gemini-3.5-flash` | 1.50/9.00 | — |
| 10 | `claude-sonnet-5` | 2.00/10.00 | §5.19 "price-performance anchor"; 1M ctx flat (no long-context surcharge). |
| 11 | `claude-sonnet-4-6` | 3.00/15.00 | Superseded generation at a higher price than Sonnet 5 — no reason to pick it for new work. |

### Premium / deep-reasoning tier
| Rank | Model (platform) | $in/$out | Caveat |
|---|---|---|---|
| 1 | `x-ai/grok-4.6` / `qwen/qwen3.8-max` (OpenRouter) | 2.00/6.00 | Cheapest frontier-positioned rows; capability vs peers unbenchmarked here — [judgment call]. |
| 2 | `gemini-3.1-pro-preview` | 2.00/12.00 | Preview-only flagship (§4.19); tiered pricing above 200K prompt tokens. |
| 3 | `gpt-5.6-sol` (OpenAI direct) | 2.50/15.00 | Post-July-2026 cut; >272K input bills 5.00/22.50; fast mode 2×. |
| 4 | `moonshotai/kimi-k3` (OpenRouter) | 3.00/15.00 | 1M ctx native-multimodal open-weight. |
| 5 | `claude-opus-5` | 5.00/25.00 | Fast Mode $10/$50 (§5.3). |
| 6 | `gpt-5.6-sol` (Bedrock/Azure) | 5.50/33.00 | Same model, ~2.2× the direct price at access date — see confidence flags below. |
| 7 | `claude-fable-5` / `claude-mythos-5` | 10.00/50.00 | §5.19: avoid for budget workloads; limited availability. |
| 8 | `gpt-5.6-cyber` | 12.50/75.00 | Short-context, gated (§3.3). |
| 9 | `gpt-5.4-pro` (Azure) | 30.00/180.00 | Most expensive row in the suite; "maximum analysis depth" positioning (§7.3). |

### Price-confidence flags (raised by the chapters — read before trusting any row above)
- **OpenRouter listing lag, both directions** (§8.2/§8.19): `openai/gpt-5.6-sol` listed
  at 5.00/30.00 while OpenAI direct lists 2.50/15.00 post-cut ("listing appears to lag");
  `google/gemini-3.7-flash` listed at 0.375/1.875, *below* Google's 0.75/3.75 promo.
  "Billed price follows the listing" — verify at call time.
- **Azure parity lag** (§7.19 + sidecar notes): documented 2-week+ lag on the 2026-07
  OpenAI cuts; `gpt-5.6-luna` on Azure bills 1.10/6.60 (~5× OpenAI direct's 0.10/0.60)
  until the announced −80% cut lands; Sol's cut to ~5.00/30.00 "pending in billing".
- **Bedrock LOW-confidence rows** (§6.2 sidecar): `meta.llama3-3-70b` price "anomalous vs
  earlier published rates — re-verify"; `cohere.embed-v4` and
  `amazon.nova-multimodal-embeddings` model-id strings and prices unconfirmed.
- **Promo expiry**: Gemini 3.7/3.6-flash pricing is promotional through 2026-12-31 (§4.19:
  "reproducible pricing beyond 2026-12-31" flagged as a weakness).
- **Hidden multipliers**: OpenAI >272K-input surcharge (2×/1.5×) and fast-mode 2× (§3.19
  "cost watch-outs"); Anthropic 4.7+ tokenizer yields ~30% more tokens than 4.5-era
  (§5.3) — cross-generation price comparisons on token counts are skewed; Bedrock adds a
  10% premium on regional/cross-region Claude endpoints (§6.3); Anthropic
  data-residency and Fast Mode multipliers stack (§5.3).
- Discounts stack differently per provider: cache reads 0.1× + batch 50% (Anthropic);
  cache ~90% + batch 50% (Gemini); cached input 0.01–0.25× + batch 50% (OpenAI). A
  "more expensive" list price can win after caching — model the workload, not the sticker.

---

## 24. Selection dimensions

### 24.1 Latency (qualitative tiers only — no measured figures in the source chapters)
```
fastest ──────────────────────────────────────────────────────────► slowest
local small (1–9B, resident in VRAM; no network hop)
  > hosted flash/mini/lite (luna, haiku, flash-lite, nova-micro/lite)
    > frontier default modes (sol, opus, sonnet, gemini-pro)
      > deep-reasoning / high-effort modes (xhigh/max effort, gpt-5.4-pro,
        deep-research-* — minutes-scale by design)
```
Modifiers documented by chapters: OpenAI Sol "fast mode" and Anthropic Opus "Fast Mode"
buy latency for 2× price; OpenRouter adds an extra network hop ("measure vs direct",
§8.19); Azure's content-filter layer adds latency/refusal deltas vs OpenAI direct
(§7.17); Ollama throughput collapses under multi-user load (§9.19: "use vLLM/SGLang" for
high QPS); verbose thinking on reasoning models (e.g. deepseek-r1 distills, §9.3)
inflates wall-clock even when tokens/s is fine.

### 24.2 Context-window ladder (from the sidecars)
| Rung | Models (representative) |
|---|---|
| ≤16K | `Phi-4` (16K), `text-embedding-3-*` (8K inputs) |
| 128–131K | gpt-oss, muse-glimmer, llama3.x, mistral-medium-2505, nova-micro, deepseek.v3.2/r1 (Bedrock), `gpt-chat-latest` |
| 200K | claude-haiku-4-5, claude-sonnet-4-6, o4-mini |
| 256–262K | qwen3.5/3.6, gemma-4 (12B+), mistral-medium-3.5, jamba-1.5, Qwen3.8 native |
| 400K | gpt-5.3-codex, gpt-5, gpt-5.4-mini |
| 500K | grok-4.6 |
| 1M–1.05M | gpt-5.6 trio, gpt-5.5/5.4, gpt-4.1, all Claude 5, all Gemini reasoning models, DeepSeek-V4, GLM-5.2, Kimi K3, nova-2-lite, llama4-maverick/scout (Bedrock), nemotron-3.5-lightning |
| >1M | `meta-llama/Llama-4-Scout` **10M native claim** on the HF card (§10.2 — partner providers frequently serve reduced windows); Qwen3.8 "extensible up to 1,010,000" |
Caveats: 1M ≠ 1M — OpenAI caps input at 922K of the shared window on Azure (§7.3),
surcharges >272K (§3.3); Gemini prices tier at 200K prompt tokens for Pro; Anthropic
Sonnet 5 is flat-priced at 1M (§5.3); Ollama defaults **every** model to 4096 tokens
until `num_ctx` is raised (§9.3); OpenRouter per-endpoint context can be lower than the
model's native figure (§8.3); HF card figures are native values, providers may serve less
(§10.3).

### 24.3 Accuracy proxy — honesty note
This suite intentionally publishes **no benchmark table**. The chapters record vendor
positioning statements and documented capabilities, not leaderboard scores, because (a)
vendor-reported benchmarks are unverifiable marketing surface, and (b) per-endpoint
quantization (OpenRouter §8.3), default 4-bit quants (Ollama §9.3), and platform feature
lag (Bedrock §6.19) mean *the same model id does not score the same everywhere*. For
capability claims, use each chapter's §N.19 verdict and run your own task-specific evals;
OpenRouter's one-key hot-swap (§8.19) and Bedrock's single Converse schema (§6.19) are
the documented cheap paths to A/B evaluation.

### 24.4 Local vs cloud decision factors
| Factor | Favors local (Ollama/HF self-host) | Favors cloud |
|---|---|---|
| Data control | Absolute — nothing leaves the host (§9.19 "privacy-constrained and offline") | ZDR/opt-out regimes exist but are contractual (§§3.17, 5.17, 8.17) |
| Capability ceiling | ~35B-class practical ceiling on workstation hardware; "trail current hosted frontier models" (§9.19) | Frontier models only exist hosted; giant open MoEs are "effectively Providers-only" (§10.19) |
| Cost shape | Fixed hardware, zero marginal (§9.19 "zero-cost experimentation") | Pure marginal, discounts via cache/batch |
| Throughput | 1–few users per box (§9.3 scheduler note); vLLM/SGLang for more | Elastic; rate-limit/quota governed |
| Compliance | No certifications to inherit (§9.17) — you own the audit | Bedrock/Azure inherit cloud cert portfolios (§§6.17, 7.17) |
| Ops burden | Model files, quant choice, CVE currency, port 11434 exposure risk (§9.17) | Key management, quota tiers, deprecation watch |

### 24.5 Compliance / enterprise (documented-only, per §N.17 of each chapter)
| Provider | Certifications (documented) | Uptime SLA (documented) | Data-usage default |
|---|---|---|---|
| OpenAI | SOC 2 T2 / CSA STAR / ISO 27001 historically claimed [UNVERIFIED at access] | None standard; **Scale Tier 99.9%** + latency commitments | No training by default; ZDR by approval |
| Gemini API | [UNVERIFIED — none documented for this API path; Vertex AI is the contractual surface] | None published | Paid: no training; **free tier trains + human review** |
| Anthropic | [UNVERIFIED — Trust Center not verified this pass] | Not verified | No training by default; 30-day deletion; ZDR by agreement |
| Bedrock | SOC 1/2/3, ISO 27001/17/18/9001, PCI DSS, HIPAA-eligible, FedRAMP High (GovCloud) | **99.9%** monthly (credit-tiered) | AWS platform terms; KMS/PrivateLink/CloudTrail |
| Azure | Azure portfolio: ISO 2700x, SOC 1/2/3, HIPAA BAA, FedRAMP High (Gov), EU Data Boundary | **99.9%** + PTU latency SLA (99% of 5-min windows) | Prompts not available to model providers; abuse review with opt-out |
| OpenRouter | [UNVERIFIED — none published] | None published | ZDR by default (no prompt logging unless opt-in); provider-level training toggles |
| Ollama | None (local runtime); Ollama Cloud: no certs published | None | Local: n/a; **no API auth — network exposure is on you** (§9.17) |
| Hugging Face | [UNVERIFIED — check trust.huggingface.co]; Enterprise support-SLA only | None published for Providers/Endpoints | Weights are yours when self-hosting; per-provider policies on Inference Providers |
**Shortlist for regulated workloads: Bedrock and Azure** — the only two with documented
certification scope *and* uptime SLA (§6.19, §7.19).

### 24.6 Region notes (chapter-documented)
- Bedrock: geo/global inference profiles enable residency-aware routing; **GPT-5.x is
  US-only** (us-east in-region, no cross-region profiles) (§6.3, §6.19); Claude on
  regional endpoints carries the 10% premium (§6.3); Nova 2 Lite has *no* single-region
  deployment (§6.3).
- Azure: EU/US data-zone processing; EU Data Boundary (§7.17, §7.19).
- Gemini API: no residency control — Vertex AI is the residency path (§4.19).
- Anthropic: data-residency billing multipliers exist (§5.3); Fable 5 availability is
  account-dependent (§5.3).
- OpenRouter: enterprise agreements offer regional routing (§8.17); per-request `zdr`
  and provider allow-lists constrain where prompts land (§8.17).
- Local (Ollama/HF self-host): residency is wherever the box is.

### 24.7 Open-weights vs closed
- Open-weight, current-generation, permissive: gpt-oss 20b/120b (Apache-2.0), Gemma 4
  (Apache-2.0 as of the 2026 release — §10.3), Muse Glimmer 30B (Apache-2.0), Qwen3.6-27B
  (Apache-2.0), DeepSeek V4 (MIT), GLM-5.2 (MIT), Phi-4 (MIT).
- Open-weight but license-encumbered: Qwen3.8-Max (custom license), Kimi K3 (custom),
  Mistral Medium 3.5 (modified MIT with revenue exception), FLUX.2-dev (non-commercial),
  Llama (Meta license). §10.19: "license heterogeneity … requires per-repo legal review."
- Closed frontier (API-only): GPT-5.x, Claude 5, Gemini 3.x, Grok, Nova. §3.19 lists "no
  current open-weight in catalog" as an OpenAI weakness *except* gpt-oss, which ships via
  Bedrock/Azure/Ollama/HF rather than the OpenAI API.
- Same open model, four consumption modes: e.g. gpt-oss-120b appears in the sidecars on
  Ollama (local), HF (self-host/Providers), Bedrock and Azure (managed), and OpenRouter
  ($0.03/$0.17 hosted) — pick by ops model, not by model.

---

## 25. Decision trees

### 25.1 General app default
```
START: general-purpose LLM feature, no hard constraints
│
├─ Need >200K context or heavy multimodal input?
│   ├─ YES ─ audio/video/PDF in? ── YES ─► gemini-3.7-flash (1M ctx, TIVAP-in, §4.19)
│   │                     └─ NO ──► claude-sonnet-5 (1M flat) or gpt-5.6-terra (1.05M)
│   └─ NO
│      ├─ Output must follow a strict JSON schema? ─ YES ─► claude-sonnet-5
│      │                                                    (grammar-backed SO, §5.19)
│      └─ NO ─► default trio, pick by ecosystem already in use:
│               gpt-5.6-terra ($1/$6) | claude-sonnet-5 ($2/$10) |
│               gemini-3.7-flash ($0.75/$3.75 promo)
│               └─ escalation path for hard cases: sol / opus-5 / gemini-3.1-pro
└─ Uncertain which? OpenRouter one-key A/B across all three (§8.19), then go direct.
```

### 25.2 Cost-sensitive high volume
```
START: millions of requests/day, cost dominates
│
├─ Task is simple (classify/route/extract/short summary)?
│   ├─ YES ─ latency-tolerant (async OK)?
│   │   ├─ YES ─► gpt-5.6-luna + Batch API + caching (=> $0.05/1M batched in, §3.19)
│   │   │         or gemini-2.5-flash-lite + batch (−50%)
│   │   └─ NO ──► nova-micro ($0.035/$0.14) | qwen3.7-flash via OR ($0.03/$0.13)
│   │             | haiku-4.5 if Claude-ecosystem (cache-aware rate limits, §5.19)
│   └─ NO (needs mid intelligence)
│       ├─ Open-weight acceptable? ─ YES ─► gpt-oss-120b via OR ($0.03/$0.17)
│       │                                   or minimax-m3 / glm-5.2 (verify listing, §23)
│       └─ NO ──► gemini-3.7-flash promo (re-price at 2026-12-31!) or gpt-5.6-terra
├─ Repeated system prompts/context? ► engineer caching FIRST (0.01×–0.25× reads)
│                                     — often beats switching models down a tier.
└─ NEVER: :free tiers in production (§26); watch OpenAI >272K surcharge (§3.19).
```

### 25.3 Privacy-constrained
```
START: data must not reach a third party / strict residency / no-training guarantees
│
├─ Data may not leave your infrastructure AT ALL?
│   ├─ YES ─ workstation/edge scale? ─► Ollama: qwen3.6:27b / gpt-oss:20b / gemma4
│   │        │                          (bind 127.0.0.1, raise num_ctx — §9.17/§9.3)
│   │        └─ server scale / multi-user? ─► self-host vLLM/SGLang with HF weights
│   │           (safetensors only, pin revisions — §10.17); TGI is archived (§10.18)
│   └─ NO, cloud OK with controls
│       ├─ Need certifications + SLA on paper?
│       │   ├─ AWS shop  ─► Bedrock (FedRAMP/HIPAA scope, geo profiles, KMS — §6.17)
│       │   └─ MS shop   ─► Azure (EU Data Boundary, no-provider-access terms — §7.17)
│       ├─ Contractual ZDR enough? ─► Anthropic ZDR / OpenAI ZDR (approval-gated)
│       └─ Aggregator? ─► OpenRouter ZDR routing + data_collection:"deny" (§8.17)
│                         — but no published certs (§8.17): fails formal audits.
└─ HARD AVOID: Gemini API free tier (trains + human review, §4.17); :free OpenRouter
  endpoints (provider may train, §8.17); any 0.0.0.0-exposed Ollama (§9.17).
```

### 25.4 Agentic coding
```
START: autonomous/semi-autonomous coding agent
│
├─ Hosted frontier quality required?
│   ├─ Max capability ──► gpt-5.3-codex (purpose-built, $1.75/$14, §3.3)
│   │                     or claude-opus-5 (richest tool stack + Agent SDK/MCP, §5.19)
│   ├─ Cost-balanced ──► claude-sonnet-5 | gemini-3.7-flash ("complex coding and
│   │                    agentic workflows", §4.3)
│   └─ Enterprise runtime needed? ─► Azure Agent Service (MCP+A2A, Entra per-agent
│                                    identity, §7.19) or AWS AgentCore (§6.19)
├─ Local-only?
│   ├─ 24–32 GB VRAM ─► qwen3-coder:30b (coding) + muse-glimmer (agent loop control)
│   └─ 16 GB ────────► gpt-oss:20b — accept: "trail current hosted frontier" (§9.19)
├─ Long-horizon tasks: budget for 400K–1M context; hold cache breakpoints stable
│  (effort changes invalidate Anthropic caches, §5.18).
└─ AVOID: sub-9B local tags for multi-step agent chains (§26); Bedrock Sonnet-5 if the
  agent depends on structured outputs (absent on runtime, §6.3).
```

---

## 26. Avoid-lists (evidence-based)

### 26.1 Dead or dying — do not build new work on these
| Item | Evidence / date |
|---|---|
| OpenAI **Assistants API** | Shutdown **2026-08-26** — 12 days after access date (§3.18/§3.19). Migrate to Responses + Conversations. |
| OpenAI `sora-2` / Videos API | API shuts down **2026-09-24**, "none listed" as replacement (§3.18). |
| **Imagen 4** (Gemini API) | Shutdown **2026-08-17** — 3 days after access date (§4.18). Migrate to Nano Banana line. |
| **Nova gen-1** (Bedrock) | Premier EOL 2026-09-14; Canvas/Reel/Sonic-gen1 EOL 2026-09-30 (third-party-sourced dates — verify per model card, §6.18). |
| `gpt-3.5-turbo`, `gpt-4-0613`, `o1`, `gpt-5-2025-08-07` line, `o3` | Staged shutdowns 2026-10-23 / 2026-12-11 (§3.18). |
| Gemini 2.0 family, `gemini-3-pro-preview` | Already shut down (§4.18) — preview IDs churn. |
| Retired Claudes (opus-4/4.1, sonnet-4, 3.x era) | Requests fail (§5.18); `claude-sonnet-4-5` retirement floor 2026-09-29 — imminent. |
| HF **TGI** | Repo archived 2026-03-21 (§10.18) — deploy vLLM/SGLang instead. |
| Azure **PromptFlow**, dated `api-version` scheme, Assistants preview | Deprecated; migrate to Framework Workflows / v1 URL / Responses (§7.18). |
| Ollama `/api/embeddings` (old form), llama2/3, gemma3, phi3, llava tags | Superseded (§9.18) — soft-deprecated but stale ≥1 year. |

### 26.2 Fine-tuning wind-downs — avoid FT-dependent product plans
- OpenAI: "platform winding down, no 5.6 FT" (§3.19) — fine-tuning-dependent products
  are on the explicit avoid list.
- Gemini API: fine-tuning "not available on this API at all" (§4.19); 1.5-era tunes
  deleted since 2025-05 (§4.18).
- Anthropic: "no self-serve fine-tuning" (§5.19).
- Bedrock: no FT for frontier models — only Nova/Llama/open-weights customization (§6.19).
- Remaining documented FT paths: Bedrock Llama 3.x, Azure gpt-oss-20b SFT (preview),
  and self-service tuning of open weights (HF/Ollama ecosystem).

### 26.3 Production hazards (works in demo, fails at scale)
| Avoid | Why (evidence) |
|---|---|
| OpenRouter `:free` variants in production | Free-tier rate floors are prototyping-grade (§8.19 "prototyping on :free tiers"); endpoints typically served "under provider terms allowing data use" (§8.17). |
| `openrouter/auto` / `*-latest` aliases where outputs must be stable | §8.18: avoid evergreen aliases for reproducibility; auto row: "avoid: reproducibility, strict output stability". |
| Preview-tagged models for pinned production (Azure, Gemini) | Auto-upgrade / churn: §7.3 ("not for production pinning"), §4.19 (two 3.x preview IDs already shut down). Gemini's *flagship* Pro tier is preview-only — plan for ID churn. |
| Ollama defaults for long-context work | 4096-token default context regardless of model (§9.3); default ~4-bit quants cost accuracy on hard reasoning. |
| Non-default `temperature`/`top_p`/`top_k` on Claude 4.7+/5 | Returns **400** (§5.3). Also: manual thinking mode 400s on Opus 4.6+/Sonnet 4.7+. |
| Assuming feature parity across platforms | Bedrock: "no structured outputs on Sonnet 5 runtime or GPT-5.6"; "every capability must be checked per model card, per region" (§6.19). OpenRouter: `supported_parameters` is the truth source (§8.3). HF Providers: per-provider tool/JSON/context variance (§10.19). |
| Azure for ungated content or day-zero parity | Default content filters "add refusals and latency"; "identical models can refuse/400 differently on Azure" (§7.17/§7.19); price/feature lag vs OpenAI direct. |
| GPT-5.6 on Azure without quota planning | Default quota only for tenant Tiers 5–6 (§7.3). |
| Gemini free tier for sensitive data | Inputs used for product improvement, human review possible (§4.17). |
| Exposed Ollama hosts | No API auth by design; historical mass exposure + pull-path CVEs (§9.17). |
| `trust_remote_code=True` / pickle checkpoints (HF) | Arbitrary code execution at load; prefer safetensors, pin revisions (§10.17). |

### 26.4 Capability mismatches
- **Local small models (≤9B) for complex agentic work**: §9.3 — smallest Qwen tags
  "hallucinate heavily on factual queries"; §9.19 — even the best ~35B locals "trail
  current hosted frontier models". Use them for routing/edge, not multi-step autonomy.
- **Gemini image models inside agent loops**: no function calling / structured outputs
  (§4.3, §4.19).
- **GPT-5.6 / Claude for audio output**: not supported — separate audio models (§3.19,
  §5.19). Anthropic for anything embeddings/speech/image-gen: none offered (§5.19).
- **`gpt-5.6-luna` for hardest reasoning**: sidecar avoid_for; nano-tier positioning.
- **Fable 5 / Mythos 5 for budget work**: $10/$50, limited availability (§5.19).
- **DeepSeek-R1 distills as current reasoners**: ~1.5 generations old, verbose thinking
  inflates latency/KV (§9.3).
- **OpenRouter for embeddings or lab-beta features**: none/unavailable (§8.19).
- **Jamba 1.5, Command R/R+**: maintenance-mode/Legacy on Bedrock (§6.3, §6.18).

---

## 27. Scorecards & tradeoffs

Axes (1–5, **[judgment call]** syntheses of chapter evidence): **Cap** = capability
ceiling of best available model; **Cost** = cost floor quality (5 = excellent cheap
options); **Open** = openness (open weights, portability, exit cost); **Ops** = ops
simplicity (5 = one key and go); **Eco** = ecosystem breadth (modalities, tooling,
agent/RAG surface).

**OpenAI** — Highest documented capability ceiling of the pure labs (Sol, 5.3-codex,
Realtime GA, gpt-image-2) with an unusually deep price ladder (1M context even at Luna's
$0.10 tier) and aggressive batch/cache economics. Costs: fine-tuning winding down,
Assistants API dying, video API dying, no open weights in its own catalog, no standard
SLA without Scale Tier. (§3.19)
```
Cap  ##### 5  Sol/codex frontier line, "most capable agentic coding" claim
Cost ####- 4  Luna $0.05 batched-in/1M; but >272K & fast-mode multipliers
Open #---- 1  no open weights in own catalog (gpt-oss ships elsewhere)
Ops  ####- 4  one key; Responses migration churn deducts one
Eco  ##### 5  text/image/audio/realtime/embeddings/moderation in one API
```

**Google Gemini API** — The multimodal price/performance play: every reasoning model
takes 1M tokens of text+image+video+audio+PDF, and the flash tier undercuts peers with
stacking batch/cache discounts; only provider with integrated image+video+TTS+music
generation behind one key. Costs: flagship Pro is preview-only with ID churn, no
fine-tuning, no SLA/residency on this path, free tier trains on your data. (§4.19)
```
Cap  ####- 4  3.1-pro competitive but preview-only; flash line strong
Cost ##### 5  $0.10 flash-lite; promo 3.7-flash; −50% batch + ~90% cache
Open ##--- 2  Gemma 4 open weights adjacent; core models closed
Ops  ####- 4  one key + generous free tier; preview churn deducts
Eco  ##### 5  widest modality coverage in the suite (in AND out)
```

**Anthropic** — The agent/tool-use specialist: richest server-tool set, MCP/Agent-SDK
origin, grammar-backed structured outputs, 1M context at flat Sonnet pricing, and the
strongest documented cost-engineering combo (0.1× cache reads + 50% batch +
cache-aware rate limits). Costs: text(+image-in) only — no embeddings, speech, or media
generation; no fine-tuning; sampling knobs removed on 4.7+; top tier is expensive and
availability-gated. (§5.19)
```
Cap  ##### 5  Opus/Fable 5 frontier reasoning + best-documented tool stack
Cost ###-- 3  Sonnet $2/$10 anchor is fair, not cheap; Haiku 200K-limited
Open #---- 1  fully closed; no weights, no FT
Ops  ####- 4  clean single API; 4.7+ breaking changes (400s) deduct
Eco  ##--- 2  no embeddings/audio/image — must pair providers
```

**AWS Bedrock** — The governance umbrella: frontier Claude + GPT-5.6 + Llama + Nova
under existing IAM/VPC/CloudTrail, with certifications (FedRAMP High, HIPAA scope),
99.9% SLA, geo-residency profiles, and multi-vendor A/B through one Converse schema.
Costs: feature lag is structural (no SO on Sonnet-5 runtime/GPT-5.6; per-model per-region
matrices), GPT-5.x is US-only mantle-only, frontier FT absent. (§6.19)
```
Cap  ####- 4  frontier models present, but day-zero features lag natively
Cost ####- 4  nova-micro $0.035; Flex/batch/geo tiers; 10% regional premium
Open ###-- 3  broad open-weight lineup (Llama/DeepSeek/Qwen/gpt-oss) hosted
Ops  ###-- 3  IAM/SigV4 overhead, mitigated by API keys + mantle
Eco  ##### 5  agents (AgentCore), KBs, Guardrails, multi-vendor catalog
```

**Azure AI Foundry** — OpenAI's line under enterprise controls: the only surveyed
provider with both a 99.9% uptime SLA *and* a provisioned-throughput latency SLA, plus
EU Data Boundary, Entra/RBAC, the most complete managed agent runtime, and hybrid/edge
SLM story (Phi + Foundry Local). Costs: price/feature lag vs OpenAI direct (Luna ~5×
until cuts land), content-filter behavioral deltas, heavyweight quota machinery,
partner-tier-only Anthropic. (§7.19)
```
Cap  ##### 5  full GPT-5.6/codex/realtime/Sora line + DeepSeek/Grok
Cost ###-- 3  documented lag on OpenAI's 2026-07 cuts; PTU commitments
Open ###-- 3  Phi (MIT) + gpt-oss + Llama on managed compute/Foundry Local
Ops  ##--- 2  resource/deployment/quota-tier machinery is heavyweight
Eco  ##### 5  Agent Service (MCP+A2A), Speech, M365 distribution
```

**OpenRouter** — The routing/insurance layer: one key over the whole market, same-day
new-model listings, provider fallback that beats any single lab's uptime, ZDR-by-default
privacy posture, `:floor` price routing. Costs: no embeddings, no lab-beta features, an
extra latency hop, no published certifications, and listed prices can lag lab changes in
both directions — you are billed the listing. (§8.19)
```
Cap  ####- 4  everything listed same-day, minus lab-native beta features
Cost ##### 5  :floor routing, $0.03 open-weight tiers, :free prototyping
Open ####- 4  deepest hosted open-weight market; itself closed infra
Ops  ##### 5  one key, OpenAI-compatible, hot-swap strings
Eco  ###-- 3  text-completion-centric; no embeddings/media APIs
```

**Ollama** — The local default: zero marginal cost, absolute data control, OpenAI/
Anthropic-compatible endpoints, and a current open-weight lineup (qwen3.5/3.6, gemma4,
muse-glimmer, gpt-oss) that covers 16–32 GB machines well. Costs: frontier gap is real,
4096-token default context is a standing trap, single-box scheduler, no auth, no
compliance story. (§9.19)
```
Cap  ##--- 2  ~35B practical ceiling "trails hosted frontier" (§9.19)
Cost ##### 5  hardware-only cost; free experimentation
Open ##### 5  entirely open weights, offline, no vendor dependency
Ops  ####- 4  one-command pull/run; num_ctx & quant tuning deduct
Eco  ###-- 3  text/vision/embeddings local; no audio/video gen, low QPS
```

**Hugging Face** — The open-weight frontier gateway: 2.4T-param Qwen, DeepSeek V4, Kimi
K3, GLM-5.2 behind one token with zero markup and provider failover, plus TEI for
embeddings, cheap dedicated GPU serving, and full self-host exit. Costs: no proprietary
frontier models, no HF-side SLA, per-provider feature variance, license heterogeneity,
pickle/`trust_remote_code` hygiene burden. (§10.19)
```
Cap  ####- 4  entire open frontier (1M-ctx MoEs); no GPT/Claude/Gemini
Cost ####- 4  zero-markup Providers, L4 at $0.80/h, ZeroGPU demos
Open ##### 5  weights are yours; the definitional open platform
Ops  ###-- 3  router simple; self-host/licensing/security discipline needed
Eco  ####- 4  embeddings/vision/audio/video open models + Spaces/TEI
```

---

## 28. Migration & versioning strategy

### 28.1 Pinning vs aliases — per provider
| Provider | Alias scheme (documented) | Pin-or-alias recommendation |
|---|---|---|
| OpenAI | `gpt-5.6` alias → Sol; `chat-latest`, `daybreak-*-latest` evergreen; dated snapshots exist for older lines | Pin dated snapshots for reproducibility; aliases only where silent upgrades are acceptable. `-latest` families are explicitly continuously updated. |
| Gemini | Stable ids (`gemini-3.7-flash`) vs `-preview` ids | Never ship `-preview` ids in pinned production (§4.19 — two 3.x preview ids already shut down); stable ids still deprecate as generations roll (2.0 gone). |
| Anthropic | 5-era ids dropped date suffixes (`claude-opus-5`); 4.x era used dated ids (`claude-haiku-4-5-20251001`) | Ids are effectively pins with published retirement floors (§5.18: Opus 5 ≥2027-07-24). Track the floors; ≥60-day notice policy documented. |
| Bedrock | "Model IDs are immutable; upgrades are explicit ID swaps" (§6.18); inference profiles add geo/global indirection | Safest pinning story of the surveyed platforms; put the profile ARN, not just the model id, in config. |
| Azure | Deployment-name indirection: your app calls *your deployment*, which maps to model+version; preview models auto-upgrade | Use deployment names as the stable handle; avoid preview models for pinned workloads (§7.18). Migrate dated `api-version` clients to the v1 surface. |
| OpenRouter | Evergreen slugs, `:free`/`:floor`/`:batch` suffixes, `canonical_slug` dated variants, `models` fallback arrays, `expiration_date` field | Pin `canonical_slug`-style dated variants (e.g. `deepseek-v4-pro-0813`) for reproducibility (§8.18); watch `expiration_date` for scheduled removals. |
| Ollama | Mutable tags (`qwen3.6` moves); content-addressed digests | Pin SHA256 digests for production (§9.17); registry keeps old blobs, so rollback is cheap — but cloud tags hard-retire (§9.18). |
| Hugging Face | Repo revisions (git) | Pin `revision="<commit-sha>"` (§10.17) — the hub never deletes repos (§10.18), making HF the strongest long-term reproducibility anchor. |

### 28.2 Deprecation-watch practice
The access-date snapshot alone contained four shutdowns within ~6 weeks (Assistants API
2026-08-26, Imagen 4 2026-08-17, Nova gen-1 September, sora-2 API 2026-09-24). Treat
deprecation-watch as an operational task, not an annual review:
1. Subscribe/poll each provider's deprecations page (OpenAI `/docs/deprecations`,
   Anthropic model-deprecations, Bedrock model-lifecycle/model cards, Azure model
   retirements page, Gemini models page) — monthly minimum, before each release train.
2. Alert on **announced dates**, not on breakage: chapters show 60-day (Anthropic
   policy) to multi-month windows; Bedrock EOL dates in this suite are partly
   third-party-sourced and must be confirmed on model cards (§6.18).
3. Keep the sidecars fresh and re-run `scripts/build_matrix.py --check` — a diff in row
   counts or confidence grades is your earliest local signal.
4. Test successor models *before* the shutdown date using the documented mappings
   (§3.18, §4.18, §5.18, §6.18 tables map every legacy id to a successor).

### 28.3 The config-not-code rule
Model names, effort/thinking parameters, and per-model token budgets belong in
configuration (env vars / config service), never in code paths. Chapter evidence for why:
- Swaps are forced on you: retired Claude ids **fail hard** (§5.18); Gemini preview ids
  vanish (§4.18); OpenAI staged shutdowns land mid-lifecycle (§3.18).
- Model changes ripple into non-name parameters: Claude 4.7+ rejects sampling params and
  manual thinking with 400s (§5.3); `gpt-5.1+` defaults `reasoning_effort` to `none`
  and rejects `temperature` (§7.3); Anthropic effort changes invalidate prompt-cache
  breakpoints (§5.18); the 4.7+ tokenizer re-bases token budgets by ~30% (§5.3).
  A model swap is therefore a *config bundle* swap (name + params + budgets), which is
  only atomic if it lives in config.
- Cross-ref Part III §11: env-config plus thin adapters is the pattern that makes this
  rule executable.

### 28.4 Multi-provider abstraction as insurance (cross-ref Part III §11)
- Minimum viable insurance: OpenAI-compatible wire format is already the lingua franca —
  Bedrock mantle serves GPT-5.x on the Responses API (§6.3), OpenRouter and HF's router
  are OpenAI-compatible (§8.7, §10.19), Ollama exposes OpenAI/Anthropic-compatible
  endpoints (§9.19), Azure moved to plain `OpenAI()` clients on the v1 URL (§7.18).
  A thin adapter over that shape (Part III §11) covers 6 of 8 providers.
- Managed insurance: OpenRouter fallback arrays ("multi-provider fallback beats any
  single lab's uptime", §8.19) or Bedrock's one-Converse-schema multi-vendor A/B (§6.19).
- What abstraction does **not** cover — plan provider-specific seams for: Anthropic
  thinking/cache semantics (§5.3), Gemini thought-signature round-tripping (§4.3),
  lab-native betas absent on aggregators (§8.3), per-platform feature matrices
  (§6.19), and OpenRouter-specific request fields you may come to depend on (§8.18).
- Exit-cost asymmetry worth engineering for: migrating OpenRouter→direct-lab is "low-cost
  by design" (§8.18); migrating off Azure deployment-name indirection or Bedrock IAM
  integration is not. If lock-in risk matters, keep the provider-specific layer thin and
  owned by you — that is the Part III §11 blueprint's core argument.

---

*End of Part IV. Generated tables: re-run `python3 scripts/build_matrix.py` after any
sidecar change. All suitability claims trace to Part II chapter sections cited inline;
unlabeled rankings are by published price only; capability orderings without chapter
evidence are marked [judgment call].*


---


# Appendix B — Master Source Register

Every provider chapter ends with its own Sources section (official URLs + access date 2026-08-14); those
per-chapter registers are authoritative. Primary roots: platform.openai.com/docs · ai.google.dev/gemini-api
/docs · platform.claude.com / docs.claude.com · docs.aws.amazon.com/bedrock · learn.microsoft.com (AI
Foundry) · openrouter.ai/docs · docs.ollama.com + github.com/ollama/ollama · huggingface.co/docs.
Cross-part claims cite chapters as "ch. N §N.x" and inherit those sources.

# Appendix C — Glossary

Context window: max input tokens per request. Output limit: max tokens generated per response. Tool use /
function calling: model emits structured calls your code executes. Structured output: schema-constrained
generation (JSON schema). Prompt/context caching: discounted reuse of repeated prompt prefixes. Batch API:
async bulk processing at discount. Embedding: vector representation for retrieval/similarity. RAG:
retrieval-augmented generation. MCP: Model Context Protocol — open standard connecting models to tools/data.
Quantization: reduced-precision weights for local inference (e.g. Q4). TGI/TEI: Hugging Face text
generation / embedding inference servers. PTU: Azure provisioned throughput unit. Inference profile:
Bedrock routing construct for cross-region capacity. BYOK: bring-your-own-key routing (OpenRouter). ZDR:
zero-data-retention routing. Open weights: downloadable model weights (license still applies).
