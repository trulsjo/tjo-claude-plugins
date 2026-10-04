"""Self-check for the Kokoro model check and repair.  Run: python test_ensure_deps.py  (needs kokoro-onnx)"""
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
               import_problem=lambda: None, installed=True, between=()):
    """Run ensure_kokoro on a model dir holding `files` (name -> text), where a download writes
    the text `serves`. Returns (ok, detail) of the model line, and the files downloaded.
    `check` may be a tuple: one run each on the same dir, with `between[i]()` called after run i;
    the result is that of the last run. `installed=False` stands for a missing kokoro-onnx."""
    real = (m.KOKORO_DIR, m.download_kokoro_file, m.kokoro_load_problem, m.kokoro_import_problem,
            m.pip_install, importlib.util.find_spec)
    downloads = []

    def fake_download(f):
        downloads.append(f)
        (m.KOKORO_DIR / f).write_text(serves)
        return True

    checks = check if isinstance(check, tuple) else (check,)
    with tempfile.TemporaryDirectory() as d:
        m.KOKORO_DIR, m.download_kokoro_file = Path(d), fake_download
        m.kokoro_load_problem, m.kokoro_import_problem = load_problem, import_problem
        if not installed:
            m.pip_install = lambda *packages: None
            importlib.util.find_spec = lambda name: None
        try:
            for name, text in files.items():
                (m.KOKORO_DIR / name).write_text(text)
            for i, one in enumerate(checks):
                if i:
                    between[i - 1]()
                del downloads[:]
                report = []
                with contextlib.redirect_stdout(io.StringIO()):
                    m.ensure_kokoro(one, report)
        finally:
            (m.KOKORO_DIR, m.download_kokoro_file, m.kokoro_load_problem, m.kokoro_import_problem,
             m.pip_install, importlib.util.find_spec) = real
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


def test_broken_install_after_a_download_is_not_recorded():
    # both files were missing and are downloaded, then the import fails: not a download that
    # "did not help", so the next run does not say so
    ok, detail, downloads = model_line((False, False), {}, between=[lambda: None],
                                       import_problem=lambda: "ImportError: DLL")
    assert not ok and "cannot be imported" in detail and "did not help" not in detail, detail


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


def test_download_that_did_not_help_is_not_repeated():
    def nothing():
        pass

    for second in (False, True):  # the record is honoured by install mode and by check-only mode
        ok, detail, downloads = model_line((False, second), GARBAGE, serves="garbage",
                                           between=[nothing])
        assert not ok and downloads == [], (detail, downloads)
        assert "does not load (InvalidProtobuf" in detail and "download did not help" in detail, detail
    # the run that did download says so too
    ok, detail, downloads = model_line(False, GARBAGE, serves="garbage")
    assert len(downloads) == 2 and "download did not help" in detail, (detail, downloads)


def test_changed_model_file_is_downloaded_again():
    def change():
        (m.KOKORO_DIR / m.KOKORO_FILES[0]).write_text("other garbage")

    ok, detail, downloads = model_line((False, False), GARBAGE, serves="garbage", between=[change])
    assert not ok and len(downloads) == 2, (detail, downloads)


def test_different_error_is_downloaded_again():
    def other_error():
        m.kokoro_load_problem = lambda: "RuntimeError: espeak"

    ok, detail, downloads = model_line((False, False), GARBAGE, serves="garbage",
                                       between=[other_error])
    assert not ok and len(downloads) == 2 and "espeak" in detail, (detail, downloads)


def test_model_that_loads_clears_the_record():
    def loads():
        m.kokoro_load_problem = lambda: None

    def fails():
        m.kokoro_load_problem = fake_load_problem

    # same files, same error as recorded - but it loaded in between, so the record is gone
    ok, detail, downloads = model_line((False, False, False), GARBAGE, serves="garbage",
                                       between=[loads, fails])
    assert not ok and len(downloads) == 2, (detail, downloads)


def test_check_writes_nothing():
    seen = []

    def listing():
        seen.append(sorted(p.name for p in m.KOKORO_DIR.iterdir()))

    model_line((True, True), GARBAGE, between=[listing])
    assert seen == [sorted(m.KOKORO_FILES)], seen

    # a check does not clear the record either: the run after it still downloads nothing
    def loads():
        m.kokoro_load_problem = lambda: None

    def fails():
        m.kokoro_load_problem = fake_load_problem

    ok, detail, downloads = model_line((False, True, False), GARBAGE, serves="garbage",
                                       between=[loads, fails])
    assert not ok and downloads == [], (detail, downloads)


def test_failed_download_is_not_recorded():
    tried = []

    def failing_download():
        m.download_kokoro_file = lambda f: bool(tried.append(f))

    # a check, then two install runs whose downloads fail: the second one tries again
    ok, detail, _ = model_line((True, False, False), GARBAGE,
                               between=[failing_download, tried.clear])
    assert not ok and len(tried) == 2 and "did not help" not in detail, (detail, tried)


def test_model_is_not_checked_without_kokoro_onnx():
    for check in (True, False):
        ok, detail, downloads = model_line(check, GARBAGE, installed=False)
        assert not ok and "not checked" in detail and "kokoro-onnx is missing" in detail, detail
        assert downloads == []
        # a missing file is still named, and still not downloaded
        ok, detail, downloads = model_line(check, {m.KOKORO_FILES[0]: "healthy"}, installed=False)
        assert not ok and m.KOKORO_FILES[1] in detail and downloads == [], (detail, downloads)


if __name__ == "__main__":
    assert importlib.util.find_spec("kokoro_onnx"), "these checks need kokoro-onnx installed"
    test_check_reports_a_model_that_does_not_load()
    test_install_downloads_a_model_that_does_not_load()
    test_healthy_model_is_not_downloaded()
    test_missing_file_is_downloaded_alone()
    test_broken_install_downloads_nothing()
    test_broken_install_after_a_download_is_not_recorded()
    test_model_still_broken_after_download_stays_optional()
    test_download_that_did_not_help_is_not_repeated()
    test_changed_model_file_is_downloaded_again()
    test_different_error_is_downloaded_again()
    test_model_that_loads_clears_the_record()
    test_check_writes_nothing()
    test_failed_download_is_not_recorded()
    test_model_is_not_checked_without_kokoro_onnx()
    print("ok")
