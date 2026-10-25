import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import rsalib as R
from Crypto.Util.number import bytes_to_long

try:
    import gmpy2
    def _dec(x):
        return int(gmpy2.powmod(x, d, n))
except ImportError:
    def _dec(x):
        return pow(x, d, n)

SECRET = b"crypto{???}"


rng = random.Random(20260930)
while True:
    p = R.gen_prime(64, rng)
    q = R.gen_prime(64, rng)
    if (p % 3) != 1 and (q % 3) != 1 and p != q:
        break
n = p * q
e = 3
d = pow(e, -1, (p - 1) * (q - 1))

K = 16

padded = b"\x00\x02" + b"\xAB" + b"\x00" + SECRET
m = bytes_to_long(padded)
ct = pow(m, e, n)


def oracle(x):
    dec = _dec(int(x))
    block = dec.to_bytes(K, "big")
    return block[0:2] == b"\x00\x02"


if __name__ == "__main__":
    print(f"n  = {n}")
    print(f"e  = {e}")
    print(f"ct = {ct}")
