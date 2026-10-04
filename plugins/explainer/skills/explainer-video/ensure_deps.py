"""Check, and install when missing, everything make_explainer.py needs.

Usage:  python ensure_deps.py [--check]      (--check: report only, install nothing)

Installs:
  manim, piper-tts   pip install --user
  ffmpeg             winget (Windows) / brew (macOS); on Linux prints the apt command (needs sudo)
  Piper voice        downloaded to ~/.cache/piper-voices
Exit code 0 = ready; 1 = something is still missing (the report says what and how to fix it).
"""
import argparse
import importlib.util
import platform
import shutil
import subprocess
import sys
from pathlib import Path

VOICE = "en_US-lessac-medium"
VOICES = Path.home() / ".cache" / "piper-voices"
PIP_PACKAGES = {"manim": "manim", "piper": "piper-tts"}
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


def ensure_pip(check, report):
    missing = [pkg for mod, pkg in PIP_PACKAGES.items() if importlib.util.find_spec(mod) is None]
    if missing and not check:
        in_venv = sys.prefix != sys.base_prefix  # --user is refused inside a venv
        run([sys.executable, "-m", "pip", "install", *([] if in_venv else ["--user"]), "--quiet", *missing])
        importlib.invalidate_caches()
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="report only, install nothing")
    a = ap.parse_args()
    report = []
    if ensure_python(report):
        ensure_pip(a.check, report)
        ensure_ffmpeg(a.check, report)
        ensure_voice(a.check, report)
    print()
    for name, ok, detail in report:
        print(f"  [{'ok' if ok else 'MISSING'}] {name}: {detail}")
    ready = all(ok for _, ok, _ in report)
    print("\nready" if ready else "\nNOT ready - fix the MISSING items above")
    sys.exit(0 if ready else 1)


if __name__ == "__main__":
    main()
