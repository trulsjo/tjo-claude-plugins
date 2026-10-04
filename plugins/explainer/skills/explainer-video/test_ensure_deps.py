"""Self-check for the Kokoro model repair.  Run: python test_ensure_deps.py  (needs kokoro-onnx)"""
import contextlib
import importlib.util
import io
import sys
import tempfile
from pathlib import Path

import ensure_deps as m

GARBAGE = dict.fromkeys(m.KOKORO_FILES, "garbage")
HEALTHY = dict.fromkeys(m.KOKORO_FILES, "healthy")


def fake_load_problem():
    """Stands in for the model load: a file loads when its text is 'healthy'."""
    bad = [f for f in m.KOKORO_FILES if (m.KOKORO_DIR / f).read_text() != "healthy"]
    return f"InvalidProtobuf: {bad[0]}" if bad else None


def model_line(check, files, serves="healthy", load_problem=fake_load_problem,
               import_problem=lambda: None):
    """Run ensure_kokoro on a model dir holding `files` (name -> text), where a download writes
    the text `serves`. Returns (ok, detail) of the model line, and the files downloaded."""
    real = m.KOKORO_DIR, m.download_kokoro_file, m.kokoro_load_problem, m.kokoro_import_problem
    downloads = []

    def fake_download(f):
        downloads.append(f)
        (m.KOKORO_DIR / f).write_text(serves)

    with tempfile.TemporaryDirectory() as d:
        m.KOKORO_DIR, m.download_kokoro_file = Path(d), fake_download
        m.kokoro_load_problem, m.kokoro_import_problem = load_problem, import_problem
        try:
            for name, text in files.items():
                (m.KOKORO_DIR / name).write_text(text)
            report = []
            with contextlib.redirect_stdout(io.StringIO()):
                m.ensure_kokoro(check, report)
        finally:
            (m.KOKORO_DIR, m.download_kokoro_file, m.kokoro_load_problem,
             m.kokoro_import_problem) = real
    (_, ok, detail), = [line for line in report if line[0].endswith("model")]
    return ok, detail, downloads


def test_check_reports_a_model_that_does_not_load():
    # the real load, on real garbage: MISSING, with the loader's reason, and nothing downloaded
    ok, detail, downloads = model_line(True, GARBAGE, load_problem=m.kokoro_load_problem)
    assert not ok and detail.startswith("does not load (") and len(detail) > 20, detail
    assert downloads == [], "check-only mode downloads nothing"


def test_install_downloads_a_model_that_does_not_load():
    ok, detail, downloads = model_line(False, GARBAGE)
    assert ok and sorted(downloads) == sorted(m.KOKORO_FILES), (detail, downloads)
    # one broken file is enough
    broken_voices = {**HEALTHY, m.KOKORO_FILES[1]: "garbage"}
    ok, detail, downloads = model_line(False, broken_voices)
    assert ok and downloads, (detail, downloads)


def test_healthy_model_is_not_downloaded():
    for check in (True, False):
        ok, detail, downloads = model_line(check, HEALTHY)
        assert ok and downloads == [], (check, detail, downloads)


def test_missing_file_is_downloaded_alone():
    name = m.KOKORO_FILES[0]
    ok, detail, downloads = model_line(True, {name: "healthy"})
    assert not ok and m.KOKORO_FILES[1] in detail and downloads == [], detail
    ok, detail, downloads = model_line(False, {name: "healthy"})
    assert ok and downloads == [m.KOKORO_FILES[1]], (detail, downloads)
    # one file missing and the other broken: repaired in one run, each file downloaded once
    ok, detail, downloads = model_line(False, {name: "garbage"})
    assert ok and sorted(downloads) == sorted(m.KOKORO_FILES), (detail, downloads)


def test_broken_install_downloads_nothing():
    # kokoro-onnx is installed but its import fails: the model is not at fault
    ok, detail, downloads = model_line(False, GARBAGE, import_problem=lambda: "ImportError: DLL")
    assert not ok and "cannot be imported (ImportError: DLL)" in detail, detail
    assert downloads == []


def test_model_still_broken_after_download_stays_optional():
    ok, detail, downloads = model_line(False, GARBAGE, serves="garbage")
    assert not ok and "does not load" in detail and len(downloads) == 2, (detail, downloads)
    # the whole step still ends in `ready`, and says Piper will narrate
    real = m.ensure_kokoro, m.ensure_pip, m.ensure_ffmpeg, m.ensure_voice, sys.argv

    def nothing(check, report):
        pass

    m.ensure_pip = m.ensure_ffmpeg = m.ensure_voice = nothing
    m.ensure_kokoro = lambda check, report: report.append((f"{m.KOKORO} model", ok, detail))
    sys.argv = ["ensure_deps.py"]
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            m.main()
        raise AssertionError("main() must exit")
    except SystemExit as e:
        assert e.code == 0, out.getvalue()
    finally:
        m.ensure_kokoro, m.ensure_pip, m.ensure_ffmpeg, m.ensure_voice, sys.argv = real
    lines = out.getvalue().splitlines()
    assert "ready" in lines and any("narrated by Piper" in line for line in lines), lines
    assert any("[MISSING]" in line and "does not load" in line for line in lines), lines


if __name__ == "__main__":
    assert importlib.util.find_spec("kokoro_onnx"), "these checks need kokoro-onnx installed"
    test_check_reports_a_model_that_does_not_load()
    test_install_downloads_a_model_that_does_not_load()
    test_healthy_model_is_not_downloaded()
    test_missing_file_is_downloaded_alone()
    test_broken_install_downloads_nothing()
    test_model_still_broken_after_download_stays_optional()
    print("ok")
