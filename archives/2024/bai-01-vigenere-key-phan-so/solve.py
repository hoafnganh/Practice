# Simple Crypto (2024) - file ten la base64, noi dung la Vigenere ciphertext
# Filename b64 -> "The key is hidden in one in a prime number" => key = 1/prime
# 1/17 = 0.058823... ; key thuc te = "058823" (cat 6 chu so, LAP LAI)
# => "verysimplecryptochallengewasntit"
# Gotcha: repetend day du 16 chu so "0588235294117647" KHONG giai ra (chi "verysi" dau)
import base64

name = 'VGhlIGtleSBpcyBoaWRkZW4gaW4gb25lIGluIGEgcHJpbWUgbnVtYmVy'
ct = 'vjzgulmutmeuyubwekaqtmpjebiapwiy'
key = '058823'

print(base64.b64decode(name).decode())
print(''.join(chr((ord(c) - 97 - int(k)) % 26 + 97) for c, k in zip(ct, key * 64)))
