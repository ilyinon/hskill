# Technical routing

Read this only when the task does not already identify its technical topic. Select one relevant row, then the matching playbook; do not read the entire linked family. All paths are relative to this file.

| Evidence or task | Entry |
|---|---|
| Unknown application or API | [Surface mapping](../attack-surface-mapping/SKILL.md); API documentation: [API recon](../api-recon-and-docs/SKILL.md) |
| Login, reset, session | [Authentication](../authbypass-authentication-flaws/SKILL.md); JWT signing/key/claims: [validation](../jwt-oauth-token-attacks/SKILL.md); federation: [OAuth/OIDC](../oauth-oidc-misconfiguration/SKILL.md) or [SAML](../saml-sso-assertion-attacks/SKILL.md) |
| Object, tenant, or function permissions | [IDOR](../idor-broken-object-authorization/SKILL.md); API-specific: [BOLA](../api-authorization-and-bola/SKILL.md) |
| Input evaluated by an interpreter; type unclear | [Injection routing](../injection-checking/SKILL.md) |
| URL fetched by server | [SSRF](../ssrf-server-side-request-forgery/SKILL.md) |
| XML/SVG/Office parsing | [XXE](../xxe-xml-external-entity/SKILL.md); stylesheet transform: [XSLT](../xslt-injection/SKILL.md) |
| Upload, preview, filename, download | [Upload workflow](../upload-insecure-files/SKILL.md); file path/include: [traversal](../path-traversal-lfi/SKILL.md) |
| Money, quota, approval, one-time action | [Business logic](../business-logic-vulnerabilities/SKILL.md); concurrency: [race](../race-condition/SKILL.md) |
| GraphQL or real-time API | [GraphQL](../graphql-and-hidden-parameters/SKILL.md) or [WebSocket](../websocket-security/SKILL.md) |
| Browser origin, request, or cache boundary | [Auth/browser routing](../auth-sec/SKILL.md); framing: [smuggling](../request-smuggling/SKILL.md); caching: [cache attacks](../web-cache-deception/SKILL.md) |
| Exposed service or middleware | [Service playbook](../unauthorized-access-common-services/SKILL.md), only the identified service section |
| Active Directory / Windows | [Kerberos](../active-directory-kerberos-attacks/SKILL.md), [ACL](../active-directory-acl-abuse/SKILL.md), [AD CS](../active-directory-certificate-services/SKILL.md); local host: [Windows privilege](../windows-privilege-escalation/SKILL.md) |
| Linux / macOS / container / Kubernetes | [Linux privilege](../linux-privilege-escalation/SKILL.md), [macOS controls](../macos-security-bypass/SKILL.md), [container](../container-escape-techniques/SKILL.md), [Kubernetes](../kubernetes-pentesting/SKILL.md) |
| Mobile application | [Android](../android-pentesting-tricks/SKILL.md) or [iOS](../ios-pentesting-tricks/SKILL.md) |
| Binary, VM, or memory corruption | [Binary protections](../binary-protection-bypass/SKILL.md), [VM reversing](../vm-and-bytecode-reverse/SKILL.md), [symbolic execution](../symbolic-execution-tools/SKILL.md); stack or heap: [ROP](../stack-overflow-and-rop/SKILL.md) or [heap](../heap-exploitation/SKILL.md) |
| Cryptographic construction | [Classical](../classical-cipher-analysis/SKILL.md), [symmetric](../symmetric-cipher-attacks/SKILL.md), [RSA](../rsa-attack-techniques/SKILL.md), [hash](../hash-attack-techniques/SKILL.md), [lattice](../lattice-crypto-attacks/SKILL.md) |
| Memory dump, capture, hidden data | [Memory](../memory-forensics-volatility/SKILL.md), [PCAP](../traffic-analysis-pcap/SKILL.md), [steganography](../steganography-techniques/SKILL.md) |
| AI application or smart contract | [AI/ML](../ai-ml-security/SKILL.md), [LLM](../llm-prompt-injection/SKILL.md), [Solidity](../smart-contract-vulnerabilities/SKILL.md), [DeFi](../defi-attack-patterns/SKILL.md) |

For a narrower unlisted topic, search sibling directory names first (`rg --files` with a specific topic filter), then inspect that topic's description. These rows are navigation, not a checklist or automatic authorization to execute techniques.
