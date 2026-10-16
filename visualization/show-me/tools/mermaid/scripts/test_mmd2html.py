#!/usr/bin/env python3
"""Generated viewers and renderer caches belong in the OS temporary directory."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import mmd2html


class TemporaryOutputTests(unittest.TestCase):
    def test_unix_prefers_tmpdir_and_falls_back_to_tmp(self):
        with patch("mmd2html.os.name", "posix"), patch.dict(os.environ, {"TMPDIR": "/chosen-temp"}, clear=True):
            self.assertEqual(mmd2html.temporary_root(), "/chosen-temp")
        with patch("mmd2html.os.name", "posix"), patch.dict(os.environ, {}, clear=True):
            self.assertEqual(mmd2html.temporary_root(), "/tmp")

    def test_windows_uses_temp(self):
        with patch("mmd2html.os.name", "nt"), patch.dict(os.environ, {"TEMP": "C:\\Temp"}, clear=True):
            self.assertEqual(mmd2html.temporary_root(), "C:\\Temp")

    def test_default_output_and_resources_use_unique_temporary_directories(self):
        with tempfile.TemporaryDirectory(prefix="show-me-output-test-") as temp:
            root = Path(temp)
            inputs = root / "inputs"
            inputs.mkdir()
            outputs = root / "temporary outputs"
            outputs.mkdir()
            source = inputs / "sequence.mmd"
            source.write_text("sequenceDiagram\nA->>B: hello\n")
            renderer = inputs / "mermaid.min.js"
            renderer.write_text("/* packaging fixture */")
            env = {**os.environ, "TMPDIR": str(outputs), "TEMP": str(outputs)}
            for _ in range(2):
                subprocess.run([
                    sys.executable, "-B", str(Path(mmd2html.__file__)), str(source),
                    "--mermaid", str(renderer),
                ], check=True, capture_output=True, text=True, env=env)
            results = list(outputs.glob("show-me-*/sequence.html"))
            self.assertEqual(len(results), 2)
            self.assertFalse((inputs / "sequence.html").exists())
            for result in results:
                self.assertIn("A->>B: hello", result.read_text())
                self.assertEqual((result.parent / "mermaid.min.js").read_bytes(), renderer.read_bytes())

    def test_renderer_cache_is_under_temporary_root(self):
        self.assertEqual(mmd2html.CACHE_DIR.parent, Path(mmd2html.temporary_root()))

    def test_explicit_output_path_is_honored(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "flow.mmd"
            source.write_text("flowchart LR\nA-->B\n")
            renderer = root / "renderer.js"
            renderer.write_text("/* packaging fixture */")
            output = root / "chosen destination" / "diagram.html"
            subprocess.run([
                sys.executable, "-B", str(Path(mmd2html.__file__)), str(source),
                "--mermaid", str(renderer), "-o", str(output),
            ], check=True, capture_output=True, text=True)
            self.assertTrue(output.is_file())
            self.assertTrue((output.parent / "mermaid.min.js").is_file())


if __name__ == "__main__":
    unittest.main()
