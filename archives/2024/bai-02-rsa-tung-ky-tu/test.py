from Crypto.Util.number import getPrime 
N = getPrime(24)
print(N)
print(format(N, "08X")) # 0000000B
print(int("0000000B", 16))