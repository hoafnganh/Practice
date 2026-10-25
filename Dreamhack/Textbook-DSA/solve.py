from pwn import *
from Crypto.Util.number import *
from hashlib import sha1

r = remote("host3.dreamhack.games", 13725)
# context.log_level = "debug"
# print(r.recvline())
# print(r.recvline())
# print(r.recvline())
# print(r.recvline())
r.recvline()
r.recvline()
r.recvline()
r.recvline()
# Nhận thông tin
r.sendline(b"3")
p = int(r.recvline().decode().split(' = ')[1])
q = int(r.recvline().decode().split(' = ')[1])
g = int(r.recvline().decode().split(' = ')[1])
y = int(r.recvline().decode().split(' = ')[1])
token = r.recvline().decode().strip().split(' = ')[1][2:-1]
print(token)
r.recvline()
r.recvline()
r.recvline()
# Kí "a"
r.sendline(b"1")
r.recvuntil(b"Input message (hex): ")
r.sendline(b"61")
line = (r.recvline().decode().strip())
Ra, sa = map(int, line[1:-1].split(', '))
# print(R, s)
ha = bytes_to_long(sha1(bytes.fromhex("61")).digest())
r.recvline()
r.recvline()
r.recvline()
# Kí "b"
r.sendline(b"1")
r.recvuntil(b"Input message (hex): ")
r.sendline(b"62")
line = (r.recvline().decode().strip())
Rb, sb = map(int, line[1:-1].split(', '))
# print(R, s)
hb = bytes_to_long(sha1(bytes.fromhex("62")).digest())
# Tìm x
x = (sa - sb) * inverse(ha - hb, q) % q
h = bytes_to_long(sha1(token.encode()).digest())
k_ = 1
r_ = pow(g, k_, p) % q
s_ = inverse(k_, q) * (h + x * r_) % q

r.recvline()
r.recvline()
r.recvline()

r.sendline(b"2")
r.recvuntil(b": ")
r.sendline(token.encode().hex())
r.recvuntil(b": ")
r.sendline(f"{r_}, {s_}".encode())
print(r.recvall(timeout=5).decode())

