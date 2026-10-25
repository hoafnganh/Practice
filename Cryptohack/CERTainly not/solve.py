from Crypto.PublicKey import RSA

with open ("2048b-rsa-example-cert_3220bd92e30015fe4fbeb84a755e7ca5.der", "rb") as f:
    data = f.read()
    key = RSA.import_key(data)
print(key.n)