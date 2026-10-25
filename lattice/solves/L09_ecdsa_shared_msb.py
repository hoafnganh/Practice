# -*- coding: utf-8 -*-
"""solve.py — L09: shared MSB -> khu t bang tru phuong trinh -> HNP -> d."""
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

ts, a_eqs, B = L.hnp_from_biased_nonces(cv, sigs, 40, mode="shared_msb")
cands = L.hnp_solve_embedding(cv.n, ts, a_eqs, B, ntry=10)
for d in cands:
    if cv.mul(d) == Q:
        print("d =", hex(d))
        flag = L.aes_decrypt_flag(ct, nonce, d)
        print(flag.decode())
        break
else:
    raise SystemExit("khong tim duoc d")
