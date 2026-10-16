For other original section numbers, use the [entry index](../SKILL.md#references).


# SKILL: Upload Insecure Files — Validation Bypass, Storage Abuse, and Processing Chains

> **AI LOAD INSTRUCTION**: Expert file upload attack playbook. Use when the target accepts files, imports, avatars, media, documents, or archives and you need the full workflow: validation bypass, storage path abuse, post-upload access, parser exploitation, multi-tenant overwrite, and chaining into XSS, XXE, CMDi, traversal, or business logic impact. For web server parsing vulnerabilities, PUT method exploitation, and specific CVEs (WebLogic, Flink, Tomcat), load the companion [SCENARIOS.md](../SCENARIOS.md).

## 0. RELATED ROUTING

### Extended Scenarios

Also load [SCENARIOS.md](../SCENARIOS.md) when you need:
- IIS parsing vulnerabilities — `x.asp/` directory parsing, `;` semicolon truncation (`shell.asp;.jpg`)
- Nginx parsing misconfiguration — `avatar.jpg/.php` with `cgi.fix_pathinfo=1`
- Apache parsing — multiple extensions, `AddHandler`, CVE-2017-15715 `\n` (0x0A) bypass
- PUT method exploitation — IIS WebDAV PUT+COPY, Tomcat CVE-2017-12615 `readonly` + `.jsp/` bypass
- WebLogic CVE-2018-2894 arbitrary file upload via Web Service Test Page
- Apache Flink CVE-2020-17518 file upload with path traversal
- Upload + parsing vulnerability chain — EXIF PHP code + Nginx `/.php` path info
- Full extension bypass reference table (PHP/ASP/JSP alternatives, case variations, null bytes)

Use this file as the deep upload workflow reference. Also load:

- [path traversal lfi](../../path-traversal-lfi/SKILL.md) when filename, extraction path, or include path becomes file-system control
- [xss cross site scripting](../../xss-cross-site-scripting/SKILL.md) when uploads are rendered in browser contexts
- [xxe xml external entity](../../xxe-xml-external-entity/SKILL.md) when SVG, OOXML, or XML imports are accepted
- [cmdi command injection](../../cmdi-command-injection/SKILL.md) when a processor, converter, or media pipeline executes system tools
- [business logic vulnerabilities](../../business-logic-vulnerabilities/SKILL.md) when quotas, overwrite rules, approvals, or storage paths create logic bugs
- [ghost-bits-cast-attack](../../ghost-bits-cast-attack/SKILL.md) when the server is **Apache Tomcat** and the WAF blocks `.jsp` in `filename*` — Tomcat's `RFC2231Utility` narrows each char to byte, so `1.陪sp` (U+966A low byte = `j`) writes `1.jsp` to disk while the WAF sees no `.jsp` literal

---

## 1. CORE MODEL

Every upload feature should be tested as four separate trust boundaries:

1. **Accept**: what validation happens before the file is stored?
2. **Store**: where is the file written and under what name and permissions?
3. **Process**: what background tools, converters, scanners, parsers, or extractors touch it?
4. **Serve**: how is it later downloaded, rendered, transformed, or shared?

Many targets validate only one stage. The bug usually appears in a different stage than the one where the file was uploaded.

---

## 2. RECON QUESTIONS FIRST

Before payload selection, answer these:

- Which extensions are allowed, denied, or normalized?
- Does the backend trust extension, MIME type, magic bytes, or all three?
- Is the file renamed, transcoded, unzipped, scanned, or re-hosted?
- Is retrieval direct, proxied, signed, or served from a CDN?
- Can one user predict or overwrite another user's file path?
- Do filenames, metadata, or previews reflect back into HTML, logs, admin consoles, or PDFs?

---

## 3. VALIDATION BYPASS MATRIX

| Validation Style | What to Test |
|---|---|
| extension blacklist | double extension, case toggles, trailing dot, alternate separators |
| content-type only | mismatched multipart `Content-Type`, browser vs proxy rewrite |
| magic-byte only | polyglot files or valid header plus dangerous tail content |
| server-side rename | whether dangerous content survives rename and later rendering |
| image-only policy | SVG, malformed image plus metadata, parser differential |
| archive or import only | zip contents, nested path names, XML members, decompression behavior |

Representative bypass families:

```text
shell.php.jpg
avatar.jpg.php
file.asp;.jpg
file.php%00.jpg
file.svg
archive.zip
```

This small sample set already covers the main use cases of the former standalone upload payload helper, so no extra entry is needed for first-pass selection.

Do not stop at upload success. Successful upload without dangerous retrieval or processing is not enough.

---

## 4. STORAGE AND RETRIEVAL ABUSE

### Predictable or controllable paths

Look for patterns like:

```text
/uploads/USER_ID/avatar.png
/files/org-slug/report.pdf
/cdn/tmp/<uuid>/<filename>
```

Test for:

- cross-tenant read by guessing IDs, slugs, or UUID patterns
- overwrite by reusing another user's filename
- path normalization bugs in filename or archive members
- private file exposed through direct object URL despite UI-level access control

### Filename-based injection surfaces

A safe file can still be dangerous if the **filename** is reflected into:

- gallery HTML
- admin moderation panels
- PDF/CSV export jobs
- logs, audit views, or email notifications

If filename is reflected, treat it like stored input, not like passive metadata.

---

## 5. PROCESSING-CHAIN ATTACKS

The highest-value upload bugs often live in asynchronous processors.

### Common processor classes

| Processor | Risk |
|---|---|
| image resizing or thumbnailing | parser differential, ImageMagick or library bugs, metadata reflection |
| video or audio transcoding | FFmpeg-style parsing and protocol abuse |
| archive extraction | zip slip, overwrite, decompression bombs |
| document import | CSV formula injection, office XML parsing, macro-adjacent workflows |
| XML or SVG parsing | XXE, SSRF, local file disclosure |
| HTML to PDF or preview rendering | SSRF, script execution, local file references |
| AV or DLP scanning | unzip depth, hidden nested content, race conditions |

### What to prove

1. The file is touched by a processor.
2. The processor behaves differently from the upload validator.
3. That difference creates impact: read, execute, overwrite, SSRF, or stored client-side execution.

---

## 6. HIGH-VALUE EXPLOITATION PATHS

### Browser execution

- SVG served as active content
- HTML or text uploads rendered inline
- EXIF or filename reflected into an HTML page

### XML and document parsing

- SVG XXE for file read or SSRF
- OOXML import for XML entity or parser abuse
- CSV import for formula execution in analyst workflows

### Server-side execution or file-system impact

- image or document converter invoking shell tools
- zip slip writing outside intended directory
- upload-to-LFI chain where uploaded content later becomes includable

### Access-control and sharing bugs

- private upload accessible via predictable URL
- moderation or quarantine path still publicly reachable
- one user replacing another user's public asset

---

## 7. AUTHORIZATION AND BUSINESS LOGIC CHECKS

Upload features frequently hide non-parser bugs:

- upload quota enforced in UI but not API
- plan restrictions checked on upload page but not on import endpoint
- file ownership checked on list view but not on direct download or replace endpoint
- approval workflow bypassed by calling the final storage endpoint directly
- delete or replace action missing object-level authorization

When the upload path includes account, project, or organization identifiers, always run an A/B authorization test.

---

