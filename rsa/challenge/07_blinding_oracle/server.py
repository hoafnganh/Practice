import socket
import sys
import threading
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes, inverse

FLAG = "crypto{???}"

p = getPrime(512)
q = getPrime(512)
n = p * q
e = 65537
d = pow(e, -1, (p - 1) * (q - 1))
m = bytes_to_long(FLAG.encode())
c = pow(m, e, n)


def handle(conn):
    f = conn.makefile("rwb")
    f.write(f"n = {n}\ne = {e}\nc = {c}\n".encode())
    f.flush()
    while True:
        f.write(b"Text to decrypt: ")
        f.flush()
        line = f.readline()
        if not line:
            break
        line = line.strip()
        if not line:
            continue
        try:
            ct = int(line)
            pt = pow(ct, d, n)
            if pt == m or b"crypto{" in long_to_bytes(pt):
                f.write(b"Nope!\n")
            else:
                f.write(f"m = {pt}\n".encode())
        except ValueError:
            f.write(b"Bad input!\n")
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
