import json
from Crypto.Util.number import *
import owiener

with open("output.txt", "r") as f:
    data = json.loads(f.read())
    e = int(data["e"])
    n = int(data["n"])
    c = int(data["c"])

# print(n, e, c)

d = owiener.attack(e, n)
# print(d)
print(long_to_bytes(pow(c, d, n)))