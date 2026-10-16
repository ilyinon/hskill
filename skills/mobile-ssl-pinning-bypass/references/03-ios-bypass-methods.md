# mobile-ssl-pinning-bypass technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 3. iOS BYPASS METHODS

### 3.1 Frida (SecTrust Hooks)

```javascript
// Hook core iOS SSL validation functions
var SecTrustEvaluateWithError = Module.findExportByName('Security', 'SecTrustEvaluateWithError');
Interceptor.attach(SecTrustEvaluateWithError, {
    onLeave: function(retval) {
        retval.replace(ptr(1));
    }
});

var SecTrustEvaluate = Module.findExportByName('Security', 'SecTrustEvaluate');
Interceptor.attach(SecTrustEvaluate, {
    onLeave: function(retval) {
        retval.replace(ptr(0));
    }
});

// Hook SSLHandshake (lower-level)
var SSLHandshake = Module.findExportByName('Security', 'SSLHandshake');
if (SSLHandshake) {
    Interceptor.attach(SSLHandshake, {
        onLeave: function(retval) {
            if (retval.toInt32() === -9807) { // errSSLXCertChainInvalid
                retval.replace(ptr(0));
            }
        }
    });
}

// Hook NSURLSession delegate method
try {
    var cls = ObjC.classes.NSURLSession;
    // Hook URLSession:didReceiveChallenge:completionHandler: on delegates
    ObjC.enumerateLoadedClasses({
        onMatch: function(name) {
            try {
                var methods = ObjC.classes[name].$ownMethods;
                for (var i = 0; i < methods.length; i++) {
                    if (methods[i].indexOf('didReceiveChallenge') !== -1 &&
                        methods[i].indexOf('completionHandler') !== -1) {
                        console.log('[SSL] Found delegate: ' + name + ' ' + methods[i]);
                    }
                }
            } catch(e) {}
        },
        onComplete: function() {}
    });
} catch(e) {}
```

### 3.2 Objection (One Command)

```bash
objection -g com.target.app explore --startup-command "ios sslpinning disable"
```

### 3.3 SSL Kill Switch 2 (Jailbreak Tweak)

```bash
# Install via Cydia/Sileo
# Package: com.nablac0d3.sslkillswitch2
# Disables SSL pinning system-wide or per-app via Settings toggle

# Hooks:
# - SecTrustEvaluate
# - SSLHandshake
# - SSLSetSessionOption
# - tls_helper_create_peer_trust
```

### 3.4 Library-Specific Hooks

| Library | iOS Hook Point | Frida Approach |
|---|---|---|
| AFNetworking | `AFSecurityPolicy.evaluateServerTrust:forDomain:` | Return YES |
| Alamofire | `ServerTrustManager.evaluate(_:forHost:)` | Skip evaluation |
| TrustKit | `TSKPinningValidator verifyPublicKeyPin:` | Return success |
| NSURLSession | `URLSession:didReceiveChallenge:completionHandler:` | Call completionHandler with .useCredential |

### 3.5 Manual Binary Patch

```bash
# Find pinning function in binary
strings decrypted_binary | grep -i "pin\|cert\|trust"
# Disassemble and find the validation function
# Replace comparison/branch instruction with NOP or unconditional pass

# LLDB runtime modification
lldb -n TargetApp
(lldb) breakpoint set -n "SecTrustEvaluateWithError"
(lldb) breakpoint command add 1
> thread return 1
> continue
> DONE
```

---

## 4. FRAMEWORK-SPECIFIC BYPASSES

### 4.1 Flutter

Flutter uses Dart's `dart:io` library with BoringSSL underneath. Standard Frida hooks on Java/ObjC layers don't work.

```javascript
// Flutter SSL bypass — must hook BoringSSL directly
// Find ssl_crypto_x509_session_verify_cert_chain in libflutter.so
var libflutter = Process.findModuleByName('libflutter.so');  // Android
// var libflutter = Process.findModuleByName('Flutter');       // iOS

// Hook ssl_verify_peer_cert (BoringSSL function)
// Signature varies by Flutter version — use pattern scanning
var pattern = 'FF C3 ..';  // Example pattern, varies
var matches = Memory.scan(libflutter.base, libflutter.size, pattern, {
    onMatch: function(address, size) {
        console.log('[Flutter] Potential verify function at: ' + address);
        Interceptor.attach(address, {
            onLeave: function(retval) {
                retval.replace(ptr(0));  // SSL_VERIFY_OK
            }
        });
    },
    onComplete: function() {}
});

// Alternative: use reflutter tool for automated patching
// reflutter target.apk
// This patches BoringSSL in the Flutter engine directly
```

**reflutter tool** (recommended for Flutter apps):

```bash
pip install reflutter
reflutter target.apk
# Outputs patched APK that redirects traffic to your proxy
# Also disables SSL verification in the BoringSSL engine
```

### 4.2 React Native

React Native uses platform networking: OkHttp on Android, NSURLSession on iOS.

| Platform | Networking Stack | Bypass Method |
|---|---|---|
| Android | OkHttp3 | Standard OkHttp CertificatePinner hook |
| iOS | NSURLSession | Standard SecTrust hooks |
| Android (Hermes) | Same OkHttp | Same hooks, but Hermes JIT may need additional handling |

```javascript
// React Native Android — same as OkHttp bypass
Java.perform(function() {
    try {
        var CP = Java.use('okhttp3.CertificatePinner');
        CP.check.overload('java.lang.String', 'java.util.List').implementation = function() {};
    } catch(e) { console.log('OkHttp3 not found, trying okhttp2...'); }

    try {
        var CP2 = Java.use('com.squareup.okhttp.CertificatePinner');
        CP2.check.overload('java.lang.String', 'java.util.List').implementation = function() {};
    } catch(e) {}
});
```

### 4.3 Xamarin

```csharp
// Xamarin pinning typically via:
// ServicePointManager.ServerCertificateValidationCallback
// or custom HttpClientHandler
```

```javascript
// Frida bypass for Xamarin (Mono runtime)
// Hook Mono method: System.Net.ServicePointManager.set_ServerCertificateValidationCallback
var mono_method = Module.findExportByName('libmonosgen-2.0.so',
    'mono_runtime_invoke');
// More practical: hook the managed callback at CIL level
// Use Frida's Mono bridge or objection's built-in Xamarin support

// Objection has built-in Xamarin bypass:
// objection -g com.target.app explore
// > android sslpinning disable   (covers Xamarin on Android)
```

---

## 5. CERTIFICATE TRANSPARENCY & HPKP

| Technology | Status | Impact on Testing |
|---|---|---|
| Certificate Transparency (CT) | Active, enforced by browsers | Mobile apps rarely enforce CT; not a bypass obstacle |
| HPKP (HTTP Public Key Pinning) | Deprecated (2018) | Legacy apps may still check; remove header from proxy response |
| Expect-CT header | Deprecated (2024) | Minimal impact on mobile testing |
| CT in mobile apps | Rare | Only Google apps enforce via custom CT checks |

---

