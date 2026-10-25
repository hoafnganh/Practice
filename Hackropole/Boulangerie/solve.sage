from pwn import *

r = remote("localhost", 4000)

recette = ["pain", "ananas", "croissant", "pain au chocolat"]
for _ in range(64):
    r.recvuntil(b"Et voila : ")
    line = r.recvline().decode().strip()[1:-1]
    c, e, n = map(int, line.split(", "))
    for i in recette:
        m = int.from_bytes(i.encode())
        q = gcd(pow(m, e, n) - c, n)
        if q != 1 and q != n:
            a = i
            print(q)
            break

    r.recvuntil(b"Alors ? ")
    r.sendline(b"1")
    r.recvuntil(b"Alors alors ??? ")
    r.sendline(a.encode())
print(r.recvall(timeout=5))