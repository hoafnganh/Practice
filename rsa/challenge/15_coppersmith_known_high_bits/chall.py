import sys, os, random

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import rsalib as R
from Crypto.Util.number import bytes_to_long

FLAG = "crypto{???}"
rng = random.Random(20260930)

k = R.gen_rsa_key(512, e=65537, rng=rng)
n, p = k["n"], k["p"]
U = 116
p_high = p >> U
assert p == (p_high << U) + (p - (p_high << U))
m = bytes_to_long(FLAG.encode())
c = pow(m, 65537, n)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt"), "w") as f:
    f.write(f"n = {n}\n")
    f.write("e = 65537\n")
    f.write(f"p_high = {p_high}   # 140 bit cao nhat cua p (p co 256 bit)\n")
    f.write(f"c = {c}\n")
print(f"output.txt written. n bits = {n.bit_length()}, p bits = {p.bit_length()}, unknown = {U} bit")
