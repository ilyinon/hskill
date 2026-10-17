import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import ablation_eval as experiment


class AblationEvaluation(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.folder = Path(self.temporary.name)
        self.root = self.folder / "repo"
        (self.root / "skills/hack/references").mkdir(parents=True)
        (self.root / "skills/hack/SKILL.md").write_text("---\nname: hack\ndescription: Test fixture\n---\n")
        (self.root / "skills/hack/references/conditional.md").write_text("# Guidance\n\nOne optional reasoning procedure.\n")
        (self.root / "skills/hack/references/other.md").write_text("Unrelated content retained.\n")
        (self.root / "tests/fixtures").mkdir(parents=True)
        (self.root / "tests/fixtures/input.txt").write_text("Raw input, not an answer.\n")
        self.manifest = self.root / "tests/eval_cases.json"
        self.manifest.write_text(json.dumps({"schema_version": 2, "cases": [{"id": "unit-case", "request": "Solve the supplied unit task.",
            "artifacts": ["tests/fixtures/input.txt"], "criteria": {"completion": "Explicit rubric outside worker"}, "finding_expected": "not_applicable"}]}))
        self.output = self.folder / "experiment"

    def prepare(self, repeats=1):
        return experiment.prepare(self.output, "hack/references/conditional.md", ["unit-case"], repeats, 7, self.root)

    def populated(self):
        self.prepare()
        _, data, _ = experiment.load(self.output, self.root)
        for job in data["jobs"]:
            worker = self.output / "workers" / job["id"]
            (worker / "answer.md").write_text("Unit bookkeeping answer, not a real agent evaluation.\n")
            (worker / "reads.json").write_text(json.dumps(["skills/hack/SKILL.md", "skills/hack/references/conditional.md"]))
        grades = experiment.seal(self.output, self.root)
        grades["reviewer"] = "unit bookkeeping test"
        for row in grades["jobs"]:
            row.update(context_id=row["id"], criteria={"completion": "pass"}, finding="not_applicable", false_claims=0, unnecessary_actions=0,
                       notes="Synthetic grade used only to test aggregation.")
            row["environment"] = {"model_id": "unit-test-model-v1", "settings": {"sampling_seed": 1}, "settings_complete": True,
                                  "tools_fingerprint": "unit-test-tools-v1", "context_mode": "fresh-per-job"}
        path = self.folder / "grades.json"
        path.write_text(json.dumps(grades))
        return grades, path, data

    def test_blinded_workers_differ_only_in_selected_reference(self):
        self.prepare(2)
        _, data, _ = experiment.load(self.output, self.root)
        self.assertEqual(len(data["jobs"]), 4)
        for job in data["jobs"]:
            worker = self.output / "workers" / job["id"]
            expected = {"request.md", "artifacts/input.txt"}
            self.assertEqual(set(experiment.files(worker / "task")), expected)
            self.assertEqual((worker / "skills/hack/SKILL.md").read_bytes(), (self.root / "skills/hack/SKILL.md").read_bytes())
            changed = {k for k, v in job["snapshot"].items() if data["source_snapshot"].get(k) != v}
            self.assertEqual(changed, {"hack/references/conditional.md"} if data["conditions"][job["condition"]] == "ablated" else set())

    def test_preparation_refuses_entry_ablation_existing_run_or_unknown_case(self):
        with self.assertRaises(ValueError): experiment.prepare(self.output, "hack/SKILL.md", ["unit-case"], root=self.root)
        with self.assertRaises(ValueError): experiment.prepare(self.output, "hack/references/conditional.md", ["absent"], root=self.root)
        self.prepare()
        with self.assertRaises(ValueError): self.prepare()

    def test_answer_must_exist_before_grading_template_and_is_frozen_after(self):
        self.prepare()
        with self.assertRaises(OSError): experiment.seal(self.output, self.root)
        # A separate experiment populates the actual sealing path.
        self.output = self.folder / "second"
        _, path, data = self.populated()
        worker = self.output / "workers" / data["jobs"][0]["id"]
        (worker / "answer.md").write_text("Changed after grades were revealed.\n")
        with self.assertRaises(ValueError): experiment.report(path, self.root)

    def test_only_matching_complete_conditions_produce_pairs(self):
        grades, path, _ = self.populated()
        result = experiment.report(path, self.root)
        self.assertTrue(result["controlled_comparable"])
        self.assertEqual(len(result["pairs"]), 1)
        self.assertTrue(result["pairs"][0]["full_module_read"])
        grades["jobs"][1]["environment"]["settings"]["sampling_seed"] = 2
        path.write_text(json.dumps(grades))
        result = experiment.report(path, self.root)
        self.assertFalse(result["controlled_comparable"])
        self.assertEqual(result["pairs"], [])

    def test_unknown_metadata_shared_context_and_ungraded_results_block_comparison(self):
        grades, path, _ = self.populated()
        grades["jobs"][0]["environment"]["model_id"] = "unknown inherited runtime"
        grades["jobs"][1]["context_id"] = grades["jobs"][0]["context_id"]
        grades["jobs"][0]["criteria"]["completion"] = "ungraded"
        grades["jobs"][0]["unnecessary_actions"] = None
        path.write_text(json.dumps(grades))
        result = experiment.report(path, self.root)
        self.assertFalse(result["controlled_comparable"])
        self.assertEqual(result["pairs"], [])
        self.assertGreaterEqual(len(result["comparison_blockers"]), 4)

    def test_wrong_finding_classification_cannot_pass_all_criteria(self):
        grades, path, _ = self.populated()
        grades["jobs"][0]["finding"] = "reported"
        path.write_text(json.dumps(grades))
        result = experiment.report(path, self.root)
        self.assertEqual(result["jobs"][0]["outcome"], "fail")
        grades["jobs"][0]["finding"] = "ungraded"
        path.write_text(json.dumps(grades))
        self.assertFalse(experiment.report(path, self.root)["controlled_comparable"])

    def test_unknown_nested_settings_do_not_become_controlled_by_assertion(self):
        grades, path, _ = self.populated()
        for row in grades["jobs"]:
            row["environment"]["settings"] = {"sampling": {"seed": "unavailable"}}
            row["environment"]["settings_complete"] = True
        path.write_text(json.dumps(grades))
        self.assertFalse(experiment.report(path, self.root)["controlled_comparable"])

    def test_changed_frozen_inputs_or_rubrics_are_rejected(self):
        _, path, data = self.populated()
        source = self.output / "workers" / data["jobs"][0]["id"] / "skills/hack/references/other.md"
        original = source.read_bytes(); source.write_text("Modified outside intervention.\n")
        with self.assertRaises(ValueError): experiment.report(path, self.root)
        source.write_bytes(original)
        manifest = json.loads(self.manifest.read_text())
        manifest["cases"][0]["criteria"]["completion"] = "Changed grading rule"
        self.manifest.write_text(json.dumps(manifest))
        with self.assertRaises(ValueError): experiment.report(path, self.root)

    def test_repeated_ranges_count_actual_text_and_read_log_is_frozen(self):
        grades, path, data = self.populated()
        worker = self.output / "workers" / data["jobs"][0]["id"]
        record = {"path": "skills/hack/SKILL.md", "start_line": 1, "end_line": 1}
        (worker / "reads.json").write_text(json.dumps([record, record]))
        with self.assertRaises(ValueError): experiment.report(path, self.root)
        class CharacterEncoding:
            def encode(self, text, **kwargs): return list(text)
        reads = experiment.read_log(worker, CharacterEncoding())
        self.assertEqual(sum(r["file_text_tokens"] for r in reads), 8)
        record["end_line"] = 1000
        (worker / "reads.json").write_text(json.dumps([record]))
        with self.assertRaises(ValueError): experiment.read_log(worker)

    def test_missing_jobs_invalid_counts_and_unexplained_grades_are_rejected(self):
        grades, path, _ = self.populated()
        original = json.loads(json.dumps(grades))
        grades["jobs"].pop(); path.write_text(json.dumps(grades))
        with self.assertRaises(ValueError): experiment.report(path, self.root)
        grades = original; grades["jobs"][0]["false_claims"] = True; path.write_text(json.dumps(grades))
        with self.assertRaises(ValueError): experiment.report(path, self.root)
        grades["jobs"][0]["false_claims"] = 0; grades["jobs"][0]["notes"] = ""; path.write_text(json.dumps(grades))
        with self.assertRaises(ValueError): experiment.report(path, self.root)


if __name__ == "__main__":
    unittest.main()
