"""Standard-library contract tests for super-idea; no model access required."""

import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import uuid


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "gen_entropy.py"
SPEC = importlib.util.spec_from_file_location("gen_entropy", SCRIPT)
entropy = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(entropy)


class EntropyTests(unittest.TestCase):
    def cli(self, *args, cwd=None):
        return subprocess.run([sys.executable, "-I", "-S", str(SCRIPT), *args],
                              cwd=cwd, capture_output=True, text=True, check=False)

    def test_secure_sha256_source(self):
        raw = bytes(range(32))
        with patch.object(entropy.secrets, "token_bytes", return_value=raw) as source:
            payload = entropy.generate_payload(1)
        source.assert_called_once_with(32)
        self.assertEqual(payload["anchors"][0]["seed"], hashlib.sha256(raw).hexdigest())

    def test_secure_uuid4_source(self):
        seed = uuid.UUID("01234567-1234-4234-8234-123456789abc")
        with patch.object(entropy.uuid, "uuid4", return_value=seed) as source:
            payload = entropy.generate_payload(1, "uuid4")
        source.assert_called_once_with()
        self.assertEqual(payload["anchors"][0]["seed"], str(seed))

    def test_secure_hex_source(self):
        with patch.object(entropy.secrets, "token_hex", return_value="0123456789abcdef") as source:
            payload = entropy.generate_payload(1, "hex")
        source.assert_called_once_with(8)
        self.assertEqual(payload["anchors"][0]["seed"], "0123456789abcdef")

    def test_all_characters_map_to_exact_bank_entries(self):
        self.assertEqual(list(entropy.DIMENSIONS), ["domain", "mechanism", "sensory", "form"])
        for bank in entropy.DIMENSIONS.values():
            self.assertEqual(len(bank), 16)
            self.assertEqual(len(set(bank)), 16)
        for value in range(16):
            character = format(value, "x")
            with self.subTest(character=character), patch.object(entropy.secrets, "token_hex", return_value=character * 16):
                anchor = entropy.generate_payload(1, "hex")["anchors"][0]
                for position, (axis, bank) in enumerate(entropy.DIMENSIONS.items()):
                    binding = anchor["bindings"][axis]
                    self.assertEqual(binding, {"position": position, "character": character, "anchor": bank[value]})

    def test_positions_are_distinct_and_uuid_hyphens_removed(self):
        seed = uuid.UUID("01234567-1234-4234-8234-123456789abc")
        with patch.object(entropy.uuid, "uuid4", return_value=seed):
            anchor = entropy.generate_payload(1, "uuid4")["anchors"][0]
        for index, (axis, bank) in enumerate(entropy.DIMENSIONS.items()):
            self.assertEqual(anchor["bindings"][axis]["anchor"], bank[index])

    def test_cli_kinds_formats_counts_and_seed_validity(self):
        for kind in ("sha256", "uuid4", "hex"):
            for fmt in ("text", "json"):
                with self.subTest(kind=kind, format=fmt):
                    result = self.cli("--count", "4", "--kind", kind, "--format", fmt)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stderr, "")
                    if fmt == "json":
                        payload = json.loads(result.stdout)
                        self.assertEqual(payload["schema_version"], 1)
                        self.assertEqual(payload["kind"], kind)
                        self.assertEqual(len(payload["anchors"]), 4)
                        for i, anchor in enumerate(payload["anchors"], 1):
                            self.assertEqual(anchor["id"], f"S{i:02d}")
                            seed = anchor["seed"]
                            if kind == "uuid4":
                                self.assertEqual(uuid.UUID(seed).version, 4)
                            else:
                                self.assertEqual(len(seed), 64 if kind == "sha256" else 16)
                                self.assertTrue(all(c in "0123456789abcdef" for c in seed))
                    else:
                        self.assertTrue(result.stdout.startswith("[SUPER_IDEA_ENTROPY_PAYLOAD]\n"))
                        self.assertTrue(result.stdout.endswith("[/SUPER_IDEA_ENTROPY_PAYLOAD]\n"))
                        self.assertEqual(result.stdout.count(" seed="), 4)

    def test_default_four_sha256_anchors(self):
        result = self.cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("kind=sha256", result.stdout)
        self.assertEqual(result.stdout.count(" seed="), 4)

    def test_count_boundaries(self):
        for count in (1, 32):
            result = self.cli("-n", str(count), "--format", "json")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(len(json.loads(result.stdout)["anchors"]), count)

    def test_invalid_cli_inputs_fail_without_stdout(self):
        for args in (("-n", "0"), ("-n", "33"), ("-n", "-1"), ("-n", "1.5"),
                     ("-n", "abc"), ("-n",), ("--kind", "bad"), ("--format", "bad")):
            with self.subTest(args=args):
                result = self.cli(*args)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")

    def test_invalid_programmatic_inputs(self):
        for value in (0, 33, -1, True, 1.5, "4", None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                entropy.generate_payload(value)
        with self.assertRaises(ValueError):
            entropy.generate_payload(1, "bad")

    def test_random_source_failure_is_not_hidden(self):
        for kind, target, method in (("sha256", entropy.secrets, "token_bytes"),
                                     ("hex", entropy.secrets, "token_hex"),
                                     ("uuid4", entropy.uuid, "uuid4")):
            output = io.StringIO()
            with self.subTest(kind=kind), patch.object(target, method, side_effect=OSError("secure randomness unavailable")):
                with patch.object(sys, "argv", [str(SCRIPT), "--kind", kind]):
                    with contextlib.redirect_stdout(output), self.assertRaises(OSError):
                        entropy.main()
                self.assertEqual(output.getvalue(), "")

    def test_render_preserves_every_binding_and_seed(self):
        payload = entropy.generate_payload()
        rendered = entropy.render_payload(payload)
        self.assertIn(payload["instruction"], rendered)
        for anchor in payload["anchors"]:
            self.assertIn(anchor["id"], rendered)
            self.assertIn(anchor["seed"], rendered)
            for axis, binding in anchor["bindings"].items():
                self.assertIn(f"hex[{binding['position']}]={binding['character']} -> {axis}: {binding['anchor']}", rendered)

    def test_standalone_without_site_packages(self):
        with tempfile.TemporaryDirectory() as folder:
            result = self.cli("--format", "json", cwd=folder)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)["anchors"]), 4)

    def test_freshness_smoke_not_statistical_proof(self):
        for kind in ("sha256", "uuid4", "hex"):
            first = entropy.generate_payload(1, kind)["anchors"][0]["seed"]
            second = entropy.generate_payload(1, kind)["anchors"][0]["seed"]
            self.assertNotEqual(first, second)


if __name__ == "__main__":
    unittest.main()
