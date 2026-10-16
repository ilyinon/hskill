# mobile-ssl-pinning-bypass technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 2. ANDROID BYPASS METHODS

### 2.1 Frida Universal SSL Bypass

```javascript
// Hooks TrustManager, OkHttp, Volley, Retrofit, Conscrypt
Java.perform(function() {

    // ── TrustManagerImpl (Android system) ──
    try {
        var TMI = Java.use('com.android.org.conscrypt.TrustManagerImpl');
        TMI.verifyChain.implementation = function() {
            console.log('[Bypass] TrustManagerImpl.verifyChain');
            return arguments[0]; // return untouched chain
        };
    } catch(e) {}

    // ── X509TrustManager (custom implementations) ──
    var TrustManager = Java.registerClass({
        name: 'com.bypass.TrustManager',
        implements: [Java.use('javax.net.ssl.X509TrustManager')],
        methods: {
            checkClientTrusted: function() {},
            checkServerTrusted: function() {},
            getAcceptedIssuers: function() { return []; }
        }
    });

    var SSLContext = Java.use('javax.net.ssl.SSLContext');
    SSLContext.init.overload('[Ljavax.net.ssl.KeyManager;',
        '[Ljavax.net.ssl.TrustManager;', 'java.security.SecureRandom')
        .implementation = function(km, tm, sr) {
        console.log('[Bypass] SSLContext.init');
        this.init(km, [TrustManager.$new()], sr);
    };

    // ── OkHttp3 CertificatePinner ──
    try {
        var CP = Java.use('okhttp3.CertificatePinner');
        CP.check.overload('java.lang.String', 'java.util.List').implementation = function() {
            console.log('[Bypass] OkHttp3 CertificatePinner.check: ' + arguments[0]);
        };
        // check$okhttp variant (OkHttp 4.x)
        try { CP['check$okhttp'].implementation = function() {}; } catch(e) {}
    } catch(e) {}

    // ── Retrofit / OkHttp interceptor ──
    try {
        var OkHttpClient = Java.use('okhttp3.OkHttpClient$Builder');
        OkHttpClient.certificatePinner.implementation = function(pinner) {
            console.log('[Bypass] OkHttpClient.Builder.certificatePinner');
            return this; // return builder without pinner
        };
    } catch(e) {}

    // ── Volley (HurlStack) ──
    try {
        var HurlStack = Java.use('com.android.volley.toolbox.HurlStack');
        HurlStack.createConnection.implementation = function(url) {
            console.log('[Bypass] Volley HurlStack: ' + url);
            var conn = this.createConnection(url);
            // Remove hostname verifier
            conn.setHostnameVerifier(Java.use(
                'javax.net.ssl.HttpsURLConnection').getDefaultHostnameVerifier());
            return conn;
        };
    } catch(e) {}

    // ── Conscrypt / BoringSSL (modern Android) ──
    try {
        var Conscrypt = Java.use('org.conscrypt.ConscryptFileDescriptorSocket');
        Conscrypt.verifyCertificateChain.implementation = function() {
            console.log('[Bypass] Conscrypt verifyCertificateChain');
        };
    } catch(e) {}

    // ── Apache HttpClient (legacy) ──
    try {
        var AbstractVerifier = Java.use('org.apache.http.conn.ssl.AbstractVerifier');
        AbstractVerifier.verify.overload('java.lang.String', '[Ljava.lang.String;',
            '[Ljava.lang.String;', 'boolean').implementation = function() {
            console.log('[Bypass] Apache AbstractVerifier');
        };
    } catch(e) {}

    // ── HostnameVerifier ──
    try {
        var HV = Java.use('javax.net.ssl.HttpsURLConnection');
        HV.setDefaultHostnameVerifier.implementation = function(v) {
            console.log('[Bypass] Ignoring custom HostnameVerifier');
        };
    } catch(e) {}

    console.log('[+] Android universal SSL bypass loaded');
});
```

### 2.2 Objection (One Command)

```bash
objection -g com.target.app explore --startup-command "android sslpinning disable"
```

### 2.3 Network Security Config (Debug Override)

```xml
<!-- AndroidManifest.xml: android:networkSecurityConfig="@xml/network_security_config" -->

<!-- res/xml/network_security_config.xml -->
<network-security-config>
  <base-config>
    <trust-anchors>
      <certificates src="system" />
      <certificates src="user" />     <!-- Trust user-installed CAs -->
    </trust-anchors>
  </base-config>
</network-security-config>
```

Workflow: decompile APK → add/modify config → repackage → re-sign → install.

```bash
apktool d target.apk -o target_dir
# Edit res/xml/network_security_config.xml
# Add reference in AndroidManifest.xml if missing
apktool b target_dir -o target_patched.apk
zipalign -v 4 target_patched.apk target_aligned.apk
apksigner sign --ks my-key.keystore target_aligned.apk
adb install target_aligned.apk
```

### 2.4 Xposed / LSPosed Modules

| Module | Method | Scope | Root Required |
|---|---|---|---|
| JustTrustMe | Hooks TrustManager + OkHttp | Per-app | Yes (Xposed) |
| SSLUnpinning | Hooks certificate validation | Per-app | Yes (LSPosed) |
| TrustMeAlready | Global TrustManager bypass | System-wide | Yes (LSPosed) |

### 2.5 Magisk + System CA Installation

```bash
# Install proxy CA as system cert (Android 7+ requires this for system-level trust)
# Method 1: MagiskTrustUserCerts module
# Moves user CAs to /system/etc/security/cacerts/ via Magisk overlay

# Method 2: Manual (requires root)
adb push burp_ca.pem /sdcard/
adb shell
su
mount -o remount,rw /system
cp /sdcard/burp_ca.pem /system/etc/security/cacerts/9a5ba575.0  # hash-named
chmod 644 /system/etc/security/cacerts/9a5ba575.0
mount -o remount,ro /system

# Get correct hash filename:
openssl x509 -inform PEM -subject_hash_old -in burp_ca.pem | head -1
# Output: 9a5ba575 → filename is 9a5ba575.0
```

### 2.6 Manual Decompile → Patch → Repackage

```bash
# Step 1: Decompile
jadx -d decompiled/ target.apk

# Step 2: Find pinning code
grep -r "CertificatePinner\|X509TrustManager\|checkServerTrusted\|ssl" decompiled/

# Step 3: Identify pinning implementation and patch
# Use smali editing for precise control:
apktool d target.apk
# Edit smali files to NOP out pinning checks
# Look for invoke-virtual {checkServerTrusted} and replace with return-void

# Step 4: Repackage and sign
apktool b target_dir -o patched.apk
apksigner sign --ks debug.keystore patched.apk
```

---

