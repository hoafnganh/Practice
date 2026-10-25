import requests
import string

url = "https://aes.cryptohack.org/ctrime"

flag = "crypto{CRIME"

alphabet = string.printable

while not flag.endswith("}"):
    leng = len(requests.get(f"{url}/encrypt/{flag.encode().hex()}").json()["ciphertext"])
    # print("Flag length:", leng)
    for i in alphabet:
        print("i =", i)
        data = requests.get(f"{url}/encrypt/{(flag + i).encode().hex()}").json()
        print(len(data["ciphertext"]))
        if len(data["ciphertext"]) <= leng:
            flag += i
            print(flag)
            break
print(bytes.fromhex(flag).decode())
