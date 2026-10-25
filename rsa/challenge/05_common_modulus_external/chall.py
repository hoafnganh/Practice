import sys, os, random

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import rsalib as R
from Crypto.Util.number import bytes_to_long

FLAG = "crypto{??}"
rng = random.Random(20260930)

k = R.gen_rsa_key(1024, e=17, rng=rng)
n, phi = k["n"], k["phi"]
e_b = 17
e_c = 23
assert __import__("math").gcd(e_b, e_c) == 1
assert __import__("math").gcd(e_c, phi) == 1

m = bytes_to_long(FLAG.encode())
c_b = pow(m, e_b, n)
c_c = pow(m, e_c, n)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt"), "w") as f:
    f.write(f"n = {n}\n")
    f.write(f"e_b = {e_b}\n")
    f.write(f"e_c = {e_c}\n")
    f.write(f"c_b = {c_b}\n")
    f.write(f"c_c = {c_c}\n")
print("output.txt written. n bits =", n.bit_length())
