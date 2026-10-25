import requests, base64

url = "http://host3.dreamhack.games:13220"

token="9i4HfYcPn3+igvGrcxbA2ISyBoAevirotJxOsIeO1IA1YhXRAcFdoSdZQnbq+zqa"

data = requests.get(f"{url}/gb/1").json()
enc_data = data["result"]["article"]["enc_data"]
# print(enc_data)
enc_data = base64.b64decode(enc_data)
blocks = [enc_data[i:i + 16] for i in range(0, len(enc_data), 16)]
C1, C2 = blocks[0], blocks[1]
# {"content": "The
#  password is: xx
# xxxxxx", "author
# ": "admin"}

print(enc_data.hex())
# 72af4045854b64ee07dcb8fe5613140f  {"content": "The
# 83038c896d50341111b668d07799d362   password is: xx
# d01f49bcf6d1fb1b5c32fd5a928feb38  xxxxxx", "author
# e14458b41418db8848d2515a471b2f92  ": "admin"}\\\\\

def oracle(R, C):
    e = base64.b64encode(bytes(R) + bytes(C)).decode()
    r = requests.get(f"{url}/secure/decrypt", params = {"e_data": e, "token": token, "sig": "x"})
    return r.json()["result"]["message"] != "ValueError"



for k in range(256):
    I = bytearray(16)
    known = b" password is: "
    for j in range(14):
        I[j] = known[j] ^ C1[j]