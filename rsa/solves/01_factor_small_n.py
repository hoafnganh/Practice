# solve.py — challenge 01: factor n roi giai ma
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
from Crypto.Util.number import long_to_bytes

ns = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt")) as f:
    for line in f:
        k, v = line.split("=")
        ns[k.strip()] = int(v.strip())
n, e, c = ns["n"], ns["e"], ns["c"]

from sympy import factorint
factors = factorint(n)
ps = list(factors.keys())
assert len(ps) == 2, f"n phai la tich 2 so nguyen to, thay: {factors}"
p, q = ps
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
m = pow(c, d, n)
print("p =", p)
print("q =", q)
print("FLAG:", long_to_bytes(m).decode())
