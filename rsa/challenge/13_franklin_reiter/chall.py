import sys, os, random

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import rsalib as R
from Crypto.Util.number import bytes_to_long

FLAG = "crypto{???}"
rng = random.Random(20260930)

k = R.gen_rsa_key(1024, e=3, rng=rng)
n = k["n"]

M1 = bytes_to_long(FLAG.encode() + (1).to_bytes(4, "big"))
M2 = bytes_to_long(FLAG.encode() + (2).to_bytes(4, "big"))
assert M2 == M1 + 1
c1 = pow(M1, 3, n)
c2 = pow(M2, 3, n)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt"), "w") as f:
    f.write(f"n = {n}\n")
    f.write("e = 3\n")
    f.write(f"c1 = {c1}\n")
    f.write(f"c2 = {c2}\n")
print("output.txt")
