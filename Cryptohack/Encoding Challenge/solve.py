import base64
import codecs
import random
import json
from pwn import *
from Crypto.Util.number import *
# nc socket.cryptohack.org 13377
r = remote("socket.cryptohack.org", 13377)

for i in range(100):
    data = r.recvline()
    print(f"Lượt thứ {i}", data)
    enc = json.loads(data.decode().strip())
    enc_type = enc["type"] # str
    ct = enc["encoded"] # str
    if enc_type == "rot13":
        pt = codecs.decode(ct, 'rot13')
    elif enc_type == "base64":
        pt = base64.b64decode(ct).decode()
    elif enc_type == "hex":
        pt = bytes.fromhex(ct).decode()
    elif enc_type == "bigint":
        pt = long_to_bytes(int(ct, 16)).decode()
    else:
        pt = "".join(chr(b) for b in ct)
    payload = json.dumps({"decoded": f"{pt}"})
    r.sendline(payload.encode())
print(r.recvline().decode().strip())

