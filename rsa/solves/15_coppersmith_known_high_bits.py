# solve.py — challenge 15: Coppersmith known-high-bits factoring
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import rsalib as R
from Crypto.Util.number import long_to_bytes

d = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt")) as f:
    for line in f:
        if "=" in line:
            k, v = line.split("=")
            d[k.strip()] = int(v.strip().split("#")[0].strip())
n, e, p_high, c = d["n"], d["e"], d["p_high"], d["c"]

U = 116  # so bit chua biet cua p (de bai: leak 140/256 bit cao)
res = R.coppersmith_known_high_bits(n, p_high, U, m=8, t=8, verbose=True)
assert res, "Coppersmith that bai"
p = res[0]
q = n // p
phi = (p - 1) * (q - 1)
dk = pow(e, -1, phi)
print("p =", p)
print("FLAG:", long_to_bytes(pow(c, dk, n)).decode())
