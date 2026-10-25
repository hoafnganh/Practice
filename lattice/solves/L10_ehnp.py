# -*- coding: utf-8 -*-
"""solve.py — L10: EHNP — mảnh rời của nonce + khóa -> d."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_NAME = os.path.splitext(os.path.basename(__file__))[0]
sys.path.insert(0, os.path.normpath(
    os.path.join(_HERE, "..", "challenge", "lattice", "_lib")))
os.chdir(os.path.normpath(
    os.path.join(_HERE, "..", "challenge", "lattice", _NAME)))
import latlib as L  # noqa: E402

cv = L.P192
n = cv.n
sigs, tail = [], {}
for line in open("output.txt"):
    line = line.strip()
    if not line:
        continue
    if " = " in line:
        k, _, v = line.partition(" = ")
        tail[k.strip()] = v.strip()
    elif "dbar" in tail:
        z, r, s, kbar = map(int, line.split())
        sigs.append((z, r, s, kbar))
dbar = int(tail["dbar"])
Q = (int(tail["Qx"]), int(tail["Qy"]))
nonce = bytes.fromhex(tail["nonce"])
ct = bytes.fromhex(tail["ct"])

# EHNP (paper 5.3.3): beta_i = s_i*kbar_i - z_i  (ham tu tru -r_i*dbar)
eqs = []
for (z, r, s, kbar) in sigs:
    alpha = r % n
    rho = (-s << 4) % n
    beta = (s * kbar - z) % n
    eqs.append((alpha, [(rho, 24)], beta))

cands = L.ehnp_solve(n, dbar, [(60, 40)], eqs)
for d in cands:
    if cv.mul(d) == Q:
        print("d =", hex(d))
        flag = L.aes_decrypt_flag(ct, nonce, d)
        print(flag.decode())
        break
else:
    raise SystemExit("khong tim duoc d")
