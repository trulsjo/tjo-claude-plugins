"""Self-check for engine selection and audio caching.  Run: python test_make_explainer.py"""
import contextlib
import io
import tempfile
import wave
from pathlib import Path

import make_explainer as m


def exits(fn):
    try:
        fn()
    except SystemExit as e:
        return str(e.code)
    raise AssertionError("expected the run to stop")


def test_pick_engine():
    ok, broken = (lambda: None), (lambda: "kokoro-onnx is not installed")
    # no engine key: Kokoro when available
    assert m.pick_engine({}, ok) == ("kokoro", m.DEFAULT_VOICE["kokoro"])
    assert m.pick_engine({"voice": "bm_george"}, ok) == ("kokoro", "bm_george")
    # explicit Piper never asks about Kokoro
    assert m.pick_engine({"engine": "piper"}, broken) == ("piper", m.DEFAULT_VOICE["piper"])
    assert m.pick_engine({"engine": "piper", "voice": "nb_NO-talesyntese-medium"}, broken) == (
        "piper", "nb_NO-talesyntese-medium")
    # no engine key, Kokoro unavailable: Piper, and one line naming the reason
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        assert m.pick_engine({"voice": "af_heart"}, broken) == ("piper", m.DEFAULT_VOICE["piper"])
    assert out.getvalue().count("\n") == 1 and "kokoro-onnx is not installed" in out.getvalue()
    with contextlib.redirect_stdout(io.StringIO()):
        assert m.pick_engine({"voice": "en_GB-alba-medium"}, broken) == ("piper", "en_GB-alba-medium")
    # explicit Kokoro that is unavailable stops instead of falling back
    assert "kokoro-onnx is not installed" in exits(lambda: m.pick_engine({"engine": "kokoro"}, broken))
    # unknown engine: error lists the valid ones
    msg = exits(lambda: m.pick_engine({"engine": "elevenlabs"}, ok))
    assert "elevenlabs" in msg and "kokoro" in msg and "piper" in msg


def test_engine_change_rebuilds_audio():
    spoken = []

    def fake(name):
        def speaker(voice):
            def speak(text, wav):
                spoken.append((name, wav.stem))
                with wave.open(str(wav), "wb") as w:
                    w.setnchannels(1), w.setsampwidth(2), w.setframerate(8000)
                    w.writeframes(b"\0\0" * 8000)
            return speak
        return speaker

    real, m.ENGINES = m.ENGINES, {"kokoro": fake("kokoro"), "piper": fake("piper")}
    try:
        scenes = [{"id": "S01", "narration": "one"}, {"id": "S02", "narration": "two"}]
        with tempfile.TemporaryDirectory() as d, contextlib.redirect_stdout(io.StringIO()):
            assert m.tts(Path(d), scenes, "piper", "v") == {"S01": 1.0, "S02": 1.0}
            assert spoken == [("piper", "S01"), ("piper", "S02")]
            m.tts(Path(d), scenes, "piper", "v")
            assert len(spoken) == 2, "same engine must rebuild nothing"
            m.tts(Path(d), scenes, "kokoro", "v")
            assert spoken[2:] == [("kokoro", "S01"), ("kokoro", "S02")], "engine change must rebuild all"
    finally:
        m.ENGINES = real


if __name__ == "__main__":
    test_pick_engine()
    test_engine_change_rebuilds_audio()
    print("ok")
