"""Check the observable controls in the synthetic analysis fixtures."""
import datetime
from html.parser import HTMLParser
from io import BytesIO
import json
from pathlib import Path
import struct
from tempfile import TemporaryDirectory
import unittest
from urllib.parse import urljoin
import zipfile
import zlib

from scripts import eval_skills

FIXTURES = Path(__file__).resolve().parent / "fixtures"


class Gallery(HTMLParser):
    def __init__(self):
        super().__init__()
        self.base = None
        self.assets = []
        self.published = None

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "base":
            self.base = attrs["href"]
        elif tag in {"a", "img"}:
            self.assets.append(attrs["href" if tag == "a" else "src"])
        elif tag == "time":
            self.published = attrs["datetime"]


class AnalysisFixtures(unittest.TestCase):
    def test_archive_has_distinct_dates_and_a_non_image_replay(self):
        root = FIXTURES / "osint/archives"
        gallery = Gallery()
        gallery.feed((root / "page.html").read_text())
        captures = json.loads((root / "captures.json").read_text())
        assets = {urljoin(gallery.base, asset) for asset in gallery.assets}
        self.assertEqual(assets, {row["original"] for row in captures["assets"]})
        page = captures["page"]
        full_image = next(row for row in captures["assets"] if row.get("saved_body") == "replay/f2.jpg")
        jpeg = (root / full_image["saved_body"]).read_bytes()
        self.assertTrue(jpeg.startswith(b"\xff\xd8") and jpeg.endswith(b"\xff\xd9"))
        self.assertLess(gallery.published, page["requested_capture_utc"][:10])
        self.assertLess(page["requested_capture_utc"], page["effective_capture_utc"])
        self.assertLess(page["effective_capture_utc"], full_image["effective_capture_utc"])
        failed = next(row for row in captures["assets"] if row["lookup"] == "replay_error")
        self.assertEqual(failed["http_status"], 200)
        self.assertTrue((root / failed["saved_body"]).read_bytes().startswith(b"<!doctype html>"))

    def test_analysis_cases_export_requests_and_artifacts_without_rubrics(self):
        cases = [
            case for case in eval_skills.read_manifest()["cases"]
            if case["id"].startswith(("osint-", "forensics-"))
        ]
        self.assertEqual(len(cases), 6)
        with TemporaryDirectory() as temporary:
            output = Path(temporary) / "blind"
            prepared = eval_skills.prepare(output, [case["id"] for case in cases])
            self.assertEqual(len(prepared), len(cases))
            for case in cases:
                folder = output / case["id"]
                self.assertEqual({path.name for path in folder.iterdir()}, {"request.md", "artifacts"})
                for artifact in case["artifacts"]:
                    original = Path(artifact).relative_to("tests/fixtures")
                    self.assertEqual((folder / "artifacts" / original).read_bytes(), (FIXTURES / original).read_bytes())
                request = (folder / "request.md").read_text()
                self.assertEqual(request, case["request"] + "\n\n" + eval_skills.OFFLINE_INSTRUCTION + "\n")
                for criterion in case["criteria"].values():
                    self.assertNotIn(criterion, request)

    def test_truncated_capture_retains_request_line_in_sequence_order(self):
        data = (FIXTURES / "forensics/truncated-stream.pcap").read_bytes()
        self.assertEqual(data[:4], b"\xd4\xc3\xb2\xa1")
        cursor = 24
        records = []
        while cursor < len(data):
            _, _, captured, original = struct.unpack_from("<IIII", data, cursor)
            start = cursor + 16
            end = start + captured
            frame = data[start:end]
            self.assertEqual(len(frame), captured)
            self.assertEqual(frame[12:14], b"\x08\x00")
            ip_header = (frame[14] & 15) * 4
            tcp = 14 + ip_header
            seq = struct.unpack_from("!I", frame, tcp + 4)[0]
            payload = tcp + (frame[tcp + 12] >> 4) * 4
            records.append((captured, original, seq, frame[payload:], frame[26:34]))
            cursor = end
        first, second = records
        self.assertEqual(first[:2], (83, 101))
        self.assertEqual(second[:2], (62, 62))
        self.assertEqual(first[4], second[4])
        self.assertEqual(second[2] + len(second[3]), first[2])
        request = second[3] + first[3]
        self.assertEqual(request.split(b"\r\n", 1)[0], b"GET /status HTTP/1.1")
        self.assertNotIn(b"\r\n\r\n", request)

    def test_partial_memory_records_require_more_than_pid(self):
        data = json.loads((FIXTURES / "forensics/partial-memory-records.json").read_text())
        first, missing = data["connections"]
        def clock(value):
            return datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))

        time = clock(first["opened"])
        candidates = [row for row in data["processes"] if row["pid"] == first["pid"]]
        matches = [row for row in candidates if clock(row["created"]) <= time
                   and (row["exited"] is None or time < clock(row["exited"]))]
        self.assertEqual([row["object"] for row in matches], [first["owner_object"]])
        self.assertEqual([row["name"] for row in matches], ["indexer"])
        self.assertEqual(missing["pid"], first["pid"])
        self.assertIsNone(missing["opened"])
        self.assertIsNone(missing["owner_object"])
        self.assertEqual(len(candidates), 2)
        self.assertNotEqual(data["symbol_check"]["module_scan"], data["symbol_check"]["inventory"])

    def test_png_decoy_signature_precedes_a_validated_zip_tail(self):
        data = (FIXTURES / "forensics/poster.png").read_bytes()
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        position = 8
        while position < len(data):
            size, kind = struct.unpack_from(">I4s", data, position)
            start = position + 8
            end = start + size
            checksum, = struct.unpack_from(">I", data, end)
            self.assertEqual(checksum, zlib.crc32(data[position + 4:end]))
            position = end + 4
            if kind == b"IEND":
                break
        else:
            self.fail("missing PNG end chunk")
        self.assertLess(data.index(b"PK\x03\x04"), position)
        self.assertEqual(data[position:position + 4], b"PK\x03\x04")
        with zipfile.ZipFile(BytesIO(data[position:])) as archive:
            self.assertIsNone(archive.testzip())
            self.assertEqual(archive.namelist(), ["inventory.txt"])
            self.assertEqual(archive.read("inventory.txt"), b"Inventory marker: harbor-63\n")
