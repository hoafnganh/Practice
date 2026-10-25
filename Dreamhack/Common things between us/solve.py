from math import gcd
from itertools import combinations
from Crypto.Util.number import long_to_bytes, isPrime

try:
    from gmpy2 import gcd as GCD
except ImportError:
    GCD = gcd

e = 0x10001

with open("output.txt") as f:
    lines = [ln.split() for ln in f.read().split("\n") if ln.strip()]

cts = [int(a) for a, _ in lines]
mods = [int(b) for _, b in lines]
n = len(mods)
print(f"[*] parsed {n} (ct, mod) pairs")

# 1) pairwise batch GCD over all moduli
shared = [[] for _ in range(n)]
for i, j in combinations(range(n), 2):
    g = GCD(mods[i], mods[j])
    if g != 1:
        shared[i].append(int(g))
        shared[j].append(int(g))

# clean 256-bit prime gcds (composites from double-sharing are ~512-bit)
all_g = set()
for lst in shared:
    all_g.update(lst)
primes = {g for g in all_g if g.bit_length() == 256 and isPrime(g)}
print(f"[*] {len(primes)} distinct shared primes (expect 1000), "
      f"{len(all_g) - len(primes)} composite gcds (double-shared pairs)")
assert len(primes) == 1000

# 2) assign each prime to its 4 moduli by direct division
factors = [[] for _ in range(n)]
for p in primes:
    for i in range(n):
        if mods[i] % p == 0:
            factors[i].append(p)

# 3) decrypt everything, XOR as integers -> flag
x = 0
for i in range(n):
    fs = factors[i]
    assert len(fs) == 4, f"modulus {i}: only {len(fs)} factors"
    phi = 1
    for p in fs:
        phi *= p - 1
    d = pow(e, -1, phi)
    x ^= pow(cts[i], d, mods[i])

flag = long_to_bytes(x)
print("[+] FLAG:", flag.decode())
