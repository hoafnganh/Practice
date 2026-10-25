# solve.py — challenge 10: Bellcore fault attack
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
from Crypto.Util.number import long_to_bytes

d = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt")) as f:
    for line in f:
        k, v = line.split("=")
        d[k.strip()] = int(v.strip())
n, e, c = d["n"], d["e"], d["c"]

p = None
for i in range(8):
    m, s = d[f"m{i}"], d[f"s{i}"]
    if pow(s, e, n) == m:
        continue                     # chu ky dung — khong co thong tin
    g = math.gcd(pow(s, e, n) - m, n)
    if 1 < g < n:
        p = int(g)
        print(f"cap {i} la chu ky LOI -> gcd = p = {p}")
        break
assert p is not None, "khong tim thay chu ky loi trong log"
q = n // p
phi = (p - 1) * (q - 1)
dk = pow(e, -1, phi)
print("FLAG:", long_to_bytes(pow(c, dk, n)).decode())
