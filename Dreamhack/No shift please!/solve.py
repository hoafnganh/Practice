from pwn import *
from Crypto.Util.number import *

r = remote("host3.dreamhack.games", 16895)

enc = r.recvline().decode().split(" = ")[1]
enc = bytes.fromhex(enc)
r.recvuntil(b"[1] encrypt, [2] decrypt: ")
r.sendline(b"2")
r.recvuntil(b"Input ciphertext to decrypt in hex: ")
secret = bytearray(16)

d1 = bytearray(enc)
d1[4] ^= 1
data = bytes(d1)
r.sendline(data.hex().encode())
out = r.recvline().decode().split(" = ")[1]
out = bytes.fromhex(out)
for i in (0, 1, 2, 3, 8, 9, 10, 11, 12, 13, 14, 15):
    secret[i] = out[i]

r.recvuntil(b"[1] encrypt, [2] decrypt: ")
r.sendline(b"2")
r.recvuntil(b"Input ciphertext to decrypt in hex: ")
d1 = bytearray(enc)
d1[0] ^= 1
data = bytes(d1)
r.sendline(data.hex().encode())
out = r.recvline().decode().split(" = ")[1]
out = bytes.fromhex(out)
for i in (4, 5, 6, 7):
    secret[i] = out[i]
secret = bytes(secret)
r.recvuntil(b"[1] encrypt, [2] decrypt: ")
r.sendline(b"1")
r.recvuntil(b"Input plaintext to encrypt in hex: ")
r.sendline(secret.hex().encode())
print(r.recvall(timeout=5).decode())