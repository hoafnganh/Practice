# solve.py — challenge 03: can bac ba nguyen
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import gmpy2
from Crypto.Util.number import long_to_bytes

ns = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt")) as f:
    for line in f:
        k, v = line.split("=")
        ns[k.strip()] = int(v.strip())
n, e, c = ns["n"], ns["e"], ns["c"]

m, exact = gmpy2.iroot(c, e)
assert exact, "can khong chinh phuong — m^3 da bi mod roi"
print("FLAG:", long_to_bytes(int(m)).decode())
