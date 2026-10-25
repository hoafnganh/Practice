from Crypto.Util.number import getPrime, GCD
import os
import random

random.seed(os.urandom(10))

with open("flag", "rb") as f:
    flag = f.read()

assert 1 < len(flag) < 128

plaintexts = [os.urandom(len(flag)) for _ in range(999)]
print(len(plaintexts))
last_pt = list(flag)
for i in range(999):
    for j in range(len(flag)):
        last_pt[j] ^= plaintexts[i][j]
plaintexts.append(bytes(last_pt))
print(len(plaintexts))

mods = [[] for _ in range(1000)]
select = list(range(1000))

e = 0x10001
for _ in range(1000):
    while True:
        prime = getPrime(256)
        if GCD(e, prime - 1) == 1:
            break

    random.shuffle(select)
    choices = select[:4]
    
    for ch in choices:
        mods[ch].append(prime)
        if len(mods[ch]) == 4:
            select.remove(ch)

mods = [a[0] * a[1] * a[2] * a[3] for a in mods]


for pt, mod in zip(plaintexts, mods):
    pt = int.from_bytes(pt, "big")
    ct = pow(pt, e, mod)

    print(ct, mod)
