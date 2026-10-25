from Crypto.PublicKey import RSA

with open ("bruce_rsa_6e7ecd53b443a97013397b1a1ea30e14.pub", "rb") as f:
    data = f.read()
    key = RSA.import_key(data)

print(key.n)