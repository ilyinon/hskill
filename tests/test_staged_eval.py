import base64
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import staged_eval as lab


class StagedEvaluation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)

    def start(self, name):
        session = self.folder / name
        lab.start(name, session)
        return session

    def call(self, run, action, **arguments):
        return lab.act(run, {"action": action, "arguments": arguments})["response"]

    def test_export_contains_only_initial_artifacts_and_request(self):
        cases = lab.manifest()["cases"]
        rubric = json.loads((ROOT / "tests/staged_rubrics.json").read_text())
        self.assertEqual({c["id"] for c in cases}, {c["id"] for c in rubric["cases"]})
        case = cases[0]
        session = self.start(case["id"])
        public = session / "task"
        self.assertEqual({str(p.relative_to(public)) for p in public.rglob("*") if p.is_file()},
                         {"request.md"} | {"artifacts/" + name for name in case["initial"]})
        with self.assertRaises(FileExistsError):
            lab.start(case["id"], session)

    def test_export_chain_checks_identity_revision_representation_and_continuation(self):
        session = self.start("release-export")
        self.assertEqual(self.call(session, "export", format="legacy-v1", session="preview-link", object="r17", revision=2)["outcome"], "tool-error")
        self.call(session, "inspect-client")
        self.call(session, "inspect-current")
        args = dict(format="json-v2", session="mira-s1", object="r17", revision=3)
        self.assertEqual(self.call(session, "export", **{**args, "session": "preview-link"})["outcome"], "controlled-negative")
        head = self.call(session, "export", **args)["result"]
        tail = self.call(session, "continue", cursor=head["cursor"], session="mira-s1")["result"]
        recovered = bytes.fromhex(head["hex"]) + bytes.fromhex(tail["hex"])
        self.assertEqual(recovered, b"north:r17:r3:violet-28\n")
        self.assertEqual(hashlib.sha256(recovered).hexdigest(), "3d39d3a9884098b31db70471c4563131e4f989911ef6e7738a24250bb038a377")

    def test_unrecorded_inputs_and_unmet_dependencies_remain_unknown(self):
        session = self.start("release-export")
        self.assertEqual(self.call(session, "continue", cursor="r17-part-1", session="mira-s1")["outcome"], "unknown")
        self.assertEqual(self.call(session, "export", format="json-v2", session="admin", object="r17", revision=3)["outcome"], "unknown")
        self.assertNotIn("export-head", lab.status(session)["observed"])

    def test_build_change_retains_old_source_but_requires_new_contract_and_chunks(self):
        session = self.start("changing-build")
        original = (session / "task/artifacts/build-7.json").read_bytes()
        rotated = self.call(session, "fetch", build=7, format="hex")
        self.assertEqual(rotated["outcome"], "unknown")
        self.assertFalse(rotated["result"]["payload_returned"])
        self.assertEqual(self.call(session, "fetch", build=8, format="base64-per-chunk")["outcome"], "unknown")
        contract = self.call(session, "inspect-build")["result"]
        # Reopening the on-disk session reproduces history, without an extra action.
        self.assertEqual(lab.status(session)["used"], 3)
        head = self.call(session, "fetch", build=8, format=contract["encoding"])["result"]
        tail = self.call(session, "tail", build=8, cursor=head["cursor"])["result"]
        raw = base64.b64decode(head["data"]) + base64.b64decode(tail["data"])
        self.assertEqual(bytes(b ^ contract["xor_key"] for b in raw), b"code=6421\n")
        self.assertEqual((session / "task/artifacts/build-7.json").read_bytes(), original)
        self.assertTrue(list((session / "task/artifacts").glob("*-build-8.json")))

    def test_changed_source_or_observation_cannot_silently_resume(self):
        session = self.start("changing-build")
        source = session / "task/artifacts/build-7.json"
        original = source.read_text()
        source.write_text("{}\n")
        with self.assertRaises(ValueError):
            lab.status(session)
        source.write_text(original)
        self.call(session, "fetch", build=7, format="hex")
        (session / "task/observation-01.json").write_text("{}\n")
        with self.assertRaises(ValueError):
            lab.status(session)

    def test_changed_case_digest_and_rewritten_history_are_rejected(self):
        session = self.start("release-export")
        self.call(session, "inspect-current")
        state_path = session / "session.json"
        state = json.loads(state_path.read_text())
        state["input_digest"] = "changed"
        state_path.write_text(json.dumps(state))
        with self.assertRaises(ValueError):
            lab.status(session)
        state["input_digest"] = lab.digest(next(c for c in lab.manifest()["cases"] if c["id"] == "release-export"))
        state["history"][0]["response"]["outcome"] = "effect"
        state_path.write_text(json.dumps(state))
        with self.assertRaises(ValueError):
            lab.status(session)

    def replay(self, session, policy, events):
        return self.call(session, "replay", policy=policy, events=events)["result"]

    def test_minimal_witness_controls_and_specific_repair(self):
        session = self.start("callback-reproducer")
        self.call(session, "inspect-runtime")
        first = {"type": "complete", "operation": "p1", "delivery": "d1", "amount": 30}
        retry = {**first, "delivery": "d2"}
        partial = {"type": "complete", "operation": "p2", "delivery": "d3", "amount": 20}
        for events, expected in [([first], 30), ([first, first], 30), ([first, retry], 60), ([first, partial], 50)]:
            self.assertEqual(self.replay(session, "observed", events)["final_credit"], expected)
        self.assertEqual(self.replay(session, "by-operation", [first, retry])["final_credit"], 30)
        self.assertEqual(self.replay(session, "by-operation", [first, partial])["final_credit"], 50)
        self.assertEqual(self.replay(session, "one-callback", [first, partial])["final_credit"], 30)

    def test_minimization_keeps_effect_but_invalid_trial_is_not_negative(self):
        session = self.start("callback-reproducer")
        self.call(session, "inspect-runtime")
        events = json.loads((session / "task/artifacts/events.json").read_text())
        self.assertEqual(self.replay(session, "observed", events)["final_credit"], 80)
        reduced = [event for event in events if event.get("operation") == "p1" and event.get("delivery") in {"d1", "d2"}]
        self.assertEqual(self.replay(session, "observed", reduced)["final_credit"], 60)
        response = self.call(session, "replay", policy="observed", events=[events[2], {"type": "unknown"}])
        self.assertEqual(response["outcome"], "tool-error")
        self.assertNotIn("final_credit", response)
        self.assertEqual(self.replay(session, "observed", [events[2]])["final_credit"], 30)

    def test_malformed_model_arguments_never_execute_a_partial_trial(self):
        session = self.start("callback-reproducer")
        self.call(session, "inspect-runtime")
        for arguments in [{"policy": [], "events": []}, {"policy": "observed", "events": {}},
                          {"policy": "observed", "events": [{"type": "complete", "operation": [], "delivery": "d", "amount": 30}]}]:
            response = lab.act(session, {"action": "replay", "arguments": arguments})["response"]
            self.assertEqual(response["outcome"], "tool-error")

    def test_budget_and_repeated_input_metric_do_not_claim_semantic_failure(self):
        session = self.start("changing-build")
        for _ in range(10):
            self.call(session, "inspect-build")
        report = lab.status(session)
        self.assertEqual((report["used"], report["repeated_inputs"], report["remaining"]), (10, 9, 0))
        self.assertEqual(report["outcomes"]["observation"], 10)
        with self.assertRaises(ValueError):
            self.call(session, "inspect-build")

    def test_submission_preserves_answer_but_is_never_auto_passed(self):
        session = self.start("release-export")
        answer = self.folder / "incomplete.md"
        answer.write_text("No export recovered; this is a bookkeeping test.\n")
        result = lab.finish(session, answer)
        self.assertIn("pending independent review", result["grading"])
        self.assertNotIn("passed", result)
        self.assertEqual(result["used"], 0)
        with self.assertRaises(ValueError):
            self.call(session, "inspect-client")
        with self.assertRaises(ValueError):
            lab.finish(session, answer)
        (session / "task/answer.md").write_text("replaced\n")
        with self.assertRaises(ValueError):
            lab.status(session)

    def test_file_names_cannot_escape_public_artifact_directory(self):
        for name in ("../rubric.json", "/tmp/answer", ".", "..", "a/b", ""):
            with self.assertRaises(ValueError):
                lab.check_files({name: "inert data"})


if __name__ == "__main__":
    unittest.main()
