"""Exercise only the named, reviewed offline teaching models and their controls.

No network, browser, target service, ELF execution, or real transaction occurs.
The stack checker validates its abstract contract, not an executable exploit.
"""
import copy
from contextlib import closing
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import random
import sqlite3
import unittest

from test_reference_examples import load_helpers

SKILLS = Path(__file__).resolve().parents[1] / "skills"


def example(topic):
    folder = SKILLS / topic / "references/examples"
    data = json.loads((folder / "input.json").read_text())
    path = folder / "model.py"
    if not path.exists():
        return None, data
    spec = importlib.util.spec_from_file_location("reviewed_solving_model", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, data


class SolvingExamples(unittest.TestCase):
    def test_redirect_policy_at_each_hop(self):
        m, d = example("ssrf-server-side-request-forgery")
        host = d["policy"]["allowed_host"]
        self.assertEqual(m.preview(d["direct_control"], d["responses"], host)["status"], "denied")
        broken = m.preview(d["start"], d["responses"], host)
        self.assertEqual((broken["body"], broken["trace"][-1]), ("owned-fixture-marker", d["direct_control"]))
        fixed = m.preview(d["start"], d["responses"], host, True)
        self.assertEqual((fixed["status"], fixed["trace"]), ("denied", [d["start"]]))
        responses = {"https://docs.example.invalid/ok": {"body": "allowed"}}
        self.assertEqual(m.preview(next(iter(responses)), responses, host, True)["body"], "allowed")

    def test_bound_value_and_raw_sort_are_separate(self):
        m, d = example("sqli-sql-injection")
        with closing(sqlite3.connect(":memory:")) as db:
            db.execute("CREATE TABLE catalog (name TEXT, created INTEGER)")
            db.executemany("INSERT INTO catalog VALUES (?, ?)", d["rows"])
            self.assertEqual(m.names(db, d["term_probe"], "name"), [])
            self.assertEqual(m.names(db, "", "name"), ["anna", "bo", "zoe"])
            self.assertEqual(m.names(db, "", d["sort_probe"]), ["bo", "zoe", "anna"])
            with self.assertRaises(ValueError):
                m.names(db, "", d["sort_probe"], True)
            self.assertEqual(m.names(db, "", "created", True), ["bo", "zoe", "anna"])
            self.assertEqual(m.names(db, d["term_probe"], "name", True), [])

    def test_authorized_parent_does_not_authorize_foreign_child(self):
        m, d = example("idor-broken-object-authorization")
        args = (d["parents"], d["children"])
        alice = d["session"]
        self.assertEqual(m.attachment(alice, "pB", "cB", *args)[0], 403)
        self.assertEqual(m.attachment(alice, "pA", "cB", *args), (200, "bob fixture"))
        self.assertEqual(m.attachment(alice, "pA", "cB", *args, bind_child=True), (403, None))
        self.assertEqual(m.attachment(alice, "pA", "cA", *args, bind_child=True), (200, "alice fixture"))
        bob = {"user": "bob", "tenant": "B"}
        self.assertEqual(m.attachment(bob, "pB", "cB", *args, bind_child=True), (200, "bob fixture"))

    def test_request_idempotency_and_business_uniqueness(self):
        m, d = example("business-logic-vulnerabilities")
        for fixed, expected in [(False, 200), (True, 100)]:
            ledger, results = {}, {}
            for key in d["request_keys"]:
                m.refund(d["order"], key, ledger, results, fixed)
            self.assertEqual(sum(ledger.values()), expected)
            if fixed:
                m.refund({"id": "owned-order-2", "paid_cents": 30}, "other", ledger, results, True)
                self.assertEqual(sum(ledger.values()), 130)

    def test_valid_signature_is_not_recipient_authorization(self):
        m, d = example("jwt-oauth-token-attacks")
        baseline, foreign = m.issue(d["baseline_audience"]), m.issue(d["foreign_audience"])
        self.assertEqual(m.report(baseline, True)[0], 200)
        self.assertEqual(m.report(foreign)[1]["body"], "report fixture")
        self.assertEqual(m.report(foreign, True), (401, None))
        self.assertEqual(m.report(m.issue(["other", "reports"]), True)[0], 200)
        header, payload, signature = baseline.split(".")
        changed = m.decode(payload); changed["sub"] = "bob"
        self.assertEqual(m.report(header + "." + m.part(changed) + "." + signature)[0], 401)
        self.assertEqual(m.report(m.part({"alg": "none"}) + "." + payload + ".")[0], 401)

    def test_provider_subject_pair_preserves_local_identity(self):
        m, d = example("oauth-oidc-misconfiguration")
        accounts = {(a["iss"], a["sub"]): a["local"] for a in d["accounts"]}
        self.assertEqual(m.account(d["callback_claims"], accounts), "alice-local")
        self.assertEqual(m.account(d["callback_claims"], accounts, True), "bob-local")
        self.assertEqual(m.account({"iss": d["accounts"][0]["iss"], "sub": "42"}, accounts, True), "alice-local")
        self.assertIsNone(m.account({"iss": "https://unknown.example.invalid", "sub": "42"}, accounts, True))

    def test_alternate_html_text_sink_and_fix(self):
        class Parsed(HTMLParser):
            def __init__(self, html):
                super().__init__(); self.tags = []; self.text = []; self.feed(html)
            def handle_starttag(self, tag, attrs):
                self.tags.append(tag)
            def handle_data(self, data):
                self.text.append(data)
        m, d = example("xss-cross-site-scripting")
        normal = Parsed(m.main_page(d["value"]))
        legacy = Parsed(m.legacy_preview(d["value"]))
        fixed = Parsed(m.legacy_preview(d["value"], True))
        self.assertNotIn("b", normal.tags)
        self.assertIn("b", legacy.tags)
        self.assertNotIn("b", fixed.tags)
        self.assertEqual("".join(fixed.text), d["value"])

    def test_stack_contract_uses_actual_initial_position(self):
        m, d = example("stack-overflow-and-rop")
        args = (d["addresses"], d["expected_argument"], d["required_entry_rsp_mod_16"])
        original = d["original_words"]
        fixed = [d["addresses"]["ret"]] + original
        self.assertEqual(m.check(original, d["saved_rip_slot"], *args)["status"], "misaligned")
        self.assertEqual(m.check(fixed, d["saved_rip_slot"], *args)["status"], "marker")
        self.assertEqual(m.check(original, 40960, *args)["status"], "marker")
        self.assertEqual(m.check(fixed, 40960, *args)["status"], "misaligned")

    def test_mt_state_index_and_withheld_continuation(self):
        _, d = example("symmetric-cipher-attacks")
        h = load_helpers("symmetric-cipher-attacks", ["_undo_right_xor", "_undo_left_xor_mask", "untemper", "clone_mt"])
        words = h["clone_mt"](d["observed_words"])
        wrong = random.Random(); wrong.setstate((3, tuple(words + [0]), None))
        self.assertEqual(wrong.getrandbits(32), d["observed_words"][0])
        right = random.Random(); right.setstate((3, tuple(words + [624]), None))
        independent = random.Random(1729)
        self.assertEqual([independent.getrandbits(32) for _ in range(624)], d["observed_words"])
        self.assertEqual([right.getrandbits(32) for _ in range(20)], [independent.getrandbits(32) for _ in range(20)])

    def test_tcp_sequence_reassembly_and_missing_bytes(self):
        m, _ = example("traffic-analysis-pcap")
        path = SKILLS / "traffic-analysis-pcap/references/examples/request.pcap"
        rows = m.segments(path.read_bytes())
        self.assertGreater(rows[0][4], rows[1][4])
        stream = m.reassemble(rows)
        self.assertEqual(stream, b"GET /status HTTP/1.1\r\nHost: service.example.invalid\r\n\r\n")
        self.assertEqual(m.reassemble(rows + [rows[1]]), stream)
        gap = copy.deepcopy(rows); row = list(gap[0]); row[4] += 1; gap[0] = tuple(row)
        with self.assertRaisesRegex(ValueError, "gap"):
            m.reassemble(gap)
        conflict = list(rows[1]); conflict[5] = b"X" + conflict[5][1:]
        with self.assertRaisesRegex(ValueError, "overlap"):
            m.reassemble(rows + [tuple(conflict)])
        invalid = bytearray(path.read_bytes())
        invalid[40 + 14] = 0x4F  # Header exceeds the captured IP packet.
        invalid[40 + 16:40 + 18] = b"\x00\x28"
        with self.assertRaisesRegex(ValueError, "lengths"):
            m.segments(invalid)
        invalid = bytearray(path.read_bytes())
        invalid[40 + 14 + 20 + 12] = 0xF0  # TCP header exceeds IP total length.
        invalid[40 + 16:40 + 18] = b"\x00\x28"
        with self.assertRaisesRegex(ValueError, "lengths"):
            m.segments(invalid)
