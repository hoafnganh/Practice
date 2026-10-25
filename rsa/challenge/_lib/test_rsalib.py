# -*- coding: utf-8 -*-
"""test_rsalib.py — chay: python test_rsalib.py"""
import math
import random
import sys
import time
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rsalib as R
from Crypto.Util.number import bytes_to_long, long_to_bytes


def test_integer_roots():
    print("== integer_roots ==")
    f = R.poly_mul_int([6, -1], [777, 1])
    f = R.poly_mul_int(f, [-12345, 1])
    roots = R.integer_roots(f, 20000)
    assert set(roots) == {-777, 6, 12345}
    print("  PASS")


def test_wiener():
    print("== Wiener ==")
    rng = random.Random(1)
    k = R.gen_rsa_key(1024, e=65537, rng=rng)
    p, q, n, phi = k["p"], k["q"], k["n"], k["phi"]
    while True:
        d = rng.getrandbits(250) | (1 << 249)
        if math.gcd(d, phi) == 1:
            break
    e = pow(d, -1, phi)
    t0 = time.time()
    res = R.wiener_attack(n, e)
    assert res and res[0] == d and {res[1], res[2]} == {p, q}
    print(f"  ({time.time()-t0:.2f}s) PASS")


def test_poly_gcd():
    print("== Franklin-Reiter poly gcd ==")
    rng = random.Random(2)
    k = R.gen_rsa_key(512, e=3, rng=rng)
    n = k["n"]
    m1 = bytes_to_long(b"crypto{poly_gcd_test}")
    delta = 1
    m2 = m1 + delta
    c1, c2 = pow(m1, 3, n), pow(m2, 3, n)
    g1 = [(-c1 - delta**3) % n, 3 * delta**2, -3 * delta, 1]  # (x-1)^3 - c1
    g2 = [-c2 % n, 0, 0, 1]                                    # x^3 - c2
    h, factor = R.poly_gcd_mod(g1, g2, n)
    assert factor is None and R.poly_deg(h) == 1
    m2_rec = (-h[0] * pow(h[1], -1, n)) % n
    assert m2_rec == m2
    print("  PASS")


def test_pollard_p1():
    print("== Pollard p-1 ==")
    rng = random.Random(3)
    import sympy
    primes = list(sympy.primerange(2, 500))
    while True:
        m = 1
        while m.bit_length() < 116:
            m *= primes[rng.randrange(len(primes))] ** rng.randrange(1, 4)
        p = m + 1
        if R.is_probable_prime(p):
            break
    q = R.gen_prime(128, rng)
    res = R.pollard_p1(p * q, B=20000)
    assert res and res[0] in (p, q)
    print("  PASS")


def test_lll():
    print("== LLL ==")
    from gmpy2 import mpq, mpz

    def gso_full(B):
        n = len(B)
        bstar = []
        mu = [[mpq(0)] * n for _ in range(n)]
        Bnorm = [mpq(0)] * n
        for i in range(n):
            bs = [mpq(mpz(x)) for x in B[i]]
            for j in range(i):
                s = mpq(sum(a * b for a, b in zip(B[i], bstar[j])))
                if Bnorm[j] == 0:
                    mu[i][j] = mpq(0)
                    continue
                mu[i][j] = s / Bnorm[j]
                bs = [a - mu[i][j] * b for a, b in zip(bs, bstar[j])]
            bstar.append(bs)
            Bnorm[i] = mpq(sum(a * a for a in bs))
        return bstar, mu, Bnorm

    def is_lll_reduced(B, delta=mpq(99, 100)):
        n = len(B)
        bstar, mu, Bnorm = gso_full(B)
        for i in range(n):
            for j in range(i):
                if abs(mu[i][j]) > mpq(1, 2):
                    return False, f"size mu[{i}][{j}]"
        for k in range(1, n):
            if Bnorm[k] < (delta - mu[k][k - 1] ** 2) * Bnorm[k - 1]:
                return False, f"lovasz k={k}"
        return True, ""

    import sympy
    rng = random.Random(4)
    for trial in range(5):
        dim = rng.choice([3, 5, 8])
        bits = rng.choice([20, 64, 128])
        B = [[rng.getrandbits(bits) - (1 << (bits - 1)) for _ in range(dim)]
             for _ in range(dim)]
        for i in range(dim):
            B[i][i] += (1 << bits)
        det_before = sympy.Matrix(B).det()
        t0 = time.time()
        Bl = R.lll(B)
        dt = time.time() - t0
        det_after = sympy.Matrix(Bl).det()
        ok, why = is_lll_reduced(Bl)
        print(f"  dim={dim} bits={bits}: {dt:.2f}s det_ok={abs(det_before) == abs(det_after)} "
              f"lll_reduced={ok} {why}")
        assert abs(det_before) == abs(det_after)
        assert ok, why
    print("  PASS")


def test_coppersmith():
    print("== Coppersmith stereotyped (known prefix, e=3) ==")
    rng = random.Random(5)
    k = R.gen_rsa_key(512, e=3, rng=rng)
    n = k["n"]
    flag = b"crypto{c0pp3rsm1th_w0rks}"
    u = 40
    K = bytes_to_long(flag) << u
    x0 = rng.getrandbits(u)
    M = K + x0
    c = pow(M, 3, n)
    f = [(K**3 - c) % n, (3 * K * K) % n, (3 * K) % n, 1]
    t0 = time.time()
    roots = R.coppersmith_small_roots(f, n, 1 << u, m=4, t=2)
    assert x0 in roots
    print(f"  ({time.time()-t0:.2f}s) PASS")


def test_coppersmith_known_high_bits():
    print("== Coppersmith known high bits of p ==")
    rng = random.Random(6)
    k = R.gen_rsa_key(512, e=65537, rng=rng)
    p, n = k["p"], k["n"]
    u = 116
    p_high = p >> u
    res = R.coppersmith_known_high_bits(n, p_high, u, m=8, t=8)
    assert res == [p]
    print("  PASS")


def test_quad_mod_2k():
    print("== solve_quad_mod_2k ==")
    rng = random.Random(99)
    for trial in range(300):
        k = rng.randrange(1, 13)
        mod = 1 << k
        a = rng.randrange(0, 64)
        b = rng.randrange(0, 64)
        c = rng.randrange(0, 64)
        got = R.solve_quad_mod_2k(a, b, c, k)
        if got is None:
            continue
        expect = {x for x in range(mod) if (a * x * x + b * x + c) % mod == 0}
        assert set(got) == expect, f"k={k} a={a} b={b} c={c}"
    # truong hop BDF: k·p² + (ed−kN−k−1)p + kN ≡ 0 (mod 2^s)
    rng2 = random.Random(7)
    k = R.gen_rsa_key(256, e=3, rng=rng2)
    n, p, d3 = k["n"], k["p"], k["d"]
    s = 48
    dl = d3 % (1 << s)
    found = False
    for kk in (1, 2, 3):
        bb = 3 * dl - kk * n - kk - 1
        roots = R.solve_quad_mod_2k(kk, bb, kk * n, s)
        if roots is not None and p % (1 << s) in roots:
            found = True
            break
    assert found
    print("  PASS")


def test_pkcs1():
    print("== pkcs1 ==")
    rng = random.Random(5)
    blk = R.pkcs1_pad(b"crypto{test_flag}", 64, rng)
    assert len(blk) == 64 and blk[0:2] == b"\x00\x02"
    assert R.pkcs1_unpad(blk) == b"crypto{test_flag}"
    assert R.pkcs1_conforms(int.from_bytes(blk, "big"), 64)
    assert not R.pkcs1_conforms(int.from_bytes(b"\x00\x01" + b"\xff" * 62, "big"), 64)
    print("  PASS")


if __name__ == "__main__":
    test_integer_roots()
    test_wiener()
    test_poly_gcd()
    test_pollard_p1()
    test_lll()
    test_coppersmith()
    test_coppersmith_known_high_bits()
    test_quad_mod_2k()
    test_pkcs1()
    print("ALL TESTS PASSED")
