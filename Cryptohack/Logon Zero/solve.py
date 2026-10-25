from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long
from os import urandom
import json

# nc socket.cryptohack.org 13399

r = remote("socket.cryptohack.org", 13399)


r.recvline()
passwd = (b"\x00" * 29).hex()

payload = json.dumps({"option":"reset_password","token":f"{passwd}"})
r.sendline(payload.encode())
r.recvline()
# data = json.loads(r.recvline())
for i in range(1, 128):
    print("i =", i)
    payload = json.dumps({"option": "authenticate", "password": chr(i) * 9})
    r.sendline(payload.encode())
    # if b"crypto{" in r.recvline():
    print(r.recvline())
