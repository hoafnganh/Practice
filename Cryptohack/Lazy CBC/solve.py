from Crypto.Util.number import *
from Crypto.Cipher import AES
import requests, json, os

url = "https://aes.cryptohack.org/lazy_cbc"

# p0 = key ^ D(c0)
# p1 = c0 ^ D(c1)
# p2 = c1 ^ D(c2) = D(c2) = D(c0)
# key = p2 ^ p0

def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))
pt = "e729da8cc71e509b4e210568dc605a21b15de3ec9259b70b09d3b8a2b4063af82100b80ca60d3432f7a73049909e0d02"
def encrypt(pt):
    data = requests.get(f"{url}/encrypt/{pt}").json()
    ct = data["ciphertext"]
    return ct
def receive(ct):
    c0 = ct[:32]
    data = requests.get(f"{url}/receive/{c0 + "00" * 16 + c0}").json()
    res = data["error"]
    return res

def get_flag(key):
    data = requests.get(f"{url}/get_flag/{key}").json()
    pt = data["plaintext"]
    return bytes.fromhex(pt).decode()
print(pt) # e729da8cc71e509b4e210568dc605a21b15de3ec9259b70b09d3b8a2b4063af82100b80ca60d3432f7a73049909e0d02
ct = encrypt(pt) # 04f9d8f96dbacada5bc6c0245ade5c8138908b08681ab694d697686b9480be1047b1692b9650e702a0a5fbff7d60c174
print(ct)
decrypted = receive(ct)
print(decrypted)
# e729da8cc71e509b4e210568dc605a21a05b109bdf92146e4c0e338bfab79dd1310541b8d23fa51bb31ec441f54ae80c
dec = decrypted.split(": ")[1]
print(dec)
key = xor(bytes.fromhex(dec[:32]), bytes.fromhex(dec[-32:])).hex()
# print(key)
print(get_flag(key))

