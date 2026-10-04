"""Check, and install when missing, everything make_explainer.py needs.

Usage:  python ensure_deps.py [--check]      (--check: report only, install nothing)

Installs:
  manim, piper-tts   pip install --user
  ffmpeg             winget (Windows) / brew (macOS); on Linux prints the apt command (needs sudo)
  Piper voice        downloaded to ~/.cache/piper-voices
  Kokoro             pip install --user kokoro-onnx; model (~340 MB) downloaded to ~/.cache/kokoro-onnx
Exit code 0 = ready; 1 = something is still missing (the report says what and how to fix it).
Kokoro is optional: without it the run is still ready, and videos are narrated by Piper.
"""
import argparse
import importlib.util
import platform
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

VOICE = "en_US-lessac-medium"
VOICES = Path.home() / ".cache" / "piper-voices"
KOKORO = "kokoro (optional)"
PIP_PACKAGES = {"manim": "manim", "piper": "piper-tts"}
KOKORO_DIR = Path.home() / ".cache" / "kokoro-onnx"
KOKORO_FILES = ("kokoro-v1.0.onnx", "voices-v1.0.bin")
KOKORO_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
WINGET_FFMPEG = Path.home() / "AppData/Local/Microsoft/WinGet/Packages"


def find_ffmpeg():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    for hit in WINGET_FFMPEG.glob("Gyan.FFmpeg*/**/bin/ffmpeg.exe"):
        return str(hit)
    return None


def run(cmd):
    print("  $", " ".join(str(c) for c in cmd))
    return subprocess.run([str(c) for c in cmd]).returncode == 0


def ensure_python(report):
    ok = sys.version_info >= (3, 10)
    report.append(("python >= 3.10", ok, f"{platform.python_version()} at {sys.executable}"))
    return ok


def pip_install(*packages):
    in_venv = sys.prefix != sys.base_prefix  # --user is refused inside a venv
    run([sys.executable, "-m", "pip", "install", *([] if in_venv else ["--user"]), "--quiet", *packages])
    importlib.invalidate_caches()


def ensure_pip(check, report):
    missing = [pkg for mod, pkg in PIP_PACKAGES.items() if importlib.util.find_spec(mod) is None]
    if missing and not check:
        pip_install(*missing)
        missing = [pkg for mod, pkg in PIP_PACKAGES.items() if importlib.util.find_spec(mod) is None]
    hint = ""
    if missing and platform.system() == "Linux":
        hint = " (Manim needs: sudo apt install libcairo2-dev libpango1.0-dev pkg-config python3-dev)"
    report.append(("manim, piper-tts", not missing,
                   "installed" if not missing else f"missing: {', '.join(missing)}{hint}"))


def ensure_ffmpeg(check, report):
    exe = find_ffmpeg()
    if not exe and not check:
        system = platform.system()
        if system == "Windows" and shutil.which("winget"):
            run(["winget", "install", "--id", "Gyan.FFmpeg", "-e", "--silent",
                 "--accept-source-agreements", "--accept-package-agreements"])
        elif system == "Darwin" and shutil.which("brew"):
            run(["brew", "install", "ffmpeg"])
        exe = find_ffmpeg()
    hint = {"Linux": "sudo apt install ffmpeg", "Darwin": "brew install ffmpeg"}.get(
        platform.system(), "winget install Gyan.FFmpeg")
    report.append(("ffmpeg", bool(exe), exe or f"missing - install with: {hint}"))


def ensure_voice(check, report):
    have = (VOICES / f"{VOICE}.onnx").exists()
    if not have and not check and importlib.util.find_spec("piper") is not None:
        VOICES.mkdir(parents=True, exist_ok=True)
        run([sys.executable, "-m", "piper.download_voices", "--download-dir", VOICES, VOICE])
        have = (VOICES / f"{VOICE}.onnx").exists()
    report.append((f"voice {VOICE}", have, str(VOICES) if have else "missing (needs piper-tts first)"))


def ensure_kokoro(check, report):
    """Optional: installed apart from the required packages so its failure cannot block them."""
    have = importlib.util.find_spec("kokoro_onnx") is not None
    if not have and not check:
        pip_install("kokoro-onnx")
        have = importlib.util.find_spec("kokoro_onnx") is not None
    report.append((KOKORO, have, "installed" if have else "missing: kokoro-onnx"))
    missing = [f for f in KOKORO_FILES if not (KOKORO_DIR / f).exists()]
    if missing and have and not check:
        KOKORO_DIR.mkdir(parents=True, exist_ok=True)
        for f in missing:
            print(f"  downloading {KOKORO_URL}{f}")
            part = KOKORO_DIR / f"{f}.part"  # renamed when complete, so a broken download is not used
            try:
                urllib.request.urlretrieve(KOKORO_URL + f, part)
                part.replace(KOKORO_DIR / f)
            except OSError as e:
                print(f"  download failed: {e}")
        missing = [f for f in KOKORO_FILES if not (KOKORO_DIR / f).exists()]
    report.append((f"{KOKORO} model", not missing,
                   str(KOKORO_DIR) if not missing else f"missing: {', '.join(missing)}"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="report only, install nothing")
    a = ap.parse_args()
    report = []
    if ensure_python(report):
        ensure_pip(a.check, report)
        ensure_ffmpeg(a.check, report)
        ensure_voice(a.check, report)
        ensure_kokoro(a.check, report)
    print()
    for name, ok, detail in report:
        print(f"  [{'ok' if ok else 'MISSING'}] {name}: {detail}")
    if not all(ok for name, ok, _ in report if name.startswith(KOKORO)):
        print("\n  Kokoro is unavailable - videos will be narrated by Piper")
    ready = all(ok for name, ok, _ in report if not name.startswith(KOKORO))
    print("\nready" if ready else "\nNOT ready - fix the MISSING items above")
    sys.exit(0 if ready else 1)


if __name__ == "__main__":
    main()
