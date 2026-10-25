from Crypto.Cipher import AES
from pwn import *
import string
ct = "fe000000000000000000000000009ec3307df037c689300bbf2812ff89bc0b49"
# 307df037c689300bbf2812ff89bc0b49
msg = b"The message is protected by AES!"
last_block = "307df037c689300bbf2812ff89bc0b49"
# print(len(msg))
alpha = string.printable
def encrypt(message, passphrase):
    aes = AES.new(passphrase, AES.MODE_CBC, IV)
    return aes.encrypt(message)

def decrypt(message, passphrase):
    aes = AES.new(passphrase, AES.MODE_CBC, IV)
    return aes.decrypt(message)

key = b"5d6I9pfR7C1JQt"
IV = b"\x00" * 16
found = False
# print(msg[16:]) # b'rotected by AES!'
for i in alpha:
    for j in alpha:
        key += (i + j).encode()
        # print(key)
        data = decrypt(bytes.fromhex(last_block), key)
        ct0 = xor(data, b"rotected by AES!")
        if "fe" in ct0.hex() and "9ec3" in ct0.hex():
            found = True
            break
        key = b"5d6I9pfR7C1JQt"
    if found: break
    

print(key)
print(ct0)

ct00 = decrypt(ct0, key)
IV = xor(ct00, b"The message is p")
print(IV)

