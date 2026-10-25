# "Not too weak" — semi-weak DES key pair cancels the secret IV whitening
# c_i = E_k(m_i ^ IV) ^ IV ; semi-weak pair (a,b): E_a(E_b(x)) = x
#   step 1: option 2, key A      -> c* = E_A(pad(flag) ^ IV) ^ IV
#   step 2: option 1, key B, c*  -> out[i] = E_B(c*_i ^ IV) ^ IV = pad(flag)_i  (IV cancels)
import socket
from Crypto.Util.Padding import unpad

HOST, PORT = "host3.dreamhack.games", 23079

A = b'01FE01FE01FE01FE'   # semi-weak pair
B = b'FE01FE01FE01FE01'

s = socket.create_connection((HOST, PORT), timeout=15)
f = s.makefile('rwb')

def recv_until(tok):
    buf = b''
    while not buf.endswith(tok):
        ch = f.read(1)
        if not ch:
            raise EOFError(buf)
        buf += ch
    return buf

# option 2: encrypt flag with A
recv_until(b'> ')
f.write(b'2\n'); f.flush()
recv_until(b'key(hex)> ')
f.write(A + b'\n'); f.flush()
recv_until(b'enc_flag(hex)> ')
c_star = bytes.fromhex(f.readline().strip().decode())
print(f'[+] enc_flag ({len(c_star)}B): {c_star.hex()}')

# option 1: encrypt c* with B
recv_until(b'> ')
f.write(b'1\n'); f.flush()
recv_until(b'key(hex)> ')
f.write(B + b'\n'); f.flush()
recv_until(b'msg(hex)> ')
f.write(c_star.hex().encode() + b'\n'); f.flush()
recv_until(b'enc(hex)> ')
out = bytes.fromhex(f.readline().strip().decode())

# out = pad(flag) || garbage_padding_block
flag = unpad(out[:len(c_star)], 8)
print(f'[+] FLAG: {flag.decode()}')
s.close()
