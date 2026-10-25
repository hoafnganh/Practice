# solve.py — challenge 18: Kocher timing attack (corr bit-by-bit, LSB->MSB)
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

io = None
try:
    for _ in range(80):
        try:
            io = socket.create_connection(("127.0.0.1", port), timeout=30)
            break
        except OSError:
            time.sleep(0.25)
    assert io is not None, "khong ket noi duoc server"
    f = io.makefile("rwb")

    def readline():
        return f.readline().decode()

    d = {}
    while True:
        line = readline()
        if "=" in line:
            k, v = line.split("=")
            d[k.strip()] = int(v.strip())
        else:
            first_pair = line.split()
            break
    n, e, c, count = d["n"], d["e"], d["c"], d["count"]

    Ms, Ts = [], []
    if len(first_pair) == 2:
        Ms.append(int(first_pair[0])); Ts.append(float(first_pair[1]))
    for _ in range(count - 1):
        parts = readline().split()
        Ms.append(int(parts[0])); Ts.append(float(parts[1]))
    print(f"[*] nhan {count} mau thoi gian")

    L = max(Ms[0].bit_length(), (n - 1).bit_length()) + 8
    z = [M % n for M in Ms]          # z_i = M_i^(2^j)
    C = [1] * count                  # C_i = M_i^(d mod 2^j)
    acc = [0.0] * count              # tong chi phi da quyet dinh

    def pc(x):
        return bin(x).count("1")

    BASE, PER_BIT = 40.0, 30.0
    bits = []
    for j in range(L):
        vals = [(BASE + PER_BIT * pc((C[i] * z[i]) % n)) for i in range(count)]
        resid = [Ts[i] - acc[i] for i in range(count)]
        if j == 0:
            bit = 1              # d le -> d0 = 1 chac chan
        else:
            mean_v = sum(vals) / count
            mean_r = sum(resid) / count
            cov = sum((vals[i] - mean_v) * (resid[i] - mean_r) for i in range(count)) / count
            var_v = sum((v - mean_v) ** 2 for v in vals) / count
            var_r = sum((r - mean_r) ** 2 for r in resid) / count
            corr = cov / ((var_v * var_r) ** 0.5) if var_v > 0 and var_r > 0 else 0.0
            bit = 1 if corr > 0.034 else 0
        bits.append(bit)
        # cap nhat acc: binh phuong luon, nhan neu bit = 1
        for i in range(count):
            if bit:
                acc[i] += vals[i]
                C[i] = (C[i] * z[i]) % n
            z[i] = (z[i] * z[i]) % n
            acc[i] += BASE + PER_BIT * pc(z[i])
        if j % 64 == 0:
            print(f"[*] bit {j}: -> {bit}")

    d_rec = sum(b << j for j, b in enumerate(bits))
    # kiem chung: (M^e)^d == M
    ok = all(pow(pow(Ms[i], e, n), d_rec, n) == Ms[i] for i in range(5))
    assert ok, "d khoi phuc sai"
    print(f"[*] d khoi phuc thanh cong ({d_rec.bit_length()} bit)")
    from Crypto.Util.number import long_to_bytes
    print("FLAG:", long_to_bytes(pow(c, d_rec, n)).decode())
finally:
    if io is not None:
        io.close()
    srv.terminate()
