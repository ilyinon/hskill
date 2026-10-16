"""Bounded abstract stack checker, not an emulator or executable exploit."""

def check(words, saved_rip_slot, addresses, expected_argument, required_mod=8):
    position = 0
    rsp = saved_rip_slot
    argument = None
    for step in range(12):
        if position >= len(words):
            return {"status": "truncated"}
        pc = words[position]
        position += 1
        rsp += 8  # each modeled ret consumes its next instruction word
        if pc == addresses["ret"]:
            continue
        if pc == addresses["pop_rdi_ret"]:
            if position >= len(words):
                return {"status": "truncated"}
            argument = words[position]
            position += 1
            rsp += 8
        elif pc == addresses["marker"]:
            if argument != expected_argument:
                return {"status": "wrong-argument", "rsp_mod": rsp % 16}
            return {"status": "marker" if rsp % 16 == required_mod else "misaligned", "rsp_mod": rsp % 16}
        else:
            return {"status": "unknown-address"}
    return {"status": "step-limit"}
