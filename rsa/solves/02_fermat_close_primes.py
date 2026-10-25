# solve.py — challenge 02: Fermat factorization
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import gmpy2
from Crypto.Util.number import long_to_bytes

ns = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt")) as f:
    for line in f:
        k, v = line.split("=")
        ns[k.strip()] = int(v.strip())
n, e, c = ns["n"], ns["e"], ns["c"]

a = gmpy2.isqrt(n)
if a * a < n:
    a += 1
steps = 0
while True:
    b2 = a * a - n
    b = gmpy2.isqrt(b2)
    if b * b == b2:
        break
    a += 1
    steps += 1
p = int(a - b)
q = int(a + b)
assert p * q == n
print(f"Fermat tim thay sau {steps} buoc")
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
print("FLAG:", long_to_bytes(pow(c, d, n)).decode())
