# -*- coding: utf-8 -*-
"""solve.py — L01: LLL tim da thuc toi tieu (paper 2023/032, muc 3.6)."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_NAME = os.path.splitext(os.path.basename(__file__))[0]
sys.path.insert(0, os.path.normpath(
    os.path.join(_HERE, "..", "challenge", "lattice", "_lib")))
os.chdir(os.path.normpath(
    os.path.join(_HERE, "..", "challenge", "lattice", _NAME)))
import latlib as L  # noqa: E402

beta = open("output.txt").read().split("≈ ")[1].split("\n")[0].strip()
coef = L.minimal_polynomial(beta, degree=3, scale=10 ** 12)
print("he so (thap -> cao):", coef)
assert coef[-1] == 1
# kiem chung: f(alpha) ≈ 0
from decimal import Decimal, getcontext  # noqa: E402
getcontext().prec = 60
alpha = Decimal(5) + Decimal(19) ** (Decimal(1) / 3)
val = sum(Decimal(c) * alpha ** i for i, c in enumerate(coef))
print("f(alpha) ≈", val)
assert abs(val) < Decimal("0.001")
flag = "crypto{[" + ",".join(str(c) for c in coef) + "]}"
print(flag)
