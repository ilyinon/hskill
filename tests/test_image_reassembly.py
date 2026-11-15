import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile

try:
    import numpy
    from PIL import Image
except ImportError:
    numpy = Image = None


ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "skills/osint-media-search/scripts/reassemble_png.py"
FRAGMENTS = ROOT / "tests/fixtures/osint/identifier-chain/fragments.zip"
EXPECTED_RGB = "4c3f16b8097b720d586a25ea2c930bb2f175b22ce7dfb44bfa28e2489fbc013e"


@unittest.skipUnless(Image is not None, "image helper requires Pillow and NumPy")
class ReassemblePngTests(unittest.TestCase):
    def test_assembles_all_rotated_fragments_pixel_for_pixel(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "result.png"
            result = subprocess.run(
                [sys.executable, str(HELPER), str(FRAGMENTS), str(output)],
                capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            with Image.open(output) as image:
                hashes = {
                    hashlib.sha256(image.rotate(angle, expand=True).tobytes()).hexdigest()
                    for angle in (0, 90, 180, 270)
                }
            self.assertIn(EXPECTED_RGB, hashes)

    def test_missing_piece_is_reported_without_writing_an_image(self):
        with tempfile.TemporaryDirectory() as folder:
            partial = Path(folder) / "partial.zip"
            output = Path(folder) / "result.png"
            with ZipFile(FRAGMENTS) as full, ZipFile(partial, "w") as reduced:
                for name in full.namelist()[1:]:
                    reduced.writestr(name, full.read(name))
            result = subprocess.run(
                [sys.executable, str(HELPER), str(partial), str(output)],
                capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("assembly incomplete", result.stderr)
            self.assertFalse(output.exists())
