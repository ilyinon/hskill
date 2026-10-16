# ssrf-server-side-request-forgery technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 9. THE SSRF-FILTER MINDSET

From zseano's methodology: **if developers filter only `169.254.169.254` directly but not `http://169.254.169.254/latest/meta-data`** (full path), or forget about:
- IPv6 equivalents  
- DNS names that resolve to internal IPs
- Redirect chains (server follows 302 to internal IP)

**Classic gap**: App filters `127.0.0.1` but not `127.1` or `[::1]` or `localhost`.

**Application-layer SSRF via XML** (when app parses XML):
```xml
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">]>
<request>&xxe;</request>
```
