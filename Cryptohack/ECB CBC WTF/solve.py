import requests, json
from pwn import *

url = "https://aes.cryptohack.org/ecbcbcwtf"

ciphertext = requests.get(f"{url}/encrypt_flag/").json()["ciphertext"]
print(len(ciphertext))
# 9d7613fc7d8fe8b9bfefce17b91adeed
# fbcb2a93a37d43fadc4b12437d1889eb
# 7d6729a4081f7c540f06f26beb47f015
iv = bytes.fromhex(ciphertext[:32])
b1, b2 = bytes.fromhex(ciphertext[32:64]), bytes.fromhex(ciphertext[64:]) # 2 block
# print(iv.hex(), encrypted)
block1 = requests.get(f"{url}/decrypt/{b1.hex()}").json()["plaintext"]
block1 = bytes.fromhex(block1)
flag1 = xor(block1, iv)
print(flag1)
block2 = requests.get(f"{url}/decrypt/{b2.hex()}").json()["plaintext"]
block2 = bytes.fromhex(block2)
flag2 = xor(block2, b1)
print(flag2)
