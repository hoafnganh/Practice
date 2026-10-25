# -*- coding: utf-8 -*-
"""gen.py — L09: ECDSA, cac nonce chia se 40 bit cao (khong biet gia tri)."""
import hashlib
import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "_lib"))
import latlib as L  # noqa: E402

rng = random.Random(20260109)
cv = L.SECP256K1
n = cv.n
d = rng.getrandbits(255) | (1 << 254)
Q = cv.mul(d)
t_common = rng.getrandbits(40)
sigs = []
for i in range(14):
    z = int.from_bytes(hashlib.sha256(f"slot-{i}".encode()).digest(), "big") % n
    k = ((t_common << 216) | rng.getrandbits(216)) % n
    sigs.append(L.ecdsa_sign(cv, d, z, k))
nonce, ct = L.aes_encrypt_flag(b"crypto{sh4r3d_msb_n0t_s0_s3cr3t}", d, rng)
with open("output.txt", "w") as f:
    f.write(f"Qx = {Q[0]}\nQy = {Q[1]}\n")
    for (z, r, s) in sigs:
        f.write(f"{z} {r} {s}\n")
    f.write(f"nonce = {nonce.hex()}\nct = {ct.hex()}\n")
print("gen ok, sigs:", len(sigs))
