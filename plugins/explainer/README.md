# explainer

Two skills:

- **`explain`** - the ladder. Picks the lowest format that carries the idea (controlled prose ->
  diagram -> interactive HTML page -> narrated video) and climbs one rung when an explanation did
  not land. Each rung names a fallback that needs nothing installed; the video rung asks first.
- **`explainer-video`** - the top rung, below.

## explainer-video

Ask Claude for "an explainer video on X" and it writes a narrated
script, animates each scene with [Manim](https://www.manim.community/) (3Blue1Brown's library),
voices it locally with [Kokoro](https://huggingface.co/hexgrad/Kokoro-82M), joins it with ffmpeg,
and checks one frame per scene before the final render. Nothing leaves the machine; no API keys.

### Voice

| Engine | When | Voices | Size |
|---|---|---|---|
| Kokoro-82M (via [`kokoro-onnx`](https://github.com/thewh1teagle/kokoro-onnx), Apache-2.0, CPU) | default | 28 English voices, American and British; default `af_heart` | model about 340 MB, downloaded once |
| [Piper](https://github.com/OHF-Voice/piper1-gpl) | fallback when Kokoro is unavailable (the run prints one line saying why), or `"engine": "piper"` in `script.json` | many languages, including Norwegian; default `en_US-lessac-medium` | about 60 MB per voice |

`script.json` takes optional `"engine"` (`"kokoro"` or `"piper"`) and `"voice"` keys. Kokoro has no
Norwegian voice; use Piper for that.

Idea: Karpathy, https://x.com/karpathy/status/2105819303471976479 - bespoke, discardable explainer
videos as the top rung for understanding LLM output.

## Dependencies

The skill's first step runs `skills/explainer-video/ensure_deps.py`, which checks and installs:

| Dependency | How it is installed |
|---|---|
| Python >= 3.10 | not installed - must already exist |
| `manim`, `piper-tts` | `pip install --user` (plain `pip install` inside a venv) |
| ffmpeg | `winget install Gyan.FFmpeg` on Windows, `brew install ffmpeg` on macOS; on Linux it prints the `apt` command (needs sudo) |
| Piper voice `en_US-lessac-medium` (~60 MB) | downloaded to `~/.cache/piper-voices` |
| `kokoro-onnx` and the Kokoro model (~340 MB) - optional | `pip install --user`; model downloaded to `~/.cache/kokoro-onnx`. If either fails the setup is still ready and Piper narrates. |

On Linux, Manim also needs `libcairo2-dev libpango1.0-dev pkg-config python3-dev` (sudo; printed if
the pip install fails). LaTeX is not needed: the skill uses plain `Text` with Unicode maths.

Check without installing anything: `python skills/explainer-video/ensure_deps.py --check`.
