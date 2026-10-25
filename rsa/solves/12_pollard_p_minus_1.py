# solve.py — challenge 12: Pollard p-1
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
from Crypto.Util.number import long_to_bytes

d = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt")) as f:
    for line in f:
        k, v = line.split("=")
        d[k.strip()] = int(v.strip())
n, e, c = d["n"], d["e"], d["c"]

B = 65536
a = 2
p = None
for j in range(2, B + 1):
    a = pow(a, j, n)
    if j % 64 == 0 or j == B:
        g = math.gcd(a - 1, n)
        if 1 < g < n:
            p = int(g)
            print(f"tim thay tai j = {j}: p = {p}")
            break
assert p is not None, "Pollard p-1 that bai"
q = n // p
phi = (p - 1) * (q - 1)
dk = pow(e, -1, phi)
print("FLAG:", long_to_bytes(pow(c, dk, n)).decode())
