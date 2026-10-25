import sys, os, random, math

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import rsalib as R
from Crypto.Util.number import bytes_to_long

FLAG = "crypto{???}"
rng = random.Random(20260930)

while True:
    p = R.gen_prime(512, rng)
    while True:
        dp = rng.getrandbits(20) | 1
        if math.gcd(dp, p - 1) == 1:
            break
    e = pow(dp, -1, p - 1)
    q = R.gen_prime(512, rng)
    phi = (p - 1) * (q - 1)
    if math.gcd(e, phi) == 1 and math.gcd(e, q - 1) == 1 and e.bit_length() > 500:
        break
n = p * q
d = pow(e, -1, phi)
assert d % (p - 1) == dp

m = bytes_to_long(FLAG.encode())
c = pow(m, e, n)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt"), "w") as f:
    f.write(f"n = {n}\n")
    f.write(f"e = {e}\n")
    f.write(f"c = {c}\n")
print(f"output.txt written.")
