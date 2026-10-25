from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Util.number import long_to_bytes

enc = "f049de59cbdc9189170787b20b24f7426ccb9515e8b0250f3fc0f0c14ed7bb1d4b42c09d02fe01e0973a7233d99af55ce696f599050142759adc26796d64e0d6035f2fc39d2edb8a0797a9e45ae4cd55074cf99158d3a64dc70a7e836e3b30382df30de49ba60a"

Nonce = bytes.fromhex(enc[:32])
c = bytes.fromhex(enc[32 : -32])
tag = bytes.fromhex(enc[-32:])
# print(nonce, c, tag)
print(len(Nonce), len(c), len(tag))
for pin in range(0, 10000):
    k = scrypt(long_to_bytes(pin), b"FCSC", 32, N = 2 ** 10, r = 8, p = 1)
    aes = AES.new(k, AES.MODE_GCM, nonce=Nonce)
    try:
        dec = aes.decrypt_and_verify(c, tag)
    except:
        continue
    if b"FCSC" in dec:
        print(pin)
        print(dec)
        break
