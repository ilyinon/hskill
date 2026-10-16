#!/usr/bin/env python3
"""Prepare blind offline cases and summarize explicitly reviewed agent results.

No agent, fixture program, target request, or credential use is executed here.
The rubric stays in the repository and is excluded from prepared case folders.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
OFFLINE_INSTRUCTION = "Artifacts are under ./artifacts. All data is synthetic and offline. Read the minimum relevant skill files. Do not execute fixtures, contact a target, or inspect the grading manifest."


def read_manifest(root=ROOT):
    data = json.loads((root / "tests/eval_cases.json").read_text())
    if data.get("schema_version") != 2 or not data.get("cases"):
        raise ValueError("Expected nonempty eval manifest schema_version 2")
    seen = set()
    for case in data["cases"]:
        name = case["id"]
        if not name or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in name) or name in seen:
            raise ValueError("Invalid or duplicate case ID")
        seen.add(name)
        if not case.get("request") or not case.get("criteria") or not case.get("artifacts"):
            raise ValueError(f"Incomplete case {name}")
        if not isinstance(case["criteria"], dict) or not all(isinstance(value, str) and value for value in case["criteria"].values()):
            raise ValueError(f"Invalid grading rubric {name}")
        if case.get("finding_expected") not in {"supported", "unsupported", "not_applicable"}:
            raise ValueError(f"Invalid finding classification {name}")
        for filename in case["artifacts"]:
            if Path(filename).is_absolute() or ".." in Path(filename).parts:
                raise ValueError(f"Unsafe fixture path {filename}")
            path = (root / filename).resolve()
            if not path.is_relative_to((root / "tests/fixtures").resolve()) or not path.is_file():
                raise ValueError(f"Missing or unsafe fixture {filename}")
    return data


def case_digest(case, root=ROOT):
    raw = {"request": case["request"], "instructions": OFFLINE_INSTRUCTION, "artifacts": {
        name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in case["artifacts"]}}
    return hashlib.sha256(json.dumps(raw, sort_keys=True).encode()).hexdigest()


def grading_digest(case):
    data = {"criteria": case["criteria"], "finding_expected": case["finding_expected"]}
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


def prepare(output, case_ids=None, root=ROOT):
    cases = read_manifest(root)["cases"]
    selected = [case for case in cases if not case_ids or case["id"] in case_ids]
    if not selected or (case_ids and set(case_ids) - {case["id"] for case in cases}):
        raise ValueError("Unknown or empty case selection")
    output = Path(output).resolve()
    if output.exists():
        raise ValueError("Output must be a new directory; existing runs are never overwritten")
    if output.is_relative_to((root / "skills").resolve()) or output.is_relative_to((root / "tests/fixtures").resolve()):
        raise ValueError("Prepared runs must not enter the skill or fixture collection")
    output.mkdir(parents=True)
    rows = []
    for case in selected:
        folder = output / case["id"]
        folder.mkdir()
        for name in case["artifacts"]:
            relative = Path(name).relative_to("tests/fixtures")
            destination = folder / "artifacts" / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / name, destination)
        prompt = case["request"] + "\n\n" + OFFLINE_INSTRUCTION + "\n"
        (folder / "request.md").write_text(prompt)
        rows.append({"id": case["id"], "fixture_digest": case_digest(case, root)})
    (output / "run.json").write_text(json.dumps({"schema_version": 1, "cases": rows}, indent=2) + "\n")
    return rows


def template(run, root=ROOT):
    cases = {case["id"]: case for case in read_manifest(root)["cases"]}
    rows = []
    for row in json.loads(Path(run).read_text())["cases"]:
        case = cases[row["id"]]
        if row["fixture_digest"] != case_digest(case, root):
            raise ValueError("Fixture changed since preparation")
        rows.append({**row, "grading_digest": grading_digest(case), "answer_file": "", "criteria": {key: "ungraded" for key in case["criteria"]},
                     "finding": "ungraded", "read_files": [], "notes": ""})
    return {"schema_version": 1, "label": "", "model": "", "context_mode": "", "revision": "", "reviewer": "", "cases": rows}


def report(results_path, root=ROOT, encoding=None):
    results_path = Path(results_path).resolve()
    data = json.loads(results_path.read_text())
    if data.get("schema_version") != 1 or not all(data.get(key) for key in ["label", "model", "revision", "reviewer", "cases"]):
        raise ValueError("Result metadata and at least one case are required")
    if data.get("context_mode") not in {"fresh-per-case", "shared-session"}:
        raise ValueError("Declare context_mode: fresh-per-case or shared-session")
    cases = {case["id"]: case for case in read_manifest(root)["cases"]}
    seen, rows = set(), []
    false_positives = false_negatives = 0
    for result in data["cases"]:
        name = result["id"]
        if name not in cases or name in seen:
            raise ValueError("Unknown or duplicate result case")
        seen.add(name)
        case = cases[name]
        if result["fixture_digest"] != case_digest(case, root):
            raise ValueError(f"{name}: fixture digest differs; do not compare different inputs")
        if result.get("grading_digest") != grading_digest(case):
            raise ValueError(f"{name}: grading rubric changed")
        criteria = result["criteria"]
        if set(criteria) != set(case["criteria"]) or any(value not in {"pass", "fail", "ungraded"} for value in criteria.values()):
            raise ValueError(f"{name}: missing or invalid criterion grades")
        finding = result.get("finding")
        if finding not in {"reported", "not_reported", "not_applicable", "ungraded"}:
            raise ValueError(f"{name}: invalid finding grade")
        answer_name = result.get("answer_file")
        answer_path = (results_path.parent / answer_name).resolve() if answer_name else None
        if not answer_path or not answer_path.is_file() or not answer_path.read_text().strip():
            raise ValueError(f"{name}: a preserved, nonempty answer is required")
        reads = result.get("read_files", [])
        if not reads or not all(isinstance(item, (str, dict)) for item in reads):
            raise ValueError(f"{name}: record the files actually read, including repeated reads")
        tokens = 0 if encoding else None
        binary_reads = 0
        hashes = []
        for item in reads:
            filename = item if isinstance(item, str) else item["path"]
            path = (root / filename).resolve()
            if not path.is_relative_to(root.resolve()) or not path.is_file():
                raise ValueError(f"{name}: unsafe or missing read-log path")
            raw = path.read_bytes()
            record = {"path": filename, "sha256": hashlib.sha256(raw).hexdigest()}
            try:
                text = raw.decode()
            except UnicodeError:
                binary_reads += 1
                if isinstance(item, dict):
                    raise ValueError("Line ranges require a text file")
            else:
                if isinstance(item, dict):
                    lines = text.splitlines(keepends=True)
                    start, end = item.get("start_line", 1), item.get("end_line", len(lines))
                    if type(start) is not int or type(end) is not int or not 1 <= start <= end <= len(lines):
                        raise ValueError("Invalid read-log line range")
                    text = "".join(lines[start - 1:end])
                    record.update(start_line=start, end_line=end)
                record["read_sha256"] = hashlib.sha256(text.encode()).hexdigest()
                if encoding:
                    tokens += len(encoding.encode(text, disallowed_special=()))
            hashes.append(record)
        complete = "ungraded" not in criteria.values() and finding != "ungraded"
        if case["finding_expected"] == "supported" and finding == "not_reported":
            false_negatives += 1
        if case["finding_expected"] == "unsupported" and finding == "reported":
            false_positives += 1
        mismatch = ((case["finding_expected"] == "supported" and finding != "reported") or
                    (case["finding_expected"] == "unsupported" and finding != "not_reported") or
                    (case["finding_expected"] == "not_applicable" and finding != "not_applicable"))
        outcome = "fail" if "fail" in criteria.values() or (complete and mismatch) else "pass" if complete else "ungraded"
        rows.append({"id": name, "fixture_digest": result["fixture_digest"], "grading_digest": result["grading_digest"], "outcome": outcome,
                     "criteria": criteria, "finding": finding, "read_count": len(reads), "file_text_tokens": tokens,
                     "binary_reads_excluded_from_tokens": binary_reads,
                     "read_hashes": hashes, "answer_sha256": hashlib.sha256(answer_path.read_bytes()).hexdigest()})
    return {"label": data["label"], "model": data["model"], "context_mode": data["context_mode"], "revision": data["revision"], "reviewer": data["reviewer"],
            "method": "Explicit human/independent-agent semantic grades; read logs are supplied records, not automatic telemetry. File-text token counts honor optional line ranges and repeated reads; they are not total model usage.",
            "total_cases": len(cases), "evaluated_cases": len(rows), "missing_cases": sorted(cases.keys() - seen),
            "passed": sum(row["outcome"] == "pass" for row in rows), "false_positives": false_positives,
            "failed": sum(row["outcome"] == "fail" for row in rows),
            "ungraded": sum(row["outcome"] == "ungraded" for row in rows),
            "false_negatives": false_negatives, "cases": rows}


def compare(before, after):
    if before["model"] != after["model"] or before["context_mode"] != after["context_mode"]:
        raise ValueError("Model/settings or context mode differ")
    old = {case["id"]: case for case in before["cases"]}
    new = {case["id"]: case for case in after["cases"]}
    if old.keys() != new.keys():
        raise ValueError("Case sets differ")
    rows = []
    for name in sorted(old):
        a, b = old[name], new[name]
        if a["fixture_digest"] != b["fixture_digest"]:
            raise ValueError(f"{name}: fixture inputs differ")
        if a["grading_digest"] != b["grading_digest"]:
            raise ValueError(f"{name}: grading rubrics differ")
        if a["outcome"] == "ungraded" or b["outcome"] == "ungraded":
            raise ValueError("Finish grading before comparison")
        rows.append({"id": name, "before": a["outcome"], "after": b["outcome"],
                     "read_count_delta": b["read_count"] - a["read_count"],
                     "file_text_token_delta": b["file_text_tokens"] - a["file_text_tokens"] if a["file_text_tokens"] is not None and b["file_text_tokens"] is not None else None})
    return {"before": before["label"], "after": after["label"], "cases": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate")
    p = commands.add_parser("prepare"); p.add_argument("--output", type=Path, required=True); p.add_argument("--case", action="append")
    p = commands.add_parser("template"); p.add_argument("--run", type=Path, required=True); p.add_argument("--output", type=Path, required=True)
    p = commands.add_parser("report"); p.add_argument("--results", type=Path, required=True); p.add_argument("--output", type=Path, required=True); p.add_argument("--tokens", action="store_true")
    p = commands.add_parser("compare"); p.add_argument("before", type=Path); p.add_argument("after", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "validate":
            result = {"cases": len(read_manifest()["cases"]), "errors": []}
        elif args.command == "prepare":
            result = {"prepared": len(prepare(args.output, args.case)), "output": str(args.output)}
        elif args.command == "template":
            if args.output.exists(): raise ValueError("Refusing to overwrite grades")
            result = template(args.run); args.output.write_text(json.dumps(result, indent=2) + "\n")
            result = {"template": str(args.output), "cases": len(result["cases"])}
        elif args.command == "report":
            encoding = None
            if args.tokens:
                import tiktoken
                encoding = tiktoken.get_encoding("o200k_base")
            result = report(args.results, encoding=encoding)
            args.output.write_text(json.dumps(result, indent=2) + "\n")
        else:
            result = compare(json.loads(args.before.read_text()), json.loads(args.after.read_text()))
        print(json.dumps(result, indent=2))
    except (OSError, ValueError, KeyError, TypeError, ImportError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
