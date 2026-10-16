"""Check reviewed offline fixtures. ELF/PCAP are parsed, never executed."""
import copy
import importlib.util
import json
from pathlib import Path
import struct
import unittest
import zlib

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def load_fixture(name):
    path = FIXTURES / name
    spec = importlib.util.spec_from_file_location("reviewed_fixture", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class OfflineFixtures(unittest.TestCase):
    def test_same_subject_authorization_and_secure_control(self):
        module = load_fixture("authz/handlers.py")
        alice = {"user": "alice", "tenant": "A"}
        self.assertEqual(module.read_invoice(alice, "a1")[0], 200)
        self.assertEqual(module.read_invoice(alice, "b1")[1]["owner"], "bob")
        self.assertEqual(module.read_invoice_checked(alice, "b1")[0], 403)
        self.assertEqual(module.read_invoice_checked(None, "a1")[0], 401)

    def test_ssrf_source_has_no_destination_check(self):
        module = load_fixture("ssrf/preview.py")
        calls = []
        def fake_fetch(url):
            calls.append(url)
            return "fixture content"
        module.preview("https://other.example.invalid/private", fake_fetch)
        self.assertEqual(calls, ["https://other.example.invalid/private"])

    def test_jwt_signature_and_algorithm_controls(self):
        module = load_fixture("jwt/verifier.py")
        tokens = json.loads((FIXTURES / "jwt/tokens.json").read_text())
        self.assertEqual(module.verify(tokens["baseline"])["role"], "user")
        self.assertIsNone(module.verify(tokens["changed_claim_same_signature"]))
        self.assertIsNone(module.verify(tokens["unsigned"]))
        self.assertIsNone(module.verify("not-a-token"))

    def test_pkce_binds_code_to_pending_session_and_is_single_use(self):
        module = load_fixture("oauth/callback.py")
        data = json.loads((FIXTURES / "oauth/transactions.json").read_text())
        grants = copy.deepcopy(data["issued"])
        self.assertIsNone(module.callback("alice-session", "bob-code", data["pending"], grants))
        self.assertFalse(grants["bob-code"]["used"])
        self.assertEqual(module.callback("alice-session", "alice-code", data["pending"], grants), "alice")
        self.assertIsNone(module.callback("alice-session", "alice-code", data["pending"], grants))

    def test_pcap_contains_one_dns_query_without_a_reply(self):
        data = (FIXTURES / "pcap/dns-query.pcap").read_bytes()
        magic, major, minor, _, _, _, linktype = struct.unpack("<IHHIIII", data[:24])
        self.assertEqual((magic, major, minor, linktype), (0xA1B2C3D4, 2, 4, 1))
        _, _, captured, original = struct.unpack("<IIII", data[24:40])
        self.assertEqual(captured, original)
        self.assertEqual(len(data), 40 + captured)
        frame = data[40:]
        self.assertEqual(frame[12:14], b"\x08\x00")
        self.assertEqual(frame[23], 17)  # IPv4 UDP
        _, destination_port, _, _ = struct.unpack("!HHHH", frame[34:42])
        self.assertEqual(destination_port, 53)
        _, flags, questions, answers, _, _ = struct.unpack("!HHHHHH", frame[42:54])
        self.assertEqual((flags & 0x8000, questions, answers), (0, 1, 0))

    def test_elf_header_matches_static_exercise(self):
        data = (FIXTURES / "binary/minimal.elf").read_bytes()
        self.assertEqual(data[:7], b"\x7fELF\x02\x01\x01")
        self.assertEqual(struct.unpack_from("<H", data, 18)[0], 62)
        entry, phoff = struct.unpack_from("<QQ", data, 24)
        self.assertEqual(phoff, 64)
        kind, flags, offset, virtual, _, size, _, _ = struct.unpack_from("<IIQQQQQQ", data, phoff)
        self.assertEqual((kind, flags, offset, size), (1, 5, 0, len(data)))
        self.assertEqual(data[entry - virtual:], bytes.fromhex("b83c00000031ff0f05"))

    def test_damaged_png_has_unique_small_crc_dimension_solution(self):
        data = (FIXTURES / "crypto/damaged.png").read_bytes()
        stored_crc = struct.unpack(">I", data[29:33])[0]
        matches = []
        for width in range(1, 17):
            for height in range(1, 17):
                payload = struct.pack(">II", width, height) + data[24:29]
                if zlib.crc32(b"IHDR" + payload) & 0xFFFFFFFF == stored_crc:
                    matches.append((width, height))
        self.assertEqual(matches, [(5, 7)])
        size = struct.unpack(">I", data[33:37])[0]
        self.assertEqual(data[37:41], b"IDAT")
        self.assertEqual(len(zlib.decompress(data[41:41 + size])), 7 * (1 + 5 * 3))
