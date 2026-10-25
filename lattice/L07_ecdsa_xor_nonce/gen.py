# -*- coding: utf-8 -*-
"""gen.py — L07: ECDSA secp256k1, nonce k = z XOR d, 6 chu ky."""
import hashlib
import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "_lib"))
import latlib as L  # noqa: E402

rng = random.Random(20260107)
cv = L.SECP256K1
n = cv.n
d = rng.getrandbits(255) | (1 << 254)
Q = cv.mul(d)
sigs = []
msgs = [f"payment-{i}" for i in range(6)]
for msg in msgs:
    z = int.from_bytes(hashlib.sha256(msg.encode()).digest(), "big") % n
    k = z ^ d
    if k == 0 or k >= n:
        k %= n
    sigs.append(L.ecdsa_sign(cv, d, z, k))
nonce, ct = L.aes_encrypt_flag(b"crypto{x0r_n0nc3_1s_subs3t_sum_tsj}", d, rng)
with open("output.txt", "w") as f:
    f.write(f"Qx = {Q[0]}\nQy = {Q[1]}\n")
    for (z, r, s) in sigs:
        f.write(f"{z} {r} {s}\n")
    f.write(f"nonce = {nonce.hex()}\nct = {ct.hex()}\n")
print("gen ok, sigs:", len(sigs))
