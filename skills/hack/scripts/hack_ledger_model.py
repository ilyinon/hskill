#!/usr/bin/env python3
"""Reviewed fresh-ledger teaching model, not a payment-system implementation."""
import argparse
import json
from pathlib import Path
from hack_tool_contract import parse


def simulate(operations, policy, events):
    if (not isinstance(operations, dict) or not operations or
            not all(isinstance(k, str) and k and type(v) is int and v > 0 for k, v in operations.items())):
        raise ValueError("Expected positive integer authorized operations")
    if not isinstance(policy, str) or policy not in {"observed", "by-operation", "one-callback"}:
        raise ValueError("Unknown ledger policy")
    if not isinstance(events, list) or len(events) > 32:
        raise ValueError("events must be an array of at most 32 records")
    # Validate the entire trial before reducing any event.
    for index, event in enumerate(events):
        if not isinstance(event, dict) or not isinstance(event.get("type"), str) or event["type"] not in {"log", "transport-error", "complete"}:
            raise ValueError("Invalid event at index %d; no trial was run" % index)
        if event["type"] == "complete":
            op, delivery, amount = event.get("operation"), event.get("delivery"), event.get("amount")
            if (not isinstance(op, str) or op not in operations or not isinstance(delivery, str) or not delivery or
                    type(amount) is not int or amount != operations[op]):
                raise ValueError("Operation, delivery, or amount invalid; no trial was run")
    rows, deliveries, completed = [], set(), set()
    credit = 0
    for event in events:
        if event["type"] != "complete":
            continue
        op, delivery, amount = event["operation"], event["delivery"], event["amount"]
        duplicate = (delivery in deliveries if policy == "observed" else
                     op in completed if policy == "by-operation" else bool(completed))
        applied = not duplicate
        if applied: credit += amount
        rows.append({"operation": op, "delivery": delivery, "applied": applied, "amount": amount})
        deliveries.add(delivery)
        completed.add(op)
    return {"initial_credit": 0, "final_credit": credit, "rows": rows, "reset": "fresh ledger for this call"}


def invariant(result, operations):
    credited = {key: 0 for key in operations}
    for row in result["rows"]:
        if row["applied"]: credited[row["operation"]] += row["amount"]
    return {"holds": all(credited[key] <= limit for key, limit in operations.items()),
            "credited_by_operation": credited,
            "violations": [key for key, limit in operations.items() if credited[key] > limit],
            "limit": "At-most-once credit does not alone prove legitimate operations remain usable."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    args = parser.parse_args()
    try:
        data = parse(args.input.read_text())
        if not isinstance(data, dict) or set(data) != {"operations", "policy", "events"}:
            raise ValueError("Input requires exactly operations, policy and events")
        result = simulate(data["operations"], data["policy"], data["events"])
        check = invariant(result, data["operations"])
    except (ValueError, TypeError, KeyError, OSError) as error:
        parser.exit(2, "ledger model: %s\n" % error)
    print(json.dumps({"model": "synthetic fresh ledger", "result": result, "invariant": check}, indent=2))
    raise SystemExit(0 if check["holds"] else 1)


if __name__ == "__main__":
    main()
