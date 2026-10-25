# -*- coding: utf-8 -*-
"""solve.py — L03: Coppersmith univariate tren f(x) = (m' + x)^3 - c."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_NAME = os.path.splitext(os.path.basename(__file__))[0]
sys.path.insert(0, os.path.normpath(
    os.path.join(_HERE, "..", "challenge", "lattice", "_lib")))
os.chdir(os.path.normpath(
    os.path.join(_HERE, "..", "challenge", "lattice", _NAME)))
import latlib as L  # noqa: E402
from latlib import long_to_bytes  # noqa: E402

d = {}
for line in open("output.txt"):
    if " = " in line:
        k, _, v = line.partition(" = ")
        d[k.strip()] = v.rstrip("\n")   # chi cat newline — giu dau cach cuoi prefix
N, c = int(d["N"]), int(d["c"])
prefix = d["prefix"].encode()
unk = 26  # 26 byte cuoi (flag) la phan an
m_prime = L.bytes_to_long(prefix + b"\x00" * unk)
X = 1 << (unk * 8)
assert X < N ** (1 / 3), "phan an qua lon cho e=3"

# f(x) = (m' + x)^3 - c  — KHAI TRIEN day du, he so thap -> cao
f = [(m_prime ** 3 - c) % N, (3 * m_prime ** 2) % N, (3 * m_prime) % N, 1]
roots = L.coppersmith_small_roots(f, N, X, m=3, t=9, verbose=True)
print("nghiem:", roots)
for x0 in roots:
    m = m_prime + x0
    pt = long_to_bytes(m)
    if pt.startswith(prefix) and b"crypto{" in pt:
        print(pt.decode())
        break
else:
    raise SystemExit("khong tim duoc nghiem dung")
