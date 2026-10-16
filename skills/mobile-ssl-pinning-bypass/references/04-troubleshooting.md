# mobile-ssl-pinning-bypass technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 6. TROUBLESHOOTING

### 6.1 Common Failures

| Symptom | Cause | Fix |
|---|---|---|
| Bypass script loaded but traffic still fails | Multiple pinning layers | Hook ALL layers: TrustManager + OkHttp + custom checks |
| "Client certificate required" | Mutual TLS (mTLS) | Extract client cert from app bundle/keychain, import into proxy |
| Connection works but no HTTP traffic | Non-HTTP protocol (MQTT, gRPC, WebSocket) | Use Wireshark or protocol-specific proxy |
| App crashes after bypass | Anti-tampering detects hooks | Bypass integrity checks first, then SSL |
| Proxy CA not trusted | Android 7+ user CA restrictions | Install CA as system cert (Magisk module) |
| Flutter app ignores hooks | BoringSSL not hooked at native layer | Use reflutter or native BoringSSL hooks |
| Certificate chain validation timeout | OCSP stapling mismatch | Disable OCSP checks or mock OCSP responder |

### 6.2 Diagnostic Steps

```bash
# Verify proxy CA is installed correctly
# Android:
adb shell "ls /system/etc/security/cacerts/ | grep $(openssl x509 -subject_hash_old -in ca.pem | head -1)"

# iOS: Settings → General → About → Certificate Trust Settings

# Check if target app is actually using SSL (vs. plain HTTP)
# Wireshark filter: tcp.port == 443 and ip.addr == <device_ip>

# Check if Frida is hooking the right process
frida-ps -U | grep target

# Verbose Frida output for debugging hooks
frida -U -f com.target.app -l bypass.js --debug
```

---

## 7. SSL PINNING BYPASS DECISION TREE

```
Need to intercept mobile app HTTPS traffic
│
├── Platform?
│   ├── Android ↓
│   │   ├── Rooted device available?
│   │   │   ├── Yes → Frida universal bypass (§2.1) [FIRST TRY]
│   │   │   │   ├── Works? → done
│   │   │   │   └── Fails? → add Conscrypt + Volley hooks
│   │   │   ├── Still fails? → LSPosed + TrustMeAlready (§2.4)
│   │   │   └── Still fails? → install CA as system cert (§2.5)
│   │   └── No root?
│   │       ├── Debug build? → Network Security Config (§2.3)
│   │       └── Release build? → decompile + patch + repackage (§2.6)
│   │
│   └── iOS ↓
│       ├── Jailbroken device available?
│       │   ├── Yes → Objection ios sslpinning disable (§3.2) [FIRST TRY]
│       │   │   ├── Works? → done
│       │   │   └── Fails? → Frida SecTrust hooks (§3.1)
│       │   ├── Still fails? → SSL Kill Switch 2 (§3.3)
│       │   └── Still fails? → library-specific hooks (§3.4)
│       └── No jailbreak?
│           ├── Re-sign with Frida gadget → run Frida hooks
│           └── Binary patch → sideload (§3.5)
│
├── Framework-specific app?
│   ├── Flutter → reflutter tool or BoringSSL native hooks (§4.1)
│   ├── React Native → standard platform hooks (§4.2)
│   └── Xamarin → Objection or Mono runtime hooks (§4.3)
│
├── Bypass works but issues remain?
│   ├── Client cert required? → extract + import to proxy (§6.1)
│   ├── Non-HTTP protocol? → protocol-specific tooling (§6.1)
│   └── App crashes? → fix anti-tampering first (§6.1)
│
└── All methods fail?
    ├── Analyze traffic at network level (Wireshark/tcpdump)
    ├── Check for custom proprietary protocol
    └── Consider iptables + transparent proxy approach
```

---

## 8. PROXY SETUP QUICK REFERENCE

| Proxy Tool | Best For | SSL Bypass Integration |
|---|---|---|
| Burp Suite | Full HTTP analysis | Import CA to device |
| mitmproxy | Scripted interception | `mitmproxy --set confdir=~/.mitmproxy` |
| Charles Proxy | macOS-native, easy setup | Built-in CA installation |
| Proxyman | macOS/iOS native | Direct iOS device support |
| HTTP Toolkit | Quick Android setup | Automated CA + Frida bypass |

```bash
# Android proxy setup
adb shell settings put global http_proxy <host_ip>:8080

# Remove proxy
adb shell settings put global http_proxy :0

# iOS proxy: Settings → Wi-Fi → Configure Proxy → Manual
```
