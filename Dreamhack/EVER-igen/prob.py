import random
from string import ascii_lowercase, ascii_uppercase, digits

words = ascii_uppercase + ascii_lowercase + digits
class Vigenere:
    def __init__(self, key):
        self._key = key

    def shift(self, a, d):
        if a not in words:
            return a
        index = words.index(a)
        return words[(index + d) % len(words)]

    def encrypt(self, pt):
        ct = ""
        for i in range(len(pt)):
            ct += self.shift(pt[i], self._key[i % len(self._key)])
        return ct

    def decrypt(self, ct):
        pt = ""
        for i in range(len(ct)):
            pt += self.shift(ct[i], -self._key[i % len(self._key)])
        return pt

def main():
    key = [random.randint(0, len(words)) for _ in range(16)]
    with open("secret", "r") as f:
        secret = f.read()

    assert "Vigenere", "cipher" in secret
    cipher = Vigenere(key)
    secret_enc = cipher.encrypt(secret)
    print(f"my encrypted sentence > {secret_enc}")

if __name__ == '__main__':
    main()