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
