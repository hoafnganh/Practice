# solve.py — challenge 06: tu (e,d) cua minh suy ra phi(N), roi lay d_boss
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import gmpy2
from Crypto.Util.number import long_to_bytes

d = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt")) as f:
    for line in f:
        k, v = line.split("=")
        d[k.strip()] = int(v.strip())
n, e, dv, e_boss, c_boss = d["n"], d["e"], d["d"], d["e_boss"], d["c_boss"]

ed1 = e * dv - 1          # = k * phi(N)
phi = None
k = ed1 // n              # k > (ed-1)/n ; k <= e
while k <= e:
    if ed1 % k == 0:
        phi_c = ed1 // k
        # kiem tra phi_c hop le: s = n - phi + 1 = p + q, Δ = s^2 - 4n chinh phuong
        s = n - phi_c + 1
        disc = s * s - 4 * n
        if disc > 0:
            r = gmpy2.isqrt(disc)
            if r * r == disc and ((s + r) % 2 == 0):
                phi = phi_c
                break
    k += 1
assert phi is not None, "khong tim duoc phi(N)"
d_boss = pow(e_boss, -1, phi)
print("phi(N) = ", phi)
print("FLAG:", long_to_bytes(pow(c_boss, d_boss, n)).decode())
