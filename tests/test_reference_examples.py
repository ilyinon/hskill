"""Offline checks for mathematical examples; no network or exploit execution.

Only explicitly named arithmetic helpers are extracted from reviewed examples.
Run: python3 -m unittest discover -s tests -v
"""
import ast
from pathlib import Path
import random
import re
import struct
import unittest
import zlib

ROOT = Path(__file__).resolve().parents[1] / "skills"
SAFE_CALLS = {
    "range", "zip", "bytes", "bytearray", "len", "any", "ValueError",
    "_undo_right_xor", "_undo_left_xor_mask", "untemper",
}


def load_helpers(topic, names):
    selected = {}
    for path in sorted((ROOT / topic).rglob("*.md")):
        for source in re.findall(r"^```python\s*\n(.*?)^```\s*$", path.read_text(), re.M | re.S):
            if not any(f"def {name}(" in source for name in names):
                continue
            tree = ast.parse(source)
            for node in tree.body:
                if not isinstance(node, ast.FunctionDef) or node.name not in names:
                    continue
                if node.decorator_list:
                    raise ValueError("Decorated examples are not allowed in this offline check")
                for child in ast.walk(node):
                    if isinstance(child, (ast.Import, ast.ImportFrom, ast.Attribute)):
                        raise ValueError("Only standalone arithmetic helpers are allowed")
                    if isinstance(child, ast.Call) and (not isinstance(child.func, ast.Name) or child.func.id not in SAFE_CALLS):
                        raise ValueError("Unexpected call in reference helper")
                selected[node.name] = node
    if set(selected) != set(names):
        raise ValueError(f"Missing helper definitions: {set(names) - set(selected)}")
    safe = {name: value for name, value in {
        "range": range, "zip": zip, "bytes": bytes, "bytearray": bytearray,
        "len": len, "any": any, "ValueError": ValueError,
    }.items()}
    namespace = {"__builtins__": safe}
    module = ast.Module(body=list(selected.values()), type_ignores=[])
    exec(compile(module, "<reviewed arithmetic helpers>", "exec"), namespace)
    return namespace


class ReferenceExamples(unittest.TestCase):
    def test_mt_tempering_round_trip(self):
        helpers = load_helpers("symmetric-cipher-attacks", ["_undo_right_xor", "_undo_left_xor_mask", "untemper", "clone_mt"])
        rng = random.Random(8675309)
        for value in [0, 1, 0xFFFFFFFF, 0x80000000] + [rng.getrandbits(32) for _ in range(1000)]:
            y = value ^ (value >> 11)
            y ^= (y << 7) & 0x9D2C5680
            y ^= (y << 15) & 0xEFC60000
            y ^= y >> 18
            self.assertEqual(helpers["untemper"](y), value)

    def test_mt_clone_predicts_independent_future_outputs(self):
        helpers = load_helpers("symmetric-cipher-attacks", ["_undo_right_xor", "_undo_left_xor_mask", "untemper", "clone_mt"])
        original = random.Random(1234567)
        observed = [original.getrandbits(32) for _ in range(624)]
        clone = random.Random()
        clone.setstate((3, tuple(helpers["clone_mt"](observed) + [624]), None))
        self.assertEqual([clone.getrandbits(32) for _ in range(100)], [original.getrandbits(32) for _ in range(100)])

    def test_cbc_previous_block_and_iv_layout(self):
        helpers = load_helpers("symmetric-cipher-attacks", ["cbc_bitflip", "cbc_multibyte_flip"])
        ct = bytes(range(48))
        modified = helpers["cbc_bitflip"](ct, 16, 22, 0x30, 0x31)
        # CBC P_i = D(C_i) XOR C_(i-1): unchanged target ciphertext
        # and one flipped previous byte imply exactly the desired delta.
        self.assertEqual(modified[16:], ct[16:])
        self.assertEqual(bytes(a ^ b for a, b in zip(ct, modified)), b"\0" * 6 + b"\1" + b"\0" * 41)
        with self.assertRaises(ValueError):
            helpers["cbc_bitflip"](ct, 16, 0, 0, 1)
        with self.assertRaises(ValueError):
            helpers["cbc_multibyte_flip"](ct, 16, [(16, 0, 1), (32, 0, 1)])

    def test_png_ihdr_dimension_recovery_layout(self):
        matches = []
        for path in (ROOT / "steganography-techniques").rglob("*.md"):
            text = path.read_text()
            if "ihdr = data[" in text:
                matches.append(text)
        self.assertEqual(len(matches), 1)
        text = matches[0]
        payload = struct.pack(">IIBBBBB", 5, 7, 8, 2, 0, 0, 0)
        crc = zlib.crc32(b"IHDR" + payload) & 0xFFFFFFFF
        altered = struct.pack(">II", 1, 1) + payload[8:]
        data = b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR" + altered + struct.pack(">I", crc)
        assignments = [re.search(r"^\s*(ihdr = data\[[^\n]+)", text, re.M).group(1),
                       re.search(r"^\s*(new_ihdr = struct.pack[^\n]+)", text, re.M).group(1)]
        namespace = {"data": data, "w": 5, "h": 7, "struct": struct, "__builtins__": {}}
        for statement in assignments:
            exec(compile(statement, "<reviewed PNG layout>", "exec"), namespace)
        self.assertEqual(namespace["new_ihdr"], payload)
        self.assertEqual(zlib.crc32(b"IHDR" + namespace["new_ihdr"]) & 0xFFFFFFFF, crc)


if __name__ == "__main__":
    unittest.main()
