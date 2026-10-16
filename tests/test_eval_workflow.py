import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import check_skills
import eval_skills


class EvalWorkflow(unittest.TestCase):
    def test_manifest_has_real_artifacts_and_unique_inputs(self):
        cases = eval_skills.read_manifest()["cases"]
        self.assertGreaterEqual(len(cases), 18)
        self.assertEqual(len({eval_skills.case_digest(case) for case in cases}), len(cases))

    def test_blind_export_copies_only_requests_and_raw_artifacts(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "blind"
            rows = eval_skills.prepare(target, ["jwt-direct-control"])
            case = next(case for case in eval_skills.read_manifest()["cases"] if case["id"] == rows[0]["id"])
            expected = {"run.json", case["id"] + "/request.md"}
            for name in case["artifacts"]:
                relative = Path(name).relative_to("tests/fixtures")
                path = target / case["id"] / "artifacts" / relative
                self.assertEqual(path.read_bytes(), (ROOT / name).read_bytes())
                expected.add(str(path.relative_to(target)))
            self.assertEqual({str(path.relative_to(target)) for path in target.rglob("*") if path.is_file()}, expected)
            self.assertEqual(set(json.loads((target / "run.json").read_text())), {"schema_version", "cases"})
            with self.assertRaises(ValueError):
                eval_skills.prepare(target, ["jwt-direct-control"])

    def reviewed_result(self, folder):
        run = folder / "blind"
        eval_skills.prepare(run, ["jwt-direct-control"])
        result = eval_skills.template(run / "run.json")
        result.update(label="unit-test aggregation only", model="fixture-model/settings", context_mode="fresh-per-case", revision="fixture-revision", reviewer="unit test")
        (folder / "answer.md").write_text("This is a unit-test record, not an agent evaluation.\n")
        case = result["cases"][0]
        case.update(answer_file="answer.md", criteria={key: "pass" for key in case["criteria"]}, finding="not_reported",
                    read_files=["skills/hack/SKILL.md", "skills/jwt-oauth-token-attacks/SKILL.md"], notes="Checks report bookkeeping only")
        path = folder / "results.json"
        path.write_text(json.dumps(result))
        return result, path

    def test_incomplete_or_incorrect_grades_cannot_pass(self):
        with tempfile.TemporaryDirectory() as name:
            result, path = self.reviewed_result(Path(name))
            self.assertEqual(eval_skills.report(path)["passed"], 1)
            result["cases"][0]["criteria"]["evidence"] = "ungraded"
            path.write_text(json.dumps(result))
            self.assertEqual(eval_skills.report(path)["cases"][0]["outcome"], "ungraded")
            result["cases"][0]["criteria"]["evidence"] = "pass"
            result["cases"][0]["finding"] = "reported"
            path.write_text(json.dumps(result))
            report = eval_skills.report(path)
            self.assertEqual((report["passed"], report["false_positives"]), (0, 1))

    def test_changed_input_and_mismatched_model_are_rejected(self):
        with tempfile.TemporaryDirectory() as name:
            result, path = self.reviewed_result(Path(name))
            first = eval_skills.report(path)
            other = json.loads(json.dumps(first)); other["model"] = "another-model"
            with self.assertRaises(ValueError):
                eval_skills.compare(first, other)
            result["cases"][0]["fixture_digest"] = "different"
            path.write_text(json.dumps(result))
            with self.assertRaises(ValueError):
                eval_skills.report(path)

    def test_partial_and_repeated_reads_are_counted_separately(self):
        class CharacterEncoding:
            def encode(self, text, **kwargs):
                return list(text)
        with tempfile.TemporaryDirectory() as name:
            result, path = self.reviewed_result(Path(name))
            read = {"path": "skills/hack/SKILL.md", "start_line": 1, "end_line": 1}
            result["cases"][0]["read_files"] = [read, read]
            path.write_text(json.dumps(result))
            case = eval_skills.report(path, encoding=CharacterEncoding())["cases"][0]
            self.assertEqual((case["read_count"], case["file_text_tokens"]), (2, 8))
            read["start_line"] = 0
            path.write_text(json.dumps(result))
            with self.assertRaises(ValueError):
                eval_skills.report(path)

    def test_heading_inline_code_remains_in_anchor_but_code_links_are_ignored(self):
        self.assertIn("kid-lookup", check_skills.anchors("### `kid` lookup\n"))
        self.assertEqual(check_skills.links("`[literal](missing.md)`\n```text\n[example](also-missing.md)\n```\n"), [])

    def test_material_reference_growth_is_reported(self):
        result = {"warnings": [], "document_tokens": [{"path": "topic/references/a.md", "tokens": 1600}]}
        baseline = {"document_tokens": [{"path": "topic/references/a.md", "tokens": 1000}]}
        changes = check_skills.compare_budget(result, baseline)
        self.assertTrue(result["warnings"])
        self.assertEqual(changes[0]["delta"], 600)
