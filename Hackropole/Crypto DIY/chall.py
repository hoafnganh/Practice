N = 53631231719770388398296099992823384509917463282369573510894245774887056120440201731735752915096736722856082884548917654078388282501542293219713052500317361  # N=p*q with primes p and q that are part of my secret key

g1 = 27888419610931008932601664194635863362934795268815711191831564335481311281875775885782976960387128801701810764586184606874328259752328953489610371824189861  # g1=g^(r1*(p-1)) mod N where r1 is a secret random

g2 = 48099264739307394087061906063506998841178675587231635606136922987485103900358857801144199074460106065443613588490877251721439499846448566220473205526148817  # g2=g^(r2*(q-1)) mod N where r2 is a secret random

# To encipher the message m of same size as N
# Choose two nounces s1 and s2 (plz keep them secret) and send me c1 and c2 given by:

import random

def encipher(m, g1, g2, N):
    s1 = random.randrange(2**127, 2**128)
    s2 = random.randrange(2**127, 2**128)
    return (m * pow(g1, s1, N)) % N, (m * pow(g2, s2, N)) % N

# To encipher a data use this code and send me the cipher file

nb_car_block = 64


def BlobToIntSeq(m, nb_car_block):
    m = m + bytes([71, 82, 114]) # + bytes
    l = len(m)
    r = l % nb_car_block
    if not (r == 0):
        m = m + (nb_car_block - r) * bytes([114]) # padding bằng r
        l = len(m)
    out = []
    i = 0
    j = nb_car_block
    while j <= l:
        tmp = int.from_bytes(m[i:j], "big") # cắt 1 block thành 1 int
        out = out + [tmp]
        i, j = i + nb_car_block, j + nb_car_block
    return out

import sys

plainbin = open(sys.argv[1], "rb")
plain = plainbin.read()
plainbin.close()
l = len(plain)
plainint = BlobToIntSeq(plain, nb_car_block)
cipher = open(sys.argv[1] + ".cipher", "w")
i = 0

for m in plainint:
    c1, c2 = encipher(m, g1, g2, N)
    cipher.write((str(c1)) + "\n")
    cipher.write((str(c2)) + "\n")
    i = i + 1   

cipher.close()
