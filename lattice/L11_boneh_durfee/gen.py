# -*- coding: utf-8 -*-
"""gen.py — L11: RSA 512-bit voi d ≈ 2^128 (vượt Wiener), e = d^-1 mod phi."""
import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "_lib"))
import latlib as L  # noqa: E402

rng = random.Random(20260111)


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
    d = rng.getrandbits(128) | (1 << 127) | 1
    if N % d == 0:
        continue
    try:
        e = pow(d, -1, phi)
    except ValueError:
        continue
    break
FLAG = b"crypto{b0n3h_durf33_b3y0nd_w13n3r}"
nonce, ct = L.aes_encrypt_flag(FLAG, d, rng)
with open("output.txt", "w") as f:
    f.write(f"N = {N}\ne = {e}\n")
    f.write("hint: d ≈ N^0.25 (nhưng lớn hơn (1/3)N^0.25 — Wiener bó tay)\n")
    f.write(f"nonce = {nonce.hex()}\nct = {ct.hex()}\n")
print("gen ok, e bits:", e.bit_length())
