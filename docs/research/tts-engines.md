# TTS engines that sound natural (ElevenLabs level) - research, 2026-10-04

Question: which text-to-speech engines sound as natural as elevenlabs.io today, and which one is the
best upgrade from Piper (`en_US-lessac-medium`) for the `explainer-video` skill (60-120 s English
narration, text in, WAV out, one call per scene, Windows/macOS/Linux, no API key today)?

All figures were read on **2026-10-04**. Prices and leaderboards change; re-read before deciding.

How the evidence was read: leaderboard rows from TTS Arena V2, and release/licence data from PyPI,
GitHub and Hugging Face, were read straight from their JSON APIs. Vendor pricing and docs pages
were read through a page-summarising fetch tool, so individual numbers from those pages can be
misread; where a number looked wrong it is listed under "Could not verify".

## Short answer

**Hosted, most natural (blind preference, Artificial Analysis Speech Arena [AA]):**

1. **ElevenLabs Eleven v4** - Elo 1321, rank 1. Still the baseline to beat. $0.08 / 1K characters list.
2. **Cartesia Sonic 3.6** - Elo 1278. Supports Norwegian. From $5/month.
3. **Google Gemini 3.8 Flash TTS** - Elo 1275. Has a free tier, returns WAV directly, supports
   Norwegian Bokmal and Nynorsk. Best value of the top group.
4. Also in the top group: Alibaba Qwen-Audio-3.1-TTS-Plus (1292), Inworld Realtime TTS-2 (1251).

Sonic 3.6 and Gemini 3.8 Flash overlap in their 95 % intervals; Eleven v4 is clear of both.

**Local / open weights:** nothing that runs on a normal developer machine with a licence that allows
commercial use reaches Eleven v4. The realistic picks:

1. **Kokoro-82M** (Apache-2.0, CPU, 82M parameters) - about level with ElevenLabs' *previous*
   generation (Multilingual v2 / Turbo v2.5) on both leaderboards, far behind Eleven v4.
2. **Chatterbox** (MIT; Turbo 350M, Nano 110M for CPU) - same band as Kokoro on TTS Arena V2;
   heavier (PyTorch), needs a reference voice clip, watermarks its output.
3. **Pocket TTS** (Kyutai; MIT code, CC-BY-4.0 weights, 100M, CPU) - alive and easy to install, but
   no blind-preference evidence found.

The open-weight models that score higher (Breeze TTS 2, Fish Audio S2 Pro, Voxtral TTS, Higgs Audio
v3) all have **non-commercial weights** and need a 12-16 GB+ GPU.

**Best fit for explainer-video as a drop-in upgrade from Piper: Kokoro via `kokoro-onnx`.**
It keeps every property the skill has now - local, no API key, CPU-only, `pip install`, text in and
WAV out, permissive licence, Python 3.10-3.13 - and it is the highest-ranked open model that does.
Be honest about the ceiling: it is "ElevenLabs 2024", not "ElevenLabs today". If the user wants
today's ElevenLabs level, that requires a hosted API and a key; the cheapest good one is Gemini 3.8
Flash TTS (free tier), and Eleven v4 is the top. A 90 s narration is about 1,400 characters, so the
hosted cost is cents per video (about $0.11 on Eleven v4 at list price); the real cost is the API
key, not the money.

Neither leaderboard includes Piper, so "how much better than Piper" is not measured anywhere I
found - listen to samples before switching.

## How to read the leaderboards

- **Artificial Analysis Speech Arena [AA]**: Elo from blind pairwise votes on "which sounds more
  natural". 93 models. Covers ElevenLabs v4, Gemini, OpenAI, Azure, Polly and open weights.
  Elo gap to expected preference: 33 points is about 55/45; 257 points (Eleven v4 vs Kokoro) is
  about 81/19.
- **TTS Arena V2 [TA]** (Hugging Face, TTS-AGI): same method, 39 models, fewer votes (250-2,000 per
  model), uncertainty 19-47 Elo. Does **not** include Eleven v4, Gemini, OpenAI, Azure or Polly.
  One model (Vocu V3.0) is suspended for "vote manipulation" - the arena is gameable, so treat small
  gaps as noise.
- The two arenas use different scales (AA anchors Zonos at 1000; TA sits around 1500). Compare
  within one arena only.

## Comparison: hosted APIs

AA Elo with 95 % interval. Price is the vendor's list price where I could read it; "AA:" marks a
price taken from the AA table instead.

| Engine | AA Elo (95 %) | TA Elo | Price | Free tier | Norwegian | Call |
|---|---|---|---|---|---|---|
| ElevenLabs Eleven v4 | 1321 (1303-1339) | not listed | $0.08 / 1K chars (promo $0.022 to Oct 12) | 10K credits/mo, no commercial use | unverified for v4 (yes for Flash v2.5) | REST, `elevenlabs` |
| Alibaba Qwen-Audio-3.1-TTS-Plus | 1292 (1274-1310) | not listed | AA: $19.3 / 1M | not checked | not checked | REST (not checked) |
| Cartesia Sonic 3.6 | 1278 (1262-1294) | Sonic 2: 1514 | $5/mo = 100K chars; AA: $49 / 1M | 20K chars/mo, no commercial use | yes | REST, `cartesia` |
| Google Gemini 3.8 Flash TTS | 1275 (1259-1291) | not listed | $0.50 in / $9 audio-out per 1M tokens (doubles 2027-01-01); AA: $16.5 / 1M chars | yes | yes (nb, nn) | REST, `google-genai` |
| Inworld Realtime TTS-2 | 1251 (1235-1267) | TTS MAX: 1557 | $25 / 1M chars on-demand | "up to 70 min TTS" | not checked | REST |
| Speechify Simba 3.2 | 1242 (1229-1255) | not listed | AA: $6.6 / 1M | not verified | not checked | REST |
| Gemini 3.8 Flash-Lite TTS | 1242 (1227-1257) | not listed | $0.50 in / $6 out per 1M tokens | yes | yes | as above |
| ElevenLabs Eleven v3 | 1174 (1163-1185) | 1502 +-32 | $0.08 / 1K chars | as above | unverified | as above |
| MiniMax Speech 2.8 HD | 1173 (1162-1184) | 1539 +-33 | AA: $100 / 1M | not checked | not checked | REST |
| Azure HD 2.5 (Dragon HD) | 1131 (1119-1143) | not listed | AA: $22 / 1M (vendor page unreadable) | 0.5M chars/mo | not in the Dragon HD voice list | REST, Speech SDK |
| OpenAI TTS-1 HD | 1103 (1091-1115) | not listed | $30 / 1M chars | none | yes (follows Whisper languages) | REST, `openai` |
| ElevenLabs Multilingual v2 | 1097 (1087-1107) | 1507 +-24 | $0.08 / 1K chars | as above | unverified | as above |
| OpenAI TTS-1 | 1090 (1079-1101) | not listed | $15 / 1M chars | none | yes | as above |
| ElevenLabs Flash v2.5 | 1078 (1067-1089) | 1509 +-21 | $0.04 / 1K chars | as above | yes | as above |
| Amazon Polly Generative | 1065 (1053-1077) | not listed | $30 / 1M chars | 100K chars/mo, first 12 months | not checked | REST, `boto3` |
| Hume Octave 2 | 1051 (1039-1063) | Octave: 1525 +-22 | $70/mo = 1M chars (first plan with commercial licence) | 10K chars/mo, no commercial use | not checked | REST, `hume` |
| Azure Neural (standard) | 1035 (1016-1054) | not listed | AA: $15 / 1M | 0.5M chars/mo | yes (nb-NO voices exist; not re-checked) | as above |
| Deepgram Aura-2 / Flux TTS | not listed | not listed | $0.030 / $0.045 per 1K chars | not checked | not checked | REST |
| OpenAI gpt-4o-mini-tts | not listed | not listed | $0.60 in / $12 out (unit unclear) | none | yes | as above |
| PlayHT | - | - | shut down | - | - | - |

All hosted APIs need an API key and work from any OS (HTTPS). All of them beat or match every
permissively licensed local model on AA from Azure HD 2.5 upward.

## Comparison: local / open weights

Sorted by AA Elo. "Commercial" refers to the weights licence.

| Model | AA Elo | TA Elo | Size | Hardware | Code / weights licence | Commercial | Install | Alive? |
|---|---|---|---|---|---|---|---|---|
| Breeze TTS 2 | 1216 | - | 3B | NVIDIA GPU >= 12 GB, Linux | Apache-2.0 / BreezeBlue research & non-commercial | no | clone repo | released 2026-08-25 |
| Fish Audio S2 Pro | 1117 | hosted S2: 1519 | ~5B | large GPU (figures given for H200) | Fish Audio Research License (both) | no | repo, SGLang | pushed 2026-09-16 |
| Voxtral TTS (Mistral) | 1083 | - | 4B | GPU >= 16 GB | CC-BY-NC-4.0 weights | no | vLLM-Omni server | card 2026-03-31 |
| NVIDIA Magpie Multilingual 357M | 1065 | 1405 +-28 | 357M | not checked | NVIDIA Open Model License | not checked | NeMo | card 2026-09-09 |
| **Kokoro-82M v1.0** | **1064** | **1477 +-24** | 82M | **CPU ok** | Apache-2.0 / Apache-2.0 | **yes** | `pip install kokoro-onnx` | wrapper 0.6.1, 2026-08-19; model unchanged since 2025-01 |
| Maya1 | 1049 | 1410 +-38 | not checked | not checked | Apache-2.0 | yes | not checked | card 2026-07-11 |
| Higgs Audio v3 | 1038 | - | 4B | GPU | Apache-2.0 / research & non-commercial | no | SGLang-Omni | pushed 2026-06-05 |
| **Chatterbox** (Resemble AI) | 1025 | **1480 +-19** | 500M; Turbo 350M; Nano 110M | GPU recommended; Nano: CPU | MIT / MIT | **yes** | `pip install chatterbox-tts` | 0.1.7, 2026-03-26; pushed 2026-07-21 |
| Zonos v0.1 | 1000 | - | not checked | GPU | Apache-2.0 | yes | repo | stale: last push 2025-03-05 |
| VibeVoice 1.5B (Microsoft) | 957 | - | 1.5B | GPU | MIT | research only per README | TTS code removed from repo | TTS abandoned; repo now ASR |
| XTTS v2 (Coqui) | 916 | - | not checked | GPU recommended | MPL-2.0 / Coqui Public Model License | no | `pip install coqui-tts` (Idiap fork) | fork alive (0.27.5, 2026-01-26); model frozen 2023 |
| StyleTTS 2 | 895 | - | not checked | GPU | MIT | pretrained-voice terms not checked | repo | stale: last push 2024-08-10 |
| Pocket TTS (Kyutai) | - | - | 100M | **CPU ok**, 2 cores | MIT / CC-BY-4.0 | **yes, with attribution** | `pip install pocket-tts` | 3.3.0, 2026-09-24 |
| Qwen3-TTS | hosted variants: 932-944 | - | 0.6B / 1.7B | GPU | Apache-2.0 / Apache-2.0 | yes | `pip install qwen-tts` | 0.1.1, 2026-02-06 |
| KittenTTS | - | - | 15-80M ONNX; v2 1.7B | CPU ok (small models) | Apache-2.0 / v2: Stellon Labs Community License | not checked | `pip install kittenml` (per README) | pushed 2026-10-03 |
| F5-TTS | - | - | not checked | GPU | MIT / CC-BY-NC-4.0 | no | `pip install f5-tts` | 1.1.22, 2026-07-23 |
| IndexTTS 2.5 | - | - | not checked | GPU | bilibili Model Use License | contact vendor | `uv sync` | pushed 2026-09-29 |
| Orpheus 3B | - | - | 3B | GPU | Apache-2.0 | yes | `orpheus-speech` | stale: pip 2025-03, push 2025-12 |
| Dia 1.6B / Dia2 | - | - | 1.6B / 2B | GPU | Apache-2.0 | yes | repo | stale: last push 2025-11 |
| Sesame CSM-1B | - | - | 1B | GPU | Apache-2.0 | yes | repo | stale: last push 2025-05-27 |
| Parler-TTS | - | - | not checked | GPU | Apache-2.0 | yes | `parler-tts` | stale: last push 2024-12-10 |
| Supertonic 3 | - | - | small ONNX | CPU ok | MIT / OpenRAIL-M | yes with use restrictions | `pip install supertonic` | **archived 2026-09-09** |
| Piper (current) | - | - | small ONNX | CPU ok | GPL-3.0 (piper1-gpl) / per-voice | per voice | `pip install piper-tts` | 1.8.0, 2026-09-04 |

Where the local models sit against ElevenLabs:

- AA: Kokoro 1064 vs Eleven Multilingual v2 1097, Flash v2.5 1078, Turbo v2.5 1098, **v3 1174, v4 1321**.
- TA: Kokoro 1477 +-24 and Chatterbox 1480 +-19 vs Eleven Multilingual v2 1507 +-24, v3 1502 +-32,
  Flash v2.5 1509 +-21. That is a 25-30 Elo gap with overlapping uncertainty.
- So: Kokoro and Chatterbox are roughly at the level of ElevenLabs' older models, and clearly below
  the current one. No local model on either board is above Eleven v3 except Breeze TTS 2 on AA.

## Per-engine notes: hosted

**ElevenLabs** (baseline). Models: `eleven_v4` (flagship, 90+ languages, 10,000-character limit),
`eleven_v4_turbo`, `eleven_v3`, `eleven_v3_conversational`, `eleven_multilingual_v2`,
`eleven_flash_v2_5`; Turbo v2/v2.5 deprecated in favour of Flash.
API prices per 1K characters: v4 $0.08 (promo $0.022 "through Oct 12"), v4 Turbo $0.04, v3 $0.08,
Multilingual v2 $0.08, Flash $0.04. Plans: Starter $6/month, Creator $22, Pro $99. Free plan: 10,000
credits/month, no commercial use. Output formats listed: MP3, PCM (S16LE), mu-law, A-law, Opus - no
WAV container listed, so PCM would need a header written with the stdlib `wave` module. Python SDK
`elevenlabs` 2.70.0 (2026-09-28), MIT.
Sources: https://elevenlabs.io/docs/overview/models ,
https://elevenlabs.io/pricing/api , https://elevenlabs.io/pricing ,
https://elevenlabs.io/docs/overview/capabilities/text-to-speech , https://pypi.org/project/elevenlabs/

**Cartesia Sonic.** `sonic-3.6` is the current GA model (snapshot `sonic-3.6-2026-08-27`); 44
languages including Norwegian. 1 credit = 1 character. Free: 20K credits/month, no commercial
licence. Pro $5/month for 100K credits with commercial licence; Startup $49 for 1.25M. Python SDK
`cartesia` 4.2.0 (2026-09-02), Apache-2.0.
Sources: https://docs.cartesia.ai/build-with-cartesia/tts-models/latest , https://cartesia.ai/pricing

**Google Gemini TTS.** `gemini-3.8-flash-tts` and `gemini-3.8-flash-lite-tts`; 30 curated voices
plus an extended library; "over 130 languages" including Norwegian Bokmal and Nynorsk. Non-streaming
requests return WAV (24 kHz, mono, 16-bit) by default - the closest hosted match to the skill's
"text in, WAV out". Paid price: $0.50 input and $9.00 audio output per 1M tokens for Flash ($6.00
for Flash-Lite), rising to $1.00 / $18.00 ($12.00) on 2027-01-01. Free tier exists. Python SDK
`google-genai` 2.28.0 (2026-10-02), Apache-2.0. Older Google Cloud voices rank low on AA (Chirp 3 HD
1056, Studio 1079, Neural2 895, WaveNet 918).
Sources: https://ai.google.dev/gemini-api/docs/speech-generation ,
https://ai.google.dev/gemini-api/docs/pricing

**OpenAI.** Models `gpt-4o-mini-tts` (13 voices), `tts-1`, `tts-1-hd`. WAV output supported.
Languages follow Whisper, which includes Norwegian. Usage policy requires disclosing to listeners
that the voice is AI-generated. Prices: tts-1 $15 and tts-1-hd $30 per 1M characters. On AA the
older models sit mid-table (1103 / 1090), well below the top group; gpt-4o-mini-tts is not on the AA
table I read. Python SDK `openai` 3.24.0 (2026-10-02).
Sources: https://developers.openai.com/api/docs/guides/text-to-speech ,
https://developers.openai.com/api/docs/pricing

**Azure Speech.** HD voices: DragonHD (30+ tuned voices, mostly en-US, plus de/es/fr/ja/zh),
Dragon HD Omni (700+ voices, multilingual), Dragon HD Flash (zh-CN, en-US). Real-time synthesis
only; SSML subset. Free F0 tier: 0.5M characters/month. AA: "Azure HD 2.5" 1131, "Azure Neural"
1035. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/high-definition-voices ,
https://azure.microsoft.com/en-us/pricing/details/speech/

**Amazon Polly.** Per 1M characters: Standard $4, Neural $16, Generative $30, Long-Form $100. Free
tier: Generative 100K characters/month for the first 12 months. AA: Generative 1065 (the same as
Kokoro), Long-Form 1033, Neural 894. Source: https://aws.amazon.com/polly/pricing/

**Hume Octave.** Plans: Free 10K characters, Starter $3 (30K), Creator $7 (140K), Pro $70 (1M),
Scale $200 (3.3M). The page as read gives a commercial licence only from Pro upward. AA: Octave 2
1051, Octave 1036. TA: Octave 1525 +-22 (top ten there). The two arenas disagree on Hume.
Source: https://www.hume.ai/pricing

**Inworld.** TTS-2 $25 per 1M characters on demand, TTS-2 Flash $15; all plans include a commercial
licence; free on-demand plan includes "up to 70 min TTS". Strong on both arenas (AA 1251; TA "TTS
MAX" 1557, "TTS" 1541). Source: https://inworld.ai/pricing

**Deepgram.** Flux TTS $0.045 per 1K characters, Aura-2 $0.030, Aura-1 $0.015. Not on either
leaderboard table I read, so naturalness evidence is the vendor's own samples only.
Source: https://deepgram.com/pricing

**PlayHT.** Reported acquired by Meta in July 2025 and shut down on 2025-12-31. I found this only in
third-party articles, not a primary statement - see "Could not verify". Drop it from consideration
either way: it is on neither leaderboard.
Source (secondary): https://notevibes.com/alternative/play-ht

**Others in the AA top 25**, noted only from the AA table: Alibaba Qwen-Audio-3.1-TTS-Plus (1292,
$19.3/1M), Speechify Simba 3.2 (1242, $6.6/1M), VUI Labs Luna TTS (1227), StepFun StepAudio 2.5
(1210), Soniox TTS Real-Time v2 (1179), MiniMax Speech 2.8 HD (1173), Smallest.ai Lightning V3.1 Pro
(1171), Murf Falcon 2 (1155), Gradium (1151), Fish Audio S2.1 Pro (1141, hosted).

## Per-engine notes: local

**Kokoro-82M** - recommended. 82M parameters, StyleTTS2-derived. Weights Apache-2.0; the model card
says it was trained on permissive/non-copyrighted audio and welcomes commercial deployment. v1.0
released 2025-01-27: 54 voices across 8 languages; **no Norwegian**. Two ways to run it:
- `kokoro-onnx` (MIT wrapper, ONNX Runtime): `pip install -U kokoro-onnx`, plus two files,
  `kokoro-v1.0.onnx` (~300 MB, quantised ~80 MB) and `voices-v1.0.bin`. Python 3.10-3.13. README
  claims "near real-time on macOS M1" on CPU; GPU optional. Release 0.6.1 on 2026-08-19.
- `kokoro` (official, PyTorch + espeak-ng): `pip install kokoro`. Requires Python <3.13, last
  release 0.9.4 on 2025-04-05, repo last pushed 2025-08-06. This machine runs Python 3.13.14, so
  this package would not install here; use `kokoro-onnx`.
Evidence: AA 1064 (5,283 samples), TA 1477 +-24 (1,033 votes).
Sources: https://huggingface.co/hexgrad/Kokoro-82M , https://github.com/thewh1teagle/kokoro-onnx ,
https://pypi.org/project/kokoro-onnx/ , https://pypi.org/project/kokoro/

**Chatterbox (Resemble AI).** MIT for code and weights. Variants: original (500M, English),
Multilingual V3 (500M, 23 languages **including Norwegian**), Turbo (350M, English, paralinguistic
tags such as `[laugh]`), Nano (110M, English, "3x faster than realtime on 8 CPU cores").
`pip install chatterbox-tts`; devices cuda / cpu / mps; developed and tested on Python 3.11 on
Debian. All README examples pass a ~10 s reference clip (`audio_prompt_path`). Every output carries
an inaudible Perth watermark. PyPI 0.1.7 (2026-03-26). Evidence: TA 1480 +-19 (1,780 votes); AA
1025 for "Chatterbox" and 1102 for the hosted "Chatterbox HD". The vendor cites Podonos
evaluations; see "Could not verify" for the conflict in what they show. It is the best local route
to Norwegian with a permissive licence.
Sources: https://github.com/resemble-ai/chatterbox , https://huggingface.co/ResembleAI/chatterbox ,
https://pypi.org/project/chatterbox-tts/

**Pocket TTS (Kyutai).** 100M parameters, built for CPU: "~6x real-time on a CPU of MacBook Air M4"
using 2 cores. MIT code, CC-BY-4.0 weights (attribution required; access terms forbid cloning a
voice without consent). English, French, German, Portuguese, Italian, Spanish; no Norwegian. 20+
preset English voices, each with its own source-dataset licence (listed at
https://huggingface.co/kyutai/tts-voices). `pip install pocket-tts`; CLI
`pocket-tts generate --text ... --voice ...` writes a WAV; Python 3.10-3.14; README notes default
PyTorch wheels on Windows and macOS are already CPU-only. 3.3.0 on 2026-09-24, repo pushed
2026-10-01 - the most actively maintained small model here. **No leaderboard data**: naturalness
rests on the vendor's samples.
Sources: https://github.com/kyutai-labs/pocket-tts , https://huggingface.co/kyutai/pocket-tts

**Breeze TTS 2 (BreezeBlue).** Highest open-weight model on AA (1216, above Eleven v3). 3B
parameters, released 2026-08-25. Needs an NVIDIA GPU with 12 GB minimum (24 GB for the fast path)
and Linux; no pip package. English and Chinese only. Code Apache-2.0, but weights **and self-hosted
outputs** are under a research and non-commercial licence. Not usable in an MIT plugin meant for
general use, and it does not run on Windows natively.
Source: https://huggingface.co/BreezeBlue/Breeze-TTS-2

**Fish Audio S2 Pro.** ~5B parameters (4B slow AR + 0.4B fast AR), 80+ languages including
Norwegian (tier 2). Fish Audio Research License: commercial use needs a separate licence. Speed
figures are for an H200. AA 1117. Source: https://huggingface.co/fishaudio/s2-pro

**Voxtral TTS (Mistral).** 4B, GPU >= 16 GB, served through vLLM-Omni. CC-BY-NC-4.0 because the
bundled reference voices come from non-commercial datasets. 9 languages, no Norwegian. AA 1083.
Source: https://huggingface.co/mistralai/Voxtral-4B-TTS-2603

**Higgs Audio v3 (Boson AI).** 4B; code Apache-2.0, weights research and non-commercial. AA 1038.
Source: https://github.com/boson-ai/higgs-audio

**Qwen3-TTS (Alibaba).** Apache-2.0 code and weights; 0.6B and 1.7B; 10 languages (no Norwegian);
9 preset voices of which 2 are English (Ryan, Aiden); GPU expected. Released 2026-01-22. The hosted
Qwen3 TTS variants score low on AA (932-944); the high-ranking Qwen-Audio-3.x-TTS-Plus models are
hosted only. Source: https://github.com/QwenLM/Qwen3-TTS

**VibeVoice (Microsoft).** MIT weights still on Hugging Face, but Microsoft removed the TTS code
from the repository after misuse, and the README says research use only. AA 957. Drop.
Source: https://github.com/microsoft/VibeVoice

**XTTS v2 (Coqui).** Coqui the company is gone; `coqui-ai/TTS` last pushed 2024-08. The Idiap fork
(`coqui-tts` 0.27.5, 2026-01-26; pushed 2026-10-02) keeps the code alive, but the XTTS v2 weights
are frozen since 2023-12 under the Coqui Public Model License (non-commercial). AA 916, near the
bottom. Drop. Sources: https://huggingface.co/coqui/XTTS-v2 , https://github.com/idiap/coqui-ai-TTS

**F5-TTS.** Code MIT and actively released (1.1.22, 2026-07-23), weights CC-BY-NC-4.0. Not on
either board. Source: https://huggingface.co/SWivid/F5-TTS

**Stale but permissive (Apache-2.0), no leaderboard presence:** Orpheus (pip 2025-03-17, push
2025-12-05), Dia / Dia2 (2025-11), Sesame CSM-1B (2025-05-27), Parler-TTS (2024-12-10), Zonos
(2025-03-05; AA 1000 as the anchor). StyleTTS 2 (MIT, 2024-08-10; AA 895). None is a better choice
than Kokoro, which descends from StyleTTS 2 and outranks it by ~170 Elo on AA.
Sources: https://github.com/canopyai/Orpheus-TTS , https://github.com/nari-labs/dia ,
https://github.com/SesameAILabs/csm , https://github.com/huggingface/parler-tts ,
https://github.com/Zyphra/Zonos , https://github.com/yl4579/StyleTTS2

**Small CPU models, no leaderboard data:** KittenTTS (15-80M ONNX models; repo pushed 2026-10-03;
v2 weights under a "Stellon Labs Community License") and Supertonic 3 (ONNX, 31 languages,
OpenRAIL-M weights; **repository archived 2026-09-09**, read-only, no support).
Sources: https://github.com/KittenML/KittenTTS , https://github.com/supertone-oss-archive/supertonic

**Piper (current engine).** `rhasspy/piper` is archived; development continues at
`OHF-Voice/piper1-gpl` under **GPL-3.0** (`piper-tts` 1.8.0, 2026-09-04). Worth knowing for an
MIT-licensed plugin: the skill only shells out to `python -m piper`, it does not bundle it, but the
dependency it installs is GPL. Not on either leaderboard.
Sources: https://github.com/OHF-Voice/piper1-gpl , https://pypi.org/project/piper-tts/

## Fit to `make_explainer.py`

The `tts()` function (lines 58-80) needs: text in, a WAV file out, per scene, with a `voice` string
from `script.json`. It reads the duration with the stdlib `wave` module, so the output must be PCM
WAV.

| Option | Key | New install | Output | Notes |
|---|---|---|---|---|
| Kokoro via `kokoro-onnx` | none | pip + ~300 MB model download | samples array; write WAV | Python API, not a CLI; voice names like `af_heart` |
| Pocket TTS | none | pip (PyTorch CPU) | WAV from CLI | closest to today's `python -m piper` shape; quality unranked |
| Chatterbox Turbo / Nano | none | pip (PyTorch, larger) | tensor; write WAV | needs a reference clip; watermark |
| Gemini 3.8 Flash TTS | yes | `google-genai` | WAV directly | free tier; Norwegian |
| Eleven v4 | yes | `elevenlabs` | PCM; add WAV header | the top of the board |

## Could not verify

- **ElevenLabs Norwegian support for v4 and v3.** Two reads of ElevenLabs docs disagreed (one said
  v4 yes / v3 no; one said neither lists it; both agree Flash v2.5 does). Check the language list
  at https://elevenlabs.io/docs/overview/models by hand.
- **ElevenLabs Starter plan details.** One page read "$6 (first month $1)", another "$6 first month,
  then $1"; the first is the plausible one. Free-plan attribution requirement not stated on the page
  as read.
- **Azure Speech prices.** The pricing page rendered without numbers ("$-") or with implausible ones
  ($0.000016 per 1M). The table uses AA's figures ($15 / $22 per 1M characters) instead.
- **Google Cloud TTS (Chirp 3 HD, Studio) prices.** Page returned no figures. AA lists Chirp 3 HD at
  $30 and Studio at $160 per 1M characters.
- **Gemini TTS price per character.** Google prices by token; the per-character figure ($16.5/1M)
  is AA's conversion, not Google's.
- **OpenAI gpt-4o-mini-tts price unit.** Read as "$0.60 input / $12 output per 1M characters"; OpenAI
  has historically priced this model per 1M tokens. Treat the unit as unverified.
- **Hume commercial licence tier.** The page as read grants it only from Pro ($70); not
  cross-checked against Hume's terms.
- **Chatterbox vs ElevenLabs (Podonos).** The vendor README links a Podonos evaluation of
  Chatterbox Turbo vs ElevenLabs Turbo v2.5. My read of that page came out as ElevenLabs preferred
  ~75 % to ~25 %, which contradicts the widely repeated claim that Chatterbox won ~65 % to ~25 %.
  The summariser may have swapped the A/B labels. Either way it is a vendor-commissioned test;
  the TA result (Chatterbox ~27 Elo below Eleven Multilingual v2) is the independent number.
  https://podonos.com/resembleai/chatterbox-turbo-vs-elevenlabs-turbo
- **Chatterbox without a reference clip.** Not confirmed whether `generate()` falls back to a
  built-in voice in 0.1.7. Also not confirmed: Windows and Python 3.13 support (tested by the
  vendor on Python 3.11, Debian).
- **kokoro-onnx on Windows.** The README does not mention Windows. ONNX Runtime ships Windows
  wheels, so it should work, but I did not run it. Real-time factor on a typical Windows CPU is
  also unmeasured.
- **Kokoro / Chatterbox / Pocket TTS vs Piper.** No blind comparison includes Piper. The claim that
  any of them is a clear step up rests on vendor samples and general reputation.
- **Pocket TTS, KittenTTS, Supertonic, F5-TTS, Orpheus, Dia, CSM, Parler-TTS naturalness.** Not on
  either leaderboard; no independent evidence found.
- **PlayHT shutdown.** Third-party articles only; no primary statement from PlayHT or Meta read.
- **AA table details.** The AA rows were extracted by a summarising tool from a 93-row page; two
  separate reads agreed on the top 30 and on the open-weights rows. AA "open weights" flags and
  per-character prices are AA's, not the vendors'.
- **Breeze TTS 2, Qwen-Audio-3.x-TTS-Plus, Speechify Simba, VUI Luna** - new to me; only the AA row
  (and for Breeze the model card) was read. Speechify's pricing page returned nothing usable.
- **VRAM figures** for Fish S2 Pro, Higgs v3, Qwen3-TTS, Chatterbox: not stated on the pages read.

## Sources

- [AA] Artificial Analysis TTS leaderboard / Speech Arena: https://artificialanalysis.ai/text-to-speech/leaderboard
  and https://artificialanalysis.ai/text-to-speech/arena?tab=leaderboard (page dated September 2026)
- [TA] TTS Arena V2: https://huggingface.co/spaces/TTS-AGI/TTS-Arena-V2 ; rows read from
  https://tts-agi-tts-arena-v2.hf.space/api/leaderboard?type=tts
- Release dates and package licences: https://pypi.org/pypi/<package>/json
- Repository activity and licences: GitHub REST API, `repos/<owner>/<repo>`
- Weights licences and model-card dates: https://huggingface.co/api/models/<id>
- Vendor pages: linked inline in each note above.
