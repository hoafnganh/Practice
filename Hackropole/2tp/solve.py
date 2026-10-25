from pwn import *

r = remote('localhost', 4000)

r.recvuntil(b"As an example, here is the encrypted flag: ")
ct = bytes.fromhex(r.recvline().decode())
r.recvuntil(b"Now, enter your text: ")
r.sendline(b"a" * 50)
# 0f140d293dc658f59502e710a2175264d7b69e
r.recvuntil(b"Here is your ciphertext: ")
# print(r.recvline().decode()[:-33])
enc = bytes.fromhex(r.recvline().decode())

flag = xor(ct, bytes([ord('a') ^ x for x in enc]))
print(flag)