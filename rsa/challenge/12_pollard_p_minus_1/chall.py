import sys, os, random

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import rsalib as R
from Crypto.Util.number import bytes_to_long

FLAG = "crypto{???}"
rng = random.Random(20260930)

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
while True:
    m = 1
    while m.bit_length() < 250:
        m *= primes[rng.randrange(len(primes))] ** rng.randrange(1, 4)
    p = m + 1
    if R.is_probable_prime(p) and p.bit_length() == 251:
        break
q = R.gen_prime(261, rng)
n = p * q
e = 65537
m_flag = bytes_to_long(FLAG.encode())
assert m_flag < n
c = pow(m_flag, e, n)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt"), "w") as f:
    f.write(f"n = {n}\n")
    f.write(f"e = {e}\n")
    f.write(f"c = {c}\n")
print(f"output.txt written. n bits = {n.bit_length()}, p-1 smooth (max prime 97)")
