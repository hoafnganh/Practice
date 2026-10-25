from pwn import *

context.log_level = 'error'
r = remote('localhost', 4000)

r.recvuntil(b'encrypted flag: ')
flag_line = r.recvline()
print('flag_line len:', len(flag_line), 'tail:', repr(flag_line[-5:]))
ct = bytes.fromhex(flag_line.decode())
print('ct len:', len(ct))

r.recvuntil(b'enter your text: ')
r.sendline(b'123')
r.recvuntil(b'your ciphertext: ')
enc_line = r.recvline()
print('enc_line len:', len(enc_line), 'full:', repr(enc_line))

enc_full = bytes.fromhex(enc_line.decode())
print('enc_full len:', len(enc_full))
msg = enc_full[:3]
ks = xor(b'123', msg)
print('ks[:3]:', ks.hex())
print('flag[:3] =', xor(ct[:3], ks))
