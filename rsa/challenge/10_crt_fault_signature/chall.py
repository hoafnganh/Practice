import sys, os, random

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import rsalib as R
from Crypto.Util.number import bytes_to_long

FLAG = "crypto{???}"
rng = random.Random(20260930)

k = R.gen_rsa_key(1024, e=65537, rng=rng)
n, p, q, phi, d = k["n"], k["p"], k["q"], k["phi"], k["d"]
e = 65537
dp = pow(e, -1, p - 1)
dq = pow(e, -1, q - 1)
qinv = pow(q, -1, p)

def crt(sp, sq):
    return (sp + p * ((qinv * (sq - sp)) % q)) % n

def sign(m, fault=False):
    sp = pow(m, dp, p)
    sq = pow(m, dq, q)
    if fault:
        sq = (sq + 1) % q
    return crt(sp, sq)

pairs = []
fault_idx = rng.sample(range(8), 3)
for i in range(8):
    m = rng.randrange(2, n)
    s = sign(m, fault=(i in fault_idx))
    pairs.append((i, m, s))

m_flag = bytes_to_long(FLAG.encode())
c = pow(m_flag, e, n)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt"), "w") as f:
    f.write(f"n = {n}\n")
    f.write(f"e = {e}\n")
    for i, m, s in pairs:
        f.write(f"m{i} = {m}\n")
        f.write(f"s{i} = {s}\n")
    f.write(f"c = {c}\n")

