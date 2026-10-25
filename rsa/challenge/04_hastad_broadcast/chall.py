import sys, os, random

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import rsalib as R
from Crypto.Util.number import bytes_to_long

FLAG = "crypto{???}"
rng = random.Random(20260930)

m = bytes_to_long(FLAG.encode())
assert m.bit_length() < 1000

ns, cs = [], []
for i in range(3):
    k = R.gen_rsa_key(1024, e=3, rng=rng)
    ns.append(k["n"])
    cs.append(pow(m, 3, k["n"]))

import math
assert math.gcd(ns[0], ns[1]) == 1 and math.gcd(ns[0], ns[2]) == 1 and math.gcd(ns[1], ns[2]) == 1
assert m ** 3 < min(ns)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt"), "w") as f:
    for i in range(3):
        f.write(f"n{i+1} = {ns[i]}\n")
    f.write("e = 3\n")
    for i in range(3):
        f.write(f"c{i+1} = {cs[i]}\n")
print("output.txt written")
