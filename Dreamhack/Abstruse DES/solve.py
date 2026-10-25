from pwn import *
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad

r = remote("host3.dreamhack.games", 22176)

r.recvuntil(b"> ")
r.sendline(b"3")
ct = r.recvline().decode().split('> ')[1]
r.recvuntil(b"> ")
r.sendline(b"2")
r.recvline()
r.sendline(b"1 1 1 1 1 1 1 1")
r.recvuntil(b"> ")
r.sendline(ct.encode())
flag = r.recvline().decode().split('> ')[1]
print(bytes.fromhex(flag))