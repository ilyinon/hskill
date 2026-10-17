import copy
import base64
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/hack/scripts"))
import hack_ledger_model as model
import hack_tool_contract as contract


def event(op, delivery, amount):
    return {"type": "complete", "operation": op, "delivery": delivery, "amount": amount}


class ReasoningModels(unittest.TestCase):
    def setUp(self):
        self.operations = {"x": 23, "y": 41}
        self.a, self.b, self.retry = event("x", "d1", 23), event("y", "d2", 41), event("x", "d3", 23)

    def run_model(self, events, policy="by-operation"):
        return model.simulate(self.operations, policy, events)

    def test_supplied_baselines_failure_and_legitimate_controls(self):
        self.assertEqual(self.run_model([self.a])["final_credit"], 23)
        self.assertEqual(self.run_model([self.a, self.retry], "observed")["final_credit"], 46)
        self.assertEqual(self.run_model([self.a, self.retry])["final_credit"], 23)
        self.assertEqual(self.run_model([self.a, self.b])["final_credit"], 64)
        self.assertEqual(self.run_model([self.a, self.b], "one-callback")["final_credit"], 23)

    def test_upper_bound_invariant_does_not_prove_legitimate_completion(self):
        violating = self.run_model([self.a, self.retry], "observed")
        check = model.invariant(violating, self.operations)
        self.assertFalse(check["holds"])
        self.assertEqual(check["violations"], ["x"])
        overbroad = self.run_model([self.a, self.b], "one-callback")
        self.assertTrue(model.invariant(overbroad, self.operations)["holds"])
        self.assertNotEqual(overbroad["final_credit"], 64)

    def test_field_order_and_bijective_identity_renaming_preserve_effect(self):
        original = [self.a, self.retry, self.b]
        reordered = [dict(reversed(list(row.items()))) for row in original]
        self.assertEqual(self.run_model(original), self.run_model(reordered))
        renamed = [{**row, "operation": "renamed-" + row["operation"], "delivery": "renamed-" + row["delivery"]} for row in original]
        result = model.simulate({"renamed-" + k: v for k, v in self.operations.items()}, "by-operation", renamed)
        self.assertEqual(result["final_credit"], 64)
        self.assertEqual([r["applied"] for r in result["rows"]], [r["applied"] for r in self.run_model(original)["rows"]])

    def test_logs_transport_errors_and_identical_retries_do_not_change_credit(self):
        baseline = self.run_model([self.a, self.b])
        transformed = [self.a, {"type": "log"}, {"type": "transport-error"}, self.a, self.b]
        result = self.run_model(transformed)
        self.assertEqual(result["final_credit"], baseline["final_credit"])
        self.assertEqual(self.run_model([self.a, self.a], "observed")["final_credit"], 23)

    def test_commuting_operations_and_noncommuting_policy_are_distinguished(self):
        for rows in itertools.permutations([self.a, self.b, self.retry]):
            self.assertEqual(self.run_model(list(rows))["final_credit"], 64)
        self.assertNotEqual(self.run_model([self.a, self.b], "one-callback")["final_credit"],
                            self.run_model([self.b, self.a], "one-callback")["final_credit"])

    def test_fixed_seed_generated_traces_preserve_operation_limits_and_completion(self):
        rng = random.Random(1707)
        for _ in range(100):
            rows = []
            included = set()
            for index in range(rng.randrange(1, 25)):
                op = rng.choice(list(self.operations))
                rows.append(event(op, "d%d" % index, self.operations[op]))
                included.add(op)
            result = self.run_model(rows)
            self.assertTrue(model.invariant(result, self.operations)["holds"])
            self.assertEqual(result["final_credit"], sum(self.operations[k] for k in included))
            shuffled = copy.deepcopy(rows); rng.shuffle(shuffled)
            self.assertEqual(self.run_model(shuffled)["final_credit"], result["final_credit"])

    def test_invalid_trial_is_unexecuted_and_inputs_remain_unchanged(self):
        rows = [self.a, {"type": []}]
        before = copy.deepcopy(rows)
        with self.assertRaises(ValueError): self.run_model(rows)
        self.assertEqual(rows, before)
        with self.assertRaises(ValueError): self.run_model([{**self.a, "amount": True}])
        self.assertEqual(self.run_model([self.a])["final_credit"], 23)

    def test_installed_example_is_a_concrete_counterexample(self):
        example = json.loads((ROOT / "skills/hack/assets/ledger-example.json").read_text())
        result = model.simulate(example["operations"], example["policy"], example["events"])
        self.assertEqual(result["final_credit"], 60)
        self.assertFalse(model.invariant(result, example["operations"])["holds"])

    def test_model_cli_distinguishes_invariant_violation_from_bad_input(self):
        helper = ROOT / "skills/hack/scripts/hack_ledger_model.py"
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "input.json"
            data = {"operations": self.operations, "policy": "observed", "events": [self.a, self.retry]}
            path.write_text(json.dumps(data))
            command = [sys.executable, str(helper), "--input", str(path)]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(json.loads(result.stdout)["result"]["final_credit"], 46)
            data["policy"] = "by-operation"; path.write_text(json.dumps(data))
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
            data["events"] = {}; path.write_text(json.dumps(data))
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 2)

    def test_transfer_fixtures_have_consistent_raw_evidence(self):
        folder = ROOT / "tests/fixtures/reasoning"
        supplied = json.loads((folder / "ledger.json").read_text())
        result = model.simulate(supplied["authorized_operations"], "observed", supplied["events"])
        self.assertEqual(result["final_credit"], supplied["supplied_observation"]["final_credit"])
        self.assertEqual(result["final_credit"], 87)
        self.assertFalse(model.invariant(result, supplied["authorized_operations"])["holds"])
        pipeline = json.loads((folder / "pipeline.json").read_text())
        unique = {}
        for fragment in pipeline["routes"]["current"]["fragments"]:
            if fragment["sequence"] in unique: self.assertEqual(unique[fragment["sequence"]], fragment)
            unique[fragment["sequence"]] = fragment
        body = b"".join(bytes.fromhex(unique[key]["hex"]) for key in sorted(unique))
        self.assertEqual(body, b"receipt-Q:r9:indigo\n")
        self.assertEqual(hashlib.sha256(body).hexdigest(), pipeline["goal"]["sha256"])
        tool = json.loads((folder / "tool-input.json").read_text())
        self.assertTrue(contract.validate(tool["contract"], tool["failed_call"]))
        request = {"action": "read-chunk", "arguments": {"release": 12, "format": "base64-blocks", "cursor": "tail-6"}}
        self.assertEqual(contract.validate(tool["contract"], request), [])
        self.assertEqual(b"".join(base64.b64decode(block, validate=True) for block in tool["supplied_recording"]["blocks"]), b"delta:72\n")


if __name__ == "__main__":
    unittest.main()
