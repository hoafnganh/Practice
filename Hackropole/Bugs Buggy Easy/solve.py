from pwn import *
import math
from Crypto.Util.number import *
r = remote("localhost", 4000)

def sign(n):
    r.recvuntil(b">>> ")
    r.sendline(str(n).encode())
    num = int(r.recvline().decode().strip())
    r.recvline()
    return num

enc_flag = int(r.recvline().decode().strip().split(": ")[1])
r.recvline()

n = math.gcd(sign(2) * sign(2) - sign(4), sign(3) * sign(3) - sign(9)) #24299236589088820199042788011924838863505427508504403129909890759024128204859214852155067459922997253489995211565530302080886601596090143666064035128790783223715794026457703326574364388443418821580232061646654242963685501867976906736882239787108342058691180751774288824606617832197441696401383258273231900422933191583208360560046430768082063133645953710440215312543969398162802150373090160917840645962678134215835890307284985693037078823041199079350019632480498769513929204580287963460565107578377010488671352081444551709814818265724084821889044368579962769257539894621257970579133369305964884820340361087886375774101
print(n)
e = 65537
assert pow(sign(2), e, n) == 2
# print(e)

def search_q():
    l, h = 0, n - 1
    while l <= h:
        m = (l + h) // 2
        sign_fault = (pow(sign(m), e, n) != m)
        if sign_fault:
            diff = (pow(sign(m), e, n) - m) % n
            q = math.gcd(diff, n)
            if q != 1 and q != n:
                return q
            h = m - 1
        else: l = m + 1

q = search_q()
p = n // q
assert p * q == n
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
flag = pow(enc_flag, d, n)
print(long_to_bytes(flag))