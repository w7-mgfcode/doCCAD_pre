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
