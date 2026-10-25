from Crypto.Util.number import *
from pwn import *
context.log_level = 'error'
r = remote("localhost", 1337)
n = int(r.recvline().decode().split(' = ')[1])
e = int(r.recvline().decode().split(' = ')[1])
c = int(r.recvline().decode().split(' = ')[1])

# print(n, e, c)
def send(c):
    r.recvuntil(b"> ")
    r.sendline(str(c).encode())
    return r.recvline().decode().strip()
c2e = pow(2, e, n)
ub, lb = n, 0
ct = c
for i in range(n.bit_length() + 8):
    ct = (ct * c2e) % n
    mid = (lb + ub) // 2
    # print("i =", i)
    if send(ct) == "Even":
        ub = mid
    else: lb = mid
for m in range(lb - 128, ub + 128):
    if pow(m, e, n) == c:
        print(m)
        print(long_to_bytes(m))
        break
# print(long_to_bytes(m))
# print(send(123))