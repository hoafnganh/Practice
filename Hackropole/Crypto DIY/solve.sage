N = 53631231719770388398296099992823384509917463282369573510894245774887056120440201731735752915096736722856082884548917654078388282501542293219713052500317361  # N=p*q with primes p and q that are part of my secret key

g1 = 27888419610931008932601664194635863362934795268815711191831564335481311281875775885782976960387128801701810764586184606874328259752328953489610371824189861  # g1=g^(r1*(p-1)) mod N where r1 is a secret random

g2 = 48099264739307394087061906063506998841178675587231635606136922987485103900358857801144199074460106065443613588490877251721439499846448566220473205526148817  # g2=g^(r2*(q-1)) mod N where r2 is a secret random
import math
nb_car_block = 64

p, q = math.gcd(N, g1 - 1), math.gcd(N, g2 - 1)

assert p * q == N
plainint = []

def IntSeqToBlob(plainint: list):
    data = b""
    for m in plainint:
        tmp = m.to_bytes(64, 'big')
        data += tmp
    i = data.rindex(bytes([71, 82, 114]))
    return data[:i]

with open("WIM.mp4.cipher", "rb") as f:
    for l1, l2 in zip(f, f):
        c1 = int(l1)
        c2 = int(l2)
# print(type(c1), c2)
        rems = [c1, c2]
        mods = [p, q]

        m = int(crt(rems, mods))
        plainint.append(m)
    
    data = IntSeqToBlob(plainint)

with open("WIM.mp4", "wb") as f:
    f.write(data)

