"""Build a narrated explainer video from script.json + scenes.py.

Usage:  python make_explainer.py <workdir> [--quality l|m|h] [--only S01_intro,...]

<workdir> holds:
  script.json  {"title": str, "voice": "en_US-lessac-medium",
                "scenes": [{"id": "S01_intro", "narration": "..."}, ...]}
  scenes.py    one Manim class per scene id, each subclassing NarratedScene

Stages (a scene is rebuilt only when its own inputs change - narration, voice, scenes.py,
its narration length, or the quality; signatures live in audio/*.sig and media/*.sig):
  1. tts      narration -> audio/<id>.wav (Piper, local), durations.json
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
import wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
VOICES = Path.home() / ".cache" / "piper-voices"
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


def tts(work: Path, script: dict) -> dict:
    voice = script.get("voice", "en_US-lessac-medium")
    VOICES.mkdir(parents=True, exist_ok=True)
    if not (VOICES / f"{voice}.onnx").exists():
        run([sys.executable, "-m", "piper.download_voices", "--download-dir", VOICES, voice])
    audio = work / "audio"
    audio.mkdir(exist_ok=True)
    durations = {}
    for sc in script["scenes"]:
        wav, txt, sig_file = (audio / f"{sc['id']}{ext}" for ext in (".wav", ".txt", ".sig"))
        sig = f"{voice}\n{sc['narration']}"
        if not wav.exists() or changed(sig_file, sig):
            txt.write_text(sc["narration"], encoding="utf-8")
            run([sys.executable, "-m", "piper", "--data-dir", VOICES, "-m", voice, "-f", wav,
                 "--input-file", txt])
            sig_file.write_text(sig, encoding="utf-8")
        with wave.open(str(wav)) as w:
            durations[sc["id"]] = round(w.getnframes() / w.getframerate(), 3)
    dur_file, dur_json = work / "durations.json", json.dumps(durations, indent=1)
    if changed(dur_file, dur_json):
        dur_file.write_text(dur_json, encoding="utf-8")
    print(f"tts: {len(durations)} clips, {sum(durations.values()):.1f} s of narration")
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
    if a.only:
        for sid in a.only.split(","):
            (work / "media" / f"{sid}.{a.quality}.sig").unlink(missing_ok=True)
    durations = tts(work, script)
    videos = render(work, ids, a.quality, durations)
    segs = mux(work, ids, videos, a.quality)
    frames(work, segs)
    out = concat(work, script.get("title", "explainer"), segs)
    print(f"check frames: {work / 'check'}")
    print(f"done: {out}")


if __name__ == "__main__":
    main()
