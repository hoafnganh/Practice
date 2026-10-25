import sys, os, random, math

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import rsalib as R
from Crypto.Util.number import bytes_to_long

FLAG = "crypto{???}"
rng = random.Random(20260930)


while True:
    p = R.gen_prime(512, rng)
    q = R.gen_prime(512, rng)
    if q < p < 2 * q:
        break
n = p * q
phi = (p - 1) * (q - 1)
while True:
    d = rng.getrandbits(250) | (1 << 249)
    if math.gcd(d, phi) == 1:
        break
e = pow(d, -1, phi)
m = bytes_to_long(FLAG.encode())
c = pow(m, e, n)

n14 = math.isqrt(math.isqrt(n))
assert d < n14 // 3

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt"), "w") as f:
    f.write(f"n = {n}\n")
    f.write(f"e = {e}\n")
    f.write(f"c = {c}\n")
print(f"output.txt written. n={n.bit_length()} bit, d={d.bit_length()} bit (bound ~ {n14.bit_length()} bit), e={e.bit_length()} bit")
