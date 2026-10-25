# -*- coding: utf-8 -*-
"""solve.py — L11: Boneh-Durfee cho d ≈ N^0.25."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_NAME = os.path.splitext(os.path.basename(__file__))[0]
sys.path.insert(0, os.path.normpath(
    os.path.join(_HERE, "..", "challenge", "lattice", "_lib")))
os.chdir(os.path.normpath(
    os.path.join(_HERE, "..", "challenge", "lattice", _NAME)))
import latlib as L  # noqa: E402

tail = {}
for line in open("output.txt"):
    line = line.strip()
    if " = " in line:
        k, _, v = line.partition(" = ")
        tail[k.strip()] = v.strip()
N = int(tail["N"])
e = int(tail["e"])
nonce = bytes.fromhex(tail["nonce"])
ct = bytes.fromhex(tail["ct"])

res = L.boneh_durfee_attack(N, e, d_bits=128, m=4, t=1, verbose=True)
assert res is not None, "BD that bai — thu tang m hoac giam d_bits"
d, k, s = res
# xac minh: ed ≡ 1 mod phi
phi = N + 1 - 2 * s
assert (e * d - 1) % phi == 0, "ed khong khop phi"
print("d =", d)
flag = L.aes_decrypt_flag(ct, nonce, d)
print(flag.decode())
