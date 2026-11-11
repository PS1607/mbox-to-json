"""An empty MBOX must still produce an (empty) output file, not silence."""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.main import main  # noqa: E402


def run_main(*args, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["mbox-to-json", *args])
    main()


def test_empty_mbox_writes_empty_json(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    mbox = tmp_path / "empty.mbox"
    mbox.write_bytes(b"")
    out = tmp_path / "out.json"
    run_main(str(mbox), "-o", str(out), monkeypatch=monkeypatch)
    assert out.exists()
    assert json.loads(out.read_text()) == []


def test_single_message_mbox_still_works(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    mbox = tmp_path / "one.mbox"
    mbox.write_text(
        "From nobody@example.com Mon Nov 10 00:00:00 2026\n"
        "From: nobody@example.com\n"
        "Subject: hi\n"
        "\n"
        "hello\n"
    )
    out = tmp_path / "one.json"
    run_main(str(mbox), "-o", str(out), monkeypatch=monkeypatch)
    assert out.exists()
    records = json.loads(out.read_text())
    assert len(records) == 1
