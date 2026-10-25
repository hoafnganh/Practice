import requests, json, string

alpha = string.printable
url = "https://aes.cryptohack.org/ecb_oracle"

flag = b"crypto{p3n6u1n5"

while not flag.endswith(b"}"):
    payload = b"a" * ((15 - (len(flag) % 16)) or 16)
    target = len(payload + flag) // 16
    req = requests.get(f"{url}/encrypt/{(payload).hex()}").json()['ciphertext'][target * 32 : (target + 1) * 32]
    for c in alpha:
        c = c.encode()
        tmp = requests.get(f"{url}/encrypt/{(payload + flag + c).hex()}").json()['ciphertext'][target * 32 : (target + 1) * 32]
        if req == tmp:
            flag += c
            print(flag)
            break

