#!/usr/bin/env python3
"""Bounded offline replay of progressive observations and a tiny callback model.

No target, shell hook, fixture program, network, or dynamic Python is executed.
Completion is graded separately; submitting an answer never marks a case passed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/hack/scripts"))
import hack_ledger_model
import hack_tool_contract
MANIFEST = ROOT / "tests/staged_cases.json"
OUTCOMES = {"observation", "partial", "effect", "tool-error", "controlled-negative", "unknown"}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def safe_name(name):
    if not isinstance(name, str) or not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_.-]*", name):
        raise ValueError("Artifact names must be plain basenames")
    return name


def manifest(path=MANIFEST):
    data = json.loads(Path(path).read_text())
    if data.get("schema_version") != 1 or not data.get("cases"):
        raise ValueError("Unsupported or empty staged manifest")
    ids = set()
    for case in data["cases"]:
        safe_name(case["id"])
        if case["id"] in ids or type(case["budget"]) is not int or case["budget"] < 1:
            raise ValueError("Duplicate case or invalid budget")
        ids.add(case["id"])
        if not case.get("request") or not case.get("actions"):
            raise ValueError("Request and action menu required")
        check_files(case["initial"])
        for name, action in case["actions"].items():
            safe_name(name)
            if not action.get("help") or action["kind"] not in {"recording", "callback"}:
                raise ValueError("Unknown action kind or missing help")
            if action["kind"] == "recording":
                for row in action["variants"]:
                    if not isinstance(row["when"], dict) or row["outcome"] not in OUTCOMES:
                        raise ValueError("Invalid recorded observation")
                    check_files(row.get("publish", {}))
    return data


def check_files(files):
    if not isinstance(files, dict):
        raise ValueError("Artifacts must be a mapping")
    for name, content in files.items():
        safe_name(name)
        if not isinstance(content, str):
            raise ValueError("Artifacts must contain inert text")


def callback(action, arguments):
    """Small refund ledger: operation and delivery identity are distinct."""
    if (set(arguments) != {"policy", "events"} or not isinstance(arguments["policy"], str) or
            arguments["policy"] not in {"observed", "by-operation", "one-callback"}):
        return {"outcome": "tool-error", "result": "Expected policy and events array; see the action menu."}
    try:
        result = hack_ledger_model.simulate(action["operations"], arguments["policy"], arguments["events"])
    except ValueError as error:
        return {"outcome": "tool-error", "result": str(error)}
    return {"outcome": "observation", "evidence": "ledger-replay",
            "result": result}


def observe(case, observed, name, arguments):
    if not isinstance(arguments, dict):
        return {"outcome": "tool-error", "result": "arguments must be an object"}
    action = case["actions"].get(name)
    if action is None:
        return {"outcome": "tool-error", "result": "Unknown action; use the request's menu"}
    if not set(action.get("requires", [])).issubset(observed):
        return {"outcome": "unknown", "result": "Required observation not yet available; inspect the supplied artifacts"}
    if action["kind"] == "callback":
        return callback(action, arguments)
    for row in action["variants"]:
        if (arguments == row["when"] and set(row.get("after", [])).issubset(observed) and
                not set(row.get("before", [])).intersection(observed)):
            return {key: value for key, value in row.items() if key not in {"when", "after", "before"}}
    return {"outcome": "unknown", "result": "No recorded observation for this input. This is not a negative result."}


def save(path, value):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n")
    temporary.replace(path)


def start(case_id, session):
    cases = manifest()["cases"]
    case = next((c for c in cases if c["id"] == case_id), None)
    if case is None:
        raise ValueError("Unknown case")
    session = Path(session).resolve()
    session.mkdir(parents=True, exist_ok=False)
    public = session / "task"
    artifacts = public / "artifacts"
    artifacts.mkdir(parents=True)
    for name, content in case["initial"].items():
        (artifacts / name).write_text(content)
    menu = "\n".join("- `%s`: %s" % (name, action["help"]) for name, action in case["actions"].items())
    request = (case["request"] + "\n\nAll inputs are synthetic and offline. Use only this task's artifacts, "
               "the supplied skill, and the trusted staged runner. Do not inspect its implementation, "
               "the case manifest, tests, or grading rubric. Write a JSON file containing "
               '`{"action": "NAME", "arguments": {...}}` and pass it to `act`. '
               "Every accepted call costs one simulated action, including errors. "
               "These costs do not measure total agent/tool usage. Unknown inputs have no recorded outcome. "
               "Use `status` to resume from observations. Keep actual skill reads in a separate log. "
               "Submit a concrete answer file using `finish`; it is graded separately.\n\n"
               "Action budget: %d\n\n%s\n" % (case["budget"], menu))
    (public / "request.md").write_text(request)
    save(session / "session.json", {"schema_version": 1, "case": case_id, "input_digest": digest(case), "history": []})
    return {"request": str(public / "request.md"), "session": str(session), "budget": case["budget"]}


def load(session):
    session = Path(session).resolve()
    data = json.loads((session / "session.json").read_text())
    case = next((c for c in manifest()["cases"] if c["id"] == data["case"]), None)
    if case is None or data.get("schema_version") != 1 or data["input_digest"] != digest(case):
        raise ValueError("Scenario changed; start a new session instead of mixing observations")
    for name, content in case["initial"].items():
        if (session / "task" / "artifacts" / name).read_text() != content:
            raise ValueError("Initial artifact changed; preserve the original input")
    observed = set()
    if len(data["history"]) > case["budget"]:
        raise ValueError("Invalid history length")
    for index, row in enumerate(data["history"], 1):
        response = observe(case, observed, row["action"], row["arguments"])
        if row["step"] != index or row["response"] != response:
            raise ValueError("History no longer reproduces the recorded scenario")
        if json.loads((session / "task" / ("observation-%02d.json" % index)).read_text()) != row:
            raise ValueError("Preserved observation changed")
        for name, content in response.get("publish", {}).items():
            path = session / "task" / "artifacts" / ("%02d-%s" % (index, name))
            if path.read_text() != content:
                raise ValueError("Published artifact changed")
        if response.get("evidence"):
            observed.add(response["evidence"])
    return session, data, case, observed


def act(session, request, contract=None):
    if contract is not None:
        errors = hack_tool_contract.validate(contract, request)
        if errors:
            raise ValueError("Preflight rejected arguments; no action ran: " + "; ".join(errors))
    session, data, case, observed = load(session)
    if "submission" in data:
        raise ValueError("Session already submitted")
    if len(data["history"]) >= case["budget"]:
        raise ValueError("Action budget exhausted; preserve the partial answer")
    if not isinstance(request, dict) or set(request) != {"action", "arguments"} or not isinstance(request["action"], str):
        raise ValueError("Call must contain action name and arguments")
    response = observe(case, observed, request["action"], request["arguments"])
    row = {"step": len(data["history"]) + 1, **request, "response": response}
    observation = session / "task" / ("observation-%02d.json" % row["step"])
    # Raw observations and published artifacts are append-only; old sources remain.
    for name, content in response.get("publish", {}).items():
        (session / "task" / "artifacts" / ("%02d-%s" % (row["step"], safe_name(name)))).write_text(content)
    save(observation, row)
    data["history"].append(row)
    save(session / "session.json", data)
    return row


def status(session):
    session, data, case, observed = load(session)
    signatures = [digest({key: row[key] for key in ("action", "arguments")}) for row in data["history"]]
    outcomes = {kind: sum(row["response"]["outcome"] == kind for row in data["history"]) for kind in sorted(OUTCOMES)}
    result = {"case": case["id"], "input_digest": data["input_digest"], "used": len(signatures),
              "remaining": case["budget"] - len(signatures), "repeated_inputs": len(signatures) - len(set(signatures)),
              "outcomes": outcomes, "observed": sorted(observed), "history": data["history"],
              "grading": "pending independent review; repeated input is not necessarily wasted work"}
    if "submission" in data:
        answer = session / "task" / "answer.md"
        if hashlib.sha256(answer.read_bytes()).hexdigest() != data["submission"]["sha256"]:
            raise ValueError("Submitted answer changed")
        result["submission"] = data["submission"]
    return result


def finish(session, answer):
    session, data, _, _ = load(session)
    if "submission" in data:
        raise ValueError("Session already submitted")
    answer = Path(answer).resolve()
    if not answer.is_file() or not answer.read_text().strip():
        raise ValueError("A nonempty preserved answer is required")
    target = session / "task" / "answer.md"
    if answer != target:
        shutil.copyfile(answer, target)
    data["submission"] = {"answer_file": str(target), "sha256": hashlib.sha256(target.read_bytes()).hexdigest()}
    save(session / "session.json", data)
    result = status(session)
    save(session / "report.json", result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate")
    first = commands.add_parser("start")
    first.add_argument("--case", required=True)
    first.add_argument("--session", required=True)
    for command in ("act", "status", "finish"):
        sub = commands.add_parser(command)
        sub.add_argument("--session", required=True)
        if command == "act":
            sub.add_argument("--input", required=True, type=Path)
            sub.add_argument("--contract", type=Path, help="Optional current small-dialect argument contract; validates before any action")
        if command == "finish":
            sub.add_argument("--answer", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.command == "validate":
            result = {"validated": len(manifest()["cases"])}
        elif args.command == "start":
            result = start(args.case, args.session)
        elif args.command == "act":
            contract = hack_tool_contract.parse(args.contract.read_text()) if args.contract else None
            result = act(args.session, hack_tool_contract.parse(args.input.read_text()), contract=contract)
        elif args.command == "status":
            result = status(args.session)
        else:
            result = finish(args.session, args.answer)
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.exit(2, "staged_eval: %s\n" % error)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
