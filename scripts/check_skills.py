#!/usr/bin/env python3
"""Read-only structural, reference, and optional token-budget checks.

Run: python3 scripts/check_skills.py
Optional: install PyYAML for full YAML parsing and tiktoken for token counts.
Examples and external tools are never executed. The default check is offline;
optional token counts may download tiktoken's encoding table on first use.
"""
import argparse
import json
import math
from pathlib import Path
import re

try:
    import yaml
except ImportError:
    yaml = None

try:
    import tiktoken
except ImportError:
    tiktoken = None


def prose(text):
    marker = None
    output = []
    for line in text.splitlines():
        fence = re.match(r"^[ \t]*(`{3,}|~{3,})(.*)$", line)
        if fence:
            value, tail = fence.groups()
            if marker is None:
                marker = value
            elif value[0] == marker[0] and len(value) >= len(marker) and not tail.strip():
                marker = None
            continue
        if marker is None:
            # Exclude inline code while retaining code-formatted link labels.
            if re.match(r"^#{1,6}\s", line):
                output.append(re.sub(r"(`+)(.*?)\1", r"\2", line))
            else:
                output.append(re.sub(r"(`+).*?\1", "", line))
    return "\n".join(output), marker is None


def links(text):
    plain, _ = prose(text)
    return re.findall(r"\[[^\]\n]*\]\(([^\s)]+)\)", plain)


def anchors(text):
    plain, _ = prose(text)
    found = set()
    counts = {}
    for title in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", plain, re.M):
        value = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        occurrence = counts.get(value, 0)
        counts[value] = occurrence + 1
        found.add(value + (f"-{occurrence}" if occurrence else ""))
    found.update(re.findall(r'<a\s+(?:id|name)=["\x27]([^"\x27]+)', plain))
    return found


def inspect(root, max_entry_tokens=1600, encoding=None):
    root = Path(root).resolve()
    files = sorted(root.rglob("*.md"))
    entries = sorted(root.glob("*/SKILL.md"))
    errors = []
    warnings = []
    graph = {}
    token_rows = []
    document_tokens = []
    if not root.is_dir():
        errors.append(f"Skills directory does not exist: {root}")
    elif not entries:
        errors.append(f"No */SKILL.md entry points found: {root}")
    text_by_path = {p: p.read_text() for p in files}
    for path, text in text_by_path.items():
        relative = str(path.relative_to(root))
        if encoding:
            document_tokens.append({"path": relative, "tokens": len(encoding.encode(text, disallowed_special=()))})
        _, balanced = prose(text)
        if not balanced:
            errors.append(f"{relative}: unclosed fenced example")
        graph[path] = []
        for target in links(text):
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            name, _, fragment = target.partition("#")
            destination = (path.parent / name).resolve() if name else path
            if not destination.is_relative_to(root):
                errors.append(f"{relative}: reference escapes skills directory: {target}")
            elif not destination.is_file():
                errors.append(f"{relative}: missing reference: {target}")
            else:
                graph[path].append(destination)
                destination_text = text_by_path.get(destination)
                if destination_text is None and fragment and destination.suffix == ".md":
                    destination_text = destination.read_text()
                if fragment and destination.suffix == ".md" and fragment not in anchors(destination_text):
                    errors.append(f"{relative}: missing reference section: {target}")
    names = set()
    for path in entries:
        relative = str(path.relative_to(root))
        text = text_by_path[path]
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        if not match:
            errors.append(f"{relative}: missing YAML frontmatter")
            continue
        if yaml:
            try:
                data = yaml.safe_load(match.group(1))
            except yaml.YAMLError as exc:
                errors.append(f"{relative}: invalid YAML: {exc}")
                continue
        else:
            data = dict(re.findall(r"^(name|description):\s*(.+)$", match.group(1), re.M))
        if not isinstance(data, dict):
            errors.append(f"{relative}: frontmatter is not a mapping")
            continue
        name = data.get("name")
        description = data.get("description")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64 or name != path.parent.name:
            errors.append(f"{relative}: invalid or mismatched name")
        if not isinstance(description, str) or not description.strip() or len(description) > 1024:
            errors.append(f"{relative}: missing, invalid, or overlong description")
        if isinstance(name, str):
            if name in names:
                errors.append(f"{relative}: duplicate skill name")
            names.add(name)
        if encoding:
            count = len(encoding.encode(text, disallowed_special=()))
            token_rows.append({"skill": name, "tokens": count})
            if count > max_entry_tokens:
                warnings.append(f"{relative}: {count} tokens exceeds review budget {max_entry_tokens}")
    reachable = set()
    queue = list(entries)
    while queue:
        current = queue.pop()
        if current in reachable:
            continue
        reachable.add(current)
        queue.extend(graph.get(current, []))
    orphaned = sorted(str(p.relative_to(root)) for p in files if p not in reachable)
    if orphaned:
        warnings.append(f"Unreachable from skill entry points: {', '.join(orphaned)}")
    return {
        "skills": len(entries), "markdown_files": len(files),
        "full_yaml_validation": yaml is not None,
        "errors": errors, "warnings": warnings,
        "unreachable_references": orphaned,
        "entry_tokens": sorted(token_rows, key=lambda row: row["tokens"], reverse=True),
        "document_tokens": document_tokens,
    }


def compare_budget(result, baseline):
    """Review material growth; thresholds are maintenance choices, not model limits."""
    old = {row["path"]: row["tokens"] for row in baseline["document_tokens"]}
    new = {row["path"]: row["tokens"] for row in result["document_tokens"]}
    changes = []
    for path in sorted(old.keys() | new.keys()):
        before, after = old.get(path, 0), new.get(path, 0)
        if before == after:
            continue
        changes.append({"path": path, "before": before, "after": after, "delta": after - before})
        if path in old and after - before > max(64, math.ceil(before * 0.15)):
            result["warnings"].append(f"{path}: token growth {before} -> {after}; review and intentionally refresh baseline")
        elif path not in old and not path.endswith("/SKILL.md") and after > 2000:
            result["warnings"].append(f"{path}: new reference exceeds 2000 tokens; review its task boundaries")
    result["token_changes"] = changes
    return changes


def write_summary(path, result):
    lines = ["## Skill checks", "", f"Skills: {result['skills']}; errors: {len(result['errors'])}; warnings: {len(result['warnings'])}.", ""]
    changes = result.get("token_changes", [])
    if changes:
        lines += ["| File | Before | After | Delta |", "|---|---:|---:|---:|"]
        lines += [f"| {row['path']} | {row['before']} | {row['after']} | {row['delta']:+d} |" for row in changes]
    elif "token_changes" in result:
        lines.append("No document token changes against the reviewed baseline.")
    else:
        lines.append("Token baseline comparison was not requested.")
    lines += ["", "Counts cover Markdown text only; they do not measure total model usage.", ""]
    path.write_text("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1] / "skills")
    parser.add_argument("--tokens", action="store_true", help="Use cached o200k_base tokenizer; requires tiktoken")
    parser.add_argument("--max-entry-tokens", type=int, default=1600)
    parser.add_argument("--json", type=Path)
    parser.add_argument("--baseline", type=Path, help="Compare document counts against an earlier --tokens --json report")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings as well as errors")
    parser.add_argument("--summary", type=Path, help="Write a Markdown CI summary")
    args = parser.parse_args()
    if args.tokens and tiktoken is None:
        parser.error("--tokens requires tiktoken")
    if args.baseline and not args.tokens:
        parser.error("--baseline requires --tokens")
    encoding = tiktoken.get_encoding("o200k_base") if args.tokens else None
    result = inspect(args.root, args.max_entry_tokens, encoding)
    if args.baseline:
        try:
            baseline = json.loads(args.baseline.read_text())
            if not baseline.get("document_tokens"):
                raise ValueError("baseline has no document token counts")
            compare_budget(result, baseline)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            parser.error(f"invalid token baseline: {exc}")
    if args.json:
        args.json.write_text(json.dumps(result, indent=2) + "\n")
    if args.summary:
        write_summary(args.summary, result)
    summary = {k: v for k, v in result.items() if k not in {"entry_tokens", "document_tokens"}}
    if result["entry_tokens"]:
        summary["largest_entries"] = result["entry_tokens"][:5]
    print(json.dumps(summary, indent=2))
    raise SystemExit(bool(result["errors"] or (args.strict and result["warnings"])))


if __name__ == "__main__":
    main()
