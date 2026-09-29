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
