# -*- coding: utf-8 -*-
"""gen.py — L03: RSA e=3, ban ro co khuon mau, 18 ky tu cuoi an."""
import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "_lib"))
import latlib as L  # noqa: E402

rng = random.Random(20260103)
p = L.gen_prime(384, rng)
q = L.gen_prime(384, rng)
assert p != q
N = p * q
e = 3
alphabet = "abcdefghjkmnpqrstuvwxyz23456789"
secret = "".join(rng.choice(alphabet) for _ in range(18))
FLAG = f"crypto{{{secret}}}"
prefix = b"Hello agent. Your one-time activation code is: "
m = L.bytes_to_long(prefix + FLAG.encode())
c = pow(m, e, N)
with open("output.txt", "w") as f:
    f.write(f"N = {N}\ne = 3\nc = {c}\n")
    f.write(f"prefix = {prefix.decode()}\n")
print("gen ok, flag len:", len(FLAG))
