from Crypto.Util.number import getPrime
import random

p,q = getPrime(512),getPrime(512)
N = p*q
e = 0x10001
d = pow(e,-1,(p-1)*(q-1))
print(N)

m = random.randrange(N)
print(pow(m,e,N))

while True:
    inp = int(input("> "))
    if m == inp:
        print("Interesting...")
        break
    pt = pow(inp,d,N)
    print(4*pt//N)
    print(["Null","Eins","Zwei","Drei"][4*pt//N])

print(open("flag","r").read().strip())