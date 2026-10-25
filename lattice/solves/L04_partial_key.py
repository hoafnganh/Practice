# -*- coding: utf-8 -*-
"""solve.py — L04: xap xi k tu bit cao cua d -> s -> p,q -> flag."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_NAME = os.path.splitext(os.path.basename(__file__))[0]
sys.path.insert(0, os.path.normpath(
    os.path.join(_HERE, "..", "challenge", "lattice", "_lib")))
os.chdir(os.path.normpath(
    os.path.join(_HERE, "..", "challenge", "lattice", _NAME)))
import latlib as L  # noqa: E402

d = {}
for line in open("output.txt"):
    k, _, v = line.partition(" = ")
    d[k.strip()] = v.strip()
N, e, d0 = int(d["N"]), int(d["e"]), int(d["d0"])
nonce, ct = bytes.fromhex(d["nonce"]), bytes.fromhex(d["ct"])

res = L.partial_key_exposure_ksolve(N, e, d0, ncand=600)
assert res is not None, "khong tim duoc d"
d_sec, p, q = res
assert p * q == N
print("d =", d_sec)
print("p =", p)
flag = L.aes_decrypt_flag(ct, nonce, d_sec)
print(flag.decode())
