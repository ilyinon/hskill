"""Verify the independent observations used in the blind review cases."""
from collections import defaultdict
import json
from pathlib import Path
import unittest


FIXTURES = Path(__file__).resolve().parent / "fixtures" / "review"


def load(name):
    return json.loads((FIXTURES / name).read_text())


class ReviewFixtures(unittest.TestCase):
    def test_denied_tool_proposal_has_no_dispatch_or_commit(self):
        policy = load("dispatcher/policy.json")
        events = defaultdict(list)
        for event in load("dispatcher/events.json"):
            events[event["op"]].append(event)
        state = load("dispatcher/state.json")

        denied, allowed = events["12"], events["13"]
        protected = denied[0]["resource"]
        permitted = allowed[0]["resource"]
        self.assertIn(protected, policy["protected_notes"])
        self.assertNotIn(protected, policy["allowed_actions"][denied[0]["action"]])
        self.assertIn(permitted, policy["allowed_actions"][allowed[0]["action"]])
        self.assertEqual(
            [event["stage"] for event in denied],
            ["proposed", "authorization", "assistant_summary"],
        )
        self.assertEqual(denied[1]["decision"], "denied")
        self.assertEqual(
            [event["stage"] for event in allowed],
            ["proposed", "authorization", "dispatch", "commit"],
        )
        self.assertEqual(allowed[1]["decision"], "allowed")
        self.assertEqual(allowed[-1]["resource"], permitted)
        self.assertEqual(state["before"][protected], state["after"][protected])
        self.assertEqual(state["after"][permitted], allowed[-1]["revision"])
        self.assertGreater(state["after"][permitted], state["before"][permitted])

    def test_batch_preserves_object_scope_but_exposes_extra_field(self):
        policy = load("batch-authorization/policy.json")
        observations = load("batch-authorization/observed.json")
        allowed = observations["single_owned"]
        denied = observations["single_other_tenant"]
        owned = allowed["body"]
        batch = observations["mixed_batch"]
        self.assertTrue(all(row["principal"] == policy["principal"]
                            for row in (allowed, denied, batch)))
        self.assertEqual(allowed["status"], 200)
        self.assertEqual(denied["status"], 404)
        self.assertEqual(batch["requested"], [allowed["requested"], denied["requested"]])
        self.assertEqual(policy["record_tenants"][owned["id"]], policy["tenant"])
        self.assertNotEqual(policy["record_tenants"][denied["requested"]], policy["tenant"])
        self.assertEqual([record["id"] for record in batch["body"]], [owned["id"]])
        fields = set(policy["response_fields"])
        self.assertEqual(set(owned), fields)
        row = batch["body"][0]
        self.assertEqual({key: row[key] for key in fields}, owned)
        self.assertEqual(set(row) - fields, set(policy["restricted_fields"]))

    def test_conflicting_archive_versions_have_no_same_day_image(self):
        records = load("archive-versions/captures.json")
        page, asset = records["page"], records["asset"]
        html = (FIXTURES / "archive-versions" / page["saved_body"]).read_text()
        self.assertIn(f'src="{asset["original"]}"', html)
        self.assertEqual(asset["requested_date"], page["effective_capture_utc"][:10])
        self.assertEqual(asset["on_requested_date"], "no_saved_image")
        captures = asset["captures"]
        self.assertEqual(len(captures), 2)
        self.assertLess(page["effective_capture_utc"], captures[0]["effective_capture_utc"])
        self.assertLess(captures[0]["effective_capture_utc"], captures[1]["effective_capture_utc"])
        images = [
            (FIXTURES / "archive-versions" / item["saved_body"]).read_bytes()
            for item in captures
        ]
        self.assertNotEqual(*images)
        for image in images:
            self.assertTrue(image.startswith(b"\xff\xd8") and image.endswith(b"\xff\xd9"))
