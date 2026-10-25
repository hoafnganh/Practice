# solve.py — challenge 11: LSB oracle binary search
import socket
import subprocess
import sys
import os
import time
import random

HERE = os.path.dirname(os.path.abspath(__file__))

port = random.randint(20000, 40000)
srv = subprocess.Popen([sys.executable, os.path.join(HERE, "server.py"), str(port)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)

try:
    io = socket.create_connection(("127.0.0.1", port), timeout=20)
    f = io.makefile("rwb")

    def recv_until(tok):
        buf = b""
        while tok not in buf:
            ch = f.read(1)
            if not ch:
                break
            buf += ch
        return buf

    hdr = recv_until(b"> ")
    d = {}
    for line in hdr.splitlines():
        if b"=" in line:
            k, v = line.split(b"=")
            d[k.strip().decode()] = int(v.strip())
    n, e, ct = d["n"], d["e"], d["ct"]

    def oracle(cq):
        """cq da la ciphertext (int). Tra ve True neu Even."""
        f.write(f"{cq}\n".encode())
        f.flush()
        resp = recv_until(b"> ")
        return b"Even" in resp

    # tim nhi phan: pt_i = m * 2^i mod n; chan ⇔ m*2^(i-1) mod n < n/2
    # Dung khi khoang con hep (~2^16) de tranh loi lam tron bien nhan o
    # nhung buoc cuoi (ky thuat chuan: roi quet pow(cand,e,n)==ct).
    c2e = pow(2, e, n)
    lb, ub = 0, n
    cq = ct
    iters = 0
    while ub - lb > (1 << 16) and iters <= n.bit_length() + 16:
        cq = (cq * c2e) % n          # nhan ban ro them 2
        mid = (lb + ub) // 2
        if oracle(cq):
            ub = mid
        else:
            lb = mid
        iters += 1

    # quet khoang (co bien du) tim m chinh xac
    W = 1 << 17
    m = None
    for cand in range(max(0, lb - W), ub + W):
        if pow(cand, e, n) == ct:
            m = cand
            break
    assert m is not None, f"khong tim duoc m trong [{lb-W}, {ub+W}]"
    from Crypto.Util.number import long_to_bytes
    print(f"iters = {iters}, interval width = {ub - lb}")
    print("FLAG:", long_to_bytes(m).decode())
finally:
    io.close()
    srv.terminate()
