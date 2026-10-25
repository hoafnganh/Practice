import sys, os, random

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import rsalib as R
from Crypto.Util.number import bytes_to_long

FLAG = "crypto{???}"
rng = random.Random(20260930)


base = rng.getrandbits(512) | (1 << 511) | 1
p = R.gen_prime_near(base, rng)
q = R.gen_prime_near(base + (1 << 260), rng)
assert p != q
n = p * q
e = 65537
m = bytes_to_long(FLAG.encode())
assert m < n
c = pow(m, e, n)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt"), "w") as f:
    f.write(f"n = {n}\n")
    f.write(f"e = {e}\n")
    f.write(f"c = {c}\n")
print("output.txt written. n bits =", n.bit_length())
