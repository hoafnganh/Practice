# solve.py — challenge 04: Hastad broadcast (CRT + can bac ba)
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import gmpy2
from sympy.ntheory.modular import crt
from Crypto.Util.number import long_to_bytes

d = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt")) as f:
    for line in f:
        k, v = line.split("=")
        d[k.strip()] = int(v.strip())
ns = [d["n1"], d["n2"], d["n3"]]
cs = [d["c1"], d["c2"], d["c3"]]
e = d["e"]

C, _ = crt(ns, cs)          # C ≡ m^e (mod n1*n2*n3)
C = int(C)
m, exact = gmpy2.iroot(C, e)
assert exact, "CRT + can bac That bai — kiem tra lai du lieu"
print("FLAG:", long_to_bytes(int(m)).decode())
