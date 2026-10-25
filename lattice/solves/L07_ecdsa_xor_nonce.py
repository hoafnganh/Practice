# -*- coding: utf-8 -*-
"""solve.py — L07: k = z XOR d -> he affine theo bit -> lattice TSJ -> d."""
import hashlib
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_NAME = os.path.splitext(os.path.basename(__file__))[0]
sys.path.insert(0, os.path.normpath(
    os.path.join(_HERE, "..", "challenge", "lattice", "_lib")))
os.chdir(os.path.normpath(
    os.path.join(_HERE, "..", "challenge", "lattice", _NAME)))
import latlib as L  # noqa: E402

cv = L.SECP256K1
n = cv.n
sigs, tail = [], {}
for line in open("output.txt"):
    line = line.strip()
    if not line:
        continue
    if " = " in line:
        k, _, v = line.partition(" = ")
        tail[k.strip()] = v.strip()
    elif tail:
        z, r, s = map(int, line.split())
        sigs.append((z, r, s))
Q = (int(tail["Qx"]), int(tail["Qy"]))
nonce = bytes.fromhex(tail["nonce"])
ct = bytes.fromhex(tail["ct"])

m_bits = n.bit_length()          # 256
# Phuong trinh: s*(z + d - 2*sum_j 2^j z_j d_j) = z + r*d  (mod n)
#   => sum_j d_j * 2^j*(s - r - 2*s*z_j) + (s*z - z) = 0  (mod n)
A, consts = [], []
for (z, r, s) in sigs:
    row = [(1 << j) * (s - r - 2 * s * ((z >> j) & 1)) % n
           for j in range(m_bits)]
    A.append(row)
    consts.append((s * z - z) % n)

bits = L.affine_modular_subset_sum_solve(A, consts, n, scale_bits=64)
assert bits is not None, "lattice khong tra ve nghiem"
d_rec = sum(b << j for j, b in enumerate(bits))
# xac minh bang khoa cong khai
assert cv.mul(d_rec) == Q, "d khong dung"
print("d =", hex(d_rec))
flag = L.aes_decrypt_flag(ct, nonce, d_rec)
print(flag.decode())
