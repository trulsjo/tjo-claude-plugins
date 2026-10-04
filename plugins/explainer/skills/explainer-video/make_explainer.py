"""Build a narrated explainer video from script.json + scenes.py.

Usage:  python make_explainer.py <workdir> [--quality l|m|h] [--only S01_intro,...]

<workdir> holds:
  script.json  {"title": str, "engine": "kokoro" | "piper" (optional), "voice": str (optional),
                "scenes": [{"id": "S01_intro", "narration": "..."}, ...]}
  scenes.py    one Manim class per scene id, each subclassing NarratedScene

With no "engine" key Kokoro narrates; when Kokoro is unavailable the run falls back to Piper.
A Piper voice name (it contains a hyphen) with no "engine" key selects Piper.

Stages (a scene is rebuilt only when its own inputs change - narration, engine, voice, scenes.py,
its narration length, or the quality; signatures live in audio/*.sig and media/*.sig):
  1. tts      narration -> audio/<id>.wav (Kokoro or Piper, both local), durations.json
  2. render   scenes.py class <id> -> media/.../<id>.mp4 (Manim)
  3. mux      video + audio -> segments/<quality>/<id>.mp4 (audio padded to the video length)
  4. frames   one PNG per scene -> check/<id>.png
  5. concat   segments -> <title>.mp4 (title made filesystem-safe: 'Why: 1/2' -> Why_1_2.mp4)
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
import wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
VOICES = Path.home() / ".cache" / "piper-voices"
KOKORO_DIR = Path.home() / ".cache" / "kokoro-onnx"
KOKORO_FILES = ("kokoro-v1.0.onnx", "voices-v1.0.bin")
DEFAULT_VOICE = {"kokoro": "af_heart", "piper": "en_US-lessac-medium"}
FFMPEG_DIRS = [Path.home() / "AppData/Local/Microsoft/WinGet/Packages"]
QUALITY = {"l": ("-ql", "480p15"), "m": ("-qm", "720p30"), "h": ("-qh", "1080p60")}


def ffmpeg():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    for root in FFMPEG_DIRS:
        for hit in root.glob("Gyan.FFmpeg*/**/bin/ffmpeg.exe"):
            return str(hit)
    sys.exit("ffmpeg not found on PATH or in the WinGet packages dir")


def run(cmd, **kw):
    print("  $", " ".join(str(c) for c in cmd)[:200])
    subprocess.run([str(c) for c in cmd], check=True, **kw)


def stale(out: Path, *inputs: Path) -> bool:
    return not out.exists() or any(i.stat().st_mtime > out.stat().st_mtime for i in inputs)


def changed(sig_file: Path, sig: str) -> bool:
    """True when sig_file is missing or records a different signature."""
    return not sig_file.exists() or sig_file.read_text(encoding="utf-8") != sig


def piper_speaker(voice: str):
    VOICES.mkdir(parents=True, exist_ok=True)
    if not (VOICES / f"{voice}.onnx").exists():
        run([sys.executable, "-m", "piper.download_voices", "--download-dir", VOICES, voice])

    def speak(text: str, wav: Path) -> None:
        txt = wav.with_suffix(".txt")
        txt.write_text(text, encoding="utf-8")
        run([sys.executable, "-m", "piper", "--data-dir", VOICES, "-m", voice, "-f", wav,
             "--input-file", txt])
    return speak


class KokoroUnavailable(Exception):
    """Kokoro is installed but its model does not load."""


def kokoro_speaker(voice: str):
    try:
        from kokoro_onnx import Kokoro
        kokoro = Kokoro(*(str(KOKORO_DIR / f) for f in KOKORO_FILES))
        voices = kokoro.get_voices()
    except Exception as e:  # corrupt or truncated model file, runtime error on load
        reason = (str(e).splitlines() or [""])[0]
        raise KokoroUnavailable(f"model failed to load ({type(e).__name__}: {reason}); delete "
                                f"{KOKORO_DIR} to download it again") from e
    english = [v for v in voices if v[0] in "ab"]  # a = American, b = British
    if voice not in english:
        sys.exit(f"{voice!r} is not a Kokoro voice - set \"engine\": \"piper\" for a Piper voice, "
                 f"or pick one of: {', '.join(english)}")
    lang = "en-gb" if voice[0] == "b" else "en-us"

    def speak(text: str, wav: Path) -> None:
        samples, rate = kokoro.create(text, voice=voice, lang=lang)
        with wave.open(str(wav), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(rate)
            w.writeframes((samples * 32767).clip(-32768, 32767).astype("<i2").tobytes())
    return speak


ENGINES = {"kokoro": kokoro_speaker, "piper": piper_speaker}  # engine -> (voice -> speak(text, wav))


def kokoro_problem():
    """Why Kokoro cannot narrate, or None when it can."""
    try:
        import kokoro_onnx  # noqa: F401 - a broken install (e.g. onnxruntime) fails here too
    except Exception as e:
        return f"kokoro-onnx cannot be imported: {e}"
    missing = [f for f in KOKORO_FILES if not (KOKORO_DIR / f).exists()]
    return f"model file {KOKORO_DIR / missing[0]} is missing" if missing else None


def pick_engine(script: dict, problem=kokoro_problem) -> tuple:
    """(engine, voice) for this script: Kokoro unless the script says otherwise, Piper when
    Kokoro is unavailable or the script names only a Piper voice."""
    engine, voice = script.get("engine"), script.get("voice")
    if engine is not None and engine not in ENGINES:
        sys.exit(f"unknown engine {engine!r} - valid engines: {', '.join(ENGINES)}")
    if engine is None and voice and "-" in voice:  # Piper: en_US-name-medium, Kokoro: af_heart
        engine = "piper"
    if engine != "piper":
        why = problem()
        if why and engine == "kokoro":
            sys.exit(f"Kokoro unavailable: {why} - run ensure_deps.py, or set \"engine\": \"piper\"")
        if why:
            voice = DEFAULT_VOICE["piper"]  # any voice the script named is a Kokoro one
            print(f"Kokoro unavailable ({why}) - narrating with Piper, voice {voice}")
        engine = "piper" if why else "kokoro"
    return engine, voice or DEFAULT_VOICE[engine]


def narrate(work: Path, script: dict, engine: str, voice: str) -> dict:
    """tts, re-picking the engine when Kokoro turns out not to load. The model loads before any
    audio is written, so nothing is half done at that point."""
    try:
        return tts(work, script["scenes"], engine, voice)
    except KokoroUnavailable as why:
        return tts(work, script["scenes"], *pick_engine(script, lambda: str(why)))


def tts(work: Path, scenes: list, engine: str, voice: str) -> dict:
    audio = work / "audio"
    audio.mkdir(exist_ok=True)
    durations, speak, spent = {}, None, 0.0
    for sc in scenes:
        wav, sig_file = audio / f"{sc['id']}.wav", audio / f"{sc['id']}.sig"
        sig = f"{engine}\n{voice}\n{sc['narration']}"
        if not wav.exists() or changed(sig_file, sig):
            t0 = time.perf_counter()
            speak = speak or ENGINES[engine](voice)  # loaded only when a scene needs speaking
            speak(sc["narration"], wav)
            spent += time.perf_counter() - t0
            sig_file.write_text(sig, encoding="utf-8")
        with wave.open(str(wav)) as w:
            durations[sc["id"]] = round(w.getnframes() / w.getframerate(), 3)
    dur_file, dur_json = work / "durations.json", json.dumps(durations, indent=1)
    if changed(dur_file, dur_json):
        dur_file.write_text(dur_json, encoding="utf-8")
    print(f"tts ({engine}, {voice}): {len(durations)} clips, {sum(durations.values()):.1f} s of "
          f"narration, spoken in {spent:.1f} s")
    return durations


def render(work: Path, ids, quality: str, durations: dict) -> dict:
    """Re-render a scene only when scenes.py, its narration length, or the quality changed."""
    flag, folder = QUALITY[quality]
    shutil.copy(HERE / "narrated_scene.py", work / "narrated_scene.py")
    code = hashlib.sha1((work / "scenes.py").read_bytes()
                        + (work / "narrated_scene.py").read_bytes()).hexdigest()
    videos = {}
    for sid in ids:
        mp4 = work / "media" / "videos" / "scenes" / folder / f"{sid}.mp4"
        sig_file, sig = work / "media" / f"{sid}.{quality}.sig", f"{code} {durations[sid]}"
        if not mp4.exists() or changed(sig_file, sig):
            run([sys.executable, "-m", "manim", "render", flag, "--disable_caching",
                 "-v", "WARNING", "--progress_bar", "none",
                 "--media_dir", "media", "scenes.py", sid], cwd=work)
            sig_file.write_text(sig, encoding="utf-8")
        videos[sid] = mp4
    return videos


def mux(work: Path, ids, videos: dict, quality: str) -> list:
    seg_dir = work / "segments" / quality
    seg_dir.mkdir(parents=True, exist_ok=True)
    segs = []
    for sid in ids:
        seg, wav = seg_dir / f"{sid}.mp4", work / "audio" / f"{sid}.wav"
        if stale(seg, videos[sid], wav):
            # apad + -shortest: audio is padded with silence and the clip ends with the video
            run([ffmpeg(), "-y", "-loglevel", "error", "-i", videos[sid], "-i", wav,
                 "-filter_complex", "[1:a]apad[a]", "-map", "0:v", "-map", "[a]",
                 "-c:v", "copy", "-c:a", "aac", "-ar", "48000", "-shortest", seg])
        segs.append(seg)
    return segs


def frames(work: Path, segs: list) -> None:
    """One PNG per scene, 1 s before its end, for the frame check."""
    check = work / "check"
    check.mkdir(exist_ok=True)
    for seg in segs:
        png = check / f"{seg.stem}.png"
        if stale(png, seg):
            run([ffmpeg(), "-y", "-loglevel", "error", "-sseof", "-1", "-i", seg,
                 "-frames:v", "1", png])


def concat(work: Path, title: str, segs: list) -> Path:
    lst = segs[0].parent / "list.txt"
    lst.write_text("".join(f"file '{s.name}'\n" for s in segs), encoding="utf-8")
    out = work / (re.sub(r"[^\w.-]+", "_", title).strip("_") + ".mp4")
    run([ffmpeg(), "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
         "-c", "copy", out])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workdir", type=Path)
    ap.add_argument("--quality", choices="lmh", default="m")
    ap.add_argument("--only", help="comma-separated scene ids to force re-render (all are still joined)")
    a = ap.parse_args()
    work = a.workdir.resolve()
    script = json.loads((work / "script.json").read_text(encoding="utf-8"))
    ids = [s["id"] for s in script["scenes"]]
    engine, voice = pick_engine(script)
    if a.only:
        for sid in a.only.split(","):
            (work / "media" / f"{sid}.{a.quality}.sig").unlink(missing_ok=True)
    durations = narrate(work, script, engine, voice)
    videos = render(work, ids, a.quality, durations)
    segs = mux(work, ids, videos, a.quality)
    frames(work, segs)
    out = concat(work, script.get("title", "explainer"), segs)
    print(f"check frames: {work / 'check'}")
    print(f"done: {out}")


if __name__ == "__main__":
    main()
