import sys, os, random

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import rsalib as R
from Crypto.Util.number import bytes_to_long

FLAG = "crypto{???}"
rng = random.Random(20260930)

k = R.gen_rsa_key(1024, e=3, rng=rng)
n, phi, d = k["n"], k["phi"], k["d"]
m = bytes_to_long(FLAG.encode())
assert m ** 3 < n
c = pow(m, 3, n)
assert c == m ** 3

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt"), "w") as f:
    f.write(f"n = {n}\n")
    f.write(f"e = 3\n")
    f.write(f"c = {c}\n")
print("output.txt")
