import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes

iv = bytes.fromhex("ea425b2ea4bb67445abe967e3bd1b583")
c = bytes.fromhex("69771c85e2362a35eb0157497e9e2d17858bf11492e003c4aa8ce1b76d8d3a31ccc3412ec6e619e7996190d8693299fc3873e1e6a96bcc1fe67abdf5175c753c09128fd1eb2f2f15bd07b12c5bfc2933")
H = "951bd9d2caae0d9e9a5665b4fc112809aac9f5f9ecbcfc5ad8e23cb1d020201d"
password = b"omgh4xx0r"
# with open("rockyou.txt", "r", encoding='latin-1') as f:
#     for line in f:
#         password = line.strip("\r\n")
#         # print(password)
#         h = HMAC.new(password.encode(), digestmod = SHA256)
#         h.update(b"FCSC2022")
#         # print(h.hexdigest())
#         if h.hexdigest() == H:
#             print(password)
#             break


k  = SHA256.new(password).digest()
m  = AES.new(k, AES.MODE_CBC, iv = iv).decrypt(c)
print(m)

