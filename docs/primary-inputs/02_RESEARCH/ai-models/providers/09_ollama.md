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
