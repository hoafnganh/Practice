from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64decode
from Crypto.Util.Padding import pad
import string

alpha = list(string.ascii_lowercase)
Key1 = 'a1b484aad01c7022'
Key2 = '4094r7p55q9n8s578r'
AES_iv = 'rrBd21CQ6AP4nWKPFj/GsA=='
AES_cipher_text = '3hXI6ZW/VymhzictmbBUJbyQ/BzJhbg56Jgq7OXoJjSSbl/5VdOFabA1LUKcgN9U/3T+Zh7VmVAh3EvGemwJ4hpUsQk99OhZNKo0ipMEiG8='


def dec_cc(data):
    cipher_t = [i for i in range(len(data))]
    for i in range(len(data)):
        ch = data[i]
        if ch in alpha:
            idx = alpha.index(ch)
            cipher_t[i] = alpha[(idx - 13) % 26]
        else:
            cipher_t[i] = ch
    return ''.join(cipher_t)

# print(dec_cc('7p93o619qoo2r71srs'))
cc_p = dec_cc(Key2) # hex(ac_key)[16:]

def dec_rc(data: int):
    n, e = 13119132709177697801, 65537
    p, q = 3671005097, 3573716833
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    return pow(data, d, n)

rc_p = hex(dec_rc(int(Key1, 16)))
# print(rc_p)
ac_key = (rc_p + cc_p)[2:]
# print(type(ac_key))
iv = b64decode(AES_iv)
# print(type(iv))
ct = b64decode(AES_cipher_text)
def dec_ac(data):
    cipher = AES.new(bytes.fromhex(ac_key), AES.MODE_CBC, iv)
    pt = cipher.decrypt(data)
    return pt
print(dec_ac(ct))