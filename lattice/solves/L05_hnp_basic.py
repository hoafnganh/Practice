# -*- coding: utf-8 -*-
"""solve.py — L05: giai HNP bang Kannan embedding + LLL."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_NAME = os.path.splitext(os.path.basename(__file__))[0]
sys.path.insert(0, os.path.normpath(
    os.path.join(_HERE, "..", "challenge", "lattice", "_lib")))
os.chdir(os.path.normpath(
    os.path.join(_HERE, "..", "challenge", "lattice", _NAME)))
import latlib as L  # noqa: E402

lines = open("output.txt").read().split("\n")
p = int(lines[0].split("= ")[1])
ts, vs = [], []
for line in lines[1:]:
    if not line.strip() or line.startswith("nonce"):
        break
    t, v = map(int, line.split())
    ts.append(t)
    vs.append(v)
nonce, ct = (bytes.fromhex(x.split("= ")[1])
             for x in lines if x.startswith("nonce") or x.startswith("ct"))

# HNP: k_i = v_i - t_i*alpha (mod p), k_i ∈ [0, 2^40)
# chuyen ve convention cua latlib: k_i = t'_i*alpha + a_i, k_i ∈ [0, B)
# voi t'_i = -t_i, a_i = v_i  =>  k_i = -t_i*alpha + v_i
B = 1 << 40
ts2 = [(-t) % p for t in ts]
cands = L.hnp_solve_embedding(p, ts2, vs, B, ntry=10)
print("ung vien:", cands[:3])
for alpha in cands:
    # k_i = t2_i*alpha + v_i = v_i - t_i*alpha = r_i ∈ [0, B)
    if all((t2 * alpha + v) % p < B for t2, v in zip(ts2, vs)):
        flag = L.aes_decrypt_flag(ct, nonce, alpha)
        print(flag.decode())
        break
