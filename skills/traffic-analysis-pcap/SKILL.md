---
name: traffic-analysis-pcap
description: >-
  Traffic analysis and PCAP forensics playbook. Use when analyzing network captures including Wireshark filters, protocol analysis (HTTP/DNS/FTP/SMTP/USB/WiFi), data extraction, covert channel detection, PCAP repair, TLS decryption, and tshark command-line analysis.
---

# Traffic Analysis Pcap

## Working approach

- Preserve capture provenance/hash, timestamps, interfaces, and completeness
- Summarize endpoints, protocol hierarchy, and streams before selecting filters
- Reconstruct relevant conversations/files and correlate independent records.

## Evidence and limits

Reproducible stream/packet references support the stated behavior and timeline.

A port, long DNS name, beacon-like interval, or failed TLS decode alone is not malicious activity; retransmissions, truncation, decryption limits, and benign baselines matter.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. PCAP REPAIR; 2. WIRESHARK ESSENTIAL FILTERS | [Read](./references/01-pcap-repair.md) |
| 3. PROTOCOL ANALYSIS; 4. DATA EXTRACTION; 5. NETWORKMINER; 6. TSHARK COMMAND-LINE ANALYSIS | [Read](./references/02-protocol-analysis.md) |
| 7. DECISION TREE | [Read](./references/03-decision-tree.md) |
