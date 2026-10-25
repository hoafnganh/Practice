# solve.py — challenge 17: BDF partial key exposure (LSBs of d, e = 3)
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import rsalib as R
from Crypto.Util.number import long_to_bytes

d = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt")) as f:
    for line in f:
        if "=" in line and not line.startswith("#"):
            kk, v = line.split("=")
            d[kk.strip()] = int(v.strip().split("#")[0].strip())
n, e, d_low, c = d["n"], d["e"], d["d_low"], d["c"]
S = 176

# ed - k(N - p - q + 1) = 1 ; nhan voi p, rut gon mod 2^S:
#   k*p^2 + (e*d - k*N - k - 1)*p + k*N = 0  (mod 2^S)
p_found = None
for k in (1, 2, 3):
    bb = e * d_low - k * n - k - 1
    cc = k * n
    roots = R.solve_quad_mod_2k(k, bb, cc, S)
    if not roots:
        continue
    print(f"[*] k = {k}: {len(roots)} ung vien p mod 2^S")
    for p_low in roots:
        if p_low % 2 == 0:
            continue  # p phai le
        # p = p_low + 2^S * x, x < 2^(256-176) = 2^80
        inv2s = pow(1 << S, -1, n)
        f = [(p_low * inv2s) % n, 1]        # monic: x + p_low/2^S mod N
        X = 1 << (256 - S)
        xs = R.coppersmith_small_roots(f, n, X, m=6, t=6, check_mod_n=False)
        for x0 in xs:
            p_c = p_low + (x0 << S)
            if p_c > 1 and n % p_c == 0:
                p_found = p_c
                break
        if p_found:
            break
    if p_found:
        break

assert p_found, "khong khoi phuc duoc p"
p = p_found
q = n // p
phi = (p - 1) * (q - 1)
dk = pow(e, -1, phi)
assert dk % (1 << S) == d_low, "d phai dung bit da leak"
print("p =", p)
print("FLAG:", long_to_bytes(pow(c, dk, n)).decode())
