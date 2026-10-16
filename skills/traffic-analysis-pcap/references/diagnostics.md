# PCAP: reconstruct the relevant protocol unit before interpreting it

Read when choosing a technique, interpreting a failed attempt, or deciding the next useful check. Use only rows matching the observed task; this is not an extra mandatory sweep.

## Establish applicability and branch on evidence

| Required fact | Smallest useful check |
|---|---|
| File/container and capture bounds | Identify PCAP/PCAPNG, link type, snap length, record lengths, truncation, and vantage. |
| Conversation and direction | Group the actual endpoint/port tuple; separate request and response directions. |
| Protocol framing and order | Inspect stream sequence, retransmission/overlap, IP fragmentation, encoding, and encryption. |
| Question and attribution | Separate visible request bytes, server response, process/user identity, and incident classification. |

| Observation | Competing explanations | Discriminating check and next step |
|---|---|---|
| strings/grep finds no complete request or marker | Segmentation, compression/encryption, truncation, or absence | Inspect the relevant flow's framing and completeness before concluding the value is absent. |
| Packet arrival order gives nonsense | Out-of-order delivery or a wrong flow/direction | Reassemble by protocol sequence within one direction; timestamps alone do not order TCP bytes. |
| A retransmission appears | Exact duplicate or conflicting overlap | Compare overlapping bytes; collapse exact duplicates and preserve ambiguity for conflicts. |
| There is a gap | Missing capture or a missing direction/window | Mark missing bytes. Do not invent an HTTP target, credential, or command from context. |
| A decoder rejects the file | Wrong link/container type, malformed record, or unsupported feature | Confirm file layout and a known-good parser baseline; tool failure is not absence of traffic. |

## Close the requested task

Track `capture record → directional bytes → complete protocol unit → observed event → supported incident conclusion`. For extraction, validate recovered bytes against independent lengths/format and report packet/stream locations. For triage, a visible request does not prove a server accepted it or identify the originating process. A limited fixture decoder is not a general TCP/IP implementation.
