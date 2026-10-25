from pwn import *
import json

# nc socket.cryptohack.org 11112
r = remote("socket.cryptohack.org", 11112)

payload = json.dumps({"buy":"flag"}).encode()
r.recvline()
r.recvline()
r.recvline()
r.recvline()
r.sendline(payload)
print(r.recvline())