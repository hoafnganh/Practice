# -*- coding: utf-8 -*-
"""gen.py — L12: Bleichenbacher ban lattice — thu 60 r hop le (N 512-bit, e=3).

Oracle: O(c') = 1 neu ban ro cua c' bat dau 00 02. Vi gen co m nen mo phong
oracle bang cach kiem tra truc tiep 2B <= r*m mod N < 3B.
"""
import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "_lib"))
import latlib as L  # noqa: E402
import gmpy2  # noqa: E402

rng = random.Random(20260112)
p = L.gen_prime(256, rng)
q = L.gen_prime(256, rng)
N = p * q
e = 3
FLAG = b"crypto{bl31ch3nb4ch3r_4s_hnp}"
k_bytes = 64
pad_len = k_bytes - 3 - len(FLAG)
ps = bytes(rng.randrange(1, 256) for _ in range(pad_len))
block = b"\x00\x02" + ps + b"\x00" + FLAG
m = L.bytes_to_long(block)
assert m < N
c = pow(m, e, N)

B = 1 << (512 - 16)
mG, NG = gmpy2.mpz(m), gmpy2.mpz(N)
twoB, threeB = 2 * B, 3 * B

rs = []
tried = 0
while len(rs) < 60:
    tried += 1
    r = rng.getrandbits(512) % N        # r phai ngau nhien that su —
    # neu lay r lien tiep thi cac quan he phu thuộc nhau, lattice suy bien
    x = (gmpy2.mpz(r) * mG) % NG
    if twoB <= x < threeB:
        rs.append(r)
nonce, ct = L.aes_encrypt_flag(FLAG, m, rng)
with open("output.txt", "w") as f:
    f.write(f"N = {N}\ne = 3\nc = {c}\n")
    f.write("r = " + "\n    ".join(map(str, rs)) + "\n")
    f.write(f"nonce = {nonce.hex()}\nct = {ct.hex()}\n")
print("gen ok, tried:", tried, "rs:", len(rs))
