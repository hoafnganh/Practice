# -*- coding: utf-8 -*-
"""latlib.py — thu vien chung cho cac lattice challenge (lattice/).

Tai dung LLL / Coppersmith / integer_roots da kiem chung tu bo RSA
(../_lib/rsalib.py), bo sung cac cong cu theo paper
"A Gentle Tutorial for Lattice-Based Cryptanalysis" (ePrint 2023/032):

  - Babai nearest plane (CVP xap xi), Kannan embedding
  - HNP solver (embedding + Babai)                     [paper muc 4.3]
  - CJLOSS subset sum (thuong / modular / multiple)    [paper muc 4.2]
  - Minimal polynomial tu xap xi thap phan (KLL84)     [paper muc 3.6]
  - Truncated LCG -> HNP                               [paper Hinh 2]
  - ECDSA co ban + bien doi biased nonce -> HNP        [paper muc 5.3]
  - EHNP solver (Hlavac-Rosa)                          [paper muc 4.3.2]
  - Bivariate modular small roots (Boneh-Durfee dang)  [paper muc 5.2]

Chi phu thuoc: gmpy2, pycryptodome, sympy, flint. He so da thuc THAP -> CAO.
"""
import math
import os
import sys
from fractions import Fraction

_HERE = os.path.dirname(os.path.abspath(__file__))
_RSA_LIB = os.path.normpath(os.path.join(_HERE, "..", "..", "_lib"))
if _RSA_LIB not in sys.path:
    sys.path.insert(0, _RSA_LIB)

from rsalib import (lll, integer_roots, coppersmith_small_roots, poly_trim,  # noqa: E402
                    is_probable_prime, gen_prime)

from Crypto.Util.number import bytes_to_long, long_to_bytes, inverse  # noqa: E402,F401


def aes_encrypt_flag(flag_bytes, secret_int, rng):
    """Ma hoa flag bang AES-CTR, key = sha256(secret_int). Tra ve (nonce, ct)."""
    import os
    from Crypto.Cipher import AES
    from Crypto.Hash import SHA256
    key = SHA256.new(long_to_bytes(secret_int)).digest()
    nonce = rng.getrandbits(64).to_bytes(8, 'big')
    ct = AES.new(key, AES.MODE_CTR, nonce=nonce).encrypt(flag_bytes)
    return nonce, ct


def aes_decrypt_flag(ct, nonce, secret_int):
    from Crypto.Cipher import AES
    from Crypto.Hash import SHA256
    key = SHA256.new(long_to_bytes(secret_int)).digest()
    return AES.new(key, AES.MODE_CTR, nonce=nonce).decrypt(ct)


def lll_exact(B, delta=0.99):
    """LLL voi Gram CHINH XAC (flint gram='exact'), fallback pure-Python.

    Can thiet cho lattice co entry rat lon (VD e^m trong Boneh-Durfee) —
    gram xap xi co the tra ve vector khong thuoc lattice.
    """
    rows = [[int(x) for x in row] for row in B]
    try:
        from flint import fmpz_mat
        R = fmpz_mat(rows).lll(delta=delta, gram="exact")
        return [[int(R[i, j]) for j in range(R.ncols())] for i in range(R.nrows())]
    except ImportError:
        pass
    from rsalib import _lll_pure
    return _lll_pure(rows, delta=delta)


# ---------------------------------------------------------------------------
# Gram-Schmidt / Babai (CVP xap xi) — Fraction, chinh xac
# ---------------------------------------------------------------------------

def gso(B):
    """Gram-Schmidt: tra ve (b*, mu) deu la Fraction."""
    n, w = len(B), len(B[0])
    Bs, mu = [], [[Fraction(0)] * n for _ in range(n)]
    for i in range(n):
        v = [Fraction(x) for x in B[i]]
        for j in range(i):
            nj = sum(x * x for x in Bs[j])
            if nj == 0:
                mu[i][j] = Fraction(0)
                continue
            s = sum(Fraction(B[i][q]) * Bs[j][q] for q in range(w))
            mu[i][j] = s / nj
            if mu[i][j]:
                v = [v[q] - mu[i][j] * Bs[j][q] for q in range(w)]
        Bs.append(v)
    return Bs, mu


def babai(B, t, reduce_first=True):
    """Babai nearest plane — tra ve diem lattice (list int) gan target t."""
    B = [[int(x) for x in row] for row in B]
    if reduce_first:
        B = lll(B)
    n, w = len(B), len(B[0])
    cur = [Fraction(x) for x in t]
    Bs, _ = gso(B)
    c = [0] * n
    for i in range(n - 1, -1, -1):
        nj = sum(x * x for x in Bs[i])
        if nj == 0:
            continue
        s = sum(cur[q] * Bs[i][q] for q in range(w))
        c[i] = int(math.floor(s / nj + Fraction(1, 2)))
        if c[i]:
            cur = [cur[q] - c[i] * Fraction(B[i][q]) for q in range(w)]
    v = [0] * w
    for i in range(n):
        if c[i]:
            v = [v[q] + c[i] * B[i][q] for q in range(w)]
    return v


def kannan_embed(B, t, q=1):
    """Lattice nhung: [[B 0], [t q]] — bien CVP thanh SVP."""
    B = [[int(x) for x in row] for row in B]
    return [row + [0] for row in B] + [[int(x) for x in t] + [q]]


# ---------------------------------------------------------------------------
# Hidden Number Problem [paper muc 4.3]
#   k_i = t_i*alpha + a_i (mod q), |k_i| < B  (k_i "phan bi che" nho)
# Lattice nguyen (kieu Howgrave-Graham-Smart): so an LON (alpha) chi xuat
# hien trong TO HOP cua hang b, khong xuat hien trong vector ngan:
#   hang q*e_i ;  hang a = (a_i + B/2 , B) ;  hang b = (t_i , 0)
# To hop (l_i, alpha, -1):  (l_i q + t_i alpha - a_i - B/2,  -B)
#                         = (k_i - B/2, -B)   — toan bo toa do <= B/2.
# ---------------------------------------------------------------------------
def hnp_lattice(q, ts, a_eqs, B):
    """Co so (m+2) x (m+1) cho HNP: k_i = t_i*alpha + a_i (mod q), k_i ∈ [0,B).

    To hop (-l_i, alpha, +1) cho vector (k_i - B/2, +B).
    """
    m = len(ts)
    half = B >> 1
    rows = [[q if j == i else 0 for j in range(m)] + [0] for i in range(m)]
    rows.append([(int(a) - half) % q for a in a_eqs] + [B])
    rows.append([int(t) % q for t in ts] + [0])
    return rows


def hnp_solve_embedding(q, ts, a_eqs, B, ntry=8):
    """Giai HNP + LLL. Tra ve danh sach ung vien alpha (co the co nhieu).

    q bat ky (nguyen to hoan toan khong bat buoc).
    """
    m = len(ts)
    R = lll(hnp_lattice(q, ts, a_eqs, B))
    cands = []
    half = B >> 1
    for row in R[:ntry]:
        if abs(row[-1]) != B:
            continue
        # vector dung: (k_i - B/2, +B); ban am: (B/2 - k_i, -B)
        if row[-1] > 0:
            k = [row[i] + half for i in range(m)]
        else:
            k = [half - row[i] for i in range(m)]
        k = [ki % q for ki in k]
        if not all(0 <= ki < B for ki in k):
            continue
        # alpha = (k_i - a_i) * t_i^{-1} (mod q) — lay phieu chi hoi
        from collections import Counter
        votes = Counter()
        for ti, ai, ki in zip(ts, a_eqs, k):
            if math.gcd(ti % q, q) != 1:
                continue
            votes[(ki - ai) * inverse(ti % q, q) % q] += 1
        if votes:
            alpha, cnt = votes.most_common(1)[0]
            if cnt >= max(2, m // 4) and alpha not in cands:
                cands.append(alpha)
    return cands


def hnp_check(q, ts, a_eqs, B, alpha):
    """True neu moi k_i = (t_i*alpha + a_i) mod q nam trong [0, B)."""
    for t, a in zip(ts, a_eqs):
        if (t * alpha + a) % q >= B:
            return False
    return True


# ---------------------------------------------------------------------------
# Subset sum / knapsack — CJLOSS [paper muc 4.2]
# ---------------------------------------------------------------------------

def cjloss_lattice(weights, targets, mod=None, N=None):
    """CJLOSS cho (multiple)(modular) subset sum, nguyen hoa (x2, bo 1/2).

    weights: list n so a_i (hoac list cua cot khi multiple); targets: k so s_j;
    mod: M hoac None. rows (n + k_mod + 1) x (n + k). Vector dich:
    (2e_i - 1, 0, ..., 0) — chuan <= sqrt(n).
    """
    if weights and hasattr(weights[0], "__len__"):
        cols = [[w[i] for w in weights] for i in range(len(targets))]
        n = len(weights)
    else:
        cols = [weights] * len(targets)
        n = len(weights)
    k = len(targets)
    if N is None:
        N = math.isqrt(n) + 1
    rows = []
    for i in range(n):
        rows.append([2 if j == i else 0 for j in range(n)]
                    + [N * int(cols[j][i]) for j in range(k)])
    if mod is not None:
        for j in range(k):
            rows.append([0] * n + [N * int(mod) if jj == j else 0
                                   for jj in range(k)])
    rows.append([1] * n + [N * int(s) for s in targets])
    return rows


def _read_subset_row(row, n):
    """Doc (±1,...,±1) -> hai ung vien e (0/1) theo hai dau; None neu sai format."""
    v = list(row[:n])
    out = []
    for sign in (1, -1):
        u = [sign * x for x in v]
        if all(x in (1, -1) for x in u):
            out.append([(x + 1) // 2 for x in u])
    return out


def subset_sum_solve(weights, s, ntry=4):
    """Subset sum thuong: sum e_i a_i = s. Tra ve e (0/1) hoac None."""
    R = lll_exact(cjloss_lattice(weights, [s]))
    for row in R[:ntry]:
        if any(row[len(weights):]):
            continue
        for e in (_read_subset_row(row, len(weights)) or []):
            if sum(ei * ai for ei, ai in zip(e, weights)) == s:
                return e
    return None


def modular_subset_sum_solve(weights, s, M, scale_bits=64, ntry=8):
    """Modular subset sum: sum e_i a_i = s (mod M), e_i ∈ {0,1}.

    Dung lattice kieu TSJ (affine congruence): cac bit e_i la HE SO TO HOP,
    vector ngan = (0...0 | e_1..e_n | 1). Tra ve e hoac None.
    """
    return affine_modular_subset_sum_solve([list(weights)], [-int(s)], M,
                                           scale_bits=scale_bits, ntry=ntry)


def multiple_modular_subset_sum_solve(weights, targets, M, scale_bits=64,
                                      ntry=8):
    """Multiple modular subset sum: sum_i e_i a_{j,i} = s_j (mod M), j=1..k.

    weights: list n cot (moi cot la list k so a_{j,i}) hoac list 1 chieu
    khi k=1. targets: s_j. Tra ve e (0/1) hoac None.
    """
    if weights and hasattr(weights[0], "__len__"):
        cols = weights
        k = len(cols[0])
    else:
        cols = [[w] for w in weights]
        k = 1
    A = [[cols[i][j] for i in range(len(cols))] for j in range(k)]
    consts = [-int(s) for s in targets]
    return affine_modular_subset_sum_solve(A, consts, M,
                                           scale_bits=scale_bits, ntry=ntry)


def affine_modular_subset_sum_solve(A, consts, q, scale_bits=64, ntry=8):
    """Giai he affine modulo:  c_j + sum_i A[j][i]*e_i = 0 (mod q), e∈{0,1}^m.

    Lattice kieu TSJ CTF 2022 "Signature" (CJLOSS the he moi):
      - k hang mod-q: (q*2^s tai cot j)
      - m hang don vi: (A[:,i] tai k cot dau | 1 tai cot k+i)
      - hang constant: (c_j | 0..0 | 1 tai cot cuoi)
    Cot 0..k-1 nhan 2^s de LLL "thich" vector co phan du = 0.
    Vector dich: (0...0, e_1..e_m, 1) — chuan sqrt(m+2).
    """
    k = len(consts)
    m = len(A[0]) if k else 0
    S = 1 << scale_bits
    dim = k + m + 1
    rows = []
    for j in range(k):
        row = [0] * dim
        row[j] = q          # cot se duoc scale S o duoi
        rows.append(row)
    for i in range(m):
        row = [(A[j][i]) % q for j in range(k)] + [0] * (m + 1)
        row[k + i] = 1
        rows.append(row)
    row = [int(c) % q for c in consts] + [0] * m + [1]
    rows.append(row)
    # scale k cot mod-q
    rows = [[(v * S if idx < k else v) for idx, v in enumerate(r)]
            for r in rows]
    R = lll(rows)
    for row in R[:ntry * 4]:
        if any(row[:k]):
            continue
        y = row[k:]
        for sign in (1, -1):
            yy = [sign * v for v in y]
            if yy[-1] != 1:
                continue
            bits = yy[:m]
            if all(b in (0, 1) for b in bits):
                ok = all((consts[j]
                          + sum(A[j][i] * bits[i] for i in range(m))) % q == 0
                         for j in range(k))
                if ok:
                    return bits
    return None


# ---------------------------------------------------------------------------
# Minimal polynomial (KLL84) [paper muc 3.6]
# ---------------------------------------------------------------------------

def minimal_polynomial(beta_str, degree, scale=10 ** 12, ntry=4):
    """Tim da thuc toi tieu bac `degree` cua alpha ~ beta_str (thap phan).

    Lattice theo paper: degree hang (scale*beta^i, e_i) + 1 hang cuoi
    (scale*beta^degree, 0...0). Vector dich (≈0, a_0..a_{degree-1}),
    he so monic a_degree = 1 gan ngoai lattice. Tra ve he so thap->cao
    hoac None.
    """
    from decimal import Decimal, getcontext
    getcontext().prec = max(80, len(beta_str) * 3)
    beta = Decimal(beta_str)
    pw, b = [], Decimal(1)
    for _ in range(degree + 1):
        pw.append(int(b * scale))
        b *= beta
    rows = []
    for i in range(degree):
        rows.append([pw[i]] + [1 if j == i else 0 for j in range(degree)])
    rows.append([pw[degree]] + [0] * degree)
    R = lll(rows)
    for row in R[:ntry]:
        if abs(row[0]) * 100 >= scale:
            continue  # cot 0 phai "gan 0" so voi scale
        return list(row[1:]) + [1]
    return None


# ---------------------------------------------------------------------------
# Truncated LCG -> HNP [paper Hinh 2, Frieze+88]
#   x_{i+1} = a x_i + b (mod M), chi thay y_i = x_i >> t
# ---------------------------------------------------------------------------

def truncated_lcg_solve(a, b, M, ys, t):
    """Phuc hoi x_0 tu cac bit cao y_i cua tung trang thai
    (x_{i+1} = a x_i + b (mod M), y_i = x_i >> t). Tra ve x_0 hoac None.

    Bien doi: e_i = x_i - 2^t y_i ∈ [0, 2^t) thoa
      e_i = a^i * x_0 + (c_i - 2^t y_i)  (mod M)  — dung HNP voi B = 2^t.
    """
    m = len(ys)
    ts, a_eqs = [], []
    c, ai = 0, 1
    for i in range(m):
        ts.append(ai % M)
        a_eqs.append((c - ((1 << t) * ys[i])) % M)
        c = (a * c + b) % M
        ai = ai * a % M
    B = 1 << t
    for alpha in hnp_solve_embedding(M, ts, a_eqs, B, ntry=10):
        x = alpha % M
        ok = True
        for y in ys:
            if (x >> t) != y:
                ok = False
                break
            x = (a * x + b) % M
        if ok:
            return alpha % M
    return None


# ---------------------------------------------------------------------------
# ECDSA co ban + biased nonces -> HNP [paper muc 5.3]
# ---------------------------------------------------------------------------

class Curve:
    """Weierstrass y^2 = x^3 + ax + b tren F_p."""

    def __init__(self, p, a, b, Gx, Gy, n, name=""):
        self.p, self.a, self.b = p, a, b
        self.G = (Gx, Gy)
        self.n = n
        self.name = name

    def add(self, P, Q):
        if P is None:
            return Q
        if Q is None:
            return P
        p = self.p
        x1, y1 = P
        x2, y2 = Q
        if x1 == x2 and (y1 + y2) % p == 0:
            return None
        if P == Q:
            lam = (3 * x1 * x1 + self.a) * inverse(2 * y1 % p, p) % p
        else:
            lam = (y2 - y1) * inverse((x2 - x1) % p, p) % p
        x3 = (lam * lam - x1 - x2) % p
        y3 = (lam * (x1 - x3) - y1) % p
        return (x3, y3)

    def mul(self, k, P=None):
        P = self.G if P is None else P
        R = None
        k %= self.n
        while k:
            if k & 1:
                R = self.add(R, P)
            P = self.add(P, P)
            k >>= 1
        return R


SECP256K1 = Curve(
    p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
    a=0, b=7,
    Gx=0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    Gy=0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
    n=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
    name="secp256k1",
)

P192 = Curve(
    p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFFFFFFFFFF,
    a=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFFFFFFFFFC,
    b=0x64210519E59C80E70FA7E9AB72243049FEB8DEECC146B9B1,
    Gx=0x188DA80EB03090F67CBF20EB43A18800F4FF0AFD82FF1012,
    Gy=0x07192B95FFC8DA78631011ED6B24CDD573F977A11E794811,
    n=0xFFFFFFFFFFFFFFFFFFFFFFFF99DEF836146BC9B1B4D22831,
    name="P-192",
)


def ecdsa_sign(curve, d, z, k):
    """Ky (z, r, s) voi nonce k cho truoc. z da la hash (int < n)."""
    R = curve.mul(k)
    r = R[0] % curve.n
    s = (inverse(k, curve.n) * (z + r * d)) % curve.n
    if r == 0 or s == 0:
        raise ValueError("nonce xau (r hoac s = 0)")
    return (z, r, s)


def ecdsa_verify(curve, Q, z, r, s):
    if not (1 <= r < curve.n and 1 <= s < curve.n):
        return False
    w = inverse(s, curve.n)
    P = curve.add(curve.mul(z * w % curve.n), curve.mul(r * w % curve.n, Q))
    return P is not None and P[0] % curve.n == r


def hnp_from_biased_nonces(curve, sigs, leak_bits, mode="zero_msb"):
    """Chuyen chu ky ECDSA thanh instance HNP: tra ve (ts, a_eqs, B).

    Convention: k_i = t_i * d + a_i (mod n) voi k_i ∈ [0, B) ("phan bi che").
    mode:
      zero_msb  : k_i < 2^(L-l)            (l bit cao = 0)
      zero_lsb  : k_i = 2^l * k'_i, k' nho
      known_msb : k_i = 2^(L-l) t_i + k'_i (sigs co them t_i)
      shared_msb: cac nonce chia l bit cao chung (khong biet gia tri)
    """
    n = curve.n
    L = n.bit_length()
    l = leak_bits
    ts, a_eqs = [], []
    if mode == "zero_msb":
        for (z, r, s) in sigs:
            si = inverse(s, n)
            ts.append(si * r % n)
            a_eqs.append(si * z % n)
        B = 1 << (L - l)
    elif mode == "zero_lsb":
        f = inverse(1 << l, n)
        for (z, r, s) in sigs:
            si = inverse(s, n)
            ts.append(f * si * r % n)
            a_eqs.append(f * si * z % n)
        B = 1 << (L - l)
    elif mode == "known_msb":
        for (z, r, s, t_i) in sigs:
            si = inverse(s, n)
            ts.append(si * r % n)
            a_eqs.append((si * z - (1 << (L - l)) * t_i) % n)
        B = 1 << (L - l)
    elif mode == "shared_msb":
        # hieu hai phuong trinh de khu bit cao chung t:
        # k'_i - k'_1 = (s_i^-1 z_i - s_1^-1 z_1) + (s_i^-1 r_i - s_1^-1 r_1) d
        # voi k'_i - k'_1 ∈ (-2^(L-l), 2^(L-l)) -> dich +2^(L-l) ve [0, 2^(L-l+1))
        (z1, r1, s1) = sigs[0]
        s1i = inverse(s1, n)
        for (z, r, s) in sigs[1:]:
            si = inverse(s, n)
            ts.append((si * r - s1i * r1) % n)
            a_eqs.append((si * z - s1i * z1 + (1 << (L - l))) % n)
        B = 1 << (L - l + 1)
    else:
        raise ValueError(mode)
    return ts, a_eqs, B


# ---------------------------------------------------------------------------
# EHNP (Hlavac-Rosa) [paper muc 4.3.2]
#   x = xbar + sum_j 2^pi_j x_j  (0 <= x_j < 2^nu_j)
#   alpha_i * sum_j 2^pi_j x_j + sum_j rho_{i,j} k_{i,j}
#       = beta_i - alpha_i*xbar  (mod p),   0 <= k_{i,j} < 2^mu_{i,j}
# ---------------------------------------------------------------------------

def ehnp_solve(p, xbar, chunks, eqs, embed_q=None, ntry=10):
    """Giai EHNP bang embedding CVP + LLL. Tra ve danh sach ung vien x.

    chunks: [(pi_j, nu_j)]. eqs: [(alpha_i, [(rho_ij, mu_ij), ...], beta_i)].
    Cac chunk duoc scale boi S_j = K/2^nu_j (K = 2^max nu) de dua ve [0, K);
    target dat o tam khoang (K/2); embedding bien CVP thanh SVP.
    """
    m, d = len(chunks), len(eqs)
    L = sum(len(e[1]) for e in eqs)
    K = 1 << max(nu for _, nu in chunks)
    S = [K >> nu for (_, nu) in chunks]
    if embed_q is None:
        embed_q = K
    rows = []
    # hang r_i: [p e_i | 0 | 0]
    for i in range(d):
        rows.append([p if j == i else 0 for j in range(d)] + [0] * (m + L))
    # hang x_j: [alpha_i 2^pi_j | S_j tai cot d+j | 0]
    for j, (pi, _nu) in enumerate(chunks):
        row = [(alpha * (1 << pi)) % p for (alpha, _kl, _b) in eqs]
        row += [0] * m + [0] * L
        row[d + j] = S[j]
        rows.append(row)
    # hang k_{i,j}: [rho_ij tai cot i | 0 | (K/2^mu) tai cot rieng]
    c = d + m
    for i, (_alpha, klst, _b) in enumerate(eqs):
        for (rho, mu) in klst:
            row = [0] * d + [0] * m + [0] * L
            row[i] = rho % p
            row[c] = K >> mu
            rows.append(row)
            c += 1
    # target: (beta_i - alpha_i xbar, K/2, ..., K/2)
    target = [(beta - alpha * xbar) % p for (alpha, _k, beta) in eqs]
    target += [K >> 1] * (m + L)
    emb = [row + [0] for row in rows] + [[int(t) for t in target] + [embed_q]]
    R = lll(emb)
    cands = []
    for row in R[:ntry]:
        if abs(row[-1]) != embed_q:
            continue
        neg = row[-1] < 0   # row = (u - w, -q) neu neg, (w - u, +q) neu khong
        xs, ok = [], True
        for j, (pi, nu) in enumerate(chunks):
            raw = row[d + j]
            v = (raw + (K >> 1)) if neg else ((K >> 1) - raw)  # = x_j * S_j
            if v < 0 or v % S[j]:
                ok = False
                break
            xs.append(v // S[j])
        if not ok:
            continue
        x = (xbar + sum((1 << pi) * xj for (pi, _n), xj in zip(chunks, xs))) % p
        if x not in cands:
            cands.append(x)
    return cands


# ---------------------------------------------------------------------------
# Bivariate modular small roots kieu Boneh-Durfee [paper muc 5.2]
#   f(x,y) = 0 (mod e) voi nghiem (x0 < X, y0 < Y)
#   shift: x^i f^k e^{m-k} (x-shifts) va y^j f^m (y-shifts)
# ---------------------------------------------------------------------------

def _p2_mul(f, g):
    out = {}
    for (i1, j1), c1 in f.items():
        for (i2, j2), c2 in g.items():
            kk = (i1 + i2, j1 + j2)
            out[kk] = out.get(kk, 0) + c1 * c2
    return {kk: c for kk, c in out.items() if c}


def _p2_shift(f, dx, dy):
    return {(i + dx, j + dy): c for (i, j), c in f.items()}


def resultant_x_interp(p1, p2):
    """Resultant theo x cua 2 da thuc 2 bien, bang danh gia + noi suy Lagrange.

    res(y) co bac <= D = xd1*yd2 + xd2*yd1. Tai D+1+ diem y_j, resultant
    cua hai da thuc 1 bien theo x duoc tinh boi flint (nhanh, chinh xac);
    noi suy Lagrange tren Fraction tra lai he so nguyen (thap->cao).
    """
    from flint import fmpz_poly
    xd1 = max(i for (i, _j) in p1)
    xd2 = max(i for (i, _j) in p2)
    yd1 = max(j for (_i, j) in p1)
    yd2 = max(j for (_i, j) in p2)
    D = xd1 * yd2 + xd2 * yd1
    npts = D + 9

    def univar(p, y0):
        # he so theo x cua p tai y = y0 (thap -> cao)
        xd = max(i for (i, _j) in p)
        cs = [0] * (xd + 1)
        for (i, j), c in p.items():
            cs[i] += c * (y0 ** j)
        return fmpz_poly(cs)

    pts, vals = [], []
    for t in range(-(npts // 2), npts // 2 + 1):
        r = univar(p1, t).resultant(univar(p2, t))
        pts.append(t)
        vals.append(int(r))
        if len(pts) >= npts:
            break
    # noi suy Lagrange: res(y) = sum_j v_j * L_j(y)
    from fractions import Fraction
    coeffs = [Fraction(0)] * npts
    for j in range(npts):
        # da thuc L_j = prod_{i!=j} (y - pts[i]) / (pts[j] - pts[i])
        poly = [Fraction(1)]
        den = Fraction(1)
        for i in range(npts):
            if i == j:
                continue
            poly = _frac_poly_mul(poly, [Fraction(-pts[i]), Fraction(1)])
            den *= (pts[j] - pts[i])
        scale = Fraction(vals[j]) / den
        for q in range(len(poly)):
            coeffs[q] += poly[q] * scale
    out = []
    for c in coeffs:
        assert c.denominator == 1, "noi suy khong nguyen"
        out.append(int(c))
    return poly_trim(out)


def _frac_poly_mul(f, g):
    out = [Fraction(0)] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        if a:
            for j, b in enumerate(g):
                if b:
                    out[i + j] += a * b
    return out


def _resultant_x(p1, p2):
    return resultant_x_interp(p1, p2)


def bivariate_modular_small_roots(f, e, X, Y, m=4, t=1, npoly=4,
                                  verbose=False):
    """Nghiem nho (x0,y0) cua f(x,y)=0 (mod e) voi |x0|<X, |y0|<Y.

    f: dict {(i,j): c}. Dung shift kieu BD: x^i f^k e^{m-k} (k=0..m,
    i=0..m-k) va y^j f^m (j=1..t). Tra ve list ung vien (x0, y0).
    """
    fpow = [{(0, 0): 1}]
    for _ in range(m):
        fpow.append(_p2_mul(fpow[-1], f))
    shifts = []
    for k in range(m + 1):
        for i in range(m - k + 1):
            g = _p2_shift(fpow[k], i, 0)
            shifts.append({kk: c * pow(e, m - k) for kk, c in g.items()})
    for j in range(1, t + 1):
        shifts.append(_p2_shift(fpow[m], 0, j))
    monos = sorted({kk for g in shifts for kk in g})
    if verbose:
        print(f"[bv] shifts={len(shifts)} dim={len(monos)} "
              f"X={X.bit_length()}b Y={Y.bit_length()}b e={e.bit_length()}b")
    rows = [[g.get(mo, 0) * (X ** mo[0]) * (Y ** mo[1]) for mo in monos]
            for g in shifts]
    R = lll_exact(rows)
    polys = []
    for row in R[:npoly * 2]:
        g = {}
        ok = True
        for q, mo in enumerate(monos):
            if row[q]:
                if row[q] % (X ** mo[0] * Y ** mo[1]):
                    ok = False
                    break
                g[mo] = row[q] // (X ** mo[0] * Y ** mo[1])
        if ok and len(g) >= 2:
            polys.append(g)
        if len(polys) >= npoly:
            break
    if verbose:
        print(f"[bv] {len(polys)} da thuc ngan")
    out = []
    for a in range(min(3, max(1, len(polys) - 1))):
        res = _resultant_x(polys[a], polys[a + 1])
        if not res:
            continue
        res = poly_trim(res)
        if not res or len(res) < 2:
            continue
        out.extend(integer_roots(res, Y))
        if out:
            break
    return out, polys


# ---------------------------------------------------------------------------
# Boneh-Durfee [paper muc 5.2.1]
#   f(x,y) = 1 + (N+1)x - 2xy = 0 (mod e), nghiem (k, (p+q)/2)
# ---------------------------------------------------------------------------

def boneh_durfee_attack(N, e, d_bits, m=4, t=1, verbose=False):
    """Tan cong Boneh-Durfee khi d ~ 2^d_bits (d < N^0.292).
    Tra ve (d, k, s) hoac None."""
    X = 1 << (d_bits + 4)
    Y = 1 << (N.bit_length() // 2 + 2)
    f = {(0, 0): 1, (1, 0): (N + 1) % e, (1, 1): -2}
    ys, polys = bivariate_modular_small_roots(f, e, X, Y, m=m, t=t,
                                              verbose=verbose)
    if not polys:
        return None
    for y0 in ys:
        if y0 <= 0 or 2 * y0 > N:
            continue
        coef = ((N + 1) - 2 * y0) % e
        if math.gcd(coef, e) != 1:
            continue
        k = (-inverse(coef, e)) % e
        if k == 0 or k >= X:
            continue
        phi = N + 1 - 2 * y0
        if (k * phi + 1) % e:
            continue
        d_cand = (k * phi + 1) // e
        return (d_cand, k, y0)
    return None


def partial_key_exposure_ksolve(N, e, d0, ncand=8):
    """PKE (y tuong muc 5.2.2): biet MSBs cua d (d0 = d >> ub << ub).

    k = (ed-1)/phi; k0 = floor(e*d0/N) xap xi k voi sai so ≈ (e/phi)*phan an.
    Thu cac ung vien k quanh k0; voi moi k: 2ks ≡ 1 + k(N+1) (mod e)
    -> s = s0 + l*e (s < (p+q) < 2^bitN); giai z^2 - 2sz + N = 0.
    Tra ve (d, p, q) hoac None.
    """
    k0 = (e * d0) // N
    smax = 1 << (N.bit_length() // 2 + 2)
    for kc in range(max(1, k0 - ncand), k0 + ncand + 1):
        if math.gcd(2 * kc % e, e) != 1:
            continue
        s0 = (1 + kc * (N + 1)) * inverse(2 * kc, e) % e
        s = s0
        while s <= smax:
            disc = s * s - N
            if disc >= 0:
                r = math.isqrt(disc)
                if r * r == disc:
                    p = s + r      # s = (p+q)/2, r = |p-q|/2 -> p = s + r
                    q = s - r
                    if p * q == N:
                        phi = N + 1 - 2 * s
                        if (kc * phi + 1) % e == 0:
                            return ((kc * phi + 1) // e, p, q)
            s += e
    return None
