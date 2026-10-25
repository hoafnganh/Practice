# -*- coding: utf-8 -*-
"""gen.py — L10: EHNP — nonce thieu bit 4..27, khoa thieu bit 60..99."""
import hashlib
import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "_lib"))
import latlib as L  # noqa: E402

rng = random.Random(20260110)
cv = L.P192
n = cv.n
d = rng.getrandbits(192)
while d >= n:
    d = rng.getrandbits(192)
d1 = rng.getrandbits(40)
dbar = (d - (d1 << 60)) % n
assert d == (dbar + (d1 << 60)) % n
Q = cv.mul(d)
sigs = []
for i in range(20):
    z = int.from_bytes(hashlib.sha256(f"EHNP-{i}".encode()).digest(), "big") % n
    k1 = rng.getrandbits(24)                      # mang an: bit 4..27
    kbar_msb = rng.getrandbits(n.bit_length() - 29)
    k = ((kbar_msb << 28) + (k1 << 4)) % n
    sig = L.ecdsa_sign(cv, d, z, k)
    kbar = kbar_msb << 28                          # phan biet duoc cong bo
    sigs.append((sig, kbar))
nonce, ct = L.aes_encrypt_flag(b"crypto{3hnp_chunks_r3v34l_4ll}", d, rng)
with open("output.txt", "w") as f:
    f.write(f"dbar = {dbar}\nQx = {Q[0]}\nQy = {Q[1]}\n")
    f.write("key_chunks = [(60, 40)]    # d = dbar + 2^60*d1, d1 < 2^40\n")
    f.write("nonce_chunks = [(4, 24)]  # k = kbar + 2^4*k1, k1 < 2^24\n")
    for (z, r, s), kbar in sigs:
        f.write(f"{z} {r} {s} {kbar}\n")
    f.write(f"nonce = {nonce.hex()}\nct = {ct.hex()}\n")
print("gen ok, sigs:", len(sigs))
