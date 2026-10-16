# OAuth redirect registration and delivery

Read when evaluating registered redirect URIs and response destinations. Follow the actual redirect chain; a URL string alone does not establish an open redirect.

## 8. OAUTH — REDIRECT_URI BYPASS

Authorization codes are sent to `redirect_uri`. If validation is weak:

### Retained parser and allowlist candidates
```
Original: redirect_uri=https://target.com/callback
Attack:   redirect_uri=https://target.com/callback/../../../attacker.com
          redirect_uri=https://attacker.com.target.com/callback
          redirect_uri=https://target.com@attacker.com/callback
```

### Partial path matching candidates
```
Whitelist: https://target.com/callback
Attack: https://target.com/callback%2f../admin (URL path confusion)
        https://target.com/callbackXSS (prefix match only)
```

### Localhost / Development Redirect
```
redirect_uri=http://localhost/steal
redirect_uri=urn:ietf:wg:oauth:2.0:oob  (mobile apps)
```

The candidate strings above are not universal bypasses. For example, `/callback/../../../attacker.com` remains a path on `target.com`, and `attacker.com.target.com` is a subdomain of `target.com`. Use parsed scheme/authority plus the registered exact redirect policy as controls; demonstrate actual code/token delivery to a forbidden recipient. Native loopback redirects have profile-specific exceptions. Legacy out-of-band redirects are provider-dependent. [RFC 9700 section 4.1](https://www.rfc-editor.org/rfc/rfc9700.html#section-4.1).
