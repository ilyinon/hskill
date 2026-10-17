#!/usr/bin/env python3
"""Prepare blinded, paired offline reference ablations; collect explicit grades.

No model, target, fixture program or external command is invoked. One optional
reference is replaced by a neutral stub only in temporary control snapshots.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import random
import shutil
import eval_skills

ROOT = Path(__file__).resolve().parents[1]
STUB = "# Optional reference\n\nNo additional guidance is supplied in this experimental condition.\n"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def files(root):
    return {str(p.relative_to(root)): sha(p) for p in sorted(root.rglob("*")) if p.is_file() and "__pycache__" not in p.parts}


def write_new(path, data):
    with Path(path).open("x") as stream:
        stream.write(json.dumps(data, indent=2) + "\n")


def prepare(output, module, case_ids, repeats=1, seed=0, root=ROOT):
    output, root = Path(output).resolve(), Path(root).resolve()
    relative = Path(module)
    source = (root / "skills" / relative).resolve()
    if (relative.is_absolute() or ".." in relative.parts or relative.suffix != ".md" or
            source.name == "SKILL.md" or "references" not in relative.parts or not source.is_file() or
            not source.is_relative_to(root / "skills")):
        raise ValueError("A single existing optional references/*.md module is required")
    if type(repeats) is not int or not 1 <= repeats <= 20 or not case_ids:
        raise ValueError("Select cases and 1..20 repetitions explicitly")
    cases = {c["id"]: c for c in eval_skills.read_manifest(root)["cases"]}
    if len(set(case_ids)) != len(case_ids) or set(case_ids) - cases.keys():
        raise ValueError("Unknown or duplicate selected cases")
    if output.exists() or output.is_relative_to(root):
        raise ValueError("Use a new experiment directory outside the repository")
    if any(p.is_symlink() for p in (root / "skills").rglob("*")):
        raise ValueError("Resolve skill symlinks before freezing a standalone experiment")
    source_files = files(root / "skills")
    initial = {k: v for k, v in source_files.items() if k.endswith("/SKILL.md") or "/agents/" in k}
    if not initial:
        raise ValueError("No skill entries to freeze")
    output.mkdir(parents=True)
    raw = output / "host-inputs"
    eval_skills.prepare(raw, case_ids, root)
    rng = random.Random(seed)
    roles = ["full", "ablated"]
    rng.shuffle(roles)
    conditions = dict(zip(("condition-a", "condition-b"), roles))
    jobs = []
    for repeat in range(1, repeats + 1):
        for case_id in case_ids:
            order = list(conditions)
            rng.shuffle(order)
            for condition in order:
                job_id = "trial-%03d" % (len(jobs) + 1)
                worker = output / "workers" / job_id
                shutil.copytree(root / "skills", worker / "skills", ignore=shutil.ignore_patterns("__pycache__"))
                shutil.copytree(raw / case_id, worker / "task")
                if conditions[condition] == "ablated":
                    (worker / "skills" / relative).write_text(STUB)
                snapshot = files(worker / "skills")
                changed = {k for k in snapshot.keys() | source_files.keys() if snapshot.get(k) != source_files.get(k)}
                expected = {str(relative)} if conditions[condition] == "ablated" else set()
                if changed != expected or any(snapshot.get(k) != v for k, v in initial.items()):
                    raise ValueError("Variant changed more than the selected reference")
                (worker / "instructions.md").write_text(
                    "Complete task/request.md using skills/hack/SKILL.md and only this worker's artifacts. "
                    "Read relevant references as needed. Do not inspect sibling workers, host inputs, "
                    "experiment metadata, tests or rubrics. Use a fresh context with no prior task/answer exposure. "
                    "Write a concrete answer.md and reads.json containing actual skills-relative reads "
                    '(e.g. "skills/hack/SKILL.md" or {"path":"skills/hack/SKILL.md","start_line":1,"end_line":10}). '
                    "Include repeated reads. Run reviewed skill helpers with PYTHONDONTWRITEBYTECODE=1. "
                    "Do not delegate or contact a target.\n")
                jobs.append({"id": job_id, "condition": condition, "repeat": repeat, "case": case_id,
                             "fixture_digest": eval_skills.case_digest(cases[case_id], root),
                             "grading_digest": eval_skills.grading_digest(cases[case_id]),
                             "snapshot": snapshot, "task_snapshot": files(worker / "task"),
                             "instructions_sha256": sha(worker / "instructions.md")})
    experiment = {"schema_version": 1, "module": str(relative), "seed": seed, "conditions": conditions,
                  "initial_surfaces_digest": digest(initial), "source_snapshot": source_files, "jobs": jobs}
    write_new(output / "experiment.json", experiment)
    return {"workers": [str(output / "workers" / job["id"]) for job in jobs],
            "host_manifest": str(output / "experiment.json"), "limit": "Give solvers only their own worker directory."}


def load(folder, root=ROOT):
    folder = Path(folder).resolve()
    data = json.loads((folder / "experiment.json").read_text())
    if data.get("schema_version") != 1:
        raise ValueError("Unknown experiment schema")
    cases = {c["id"]: c for c in eval_skills.read_manifest(root)["cases"]}
    ids = set()
    for job in data["jobs"]:
        if job["id"] in ids or Path(job["id"]).name != job["id"] or job["id"] in {".", ".."}:
            raise ValueError("Duplicate or unsafe job")
        ids.add(job["id"])
        case = cases[job["case"]]
        if (job["fixture_digest"] != eval_skills.case_digest(case, root) or
                job["grading_digest"] != eval_skills.grading_digest(case)):
            raise ValueError("Case inputs or grading changed")
        worker = folder / "workers" / job["id"]
        if (files(worker / "skills") != job["snapshot"] or files(worker / "task") != job["task_snapshot"] or
                sha(worker / "instructions.md") != job["instructions_sha256"]):
            raise ValueError("Frozen worker inputs changed")
    return folder, data, cases


def read_log(worker, encoding=None):
    log = json.loads((worker / "reads.json").read_text())
    if not isinstance(log, list) or not log:
        raise ValueError("Preserve a nonempty actual skill-read log")
    records = []
    for item in log:
        name = item if isinstance(item, str) else item["path"]
        path = (worker / name).resolve()
        if not path.is_relative_to((worker / "skills").resolve()) or not path.is_file():
            raise ValueError("Read path must be an actual file in this worker's skills")
        raw = path.read_bytes()
        row = {"path": "skills/" + str(path.relative_to((worker / "skills").resolve())),
               "logged_path": name, "sha256": hashlib.sha256(raw).hexdigest(), "file_text_tokens": None}
        try:
            text = raw.decode()
        except UnicodeError:
            if not isinstance(item, str): raise ValueError("Binary reads cannot have line ranges")
            row["binary"] = True
        else:
            if not isinstance(item, str):
                lines = text.splitlines(keepends=True)
                start, end = item["start_line"], item["end_line"]
                if type(start) is not int or type(end) is not int or not 1 <= start <= end <= len(lines):
                    raise ValueError("Invalid actual-read line range")
                text = "".join(lines[start - 1:end])
                row.update(start_line=start, end_line=end)
            row["read_sha256"] = hashlib.sha256(text.encode()).hexdigest()
            if encoding: row["file_text_tokens"] = len(encoding.encode(text, disallowed_special=()))
        records.append(row)
    return records


def seal(folder, root=ROOT):
    folder, data, cases = load(folder, root)
    rows = []
    for job in data["jobs"]:
        worker = folder / "workers" / job["id"]
        if not (worker / "answer.md").read_text().strip():
            raise ValueError("Preserve a nonempty answer before revealing grades")
        read_log(worker)
        rows.append({"id": job["id"], "case": job["case"], "repeat": job["repeat"],
                     "answer_sha256": sha(worker / "answer.md"), "reads_sha256": sha(worker / "reads.json"),
                     "context_id": "", "environment": {"model_id": "", "settings": {}, "settings_complete": False,
                     "tools_fingerprint": "", "context_mode": "fresh-per-job"},
                     "criteria": {key: "ungraded" for key in cases[job["case"]]["criteria"]}, "finding": "ungraded",
                     "false_claims": None, "unnecessary_actions": None, "notes": ""})
    return {"schema_version": 1, "experiment": str(folder), "experiment_sha256": sha(folder / "experiment.json"),
            "reviewer": "", "jobs": rows}


def known(value):
    return (isinstance(value, str) and bool(value.strip()) and
            not any(word in value.lower() for word in ("unknown", "unavailable", "not exposed", "inherit")))


def settings_known(value):
    if isinstance(value, dict): return all(settings_known(v) for v in value.values())
    if isinstance(value, list): return all(settings_known(v) for v in value)
    if isinstance(value, str): return value == "" or known(value)
    if type(value) is float: return math.isfinite(value)
    return value is None or type(value) in (int, bool)


def report(grades, root=ROOT, encoding=None):
    grades = json.loads(Path(grades).read_text())
    folder, data, cases = load(grades["experiment"], root)
    if grades.get("schema_version") != 1 or grades["experiment_sha256"] != sha(folder / "experiment.json") or not grades.get("reviewer"):
        raise ValueError("Missing reviewer or changed experiment")
    jobs = {job["id"]: job for job in data["jobs"]}
    if len(grades["jobs"]) != len(jobs) or {row["id"] for row in grades["jobs"]} != jobs.keys():
        raise ValueError("Missing, duplicate or foreign job grades")
    rows, environments, contexts, reasons = [], [], [], []
    for row in grades["jobs"]:
        job = jobs[row["id"]]
        if row.get("case") != job["case"] or row.get("repeat") != job["repeat"]:
            raise ValueError("Grades refer to a different case or repetition")
        worker = folder / "workers" / job["id"]
        if sha(worker / "answer.md") != row["answer_sha256"] or sha(worker / "reads.json") != row["reads_sha256"]:
            raise ValueError("Answer or actual-read log changed after sealing")
        criteria = row["criteria"]
        if set(criteria) != set(cases[job["case"]]["criteria"]) or any(v not in {"pass", "fail", "ungraded"} for v in criteria.values()):
            raise ValueError("Missing or invalid semantic grades")
        if not row.get("notes"):
            raise ValueError("Explain grades and unnecessary-action classification")
        for metric in ("false_claims", "unnecessary_actions"):
            if row[metric] is not None and (type(row[metric]) is not int or row[metric] < 0):
                raise ValueError("Invalid reviewed action/claim count")
            if row[metric] is None: reasons.append("ungraded action/claim counts")
        environment = row["environment"]
        if (not known(environment.get("model_id")) or not known(environment.get("tools_fingerprint")) or
                not isinstance(environment.get("settings"), dict) or not environment["settings"] or not settings_known(environment["settings"]) or
                environment.get("settings_complete") is not True):
            reasons.append("exact model/settings/tools not declared")
        if environment.get("context_mode") != "fresh-per-job" or not known(row.get("context_id")):
            reasons.append("fresh independent contexts not declared")
        environments.append(digest(environment)); contexts.append(row.get("context_id"))
        finding = row.get("finding")
        if finding not in {"reported", "not_reported", "not_applicable", "ungraded"}:
            raise ValueError("Missing or invalid finding grade")
        expected = {"supported": "reported", "unsupported": "not_reported", "not_applicable": "not_applicable"}[cases[job["case"]]["finding_expected"]]
        incomplete = "ungraded" in criteria.values() or finding == "ungraded"
        if incomplete: reasons.append("incomplete semantic grades")
        reads = read_log(worker, encoding)
        role = data["conditions"][job["condition"]]
        rows.append({"id": job["id"], "case": job["case"], "repeat": job["repeat"], "role": role,
                     "outcome": "fail" if "fail" in criteria.values() or (finding != "ungraded" and finding != expected) else "ungraded" if incomplete else "pass",
                     "finding": finding,
                     "false_positive": expected == "not_reported" and finding == "reported",
                     "false_negative": expected == "reported" and finding == "not_reported",
                     "module_read": any(r["path"] == "skills/" + data["module"] for r in reads),
                     "read_count": len(reads), "file_text_tokens": sum(r["file_text_tokens"] or 0 for r in reads) if encoding else None,
                     "read_hashes": reads, "false_claims": row["false_claims"], "unnecessary_actions": row["unnecessary_actions"]})
    if len(set(environments)) != 1: reasons.append("environments differ")
    if len(set(contexts)) != len(contexts): reasons.append("context reused across jobs")
    pairs = []
    if not reasons:
        for key in sorted({(row["case"], row["repeat"]) for row in rows}):
            group = {row["role"]: row for row in rows if (row["case"], row["repeat"]) == key}
            full, control = group["full"], group["ablated"]
            pairs.append({"case": key[0], "repeat": key[1], "full": full["outcome"], "ablated": control["outcome"],
                          "full_module_read": full["module_read"], "false_claim_delta": full["false_claims"] - control["false_claims"],
                          "unnecessary_action_delta": full["unnecessary_actions"] - control["unnecessary_actions"],
                          "file_text_token_delta": full["file_text_tokens"] - control["file_text_tokens"] if encoding else None})
    return {"schema_version": 1, "module": data["module"], "controlled_comparable": not reasons,
            "comparison_blockers": sorted(set(reasons)), "pairs": pairs, "jobs": rows,
            "limits": "Declared metadata and supplied read logs, not automatic telemetry. Only one reference's guidance is ablated; helpers stay available in both arms. Unread modules provide no evidence of instructional benefit. Paired observations are not statistical proof of a general gain."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("--output", type=Path, required=True); p.add_argument("--module", required=True)
    p.add_argument("--case", action="append", required=True); p.add_argument("--repeats", type=int, default=1); p.add_argument("--seed", type=int, default=0)
    p = sub.add_parser("seal"); p.add_argument("--experiment", type=Path, required=True); p.add_argument("--output", type=Path, required=True)
    p = sub.add_parser("report"); p.add_argument("--grades", type=Path, required=True); p.add_argument("--output", type=Path, required=True)
    p.add_argument("--tokens", action="store_true"); p.add_argument("--require-comparable", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            result = prepare(args.output, args.module, args.case, args.repeats, args.seed)
        elif args.command == "seal":
            result = seal(args.experiment); write_new(args.output, result)
            result = {"grade_template": str(args.output), "jobs": len(result["jobs"])}
        else:
            encoding = None
            if args.tokens:
                import tiktoken
                encoding = tiktoken.get_encoding("o200k_base")
            result = report(args.grades, encoding=encoding)
            write_new(args.output, result)
            if args.require_comparable and not result["controlled_comparable"]:
                parser.exit(2, "Comparison refused: " + "; ".join(result["comparison_blockers"]) + "\n")
        print(json.dumps(result, indent=2))
    except (ValueError, KeyError, TypeError, OSError, ImportError) as error:
        parser.exit(2, "ablation_eval: %s\n" % error)


if __name__ == "__main__":
    main()
