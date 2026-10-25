from Crypto.Cipher import AES


with open("flag.jpg.enc", "rb") as f:
    data = f.read()

key = '00112233445566778899aabbccddeeff'
key = bytes.fromhex(key)
aes = AES.new(key, AES.MODE_CTR, nonce = bytes.fromhex("0" * 16))
flag = aes.decrypt(data)
with open("flag.jpg", "wb") as f:
    f.write(flag)