import copy
import json
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/hack/scripts"))
sys.path.insert(0, str(ROOT / "scripts"))
import hack_tool_contract as contract
import staged_eval


class ToolContract(unittest.TestCase):
    def setUp(self):
        self.schema = contract.parse((ROOT / "skills/hack/assets/fetch-contract.json").read_text())
        self.call = contract.parse((ROOT / "skills/hack/assets/fetch-call.json").read_text())

    def test_current_example_accepts_exact_enumeration_and_shape(self):
        self.assertEqual(contract.validate(self.schema, self.call), [])
        for change in ({"format": "base64"}, {"build": True}, {"build": None}, {"raw": True}):
            request = copy.deepcopy(self.call)
            request["arguments"].update(change)
            self.assertTrue(contract.validate(self.schema, request))

    def test_missing_null_empty_and_unknown_are_distinct(self):
        for value in (None, {}, {"action": "fetch"}, {"action": "fetch", "arguments": {}}):
            self.assertTrue(contract.validate(self.schema, value))

    def test_numeric_enum_does_not_conflate_boolean(self):
        schema = {"type": "boolean", "enum": [1]}
        self.assertTrue(contract.validate(schema, True))
        self.assertEqual(contract.validate({"type": "number", "enum": [1]}, 1.0), [])
        self.assertEqual(contract.validate({"type": "integer"}, 10 ** 400), [])

    def test_nested_arrays_bounds_and_exact_values(self):
        schema = {"type": "array", "minItems": 1, "maxItems": 2, "items": {"type": "string", "minLength": 2, "maxLength": 3}}
        for value in ([], ["x"], ["long"], ["ab", "cd", "ef"]):
            self.assertTrue(contract.validate(schema, value))
        self.assertEqual(contract.validate(schema, ["ab", "cde"]), [])
        numeric = {"type": "number", "minimum": 0, "maximum": 1}
        self.assertEqual(contract.validate(numeric, 0.5), [])
        self.assertTrue(contract.validate(numeric, -1))
        self.assertTrue(contract.validate(numeric, float("inf")))

    def test_unsupported_schemas_never_silently_drop_restrictions(self):
        for schema in ({"type": "string", "pattern": "^a"}, {"type": "object", "$ref": "other"},
                       {"type": ["string", "null"]}, {"type": "array"},
                       {"type": "object", "additionalProperties": {}}, {"type": "integer", "minLength": 1},
                       {"type": "integer", "minimum": 3, "maximum": 2}):
            with self.assertRaises(ValueError):
                contract.validate(schema, {})

    def test_duplicate_keys_and_nonfinite_json_fail_before_validation(self):
        for text in ('{"x":1,"x":2}', '{"a":{"x":1,"x":2}}', 'NaN', '[Infinity]', '{"x":1e999}'):
            with self.assertRaises(ValueError):
                contract.parse(text)

    def test_preflight_rejection_does_not_consume_or_mutate_staged_action(self):
        with tempfile.TemporaryDirectory() as temporary:
            session = Path(temporary) / "session"
            staged_eval.start("changing-build", session)
            staged_eval.act(session, {"action": "fetch", "arguments": {"build": 7, "format": "hex"}})
            staged_eval.act(session, {"action": "inspect-build", "arguments": {}})
            before = (session / "session.json").read_bytes()
            wrong = copy.deepcopy(self.call)
            wrong["arguments"]["format"] = "base64"
            with self.assertRaises(ValueError):
                staged_eval.act(session, wrong, contract=self.schema)
            self.assertEqual((session / "session.json").read_bytes(), before)
            response = staged_eval.act(session, self.call, contract=self.schema)
            self.assertEqual((response["step"], response["response"]["outcome"]), (3, "partial"))

    def test_cli_exit_codes_distinguish_shape_failure_from_invalid_contract(self):
        helper = ROOT / "skills/hack/scripts/hack_tool_contract.py"
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary); schema = folder / "schema.json"; call = folder / "call.json"
            schema.write_text(json.dumps(self.schema)); call.write_text(json.dumps(self.call))
            command = [sys.executable, str(helper), "--schema", str(schema), "--input", str(call)]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            self.assertFalse(json.loads(result.stdout)["executed"])
            self.call["arguments"]["format"] = "base64"; call.write_text(json.dumps(self.call))
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertFalse(json.loads(result.stdout)["shape_valid"])
            schema.write_text('{"type":"object","$ref":"unknown"}')
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 2)


if __name__ == "__main__":
    unittest.main()
