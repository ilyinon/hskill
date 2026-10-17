#!/usr/bin/env python3
"""Read-only JSON argument preflight. No tool or shell command is executed.

This deliberately small schema dialect is NOT a full JSON Schema validator.
Unknown keywords fail closed; use the tool's native validator for richer schemas.
"""
import argparse
import json
import math
from pathlib import Path

TYPES = {"object", "array", "string", "integer", "number", "boolean", "null"}
KEYS = {"type", "properties", "required", "additionalProperties", "items", "enum", "const",
        "minItems", "maxItems", "minLength", "maxLength", "minimum", "maximum", "description", "title"}


def parse(text):
    def reject(value):
        raise ValueError("Non-finite JSON number: " + value)
    def pairs(rows):
        result = {}
        for key, value in rows:
            if key in result:
                raise ValueError("Duplicate JSON key: " + key)
            result[key] = value
        return result
    def finite_float(value):
        number = float(value)
        if not math.isfinite(number):
            raise ValueError("Non-finite JSON number")
        return number
    return json.loads(text, parse_constant=reject, parse_float=finite_float, object_pairs_hook=pairs)


def check_schema(schema, location="$"):
    if not isinstance(schema, dict) or set(schema) - KEYS:
        raise ValueError(location + ": unsupported schema keyword or schema shape")
    kind = schema.get("type")
    if not isinstance(kind, str) or kind not in TYPES:
        raise ValueError(location + ": one explicit supported type is required")
    groups = {"object": {"properties", "required", "additionalProperties"}, "array": {"items", "minItems", "maxItems"},
              "string": {"minLength", "maxLength"}, "integer": {"minimum", "maximum"}, "number": {"minimum", "maximum"}}
    typed = set().union(*groups.values())
    if (set(schema) & typed) - groups.get(kind, set()):
        raise ValueError(location + ": keyword does not apply to declared type")
    for key in ("description", "title"):
        if key in schema and not isinstance(schema[key], str):
            raise ValueError(location + ": invalid annotation")
    for key in ("minItems", "maxItems", "minLength", "maxLength"):
        if key in schema and (type(schema[key]) is not int or schema[key] < 0):
            raise ValueError(location + ": invalid nonnegative bound")
    for key in ("minimum", "maximum"):
        if key in schema and (type(schema[key]) not in (int, float) or (type(schema[key]) is float and not math.isfinite(schema[key]))):
            raise ValueError(location + ": invalid numeric bound")
    for lower, upper in (("minimum", "maximum"), ("minItems", "maxItems"), ("minLength", "maxLength")):
        if lower in schema and upper in schema and schema[lower] > schema[upper]:
            raise ValueError(location + ": reversed bounds")
    if "enum" in schema and (not isinstance(schema["enum"], list) or not schema["enum"]):
        raise ValueError(location + ": nonempty enum array required")
    if kind == "object":
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        if (not isinstance(properties, dict) or not isinstance(required, list) or
                not all(isinstance(key, str) for key in required) or len(set(required)) != len(required) or
                not set(required).issubset(properties) or type(schema.get("additionalProperties", True)) is not bool):
            raise ValueError(location + ": invalid object contract")
        for key, value in properties.items():
            check_schema(value, location + "." + key)
    if kind == "array":
        if "items" not in schema:
            raise ValueError(location + ": explicit array items contract required")
        check_schema(schema["items"], location + "[]")


def equal(a, b):
    if type(a) in (int, float) and type(b) in (int, float):
        return a == b
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(equal(a[key], b[key]) for key in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(equal(x, y) for x, y in zip(a, b))
    return a == b


def validate(schema, value):
    check_schema(schema)
    errors = []
    def walk(rule, item, at):
        kind = rule["type"]
        matches = {"object": isinstance(item, dict), "array": isinstance(item, list), "string": isinstance(item, str),
                   "integer": type(item) is int, "number": type(item) in (int, float),
                   "boolean": type(item) is bool, "null": item is None}
        if not matches[kind] or (type(item) is float and not math.isfinite(item)):
            errors.append(at + ": expected " + kind)
            return
        if "enum" in rule and not any(equal(item, option) for option in rule["enum"]):
            errors.append(at + ": outside enum")
        if "const" in rule and not equal(item, rule["const"]):
            errors.append(at + ": differs from const")
        if kind == "object":
            properties = rule.get("properties", {})
            for key in rule.get("required", []):
                if key not in item:
                    errors.append(at + "." + key + ": required")
            for key, child in item.items():
                if key in properties:
                    walk(properties[key], child, at + "." + key)
                elif not rule.get("additionalProperties", True):
                    errors.append(at + "." + key + ": unknown field")
        elif kind == "array":
            for index, child in enumerate(item):
                walk(rule["items"], child, at + "[%d]" % index)
        if kind in {"array", "string"}:
            low, high = ("minItems", "maxItems") if kind == "array" else ("minLength", "maxLength")
            if low in rule and len(item) < rule[low]: errors.append(at + ": too short")
            if high in rule and len(item) > rule[high]: errors.append(at + ": too long")
        if kind in {"integer", "number"}:
            if "minimum" in rule and item < rule["minimum"]: errors.append(at + ": below minimum")
            if "maximum" in rule and item > rule["maximum"]: errors.append(at + ": above maximum")
    walk(schema, value, "$")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", required=True, type=Path)
    parser.add_argument("--input", required=True, type=Path)
    args = parser.parse_args()
    try:
        errors = validate(parse(args.schema.read_text()), parse(args.input.read_text()))
    except (ValueError, TypeError, OSError) as error:
        parser.exit(2, "preflight: %s\n" % error)
    print(json.dumps({"shape_valid": not errors, "errors": errors, "executed": False,
                      "limit": "Only the supplied contract was checked; acceptance, authority and semantic prerequisites are untested."}, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
