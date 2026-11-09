# Keep bulk tool output out of the conversation

Use whenever a command can return more than ~200 lines: disassembly, hex
dumps, logs, pcaps, directory trees, HTTP bodies, scanner output. Long contexts
make every subsequent step slower and degrade reasoning; a context full of raw
listing is the common failure mode, not a detail.

## Rule

Never page a bulk artifact through the conversation (`sed -n 'N,Mp'` over a
dump, repeated `cat` of log regions). Write the full output to a file under
`work/` once, extract answers from it with scripts, and load only the slice
that answers the current question — typically tens of lines around a named
symbol, string, or offset, never whole sections.

One artifact serves many questions: re-extract from the saved file instead of
re-running the producer command.

## Binary / firmware analysis

```sh
mkdir -p work/bin
objdump -d -M intel target > work/bin/target.asm   # once, to a file
objdump -s -j .rodata target > work/bin/rodata.txt
strings -t x target > work/bin/strings.txt
```

Then interrogate the files, not the terminal:

- `rg -n 'call|jmp' work/bin/target.asm | rg 'main|auth|flag'` — find the
  interesting functions and their callers/xrefs by name or address.
- Extract a symbol-delimited function slice; do not stop at an early `ret`:

```sh
awk '
  /^[[:space:]]*[[:xdigit:]]+[[:space:]]+<[^>]+>:/ {
    if (found) exit
    found = ($0 ~ /<check_auth>:/)
  }
  found
' work/bin/target.asm
```

This bounds one symbol, not its full control-flow graph. Inspect referenced
cold blocks, tail-call targets, and stripped/aliased labels separately; an
empty slice is inconclusive.

- Decode structures, tables, and packed data with a short Python script over
  the file; record the decoded result, not the hex.
- Record findings as `function: address, behavior, relevant constants` in the
  working record, so a context reset never requires re-reading the listing.

## Logs, pcaps, HTTP

Same shape: capture to file (`tcpdump -w`, `curl -o`, tool output
redirection), then filter/aggregate (`jq`, `tshark -Y`, `awk` counts) and load
only the matching records. A 12 KB response body is quoted only when its exact
bytes are the finding.

## Limit

A pasted excerpt must support a specific hypothesis or the final evidence. If
an excerpt does not change a decision, keep its file path instead.
