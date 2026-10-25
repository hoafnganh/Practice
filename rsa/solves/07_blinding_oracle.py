# solve.py — challenge 07: blinding attack tren decipher oracle
import socket
import subprocess
import sys
import os
import time
import random

HERE = os.path.dirname(os.path.abspath(__file__))

# 1) khoi dong server o mot port rong
port = random.randint(20000, 40000)
srv = subprocess.Popen([sys.executable, os.path.join(HERE, "server.py"), str(port)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)

try:
    io = socket.create_connection(("127.0.0.1", port), timeout=10)
    f = io.makefile("rwb")

    def recv_until(tok):
        buf = b""
        while tok not in buf:
            ch = f.read(1)
            if not ch:
                break
            buf += ch
        return buf

    # 2) lay n, e, c
    hdr = recv_until(b"Text to decrypt:")
    d = {}
    for line in hdr.splitlines():
        if b"=" in line:
            k, v = line.split(b"=")
            d[k.strip().decode()] = int(v.strip())
    n, e, c = d["n"], d["e"], d["c"]

    # 3) lam mu: gui c' = c * r^e mod n  ->  m' = m * r mod n
    r = 2
    c_blind = (c * pow(r, e, n)) % n
    f.write(f"{c_blind}\n".encode())
    f.flush()
    resp = recv_until(b"\nText to decrypt:")
    mp = int(resp.split(b"m =")[1].split(b"\n")[0].strip())

    # 4) chia lai cho r
    m = (mp * pow(r, -1, n)) % n
    from Crypto.Util.number import long_to_bytes
    print("FLAG:", long_to_bytes(m).decode())
finally:
    io.close()
    srv.terminate()
