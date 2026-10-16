import datetime
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


class VerificationRegistry(unittest.TestCase):
    def test_sources_versions_and_test_claims_are_traceable(self):
        registry = json.loads((ROOT / "skills/hack/verification.json").read_text())
        self.assertEqual(registry["schema_version"], 1)
        names = set()
        loader = unittest.TestLoader()
        for record in registry["techniques"]:
            self.assertNotIn(record["id"], names)
            names.add(record["id"])
            path = (ROOT / "skills" / record["reference"]).resolve()
            self.assertTrue(path.is_relative_to((ROOT / "skills").resolve()))
            self.assertTrue(path.is_file(), record["reference"])
            self.assertTrue(record["sources"])
            self.assertTrue(all(source.startswith("https://") for source in record["sources"]))
            datetime.date.fromisoformat(record["sources_reviewed_on"])
            self.assertTrue(record["limitations"])
            self.assertIn(record["status"], {"source-reviewed", "offline-tested"})
            if record["status"] == "offline-tested":
                self.assertTrue(record["tested_environment"])
                datetime.date.fromisoformat(record["validated_on"])
                self.assertTrue(record["tests"])
                for name in record["tests"]:
                    tests = list(flatten(loader.loadTestsFromName(name)))
                    self.assertEqual(len(tests), 1)
                    self.assertEqual(tests[0].id(), name)
            else:
                self.assertEqual(record["tested_environment"], [])
                self.assertIsNone(record["validated_on"])
