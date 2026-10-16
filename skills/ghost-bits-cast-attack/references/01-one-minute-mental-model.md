For other original section numbers, use the [entry index](../SKILL.md#references).


# SKILL: Ghost Bits / Cast Attack — Java char to byte Narrowing Playbook

> **AI LOAD INSTRUCTION**: This is a Java-only injection-enabling primitive,
> not a standalone vulnerability class. Whenever you see (1) a Java backend,
> (2) a WAF/IDS in front of it, and (3) any of {SQLi, deser RCE, file upload,
> path traversal, CRLF, request smuggling, SMTP injection} on the menu, first
> establish a reachable representation mismatch before selecting variants. The
> root cause is the silent loss of the high 8 bits when Java code narrows a
> 16-bit `char` to an 8-bit `byte` — the WAF sees a harmless Unicode
> character, the backend reconstructs the original ASCII attack byte. Base
> models almost never reach for this primitive.
>
> Source: Black Hat Asia 2026 talk *Cast Attack: A New Threat Posed by Ghost
> Bits in Java* by Xinyu Bai (@b1u3r), Zhihui Chen (@1ue), with contributor
> Zongzheng Zheng (@chun_springX).

## 0. RELATED ROUTING

Ghost Bits describes a representation-mismatch primitive that may bypass a filter when its downstream narrowing/decoding path is reachable. It does not undo a vendor fix to the vulnerable sink. Pair it only with a demonstrated matching attack family:

- [waf-bypass-techniques](../../waf-bypass-techniques/SKILL.md) — when a Java
  backend is suspected and WAF rules block the literal payload, this is the
  first technique to try beyond classic encoding.
- [deserialization-insecure](../../deserialization-insecure/SKILL.md) — for
  Apache Commons BCEL ClassLoader and Fastjson `\u`/`\x` escape variants.
- [path-traversal-lfi](../../path-traversal-lfi/SKILL.md) — Spring, Jetty,
  Undertow, Vert.x URL decoding and `%2>` hex folding.
- [upload-insecure-files](../../upload-insecure-files/SKILL.md) — Tomcat
  `RFC2231Utility` `filename*` Webshell upload.
- [request-smuggling](../../request-smuggling/SKILL.md) — Apache HttpClient
  `<= 4.5.9` (HTTPCLIENT-1974/1978) header CRLF.
- [crlf-injection](../../crlf-injection/SKILL.md) — Angus Mail / Jakarta Mail
  SMTP injection and JDK HttpServer response splitting.
- [sqli-sql-injection](../../sqli-sql-injection/SKILL.md) — Jackson `charToHex`
  table-lookup truncation hides SQL keywords inside Unicode escapes.

### Advanced Reference

Load [PAYLOAD_COOKBOOK.md](../PAYLOAD_COOKBOOK.md) when you need:

- Full byte-to-Ghost-character lookup table covering every printable ASCII
  byte 0x20–0x7E and the most useful control bytes (0x00, 0x09, 0x0A, 0x0D).
- Per-component affected version matrix and patch identifiers.
- Yaklang and Python one-liner payload generators (for `poc.HTTP`,
  `codec.Encode`, raw socket).
- "Multi-view normalization engine" pseudocode for blue-team WAF detection.

---

## 1. ONE-MINUTE MENTAL MODEL

Java's `char` is a **16-bit** unsigned integer (UTF-16 code unit). Almost
every wire protocol — HTTP/1.1, SMTP, Redis RESP, file paths, raw byte
streams — is **8-bit** byte oriented. The right way to bridge them is
explicit charset encoding:

```
// Correct: explicit UTF-8, multi-byte chars become multi-byte sequences
byte[] bytes = str.getBytes(StandardCharsets.UTF_8);
out.write(bytes);
```

Tons of legacy code, framework internals, and "fast path" optimizations skip
this and silently narrow:

```
// Dangerous: high 8 bits silently dropped
byte b = (byte) ch;          // 0x966A -> 0x6A
out.write(ch);               // ByteArrayOutputStream.write(int) keeps low 8 bits
dos.writeBytes(str);         // DataOutputStream loops char->byte cast
int v = ch & 0xFF;           // explicit low-byte mask
```

The lost high 8 bits are the **Ghost Bits**. They turn a multi-byte
Unicode character into a single attacker-chosen ASCII byte at the protocol
layer.

```
View A (string layer: WAF / business validation / logs)
  sees: 陪 阮 严 灵 瘍 瘊 ...   "harmless Unicode garbage, allow"
                  |
                  v       silent narrowing somewhere in the call stack
View B (byte layer: protocol / file system / parser / class loader)
  sees: j  .  %  u  \r \n ...  "executes the dangerous semantics"

The boundary is breached at the exact moment "view A" and "view B" disagree.
```

Mathematical formulation: to make View B see byte `T`, pick any
`k in 0x01..0xFF` and use:

```
c = chr((k << 8) | T)
```

That gives you **255 candidate Unicode characters per dangerous byte** —
plenty of room to dodge any signature-based blacklist.

---

