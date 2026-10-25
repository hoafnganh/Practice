from pwn import *
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad

r = remote("host3.dreamhack.games", 16454)
def enc_msg(key, msg):
    r.recvuntil(b"> ")
    r.sendline(b"1")
    r.recvuntil(b"key(hex)> ")
    
    r.sendline(key)
    r.recvuntil(b"msg(hex)> ")
    
    r.sendline(msg)
    enc = r.recvline().decode().split("> ")[1]
    return enc
def enc_flag(key):
    r.recvuntil(b"> ")
    r.sendline(b"2")
    r.recvuntil(b"key(hex)> ")
    r.sendline(key)
    enc = r.recvline().decode().split("> ")[1]
    return enc
key1 = b"011F011F010E010E"
key2 = b"1F011F010E010E01"
enc = enc_flag(key1)
# print(enc)
pt = bytes.fromhex(enc_msg(key2, enc))
print(pt)