# -*- coding: utf-8 -*-
"""solve.py — L06: phuc hoi trang thai LCG tu bit cao (HNP)."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_NAME = os.path.splitext(os.path.basename(__file__))[0]
sys.path.insert(0, os.path.normpath(
    os.path.join(_HERE, "..", "challenge", "lattice", "_lib")))
os.chdir(os.path.normpath(
    os.path.join(_HERE, "..", "challenge", "lattice", _NAME)))
import latlib as L  # noqa: E402

lines = [x.strip() for x in open("output.txt") if x.strip()]
M = int(lines[0].split("= ")[1])
a = int(lines[1].split("= ")[1])
b = int(lines[2].split("= ")[1])
T = int(lines[3].split("= ")[1])
tail = {}
ys = []
for line in lines[4:]:
    if " = " in line:
        k, _, v = line.partition(" = ")
        tail[k.strip()] = v.strip()
    elif not tail:
        ys.append(int(line))
nonce = bytes.fromhex(tail["nonce"])
ct = bytes.fromhex(tail["ct"])

x0 = L.truncated_lcg_solve(a, b, M, ys, T)
assert x0 is not None, "khong phuc hoi duoc trang thai"
print("x0 =", x0)
flag = L.aes_decrypt_flag(ct, nonce, x0)
print(flag.decode())
