# -*- coding: utf-8 -*-
"""solve.py — L12: oracle dap PKCS -> quan he HNP -> m -> flag."""
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
rs = []
for line in open("output.txt"):
    line = line.strip()
    if not line:
        continue
    if " = " in line:
        k, _, v = line.partition(" = ")
        tail[k.strip()] = v.strip()
    elif "r" in tail:
        rs.append(int(line))
N = int(tail["N"])
c = int(tail["c"])
rs = [int(x) for x in tail["r"].split()] + rs
nonce = bytes.fromhex(tail["nonce"])
ct = bytes.fromhex(tail["ct"])
print("so quan he:", len(rs))

B = 1 << (512 - 16)                 # 2B = tien to "00 02"
# k_i = r_i*m - 2B (mod N), k_i ∈ [0, B)   ->  HNP voi an la m
ts = [r % N for r in rs]
a_eqs = [(-2 * B) % N for _ in rs]
cands = L.hnp_solve_embedding(N, ts, a_eqs, B, ntry=12)
print("ung vien m:", len(cands))
for m in cands:
    if pow(m, 3, N) != c:
        continue
    blk = L.long_to_bytes(m).rjust(64, b"\x00")
    if not (blk[:2] == b"\x00\x02" and b"\x00" in blk[2:]):
        continue
    idx = blk.index(b"\x00", 2)
    flag = blk[idx + 1:]
    if flag.startswith(b"crypto{"):
        print("m =", m)
        print(flag.decode())
        break
else:
    raise SystemExit("khong tim duoc m")
