from Crypto.Cipher import DES
from Crypto.Util.Padding import pad

class TDES:
    def __init__(self, key1, key2):
        assert len(key1) == 8
        assert len(key2) == 8
        self.keys = [key1, key2, key1]
        self.cipher = [DES.new(key, DES.MODE_ECB) for key in self.keys]
        self._block_size = 16

    def encrypt(self, plaintext, mode):
        assert len(mode) == 3
        for m in mode:
            assert m in 'ED'
        assert len(plaintext) % self._block_size == 0

        for cipher, m in zip(self.cipher, mode):
            if m == 'E':
                plaintext = cipher.encrypt(plaintext)
            else:
                plaintext = cipher.decrypt(plaintext)
        return plaintext

    def decrypt(self, plaintext, mode):
        assert len(mode) == 3
        for m in mode:
            assert m in 'ED'
        assert len(plaintext) % self._block_size == 0

        for cipher, m in zip(self.cipher[::-1], mode[::-1]):
            if m == 'D':
                plaintext = cipher.encrypt(plaintext)
            else:
                plaintext = cipher.decrypt(plaintext)
        return plaintext


if __name__ == "__main__":
    import os
    test = 0x1000
    for t in range(test):
        key1 = os.urandom(8)
        key2 = os.urandom(8)
        tdes = TDES(key1, key2)
        plain = os.urandom(64)
        assert plain == tdes.decrypt(tdes.encrypt(plain, 'EEE'), 'EEE')
        assert plain == tdes.decrypt(tdes.encrypt(plain, 'EDE'), 'EDE')
        assert plain == tdes.decrypt(tdes.encrypt(plain, 'EED'), 'EED')