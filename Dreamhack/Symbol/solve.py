from pwn import *
from Crypto.Util.number import *
r = remote("host3.dreamhack.games", 12356)

p = int(r.recvline().decode().split(" = ")[1])
ks = []
for i in range(64):
    ks.append(int(r.recvline().decode()))

r.recvuntil(b"> ")

token = 0
for i, k in enumerate(ks):
    bit = 1 if pow(k, (p - 1) // 2, p) == p - 1 else 0
    token |= bit << i

print(token)
r.sendline(str(token).encode())
print(r.recvall(timeout=5))
