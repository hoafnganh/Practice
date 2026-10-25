from Crypto.Util.number import *

e = 0x10001

ciphertexts = []
mods = []
with open("output.txt", "r") as f:
    for _ in range(1000):
        ct, mod = map(int, f.readline().strip().split(" "))
        ciphertexts.append(ct)
        mods.append(mod)
# print(mods)
# print(type(ciphertexts[0]))
# print(type(mods[0]))
chung = [[] for _ in range(1000)]
for i, j in Combinations(1000, 2):
    g = gcd(mods[i], mods[j])
    if g != 1:
        chung[i].append(g)
        chung[j].append(g)

all_g = set()
for lst in chung:
    all_g.update(lst)
primes = {g for g in all_g if g.bit_length() == 256 and is_prime(g)}
# print(is_prime(1000))

factors = [[] for _ in range(1000)]
for p in primes:
    for i in range(1000):
        if mods[i] % p == 0:
            factors[i].append(p)

x = 0
for i in range(1000):
    phi = 1
    for p in factors[i]:
        phi *= p - 1
    d = pow(e, -1, phi)
    pt = pow(ciphertexts[i], d, mods[i])
    x ^^= pt
print(long_to_bytes(x))