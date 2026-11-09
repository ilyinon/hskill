0000000000000ff0 <setup>:
    0ff0: nop
    0ff1: ret
0000000000001000 <check_auth>:
    1000: test eax,eax
    1002: je 1008 <check_auth+0x8>
    1004: ret
    1008: mov eax,0x2a
    100d: ret
0000000000001010 <next_function>:
    1010: ret
