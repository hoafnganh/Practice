from Crypto.Cipher import AES

key = bytes([i for i in range(60, 76)])
cipher = AES.new(key, AES.MODE_CBC, iv = b"\x00" * 16)
ciphertext = bytes.fromhex('1417c97254a837b486e829faab5628df')
flag = cipher.decrypt(ciphertext)
print(flag)