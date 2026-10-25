from pwn import *
from Crypto.Util.number import *
from xtp import key_gen

def dec2bin(p):
    plist = ['0b']
    for ch in p:
        plist.append(format(ord(ch), 'b').zfill(8))
    binp = "".join(plist)
    return binp # str


r = remote("host3.dreamhack.games", 8893)

flag_enc = r.recvline().decode().split(": ")[1]
# print(type(flag_enc)) # str

p = b"1" * 64
# print(p)
r.recvuntil(b"Plain text : ")
r.sendline(p)
input_enc = r.recvline().decode().strip().split(": ")[1]
# print(input_enc)
# print(type(input_enc)) #str
input_enc = int(input_enc, 10)
# print(type(input_enc))
# print(type(int('0b0101', 2)))

plist = ['0b']
for ch in p.decode():
    plist.append(format(ord(ch), 'b').zfill(8))
binp = "".join(plist)
# print(type(binp)) # str
n_key = input_enc ^ int(binp, 2)
# print(n_key)# decimal
# print(n_key)
print(type(bin(n_key)))
o_key = key_gen(bin(n_key))
pt = int(flag_enc, 2) ^ int(o_key, 2)
# pt = int(pt[2:], 2)
print(type(pt)) # str
print(long_to_bytes(pt))