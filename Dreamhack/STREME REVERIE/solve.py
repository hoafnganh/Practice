class STREAM:
    def __init__(self, seed, size):
        self.state = self.num2bits(seed, size)
        # x^32 + x^22 + x^2 + x^1 + 1
        self.taps = (32, 22, 2, 1)

    def num2bits(self, num, size):
        assert num < (1 << size)

        return bin(num)[2:].zfill(size)
    
    def bits2num(self, bits):
        return int('0b' + bits, 2)
    
    def shift(self):
        new_bit = 0
        for tap in self.taps:
            new_bit ^= int(self.state[tap - 1])
        new_bit = str(new_bit)
        self.state = new_bit + self.state[:-1]
        return new_bit
    
    def getNbits(self, num):
        sequence = ""
        for _ in range(num):
            sequence += self.shift()
        
        return sequence

    def encrypt(self, plaintext):
        ciphertext = b""
        for p in plaintext:
            stream = self.bits2num(self.getNbits(8))
            c = p ^ stream
            ciphertext += bytes([c])

        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = b""
        for c in ciphertext:
            stream = self.bits2num(self.getNbits(8))
            p = c ^ stream
            plaintext += bytes([p])

        return plaintext


ct = "c615a6cbc4bbf37fe65af240813248140925f2afb31f6c6b5bf71cdfa151fcd55999cf95e2eb9313fc75afe39d1bf836ef14931afe19e16a7c16a1bb41d5abe5d124991d"
ct = bytes.fromhex(ct)
Alice = STREAM(1, 32)
prefix = b"DH{"

known = "".join(format(ct[i] ^ prefix[i], "08b") for i in range(3)) # LSB
print(known)
for x in range (256):
    T = STREAM(0, 32)
    T.state = known[::-1] + format(x, '08b')
    flag = T.decrypt(ct[3:])
    if flag.endswith(b"}"):
        print(flag)
        break
