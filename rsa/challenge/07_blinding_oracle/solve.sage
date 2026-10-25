from pwn import *
from Crypto.Util.number import *

r = remote("localhost", 1337)
n = int(r.recvline().decode().split(' = ')[1].strip())
e = int(r.recvline().decode().split(' = ')[1].strip())
c = int(r.recvline().decode().split(' = ')[1].strip())

r.recvuntil(b"Text to decrypt: ")
c1 = c * pow(2, e, n)
r.sendline(str(c1).encode())
m = int(r.recvline().decode().split(' = ')[1].strip())
m //= 2
print(long_to_bytes(m))