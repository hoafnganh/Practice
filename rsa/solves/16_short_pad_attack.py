# solve.py — challenge 16: Coppersmith short-pad attack
# Buoc 1: resultant h(y) = res_x(x^3 - c1, (x+y)^3 - c2) — monic bac 9 mod n
# Buoc 2: Coppersmith tim nghiem nho Delta = r2 - r1 (|Delta| < 2^32)
# Buoc 3: Franklin-Reiter qua GCD da thuc -> M2 -> flag
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import rsalib as R
from Crypto.Util.number import long_to_bytes
import sympy
from sympy import symbols

d = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt")) as f:
    for line in f:
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=")
            d[k.strip()] = int(v.strip())
n, e, c1, c2 = d["n"], d["e"], d["c1"], d["c2"]
assert e == 3
PADBITS = 32

# Buoc 1: resultant (da thuc he so nguyen, bac 9 theo y, monic)
x, y = symbols("x y")
res = sympy.resultant(x**3 - c1, (x + y)**3 - c2, x)
res_poly = sympy.Poly(res, y)
hc = [int(c) % n for c in res_poly.all_coeffs()]  # cao -> thap
hc = hc[::-1]                                      # thap -> cao
assert hc[-1] == 1, "resultant phai monic"
print("[*] resultant bac", len(hc) - 1)

# Buoc 2: Coppersmith nghiem nho |Delta| < 2^32
roots = R.coppersmith_small_roots(hc, n, 1 << PADBITS, m=4, t=0, verbose=True)
assert roots, "Coppersmith khong tim duoc Delta"
delta = roots[0]
print("[*] Delta =", delta)

# Buoc 3: Franklin-Reiter: gcd((x-Delta)^3 - c1, x^3 - c2) = x - M2
g1p = [(-c1 - delta**3) % n, 3 * delta**2, -3 * delta, 1]  # (x-delta)^3 - c1
g2p = [-c2 % n, 0, 0, 1]                                    # x^3 - c2
h, fac = R.poly_gcd_mod(g1p, g2p, n)
assert fac is None and R.poly_deg(h) == 1, f"GCD that bai: {h}, {fac}"
M2 = (-h[0] * pow(h[1], -1, n)) % n
assert pow(M2, 3, n) == c2, "kiem chung M2 that bai"
flag = long_to_bytes(M2 >> PADBITS)
print("FLAG:", flag.decode())
