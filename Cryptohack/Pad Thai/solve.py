from pwn import *
import json
re = remote('socket.cryptohack.org', 13421)

re.recvline()
payload = json.dumps({"option": "encrypt"})
re.sendline(payload.encode())

ct = json.loads(re.recvline().decode())["ct"]
# print(ct)
ct = bytes.fromhex(ct)
# iv, ct = ct[:16], ct[16:]
ct = list(ct[i:i + 16] for i in range(0, len(ct), 16))

def check_padding(ct):
    msg = {"option": "unpad", "ct": ct.hex()}
    payload = json.dumps(msg)
    re.sendline(payload.encode())
    return json.loads(re.recvline().decode())['result']

def check_message(msg):
    msg = {"option": "check", "message": msg}
    re.sendline(json.dumps(msg).encode())
    return json.loads(re.recvline().decode())

def loot(b, prev):
    r = b""
    for i in range(15, -1, -1):
        k = 16 - i
        for c in range(256):
            if xor(c, prev[i]) not in b'abcdef0123456789':
                continue
            q = b'\0' * i + xor(bytes([k]), bytes([c]) + r)
            if check_padding(q + b):
                r = bytes([c]) + r
                print(r)
                break
    return r
d1 = loot(ct[1], ct[0])
p1 = xor(d1, ct[0])
# p1 = b"5534f7c4ae69721c"
d2 = loot(ct[2], ct[1])
p2 = xor(d2, ct[1])
# print(p1 + p2)
p = p1 + p2
print(check_message(p.decode()))



