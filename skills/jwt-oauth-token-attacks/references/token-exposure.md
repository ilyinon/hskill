# Token transport and exposure

Read for tokens in URLs, scripts, history, or telemetry. Keep exposure separate from credential validity and permission to use it. Status and limits: see the named record in the [verification registry](../../hack/verification.json). Record: `token-exposure`.

## 11. TOKEN LEAKAGE VECTORS

### Referer Header and URL Fragments

Browsers do not include the URL fragment in Referer. A token after `#access_token=` therefore does not leak through that header alone. Query tokens may leak depending on the effective referrer policy and destination; browser history, page scripts, or application telemetry are separate leakage paths that require their own evidence. [Referer semantics](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referer).

### Server Logs
Query tokens can reach configured access logs. Inspect the actual logging/redaction configuration and captured entries; these locations are candidates, not proof that every deployment stores tokens:
```
/var/log/nginx/access.log
/var/log/apache2/access.log
ELB/ALB logs (AWS)
CloudFront logs
CDN logs
```
