# solve.py — challenge 09: vet can dp nho qua gcd(r - r^(e*dp), n)
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import gmpy2
from Crypto.Util.number import long_to_bytes

d = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt")) as f:
    for line in f:
        k, v = line.split("=")
        d[k.strip()] = int(v.strip())
n, e, c = d["n"], d["e"], d["c"]

r = gmpy2.mpz(7516789928765)          # r bat ki, gcd(r, n) = 1
r_e = gmpy2.powmod(r, e, n)           # chi tinh 1 lan!
p = None
for dp in range(1, 1 << 21):
    # r^(e*dp) = (r^e)^dp mod n — moi vong chi ~20 luy thua binh phuong
    g = gmpy2.gcd(int(r - gmpy2.powmod(r_e, dp, n)), n)
    if 1 < g < n:
        p = int(g)
        print(f"dp = {dp}, p = {p}")
        break
assert p is not None, "khong tim duoc dp trong khoang"
q = n // p
phi = (p - 1) * (q - 1)
d_key = pow(e, -1, phi)
print("FLAG:", long_to_bytes(pow(c, d_key, n)).decode())
