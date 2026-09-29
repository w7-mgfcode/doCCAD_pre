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
