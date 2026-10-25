ct = "3cef03c64ac240c349971d9e4c951cc14ec4199f409249c21e964ac540c540944f901c934cc240934d96419f4b9e4d9f1cc41dc61dc34e9219c31bc11a914f9141c61ada"
ct = bytes.fromhex(ct)
# seed có 16 bits, mỗi lần mã hoá 1 kí tự thì xoay 8 bit một.
def num2bits(num, size):
    assert num < (1 << size)

    return bin(num)[2:].zfill(size)

flag = b"DH{"
stream = int(b"D".hex(), 16) ^ ct[0]
# print(stream)
print(*reversed(str(num2bits(stream, 8)))) # 00011110, vì num2bits trả về bit 
stream = int(b"H".hex(), 16) ^ ct[1]
print(*reversed(str(num2bits(stream, 8)))) # 11100101
# print(stream)
# stream = int(b"{".hex(), 16) ^ ct[2]
# print(stream)
seed = 0b1110010100011110
# seed = 0b0111100010100111
# print(type(seed))

class STREAM:
    def __init__(self, seed, size):
        self.state = self.num2bits(seed, size)

    def num2bits(self, num, size):
        assert num < (1 << size)

        return bin(num)[2:].zfill(size)
    
    def bits2num(self, bits):
        return int('0b' + bits, 2)
    
    def shift(self):
        new_bit = self.state[-1]
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

Bob = STREAM(seed, 16)
print(Bob.decrypt(ct))