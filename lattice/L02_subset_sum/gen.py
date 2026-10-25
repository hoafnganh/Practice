# -*- coding: utf-8 -*-
"""gen.py — L02: subset sum tu flag (128 trong so 1024-bit, density 0.125).

Mật độ phải THAP de LLL thuc su tim duoc vector ±1 — dim cang lon thi he so
xap xi cua LLL cang kem; n=128 voi trong so 1024-bit la vung an toan.
"""
import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "_lib"))
from latlib import bytes_to_long  # noqa: E402

FLAG = b"crypto{kn4ps4ck_r3d}"
rng = random.Random(20260102)
n = 160
weights = [rng.getrandbits(1024) | (1 << 1023) for _ in range(n)]
e = [(bytes_to_long(FLAG) >> i) & 1 for i in range(n)]
s = sum(ei * ai for ei, ai in zip(e, weights))
with open("output.txt", "w") as f:
    for a in weights:
        f.write(f"{a}\n")
    f.write(f"s = {s}\n")
print("gen ok, s bits:", s.bit_length())
