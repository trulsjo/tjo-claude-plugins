---
name: explainer-video
description: Make a narrated, 3Blue1Brown-style explainer video on any topic. Use when asked to explain something as a video or animation.
---

# explainer-video

A bespoke, **discardable** explainer: one topic, one viewer, built in minutes and thrown away after.

Toolchain, all local and free: **Manim** (3Blue1Brown's animation library) draws, **Piper** speaks,
**ffmpeg** joins. `make_explainer.py` (next to this file) owns every mechanical stage; you write two
files and judge the frames.

## Steps

0. **Dependencies.** `python "${CLAUDE_SKILL_DIR}/ensure_deps.py"` - checks Python, Manim,
   piper-tts, ffmpeg and the Piper voice, and installs what is missing (pip `--user`; ffmpeg via
   winget or brew). Done when it prints `ready`. If it prints `NOT ready`, show the user the MISSING
   lines - they name the fix (on Linux, system packages that need sudo) - and stop.

1. **Scope.** Settle topic, viewer and length. Default: 60-120 s, 4-7 scenes. Work in a fresh
   directory (the scratchpad unless the user names one). Done when you can state the one idea the
   viewer should leave with.

2. **Script** - write `script.json`:
   ```json
   {"title": "How TCP handshakes work", "voice": "en_US-lessac-medium",
    "scenes": [{"id": "S01_hook", "narration": "...", "visual": "three packets cross between two hosts"},
               {"id": "S02_syn", "narration": "...", "visual": "..."}]}
   ```
   - One visual idea per scene, noted in `visual` (your plan for step 3; the pipeline ignores it).
     The narration names what is on screen as it appears.
   - Spoken English: about 150 words a minute, short sentences. Spell out symbols the way a
     person says them ("C plus plus", "x squared", "arrow") - Piper reads text literally.
   - Scene ids are Python class names: `S01_hook`, `S02_syn`, ...
   - `voice` is a Piper voice (about 60 MB each), downloaded to `~/.cache/piper-voices` on first
     use. Other voices: `python -m piper.download_voices --help`.

   Done when every scene has `narration` and `visual`.

3. **Scenes** - write `scenes.py`, one class per scene id:
   ```python
   from manim import *
   from narrated_scene import NarratedScene

   class S01_hook(NarratedScene):
       def construct(self):
           t = self.budget                       # this scene's narration length, seconds
           title = Text("Three packets", font_size=56)
           self.play(Write(title), run_time=0.25 * t)
           self.play(title.animate.to_edge(UP), run_time=0.1 * t)
           ...
           self.finish()                         # pads to the narration length
   ```
   The 3b1b look: dark background, objects **build up** step by step, **transform** one shape
   into the next instead of cutting, one colour per concept held across all scenes, motion that
   lands as the narration names it. Size every `run_time` as a fraction of `t` so the picture tracks
   the voice. See **Manim gotchas** below. Done when every scene id has a class ending in
   `self.finish()`.

4. **Draft render.**
   `python "${CLAUDE_SKILL_DIR}/make_explainer.py" <workdir> --quality l`
   Done when it prints `done: <path>`. Outputs in `<workdir>`: the video is `<title>.mp4` (title
   made filesystem-safe), per-scene clips are in `segments/<quality>/`, check frames are in
   `check/`. For what a rerun rebuilds, see **Pipeline reference** below.

5. **Frame check.** Step 4 writes `check/<id>.png`, one frame per scene taken 1 s before its end.
   **Look at every one** with the Read tool. Fix and rerun step 4 for any scene with text off-frame,
   overlapping objects, unreadable text, or a picture that does not match its narration. Done when
   every scene's frame is clean.

6. **Final render.** Rerun step 4 with `--quality m` (720p) or `h` (1080p). Report the output path
   and total length, and which scenes you fixed in step 5.

## Pipeline reference

- A rerun rebuilds only the scenes whose inputs changed: an edited narration rebuilds that scene, a
  changed voice rebuilds all of them, and each quality is cached separately.
- Any edit to `scenes.py` re-renders every scene. Iterate on one scene with Manim directly -
  `python -m manim render -ql scenes.py S02_syn` in the workdir - and run the pipeline once the
  scene looks right.
- `--only S03_ack` forces a re-render with no input change.
- Preview with the pipeline's `check/` frames: `manim render -s` saves the **last** frame, which is
  blank when the scene ends in a fade-out.

## Manim gotchas

- **No LaTeX is assumed** (`ensure_deps.py` does not install it): use `Text` / `MarkupText`, not
  `MathTex` / `Tex` (they shell out to LaTeX and fail). Write maths as Unicode: `Text("x² + y² = r²")`.
- **Off-frame text** is the most common defect: the frame is about 14.2 x 8 units. Group, then
  `VGroup(...).arrange(DOWN, buff=0.4)` and `.scale_to_fit_width(config.frame_width - 1)` when wide.
- **Two animations on one object in one `play` fight.** `self.play(Write(x), Indicate(x))` ends
  with `x` invisible: `Indicate` restores the state it saw at the start, which is "not yet
  written". Play them one after the other.
- **Leftovers**: objects stay on screen until removed. End each scene with
  `self.play(FadeOut(*self.mobjects))` when the next scene starts from a clean frame.
- **`set_width` on labels** gives each label its own scale, so a short word renders huge. Give a
  column of labels one `font_size` and align them instead.
