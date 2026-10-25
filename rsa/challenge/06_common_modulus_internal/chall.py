import sys, os, random

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import rsalib as R
from Crypto.Util.number import bytes_to_long

FLAG = "crypto{???}"
rng = random.Random(20260930)

k = R.gen_rsa_key(1024, e=5, rng=rng)
n, phi = k["n"], k["phi"]
e, d = 5, k["d"]
e_boss = 65537
assert __import__("math").gcd(e_boss, phi) == 1
d_boss = pow(e_boss, -1, phi)
m_boss = bytes_to_long(FLAG.encode())
c_boss = pow(m_boss, e_boss, n)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt"), "w") as f:
    f.write(f"n = {n}\n")
    f.write(f"e = {e}\n")
    f.write(f"d = {d}\n")
    f.write(f"e_boss = {e_boss}\n")
    f.write(f"c_boss = {c_boss}\n")
print("output.txt written. n bits =", n.bit_length())
