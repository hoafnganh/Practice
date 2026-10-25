# server.py — the thong minh ky RSA (mo phong thoi gian square-and-multiply)
# Cach chay: python server.py 1337
import os
import random
import socket
import sys
import threading

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import rsalib as R
from Crypto.Util.number import bytes_to_long

FLAG = "crypto{t1m1ng_s1d3_ch4nn3l}"

rng = random.Random(20260930)
p = R.gen_prime(128, rng)
q = R.gen_prime(128, rng)
n = p * q
e = 65537
d = pow(e, -1, (p - 1) * (q - 1))

COUNT = 8192
BASE = 40.0     # us co ban moi phep nhan
PER_BIT = 30.0  # us tren moi bit 1 cua ket qua
NOISE = 10.0    # nhieu tren toan bo chu ky

MESSAGES = [rng.randrange(2, n) for _ in range(COUNT)]


def sign_timed(M, rng_noise):
    """Square-and-multiply LSB-first voi mo hinh thoi gian deterministic."""
    total = 0.0
    C = 1
    z = M % n
    for j in range(d.bit_length()):
        dj = (d >> j) & 1
        if dj:
            C = (C * z) % n
            total += BASE + PER_BIT * bin(C).count("1")
        z = (z * z) % n
        total += BASE + PER_BIT * bin(z).count("1")
    return total + rng_noise.uniform(0.0, NOISE)


def handle(conn):
    f = conn.makefile("rwb")
    f.write(f"n = {n}\ne = {e}\nc = {pow(bytes_to_long(FLAG.encode()), e, n)}\n"
            f"count = {COUNT}\n".encode())
    f.flush()
    rn = random.Random(1337)
    for i in range(COUNT):
        t = sign_timed(MESSAGES[i], rn)
        f.write(f"{MESSAGES[i]} {t:.2f}\n".encode())
    f.flush()
    conn.close()


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 1337
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", port))
    srv.listen(5)
    print(f"[server] listening on 127.0.0.1:{port}", flush=True)
    while True:
        conn, _ = srv.accept()
        threading.Thread(target=handle, args=(conn,), daemon=True).start()


if __name__ == "__main__":
    main()
