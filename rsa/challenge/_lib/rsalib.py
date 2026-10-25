# -*- coding: utf-8 -*-
"""rsalib.py — thu vien chung cho cac RSA challenge (rsa/challenge/).

Chi dung thu vien co san: gmpy2, pycryptodome, sympy, flint (LLL nhanh).
Moi ham deu duoc kiem thu trong test_rsalib.py.
He so da thuc luon luon theo thu tu THAP -> CAO: f(x) = f[0] + f[1]*x + ...
"""
import math
import random

from Crypto.Util.number import bytes_to_long, long_to_bytes  # noqa: F401


# ---------------------------------------------------------------------------
# So nguyen to
# ---------------------------------------------------------------------------

def is_probable_prime(n, rounds=30):
    if n < 2:
        return False
    for sp in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % sp == 0:
            return n == sp
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    rng = random.SystemRandom()
    for _ in range(rounds):
        a = rng.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def gen_prime(bits, rng):
    while True:
        c = rng.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_probable_prime(c):
            return c


def gen_prime_near(x, rng, span=1 << 40):
    """So nguyen to le >= x (p, q gan nhau -> Fermat)."""
    c = x | 1
    while not is_probable_prime(c):
        c += 2
    return c


def gen_rsa_key(bits=1024, e=65537, rng=None):
    rng = rng or random.Random()
    while True:
        p = gen_prime(bits // 2, rng)
        q = gen_prime(bits // 2, rng)
        if p == q:
            continue
        n = p * q
        phi = (p - 1) * (q - 1)
        if math.gcd(e, phi) != 1:
            continue
        d = pow(e, -1, phi)
        return {"p": p, "q": q, "n": n, "phi": phi, "d": d}


# ---------------------------------------------------------------------------
# Phan so lien tuc + Wiener
# ---------------------------------------------------------------------------

def cf_convergents(num, den):
    res = []
    h2, h1, k2, k1 = 0, 1, 1, 0
    a, b = num, den
    while b:
        q = a // b
        a, b = b, a % b
        h2, h1 = h1, q * h1 + h2
        k2, k1 = k1, q * k1 + k2
        res.append((h1, k1))
    return res


def wiener_attack(N, e):
    """Phuc hoi d khi d < (1/3) N^(1/4). Tra ve (d, p, q) hoac None."""
    for k, d in cf_convergents(e, N):
        if k == 0 or d == 0:
            continue
        if (e * d - 1) % k:
            continue
        phi = (e * d - 1) // k
        s = N - phi + 1
        if s <= 0:
            continue
        disc = s * s - 4 * N
        if disc < 0:
            continue
        r = math.isqrt(disc)
        if r * r != disc:
            continue
        p = (s + r) // 2
        q = (s - r) // 2
        if p * q == N:
            return d, p, q
    return None


# ---------------------------------------------------------------------------
# Da thuc tren Z_N[x] (he so thap -> cao)
# ---------------------------------------------------------------------------

def poly_trim(f):
    g = list(f)
    while g and g[-1] == 0:
        g.pop()
    return g


def poly_deg(f):
    return len(poly_trim(f)) - 1


def poly_eval_mod(f, x, N):
    r = 0
    for c in reversed(poly_trim(f)):
        r = (r * x + c) % N
    return r % N


def poly_mul_mod(f, g, N):
    f, g = poly_trim(f), poly_trim(g)
    if not f or not g:
        return []
    r = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        if a:
            for j, b in enumerate(g):
                if b:
                    r[i + j] = (r[i + j] + a * b) % N
    return poly_trim(r)


def poly_gcd_mod(f, g, N):
    """GCD monic cua f, g tren Z_N[x].

    Tra ve (h, factor):
      thanh cong: h = GCD monic, factor = None;
      that bai (he so cao nhat khong nghich dao duoc): factor = uoc so khong
      tam thuong cua N.
    """
    f = poly_trim([c % N for c in f])
    g = poly_trim([c % N for c in g])
    while g:
        lc = g[-1] % N
        g5 = math.gcd(lc, N)
        if g5 != 1:
            return None, g5
        inv = pow(lc, -1, N)
        g = [(c * inv) % N for c in g]
        r = list(f)
        dg = poly_deg(g)
        while poly_deg(r) >= dg:
            coef = r[-1]
            shift = poly_deg(r) - dg
            for i, c in enumerate(g):
                r[shift + i] = (r[shift + i] - coef * c) % N
            r = poly_trim(r)
        f, g = g, r
    if not f:
        return [], None
    lc = f[-1] % N
    inv = pow(lc, -1, N)
    return [(c * inv) % N for c in f], None


# ---------------------------------------------------------------------------
# Pollard p-1
# ---------------------------------------------------------------------------

def pollard_p1(n, B=100000):
    a = 2
    for j in range(2, B + 1):
        a = pow(a, j, n)
        if j % 16 == 0 or j == B:
            d = math.gcd(a - 1, n)
            if 1 < d < n:
                return d, n // d
    return None


# ---------------------------------------------------------------------------
# LLL — flint (C-speed) fast path, pure-Python mpfr fallback
# ---------------------------------------------------------------------------

def lll(B, delta=0.99):
    """LLL tren co so so nguyen. B: list cac hang (list int)."""
    rows = [[int(x) for x in row] for row in B]
    try:
        from flint import fmpz_mat
        M = fmpz_mat(rows)
        R = M.lll(delta=delta)
        return [[int(R[i, j]) for j in range(R.ncols())] for i in range(R.nrows())]
    except ImportError:
        pass
    return _lll_pure(rows, delta=delta)


def _lll_pure(B, delta=0.99):
    """LLL pure-Python voi GSO mpfr do chinh xac cao + phep tinh hang nguyen."""
    from gmpy2 import mpfr, mpz, get_context
    n = len(B)
    if n == 0:
        return B
    w = len(B[0])
    maxbits = max((abs(int(x)).bit_length() for row in B for x in row), default=64)
    prec = 2 * maxbits + 512
    ctx = get_context()
    old_prec = ctx.precision
    ctx.precision = prec

    B = [[mpz(x) for x in row] for row in B]
    F = mpfr
    bstar = [None] * n
    mu = [[F(0)] * n for _ in range(n)]
    Bnorm = [F(0)] * n

    def _gso(k):
        bstar[k] = [F(x) for x in B[k]]
        for j in range(k):
            if Bnorm[j] == 0:
                mu[k][j] = F(0)
                continue
            s = F(0)
            bi, bj = B[k], bstar[j]
            for t in range(w):
                if bi[t] and bj[t]:
                    s += F(bi[t]) * bj[t]
            mukj = s / Bnorm[j]
            mu[k][j] = mukj
            if mukj:
                bk = bstar[k]
                for t in range(w):
                    if bj[t] and bk[t]:
                        bk[t] -= mukj * bj[t]
        s2 = F(0)
        for a in bstar[k]:
            if a:
                s2 += a * a
        Bnorm[k] = s2

    _gso(0)
    for i in range(1, n):
        _gso(i)

    half = F("0.5")
    delt = F(delta)
    k = 1
    guard = 0
    while k < n:
        guard += 1
        if guard > 20000000:
            ctx.precision = old_prec
            raise RuntimeError("LLL loop limit")
        for j in range(k - 1, -1, -1):
            mukj = mu[k][j]
            if abs(mukj) > half:
                r = int(math.floor(mukj + half))
                if r:
                    bj, bk = B[j], B[k]
                    for t in range(w):
                        if r * bj[t]:
                            bk[t] -= r * bj[t]
                    for i in range(j):
                        if mu[j][i]:
                            mu[k][i] -= r * mu[j][i]
                    mu[k][j] = mukj - r
        m = mu[k][k - 1]
        if Bnorm[k] >= (delt - m * m) * Bnorm[k - 1]:
            k += 1
            if k < n:
                _gso(k)
            continue
        nu = mu[k][k - 1]
        Bn = Bnorm[k] + nu * nu * Bnorm[k - 1]
        Bk1, Bk = Bnorm[k - 1], Bnorm[k]
        bs_k1, bs_k = bstar[k - 1], bstar[k]
        bstar[k - 1] = [a + nu * b for a, b in zip(bs_k, bs_k1)]
        c1, c2 = Bk / Bn, nu * Bk1 / Bn
        bstar[k] = [c1 * a - c2 * b for a, b in zip(bs_k1, bs_k)]
        Bnorm[k - 1] = Bn
        Bnorm[k] = Bk1 * Bk / Bn
        mu[k][k - 1] = c2
        for j in range(k - 1):
            mu[k - 1][j], mu[k][j] = mu[k][j], mu[k - 1][j]
        for i in range(k + 1, n):
            mik1, mik = mu[i][k - 1], mu[i][k]
            mu[i][k] = mik1 - nu * mik
            mu[i][k - 1] = mik + c2 * mik1 - c2 * nu * mik
        B[k], B[k - 1] = B[k - 1], B[k]
        if k > 1:
            k -= 1
    out = [[int(x) for x in row] for row in B]
    ctx.precision = old_prec
    return out


# ---------------------------------------------------------------------------
# Tim nghiem nguyen cua da thuc he so nguyen tren [-X, X]
# ---------------------------------------------------------------------------

def _poly_eval_int(f, x):
    r = 0
    for c in reversed(f):
        r = r * x + c
    return r


def integer_roots(f, X):
    """Cac nghiem nguyen cua f (he so thap->cao) trong [-X, X].

    Uu tien: phan tich thua so bang flint (fmpz_poly.factor) — nhanh va bat
    duoc nghiem boi. Fallback: quet thay doi ki hieu + bisection so nguyen."""
    f = poly_trim(f)
    if not f or len(f) == 1:
        return []
    if X <= 0:
        return []
    roots = set()
    try:
        import flint
        P = flint.fmpz_poly([int(c) for c in f])
        _, factors = P.factor()
        for p, e in factors:
            if p.degree() == 1:
                a0, b0 = int(p[0]), int(p[1])
                if b0 != 0 and a0 % b0 == 0:
                    r = -(a0 // b0)
                    if -X <= r <= X:
                        roots.add(r)
        return sorted(roots)
    except ImportError:
        pass
    grid = 512
    step = max(1, (2 * X) // grid)
    pts = list(range(-X, X + 1, step))
    if pts[-1] != X:
        pts.append(X)
    vals = []
    for p in pts:
        vals.append(_poly_eval_int(f, p))
    for i in range(len(pts) - 1):
        a, b = vals[i], vals[i + 1]
        pa, pb = pts[i], pts[i + 1]
        if a == 0:
            roots.add(pa)
        if (a > 0 > b) or (a < 0 < b):
            lo, hi = pa, pb
            while hi - lo > 1:
                mid = (lo + hi) // 2
                v = _poly_eval_int(f, mid)
                if v == 0:
                    roots.add(mid)
                    break
                if (v > 0) == (a > 0):
                    lo = mid
                else:
                    hi = mid
            else:
                for c in (lo, hi):
                    if _poly_eval_int(f, c) == 0:
                        roots.add(c)
    if _poly_eval_int(f, X) == 0:
        roots.add(X)
    if f[0] == 0:
        roots.add(0)
    return sorted(r for r in roots if -X <= r <= X)


# ---------------------------------------------------------------------------
# Coppersmith: nghiem nho cua da thuc monic mod N (Howgrave-Graham + LLL)
# ---------------------------------------------------------------------------

def poly_mul_int(f, g):
    r = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        if a:
            for j, b in enumerate(g):
                if b:
                    r[i + j] += a * b
    return poly_trim(r)


def coppersmith_small_roots(f_coeffs, N, X, m, t, verbose=False, check_mod_n=True):
    """Tim cac nghiem nguyen x0 voi |x0| < X va f(x0) == 0 (mod N).

    f monic bac d (f[-1] == 1). X <= N^(1/d). m, t: tham so lattice
    (w = d*m + t). check_mod_n=False khi nghiem chi mod mot THUA SO cua N
    (known-bits factoring) — nguoi goi tu kiem nghiem.
    """
    f_coeffs = poly_trim([c % N for c in f_coeffs])
    d = len(f_coeffs) - 1
    assert f_coeffs[-1] == 1, "f phai monic"
    w = d * m + t
    Xp = [pow(X, k) for k in range(w)]
    Np = [pow(N, i) for i in range(m + 1)]
    fpow = [[1]]
    for _ in range(1, m + 1):
        fpow.append(poly_mul_int(fpow[-1], f_coeffs))
    rows = []
    for i in range(m):
        base = [c * Np[m - i] for c in fpow[i]]
        for j in range(d):
            coeffs = ([0] * j + base + [0] * w)[:w]
            rows.append([coeffs[kk] * Xp[kk] for kk in range(w)])
    for a in range(t):
        coeffs = ([0] * a + fpow[m] + [0] * w)[:w]
        rows.append([coeffs[kk] * Xp[kk] for kk in range(w)])
    if verbose:
        det_bits = sum(r[-1].bit_length() for r in rows if r[-1])
        print(f"[coppersmith] dim={w}, log2(det)~{det_bits}, "
              f"X={X.bit_length()} bit, N={N.bit_length()} bit")
    Bl = lll(rows)
    roots = set()
    for row in Bl[: min(8, len(Bl))]:
        h = []
        ok = True
        for k, v in enumerate(row):
            if v % Xp[k]:
                ok = False
                break
            h.append(v // Xp[k])
        if not ok:
            continue
        h = poly_trim(h)
        if not h:
            continue
        g = 0
        for c in h:
            g = math.gcd(g, abs(c))
        if g > 1:
            h = [c // g for c in h]
        for r0 in integer_roots(h, X):
            if not check_mod_n or poly_eval_mod(f_coeffs, r0, N) == 0:
                roots.add(r0)
    return sorted(roots)


def coppersmith_known_high_bits(N, p_high, unknown_bits, m, t, verbose=False):
    """Phan tich N khi biet phan CAO cua p: p = p_high*2^u + x, x < 2^u."""
    u = unknown_bits
    f = [(int(p_high) << u) % N, 1]
    X = 1 << u
    roots = coppersmith_small_roots(f, N, X, m, t, verbose=verbose, check_mod_n=False)
    out = set()
    for x0 in roots:
        p = (int(p_high) << u) + x0
        if p > 1 and N % p == 0:
            out.add(p)
    return sorted(out)


# ---------------------------------------------------------------------------
# Giao thuc bac hai mod 2^k  (cho challenge 17 — BDF)
# ---------------------------------------------------------------------------

def _ctz(x):
    if x == 0:
        return 1 << 60
    return (x & -x).bit_length() - 1


def sqrt_mod_2k(D, k, cap=1 << 16):
    """Tat ca y mod 2^k voi y^2 == D (mod 2^k)."""
    if k <= 0:
        return [0]
    mod = 1 << k
    D %= mod
    if D == 0:
        e = (k + 1) // 2
        cnt = 1 << (k - e)
        if cnt > cap:
            raise RuntimeError("qua nhieu nghiem sqrt")
        return [t << e for t in range(cnt)]
    j = _ctz(D)
    if j & 1:
        return []
    if j >= k:
        return sqrt_mod_2k(0, k, cap)
    Dp = D >> j
    sub = k - j
    if sub == 1:
        roots = [Dp % 2]
    elif sub == 2:
        if Dp % 4 == 1:
            roots = [1, 3]
        elif Dp % 4 == 0:
            roots = [0, 2]
        else:
            return []
    else:
        if Dp % 8 != 1:
            return []
        roots = [1, 3, 5, 7]
        for lvl in range(3, sub):
            m2 = 1 << lvl
            nxt = []
            for r0 in roots:
                for cand in (r0, r0 + m2):
                    if (cand * cand - Dp) % (m2 << 1) == 0:
                        nxt.append(cand)
            roots = nxt
            if not roots:
                return []
    shift = j // 2
    step = 1 << sub
    tfree = 1 << (j - shift)
    if len(roots) * tfree > cap:
        raise RuntimeError("qua nhieu nghiem sqrt")
    out = []
    for y0 in roots:
        for t in range(tfree):
            out.append(((y0 + step * t) << shift) % mod)
    return out


def solve_quad_mod_2k(a, b, c, k, cap=1 << 16):
    """Tat ca nghiem x mod 2^k cua a*x^2 + b*x + c == 0 (mod 2^k)."""
    if k <= 0:
        return [0]
    mod = 1 << k
    t = min(_ctz(a), _ctz(b), _ctz(c))
    if t >= k:
        return None
    if t > 0:
        subs = solve_quad_mod_2k(a >> t, b >> t, c >> t, k - t, cap)
        if subs is None:
            return None
        step = 1 << (k - t)
        out = []
        for r0 in subs:
            for tt in range(1 << t):
                out.append((r0 + step * tt) % mod)
        return out
    if a % 2 == 0:
        if b % 2 == 0:
            return []
        x0 = c % 2
        cur = [x0] if (a * x0 * x0 + b * x0 + c) % 2 == 0 else []
        for lvl in range(1, k):
            m2 = 1 << lvl
            nxt = []
            for r0 in cur:
                for cand in (r0, r0 + m2):
                    if (a * cand * cand + b * cand + c) % (m2 << 1) == 0:
                        nxt.append(cand)
            cur = nxt
            if not cur:
                return []
        return cur
    inv_a = pow(a, -1, mod)
    Bq = (b * inv_a) % mod
    Cq = (c * inv_a) % mod
    if Bq % 2:
        D = (Bq * Bq - 4 * Cq) % (1 << (k + 2))
        ys = sqrt_mod_2k(D, k + 2, cap)
        out = set()
        for y in ys:
            if (y - Bq) % 2 == 0:
                out.add(((y - Bq) // 2) % mod)
        return sorted(out)
    h = Bq // 2
    D = (h * h - Cq) % mod
    ys = sqrt_mod_2k(D, k, cap)
    return sorted({(y - h) % mod for y in ys})


# ---------------------------------------------------------------------------
# PKCS#1 v1.5
# ---------------------------------------------------------------------------

def pkcs1_pad(msg_bytes, k_bytes, rng):
    """0x00 0x02 || PS (>=8 byte, khac 0) || 0x00 || msg  ->  k_bytes byte."""
    plen = k_bytes - 3 - len(msg_bytes)
    if plen < 8:
        raise ValueError("msg qua dai cho modulus")
    ps = bytes(rng.randrange(1, 256) for _ in range(plen))
    return b"\x00\x02" + ps + b"\x00" + msg_bytes


def pkcs1_unpad(block):
    if block[0:2] != b"\x00\x02":
        raise ValueError("sai dinh dang PKCS#1 v1.5")
    i = block.index(b"\x00", 2)
    return block[i + 1:]


def pkcs1_conforms(int_block, k_bytes):
    """Oracle Bleichenbacher: khoi co dang 0x00 0x02 PS 0x00 M khong."""
    try:
        block = int(int_block).to_bytes(k_bytes, "big")
    except (OverflowError, ValueError):
        return False
    if block[0:2] != b"\x00\x02":
        return False
    idx = block.find(b"\x00", 2)
    return idx >= 10
