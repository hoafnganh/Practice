# -*- coding: utf-8 -*-
"""test_latlib.py — kiem thu cac ham trong latlib.py."""
import math
import random
import sys
import os
import time
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import latlib as L
from latlib import inverse

rng = random.Random(2026)
ok_count = 0
fail = []


def check(name, cond, extra=""):
    global ok_count
    if cond:
        ok_count += 1
        print(f"  OK   {name} {extra}", flush=True)
    else:
        fail.append(name)
        print(f"  FAIL {name} {extra}", flush=True)


# ---------------------------------------------------------------- Babai
print("== Babai / CVP")
B = [[2, 1], [1, 3]]
v = L.babai(B, [37, 22])
best = min(((a * 2 + c, a * 1 + c * 3) for a in range(-30, 30) for c in range(-30, 30)),
           key=lambda p: (p[0] - 37) ** 2 + (p[1] - 22) ** 2)
check("babai 2d", tuple(v) == tuple(best), f"v={v} best={best}")

emb = L.kannan_embed(B, [37, 22], q=5)
R = L.lll(emb)
found = False
for row in R:
    if abs(row[-1]) == 5:
        e_vec = [row[q] if row[-1] < 0 else -row[q] for q in range(2)]
        if [37 + e_vec[0], 22 + e_vec[1]] == list(best):
            found = True
check("kannan embed 2d", found)

# ---------------------------------------------------------------- HNP
print("== HNP")
# vi du 4.11: p=401, alpha=309, B=20  (beta = t*alpha - a mod p)
p, alpha = 401, 309
ts = [143, 293, 304]
a_paper = [62, 300, 86]
# convention moi: k = t*alpha + a  =>  k_i = beta_i = (t*alpha - a_paper)
a_eqs = [(-a) % p for a in a_paper]
sols = L.hnp_solve_embedding(p, ts, a_eqs, 20)
check("HNP paper 4.11", alpha in sols, f"sols={sols}")

# ngau nhien: q 192 bit, 24 cap, k < 2^136
q = L.P192.n
alpha = rng.randrange(1, q)
ts = [rng.randrange(1, q) for _ in range(24)]
Bb = 1 << 136
a_eqs = [rng.randrange(q) for _ in range(24)]
# ep k_i nho: a_i = k_i - t_i*alpha
ks = [rng.randrange(Bb) for _ in range(24)]
a_eqs = [(k - t * alpha) % q for k, t in zip(ks, ts)]
sols = L.hnp_solve_embedding(q, ts, a_eqs, Bb)
check("HNP 192-bit (24 cap, 56 bit leak)", alpha in sols, f"n={len(sols)}")

# ---------------------------------------------------------------- CJLOSS
print("== Subset sum (CJLOSS)")
# paper vi du 4.6
e = L.subset_sum_solve([83, 59, 47, 81, 76, 51], 291)
check("subset sum paper 4.6", e is not None and
      sum(ei * ai for ei, ai in zip(e, [83, 59, 47, 81, 76, 51])) == 291, f"e={e}")

n = 36
weights = [rng.getrandbits(96) | 1 for _ in range(n)]
e_true = [rng.randint(0, 1) for _ in range(n)]
s = sum(ei * ai for ei, ai in zip(e_true, weights))
t0 = time.time()
e = L.subset_sum_solve(weights, s)
check("subset sum 36x96bit", e == e_true, f"({time.time()-t0:.1f}s)")

M = 1 << 128
wm = [rng.getrandbits(128) for _ in range(24)]
em = [rng.randint(0, 1) for _ in range(24)]
sm = sum(ei * ai for ei, ai in zip(em, wm)) % M
e = L.modular_subset_sum_solve(wm, sm, M)
check("modular subset sum", e == em)

wm3 = [[rng.getrandbits(120) for _ in range(3)] for _ in range(20)]
em3 = [rng.randint(0, 1) for _ in range(20)]
tg3 = [sum(em3[i] * wm3[i][j] for i in range(20)) % M for j in range(3)]
t0 = time.time()
e = L.multiple_modular_subset_sum_solve(wm3, tg3, M)
check("multiple modular subset sum", e == em3, f"({time.time()-t0:.1f}s)")

# ---------------------------------------------------------------- min poly
print("== Minimal polynomial (KLL84)")
from decimal import Decimal, getcontext
getcontext().prec = 40
alpha_dec = Decimal(3) + Decimal(11) ** (Decimal(1) / 3)
beta_str = str(alpha_dec)[:15]
coef = L.minimal_polynomial(beta_str, degree=3, scale=10 ** 12)
check("minimal poly x^3-9x^2+27x-38", coef == [-38, 27, -9, 1], f"coef={coef}")

# ---------------------------------------------------------------- LCG
print("== Truncated LCG")
M = (1 << 61) - 1
a, b = rng.randrange(2, M), rng.randrange(2, M)
x0 = rng.randrange(1, M)
xs, x = [], x0
for _ in range(26):
    xs.append(x)
    x = (a * x + b) % M
t = 24
ys = [xi >> t for xi in xs]
t0 = time.time()
x0r = L.truncated_lcg_solve(a, b, M, ys, t)
check("truncated LCG (24 bit an, 26 mau)", x0r == x0, f"({time.time()-t0:.1f}s)")

# ---------------------------------------------------------------- ECDSA
print("== ECDSA biased nonce -> HNP")
cv = L.P192
n = cv.n
d = rng.randrange(1, n)
sigs = []
for i in range(24):
    z = rng.randrange(1, n)
    k = rng.getrandbits(n.bit_length() - 56)
    sigs.append(L.ecdsa_sign(cv, d, z, k))
ts, a_eqs, Bb = L.hnp_from_biased_nonces(cv, sigs, 56, mode="zero_msb")
t0 = time.time()
sols = L.hnp_solve_embedding(n, ts, a_eqs, Bb, ntry=6)
check("ECDSA zero-MSB 56 bit", d in sols, f"({time.time()-t0:.1f}s)")

sigs = []
for i in range(20):
    z = rng.randrange(1, n)
    ti = rng.getrandbits(32)
    k = (ti << (n.bit_length() - 32)) | rng.getrandbits(n.bit_length() - 32)
    sigs.append(L.ecdsa_sign(cv, d, z, k) + (ti,))
ts, a_eqs, Bb = L.hnp_from_biased_nonces(cv, sigs, 32, mode="known_msb")
sols = L.hnp_solve_embedding(n, ts, a_eqs, Bb, ntry=6)
check("ECDSA known-MSB 32 bit", d in sols)

tcommon = rng.getrandbits(40)
sigs = []
for i in range(14):
    z = rng.randrange(1, n)
    k = (tcommon << (n.bit_length() - 40)) | rng.getrandbits(n.bit_length() - 40)
    sigs.append(L.ecdsa_sign(cv, d, z, k))
ts, a_eqs, Bb = L.hnp_from_biased_nonces(cv, sigs, 40, mode="shared_msb")
sols = L.hnp_solve_embedding(n, ts, a_eqs, Bb, ntry=6)
check("ECDSA shared-MSB 40 bit", d in sols)

# k = z XOR d (TSJ style) -> affine modular subset sum, P-192, 6 chu ky
# k = z + d - 2*sum_j 2^j z_j d_j ; s*k = z + r*d (mod n)
# -> sum_j d_j*(s - r - s*2^(j+1)*z_j) + z - s*z = 0 (mod n)
m_bits = n.bit_length()
sigs = []
for i in range(6):
    z = rng.randrange(1, n)
    k = z ^ d
    if k == 0:
        continue
    sigs.append(L.ecdsa_sign(cv, d, z, k))
A, consts = [], []
for (z, r, s) in sigs:
    row = []
    for j in range(m_bits):
        zj = (z >> j) & 1
        row.append((2 ** j * (s - r - 2 * s * zj)) % n)
    A.append(row)
    consts.append((s * z - z) % n)
t0 = time.time()
e = L.affine_modular_subset_sum_solve(A, consts, n)
d_recovered = sum(ej << j for j, ej in enumerate(e)) if e else None
check("ECDSA k=z^d -> affine subset sum (6 chu ky)", d_recovered == d,
      f"({time.time()-t0:.1f}s)")

# ---------------------------------------------------------------- EHNP
print("== EHNP")
cv = L.P192
n = cv.n
d = rng.randrange(1, n)
d1 = rng.getrandbits(40)
dbar = (d - (d1 << 60)) % n
eqs = []
for i in range(20):
    z = rng.randrange(1, n)
    k1 = rng.getrandbits(24)
    kbar_msb = rng.getrandbits(n.bit_length() - 29)
    k = ((kbar_msb << 28) + (k1 << 4)) % n
    sig = L.ecdsa_sign(cv, d, z, k)
    (z, r, s) = sig
    kbar_known = kbar_msb << 28
    # r*(dbar + 2^60 d1) - s*2^4*k1 = s*kbar_known - z  (mod n)
    # eqs dang (alpha, [(rho, mu)...], beta)
    eqs.append((r, [(((-s) << 4) % n, 24)], (s * kbar_known - z) % n))
t0 = time.time()
cands = L.ehnp_solve(n, dbar, [(60, 40)], eqs)
check("EHNP (24 bit nonce x20 + 40 bit khoa)", d in cands,
      f"({time.time()-t0:.1f}s)")

# ---------------------------------------------------------------- BD + PKE
print("== Boneh-Durfee / partial key exposure")
from rsalib import gen_prime


def gen_bd_key(nbits, d_bits):
    while True:
        p = gen_prime(nbits // 2, rng)
        q = gen_prime(nbits // 2, rng)
        if p == q:
            continue
        N = p * q
        phi = (p - 1) * (q - 1)
        d = rng.getrandbits(d_bits) | (1 << (d_bits - 1))
        if math.gcd(d, phi) != 1:
            continue
        e = inverse(d, phi)
        return {"p": p, "q": q, "n": N, "phi": phi, "d": d, "e": e}


key = gen_bd_key(512, 128)
t0 = time.time()
res = L.boneh_durfee_attack(key["n"], key["e"], 128, m=4, t=1, verbose=True)
check("Boneh-Durfee d=N^0.25", res is not None and res[0] == key["d"],
      f"({time.time()-t0:.1f}s)")

key2 = gen_bd_key(512, 183)
d0 = key2["d"] >> 8 << 8
t0 = time.time()
res2 = L.partial_key_exposure_ksolve(key2["n"], key2["e"], d0, ncand=600)
if res2 is None:
    _k = (key2["e"] * key2["d"] - 1) // key2["phi"]
    _k0 = (key2["e"] * d0) // key2["n"]
    print("   [diag] k-k0 =", _k - _k0, " d-d0 =", key2["d"] - d0)
    _kc = _k
    _s = (1 + _kc * (key2["n"] + 1)) * inverse(2 * _kc, key2["e"]) % key2["e"]
    _disc = _s * _s - key2["n"]
    _r = math.isqrt(_disc)
    print("   [diag] disc square:", _r * _r == _disc,
          " gcd(2k,e):", math.gcd(2 * _kc % key2["e"], key2["e"]),
          " pq:", (_s + _r) // 2 * ((_s - _r) // 2) == key2["n"])
check("PKE xap-xi k (d=183 bit, thieu 8 bit thap)",
      res2 is not None and res2[0] == key2["d"] and res2[1] * res2[2] == key2["n"],
      f"({time.time()-t0:.1f}s)")

print()
print(f"===== {ok_count} OK, {len(fail)} FAIL {fail}")
sys.exit(1 if fail else 0)
