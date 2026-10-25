# -*- coding: utf-8 -*-
"""solve.py — L02: CJLOSS subset sum -> flag."""
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

lines = open("output.txt").read().split("\n")
weights = [int(x) for x in lines[:160]]
s = int([x for x in lines if x.startswith("s = ")][0].split("= ")[1])

e = L.subset_sum_solve(weights, s, ntry=300)
assert e is not None, "LLL khong tim duoc nghiem"
val = sum(ei << i for i, ei in enumerate(e))
flag = long_to_bytes(val)
print(flag.decode())
assert flag.startswith(b"crypto{")
