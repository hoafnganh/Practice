# nc host3.dreamhack.games 18028
from pwn import *
from Crypto.Util.number import *

re = remote("host3.dreamhack.games", 18028)

N = int(re.recvline().decode())
ct = int(re.recvline().decode())
e = 0x10001
WORDS = {b"Null\n": 0, b"Eins\n": 1, b"Zwei\n": 2, b"Drei\n": 3}
A, P = 0, 1
for i in range(513):
    inp = ct * pow(4, i * e, N) % N
    re.recvuntil(b"> ")
    re.sendline(str(inp).encode())
    a = WORDS[re.recvline()]
    print("i =", i)
    A = 4 * A + a
    P *= 4

m = -(-N * A // P)
re.sendlineafter(b"> ", str(m).encode())     # chờ prompt 514 rồi mới gửi — chắc chắn server đang đứng ở input()

data = re.recvall(timeout=15)
print(data)                                   # in byte thô, đừng decode trước khi nhìn

