# Worked case: grep misses a request split across reversed packets

Synthetic complete two-record [capture](./examples/request.pcap), [context](./examples/input.json), and [limited decoder](./examples/model.py). There is one directional Ethernet/IPv4/TCP flow and no response or handshake.

**Goal.** Recover the visible HTTP request target and state what the capture cannot establish.

**First approach.** Search packet bytes for `/status` or read payloads in arrival order. The target is split between segments; the higher-sequence segment is captured first. Neither approach reconstructs the protocol unit correctly.

**Revised approach.** Group the matching source/destination ports and direction, then order data by TCP sequence 1000 and 1008. Validate record lengths, contiguous ranges, and consistent overlap. Reassembly produces `GET /status HTTP/1.1` followed by the supplied Host header.

**Independent checks.** The reconstructed length equals the two nonoverlapping payload lengths, and the HTTP line/header terminators are present. `test_solving_examples.SolvingExamples.test_tcp_sequence_reassembly_and_missing_bytes` also accepts an exact retransmission, rejects a missing range, and rejects conflicting overlap. These controls distinguish recovery from a guessed string.

**Completed result.** The visible target is `/status`. No server response, request success, exploit, process identity, or malware attribution is supplied. The decoder deliberately excludes sequence wrap, IP fragmentation, TLS, and connection reuse; those need a suitable parser or more evidence.
