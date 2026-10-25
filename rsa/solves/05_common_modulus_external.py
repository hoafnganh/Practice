# solve.py — challenge 05: common modulus attack (Extended Euclid)
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
from Crypto.Util.number import long_to_bytes

d = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt")) as f:
    for line in f:
        k, v = line.split("=")
        d[k.strip()] = int(v.strip())
n, e_b, e_c, c_b, c_c = d["n"], d["e_b"], d["e_c"], d["c_b"], d["c_c"]

assert math.gcd(e_b, e_c) == 1
# u*e_b + v*e_c = 1
u = pow(e_b, -1, e_c)
v = (1 - u * e_b) // e_c
assert u * e_b + v * e_c == 1

if u < 0:
    c_b = pow(c_b, -1, n)
    u = -u
if v < 0:
    c_c = pow(c_c, -1, n)
    v = -v
m = (pow(c_b, u, n) * pow(c_c, v, n)) % n
print("FLAG:", long_to_bytes(m).decode())
