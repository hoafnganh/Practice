from base64 import b64decode
from Crypto.Cipher import AES
ct = b64decode("1KeGOcMvvKpPbxrNRdyqJmSGh3j+ZCvIT5RKk6lTBkSGBYSYrX7dy3Q/E8wVuQAXNFMs978T1A4qyx7EeX9fvg==")

key = b"ch@ng3Digit@lInf0rm@ti0n"
iv = b"Th3W0rldS@f3t0Ex"

aes = AES.new(key, AES.MODE_CBC, iv)

flag = aes.decrypt(ct)
print(flag)