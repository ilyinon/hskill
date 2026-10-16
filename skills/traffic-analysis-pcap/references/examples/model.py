"""Bounded fixture decoder, not a general TCP reassembly tool."""
import struct

def segments(data):
    if len(data) < 24 or data[:4] != bytes.fromhex("d4c3b2a1"):
        raise ValueError("expected little-endian classic PCAP")
    if struct.unpack_from("<I", data, 20)[0] != 1:
        raise ValueError("expected Ethernet")
    offset = 24
    result = []
    while offset < len(data):
        if offset + 16 > len(data):
            raise ValueError("truncated record")
        _, _, captured, original = struct.unpack_from("<IIII", data, offset)
        offset += 16
        frame = data[offset:offset + captured]
        if captured != original or len(frame) != captured:
            raise ValueError("truncated packet")
        offset += captured
        if len(frame) < 54 or frame[12:14] != b"\x08\x00" or frame[14] >> 4 != 4 or frame[23] != 6:
            raise ValueError("expected fixture Ethernet/IPv4/TCP")
        ip_size = (frame[14] & 15) * 4
        total = struct.unpack_from("!H", frame, 16)[0]
        if struct.unpack_from("!H", frame, 20)[0] & 0x3FFF:
            raise ValueError("fragmented IP is outside this fixture decoder")
        tcp = 14 + ip_size
        if ip_size < 20 or total < ip_size + 20 or 14 + total > len(frame):
            raise ValueError("invalid fixture lengths")
        tcp_size = (frame[tcp + 12] >> 4) * 4
        if tcp_size < 20 or ip_size + tcp_size > total:
            raise ValueError("invalid fixture lengths")
        sport, dport, seq = struct.unpack_from("!HHI", frame, tcp)
        result.append((frame[26:30], frame[30:34], sport, dport, seq, frame[tcp + tcp_size:14 + total]))
    return result

def reassemble(rows):
    if not rows or len({row[:4] for row in rows}) != 1:
        raise ValueError("select one directional flow")
    ordered = sorted(rows, key=lambda row: row[4])
    output = b""
    start = ordered[0][4]
    for row in ordered:
        sequence, body = row[4], row[5]
        if sequence > start + len(output):
            raise ValueError("capture gap")
        relative = sequence - start
        overlap = min(len(output) - relative, len(body))
        if output[relative:relative + overlap] != body[:overlap]:
            raise ValueError("conflicting overlap")
        output += body[overlap:]
    return output
