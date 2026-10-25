from pwn import *
from Crypto.Util.number import *
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
import hashlib

g = 2
r = remote("host3.dreamhack.games", 23122)
Prime = int(r.recvline().decode().split(": ")[1].strip(), 16)

# r.recvuntil(b"Alice sends her key to Bob. Key: ")
alice_k = int(r.recvline().decode().split(": ")[1].strip(), 16)
r.recvline()

r.recvuntil(b">> ")
c = getPrime(1024)

r.sendline(str(pow(g, c, Prime)).encode())
# r.sendline("123".encode())
bob_k = int(r.recvline().decode().split(": ")[1].strip(), 16)
r.recvline()

r.recvuntil(b">> ")
r.sendline(str(pow(g, c, Prime)).encode())
# r.sendline("123".encode())

r.recvline()
flag1 = r.recvline().decode().strip().split(": ")[1]
flag2 = r.recvline().decode().strip().split(": ")[1]

cipher = AES.new(hashlib.md5(str(pow(alice_k, c, Prime)).encode()).digest(), AES.MODE_ECB)
# cipher = AES.new(hashlib.md5("123".encode()).digest(), AES.MODE_ECB)
pt1 = cipher.decrypt(bytes.fromhex(flag1))
print(pt1)
cipher = AES.new(hashlib.md5(str(pow(bob_k, c, Prime)).encode()).digest(), AES.MODE_ECB)
pt2 = cipher.decrypt(bytes.fromhex(flag2))
print(pt2)