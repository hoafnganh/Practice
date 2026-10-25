# solve.py — challenge 13: Franklin-Reiter qua GCD da thuc tren Z_N[x]
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import rsalib as R
from Crypto.Util.number import long_to_bytes

d = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt")) as f:
    for line in f:
        k, v = line.split("=")
        d[k.strip()] = int(v.strip())
n, e, c1, c2 = d["n"], d["e"], d["c1"], d["c2"]
assert e == 3

# M2 = M1 + 1 (so se-ri lien tiep):
#   g1(x) = (x - 1)^3 - c1  : nghiem x = M2 (vi M2 - 1 = M1)
#   g2(x) = x^3 - c2        : nghiem x = M2
g1 = [(-1 - c1) % n, 3, -3, 1]
g2 = [(-c2) % n, 0, 0, 1]
h, factor = R.poly_gcd_mod(g1, g2, n)
assert factor is None, f"Euclid that bai — nhung day la uoc so cua N: {factor}"
assert R.poly_deg(h) == 1, f"GCD phai tuyen tinh, thay deg={R.poly_deg(h)}"

M2 = (-h[0] * pow(h[1], -1, n)) % n
assert M2 & 0xFFFFFFFF == 2, "so se-ri phai la 2"
flag_bytes = long_to_bytes(M2 >> 32)
print("FLAG:", flag_bytes.decode())
