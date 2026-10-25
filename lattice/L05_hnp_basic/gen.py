# -*- coding: utf-8 -*-
"""gen.py — L05: HNP co ban — 24 cap (t_i, v_i) voi r_i < 2^40."""
import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "_lib"))
import latlib as L  # noqa: E402

rng = random.Random(20260105)
# so nguyen to 256 bit
while True:
    p = rng.getrandbits(256) | (1 << 255) | 1
    if L.is_probable_prime(p):
        break
alpha = rng.getrandbits(255) | (1 << 254)
B = 1 << 40
pairs = []
for _ in range(24):
    t = rng.randrange(1, p)
    r = rng.randrange(B)
    v = (t * alpha + r) % p
    pairs.append((t, v))
nonce, ct = L.aes_encrypt_flag(b"crypto{h1dd3n_numb3r_bv96_l0c4t3d}", alpha, rng)
with open("output.txt", "w") as f:
    f.write(f"p = {p}\n")
    for t, v in pairs:
        f.write(f"{t} {v}\n")
    f.write(f"nonce = {nonce.hex()}\nct = {ct.hex()}\n")
print("gen ok")
