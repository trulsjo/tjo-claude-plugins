"""Base class for explainer scenes: ties a Manim scene's length to its narration clip.

make_explainer.py copies this file next to scenes.py and writes durations.json.

    from narrated_scene import NarratedScene

    class S01_intro(NarratedScene):
        def construct(self):
            t = self.budget          # seconds of narration for this scene
            self.play(Write(title), run_time=0.2 * t)
            ...
            self.finish()            # waits out whatever narration time is left
"""
import json
from pathlib import Path

from manim import Scene

_DURATIONS = json.loads(Path(__file__).with_name("durations.json").read_text(encoding="utf-8"))
TAIL = 0.6  # seconds of breathing room after the last word


class NarratedScene(Scene):
    @property
    def budget(self) -> float:
        return _DURATIONS[type(self).__name__]

    def finish(self):
        left = self.budget + TAIL - self.renderer.time
        if left > 0.05:
            self.wait(left)
