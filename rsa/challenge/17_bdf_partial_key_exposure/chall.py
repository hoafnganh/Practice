import sys, os, random, math

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import rsalib as R
from Crypto.Util.number import bytes_to_long

FLAG = "crypto{???}"
rng = random.Random(20260930)

k = R.gen_rsa_key(512, e=3, rng=rng)
n, d = k["n"], k["d"]
S = 176
d_low = d % (1 << S)
m = bytes_to_long(FLAG.encode())
c = pow(m, 3, n)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt"), "w") as f:
    f.write(f"n = {n}\n")
    f.write("e = 3\n")
    f.write(f"d_low = {d_low}   # d mod 2^{S}\n")
    f.write(f"c = {c}\n")
print(f"output.txt written. d bits = {d.bit_length()}, leaked = {S} bit")
