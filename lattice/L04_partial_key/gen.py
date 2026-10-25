# -*- coding: utf-8 -*-
"""gen.py — L04: PKE — biet bit cao cua d (thieu 8 bit thap)."""
import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "_lib"))
import latlib as L  # noqa: E402

rng = random.Random(20260104)


def gen_prime(bits):
    while True:
        c = rng.getrandbits(bits) | (1 << (bits - 1)) | 1
        if L.is_probable_prime(c):
            return c


while True:
    p, q = gen_prime(256), gen_prime(256)
    if p == q:
        continue
    N = p * q
    phi = (p - 1) * (q - 1)
    d = rng.getrandbits(183) | (1 << 182) | 1
    if N % d == 0:
        continue
    try:
        e = pow(d, -1, phi)
    except ValueError:
        continue
    break
d0 = d >> 8 << 8
FLAG = b"crypto{msb_0f_d_g1v3s_k_f0r_fr33}"
nonce, ct = L.aes_encrypt_flag(FLAG, d, rng)
with open("output.txt", "w") as f:
    f.write(f"N = {N}\ne = {e}\nd0 = {d0}\n")
    f.write(f"nonce = {nonce.hex()}\nct = {ct.hex()}\n")
print("gen ok")
