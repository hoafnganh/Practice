# -*- coding: utf-8 -*-
"""gen.py — L06: LCG 61-bit, chi in 40 bit cao, 26 mau."""
import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "_lib"))
import latlib as L  # noqa: E402

rng = random.Random(20260106)
M = (1 << 61) - 1
a = rng.randrange(2, M)
b = rng.randrange(2, M)
x0 = rng.randrange(1, M)
T = 24
ys = []
x = x0
for _ in range(26):
    ys.append(x >> T)
    x = (a * x + b) % M
nonce, ct = L.aes_encrypt_flag(b"crypto{trunc4t3d_lcg_1s_hnp_1n_d1sgu1s3}", x0, rng)
with open("output.txt", "w") as f:
    f.write(f"M = {M}\na = {a}\nb = {b}\nshift = {T}\n")
    for y in ys:
        f.write(f"{y}\n")
    f.write(f"nonce = {nonce.hex()}\nct = {ct.hex()}\n")
print("gen ok")
