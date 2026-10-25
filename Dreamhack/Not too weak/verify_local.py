# Local verification: semi-weak key pair cancels the secret IV whitening
# scheme: c_i = E_k(m_i ^ IV) ^ IV ; semi-weak pair (a,b): E_a(E_b(x)) = E_b(E_a(x)) = x
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import os

IV = os.urandom(8)
FLAG = open('flag', 'rb').read()

def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def encrypt(k, m):
    cipher = DES.new(k, mode=DES.MODE_ECB)
    m = pad(m, 8)
    m = xor(m, IV * (len(m) // 8))
    c = cipher.encrypt(m)
    c = xor(c, IV * (len(c) // 8))
    return c

# one of the 6 semi-weak pairs
A = bytes.fromhex('01FE01FE01FE01FE')
B = bytes.fromhex('FE01FE01FE01FE01')

# sanity: semi-weak property actually holds for this pair
x = os.urandom(8)
assert DES.new(A, DES.MODE_ECB).encrypt(DES.new(B, DES.MODE_ECB).encrypt(x)) == x

# attack: two different keys, each used exactly once
c_star = encrypt(A, FLAG)          # option 2: encrypt flag with A
out = encrypt(B, c_star)           # option 1: encrypt c* with B
recovered = unpad(out[:len(c_star)], 8)

print('IV (unknown to attacker):', IV.hex())
print('recovered == FLAG:', recovered == FLAG)
print(recovered)
