# solve.py — challenge 08: Wiener attack bang phan so lien tuc
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import rsalib as R
from Crypto.Util.number import long_to_bytes

d = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt")) as f:
    for line in f:
        k, v = line.split("=")
        d[k.strip()] = int(v.strip())
n, e, c = d["n"], d["e"], d["c"]

res = R.wiener_attack(n, e)
assert res is not None, "Wiener that bai"
d_rec, p, q = res
assert p * q == n
print(f"d = {d_rec}  ({d_rec.bit_length()} bit)")
print(f"p*q == n ? {p*q == n}")
print("FLAG:", long_to_bytes(pow(c, d_rec, n)).decode())
