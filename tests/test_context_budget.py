"""Exercise the documented function slice on inert disassembly text only."""
from pathlib import Path
import re
import shlex
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


class FunctionExtraction(unittest.TestCase):
    def extract(self, listing):
        reference = ROOT / "skills/hack/references/context-budget.md"
        commands = [
            shlex.split(block)
            for block in re.findall(r"^```sh\n(.*?)^```", reference.read_text(), re.M | re.S)
            if block.lstrip().startswith("awk ")
        ]
        self.assertEqual(len(commands), 1)
        command = commands[0]
        self.assertEqual(command[0], "awk")
        self.assertEqual(len(command), 3)
        self.assertEqual(command[2], "work/bin/target.asm")
        # Run only this reviewed awk program against stdin, without a shell,
        # objdump, a real binary, or access to a target file.
        return subprocess.run(
            command[:2], input=listing, text=True, capture_output=True,
            check=True, timeout=5,
        ).stdout

    def test_keeps_reachable_block_after_early_return_and_excludes_neighbors(self):
        listing = (ROOT / "tests/fixtures/binary/multi-exit.asm").read_text()
        expected = listing[listing.index("0000000000001000 <check_auth>:"):]
        expected = expected[:expected.index("0000000000001010 <next_function>:")]
        self.assertEqual(self.extract(listing), expected)

    def test_keeps_final_symbol_at_eof_without_zero_padded_address(self):
        listing = "ABCD <check_auth>:\n    abcd: nop\n    abce: ret\n"
        self.assertEqual(self.extract(listing), listing)

    def test_absent_symbol_produces_no_unrelated_slice(self):
        listing = "0000000000001010 <next_function>:\n    1010: ret\n"
        self.assertEqual(self.extract(listing), "")


if __name__ == "__main__":
    unittest.main()
