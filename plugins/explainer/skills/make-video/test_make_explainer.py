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
    # a Piper voice with no engine key means Piper, silently, whatever Kokoro's state
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        assert m.pick_engine({"voice": "en_GB-alba-medium"}, ok) == ("piper", "en_GB-alba-medium")
        assert m.pick_engine({"voice": "en_GB-alba-medium"}, broken) == ("piper", "en_GB-alba-medium")
    assert out.getvalue() == ""
    # explicit Kokoro keeps a Piper voice, so kokoro_speaker can reject it with the voice list
    assert m.pick_engine({"engine": "kokoro", "voice": "en_GB-alba-medium"}, ok) == (
        "kokoro", "en_GB-alba-medium")
    # explicit Kokoro that is unavailable stops instead of falling back
    assert "kokoro-onnx is not installed" in exits(lambda: m.pick_engine({"engine": "kokoro"}, broken))
    # unknown engine: error lists the valid ones
    msg = exits(lambda: m.pick_engine({"engine": "elevenlabs"}, ok))
    assert "elevenlabs" in msg and "kokoro" in msg and "piper" in msg


def test_engine_change_rebuilds_audio():
    spoken = []
    real = m.ENGINES
    m.ENGINES = {"kokoro": fake_speaker(spoken, "kokoro"), "piper": fake_speaker(spoken, "piper")}
    try:
        scenes = [{"id": "S01", "narration": "one"}, {"id": "S02", "narration": "two"}]
        with tempfile.TemporaryDirectory() as d, contextlib.redirect_stdout(io.StringIO()):
            assert m.tts(Path(d), scenes, "piper", "v") == {"S01": 1.0, "S02": 1.0}
            assert spoken == [("piper", "v", "S01"), ("piper", "v", "S02")]
            m.tts(Path(d), scenes, "piper", "v")
            assert len(spoken) == 2, "same engine must rebuild nothing"
            m.tts(Path(d), scenes, "kokoro", "v")
            assert spoken[2:] == [("kokoro", "v", "S01"), ("kokoro", "v", "S02")], (
                "engine change must rebuild all")
    finally:
        m.ENGINES = real


def fake_speaker(spoken, name):
    def speaker(voice):
        def speak(text, wav):
            spoken.append((name, voice, wav.stem))
            with wave.open(str(wav), "wb") as w:
                w.setnchannels(1), w.setsampwidth(2), w.setframerate(8000)
                w.writeframes(b"\0\0" * 8000)
        return speak
    return speaker


def test_kokoro_load_failure_falls_back():
    spoken = []

    def broken_kokoro(voice):
        raise m.KokoroUnavailable("model failed to load: bad protobuf")

    real, real_dir = m.ENGINES, m.KOKORO_DIR
    scenes = [{"id": "S01", "narration": "one"}]
    try:
        with tempfile.TemporaryDirectory() as d:
            # a model that does not load is reported as KokoroUnavailable, with the remedy
            m.KOKORO_DIR = Path(d)
            for f in m.KOKORO_FILES:
                (m.KOKORO_DIR / f).write_text("garbage")
            try:
                m.kokoro_speaker("af_heart")
                raise AssertionError("garbage model files must not load")
            except m.KokoroUnavailable as e:
                assert "failed to load" in str(e) and str(d) in str(e)
            m.KOKORO_DIR = real_dir

            m.ENGINES = {"kokoro": broken_kokoro, "piper": fake_speaker(spoken, "piper")}
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                m.narrate(Path(d), {"scenes": scenes}, "kokoro", "af_heart")
            assert spoken == [("piper", m.DEFAULT_VOICE["piper"], "S01")]
            assert sum("bad protobuf" in line for line in out.getvalue().splitlines()) == 1
            # explicit Kokoro stops with the reason instead of falling back
            msg = exits(lambda: m.narrate(Path(d), {"engine": "kokoro", "scenes": scenes},
                                          "kokoro", "af_heart"))
            assert "bad protobuf" in msg and len(spoken) == 1
            # once Kokoro works again, a rerun rebuilds the audio with Kokoro
            m.ENGINES = {"kokoro": fake_speaker(spoken, "kokoro"), "piper": m.ENGINES["piper"]}
            with contextlib.redirect_stdout(io.StringIO()):
                m.narrate(Path(d), {"scenes": scenes}, "kokoro", "af_heart")
            assert spoken[1:] == [("kokoro", "af_heart", "S01")]
    finally:
        m.ENGINES, m.KOKORO_DIR = real, real_dir


if __name__ == "__main__":
    test_pick_engine()
    test_kokoro_load_failure_falls_back()
    test_engine_change_rebuilds_audio()
    print("ok")
