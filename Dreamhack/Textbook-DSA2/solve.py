from pwn import *
import base64
from Crypto.Util.number import *

re = remote('host3.dreamhack.games', 15425)

re.recvline()
re.recvline()
re.recvline()
re.recvline()
re.recvline()
re.sendline(b"3")

p = int(re.recvline().decode().strip().split(" = ")[1])
q = int(re.recvline().decode().strip().split(" = ")[1])
g = re.recvline().decode().strip().split(" = ")[1]
y = re.recvline().decode().strip().split(" = ")[1]
token = re.recvline().decode().strip().split(" = ")[1][2:-1]

int_token = bytes_to_long(token.encode())
msg = long_to_bytes(int_token + q)

re.sendline(b"1")
re.recvuntil(b"Input message (hex): ")
re.sendline(msg.hex())
line = re.recvline().decode()
r, s = map(int, line[1:-2].split(", "))


re.sendline(b"2")
re.recvuntil(b"Input message (hex): ")
re.sendline((token.encode().hex()).encode())
re.recvuntil(b"Input signagure (r, s as decimal integer): ")
re.sendline(f"{r}, {s}")
print(re.recvall(timeout=15))