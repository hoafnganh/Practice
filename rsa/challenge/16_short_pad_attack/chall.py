import sys, os, random

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import rsalib as R
from Crypto.Util.number import bytes_to_long

FLAG = "crypto{???}"
rng = random.Random(20260930)

k = R.gen_rsa_key(512, e=3, rng=rng)
n = k["n"]

PADBITS = 32
r1 = rng.getrandbits(PADBITS)
r2 = rng.getrandbits(PADBITS)
while r1 == r2:
    r2 = rng.getrandbits(PADBITS)
M1 = (bytes_to_long(FLAG.encode()) << PADBITS) | r1
M2 = (bytes_to_long(FLAG.encode()) << PADBITS) | r2
assert M1 < n and M2 < n
c1 = pow(M1, 3, n)
c2 = pow(M2, 3, n)
assert M1 ** 3 > n

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt"), "w") as f:
    f.write(f"n = {n}\n")
    f.write("e = 3\n")
    f.write(f"c1 = {c1}\n")
    f.write(f"c2 = {c2}\n")
    f.write("# M_i = (msg << 32) | r_i  — 32 bit pad ngau nhien o cuoi\n")
print(f"output.txt written. r1 = {r1}, r2 = {r2} (bi mat), M1 bits = {M1.bit_length()}")
