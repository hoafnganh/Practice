# solve.py — challenge 14: Bleichenbacher (BB'98) padding oracle attack
#
# Buoc 2a: quet tuan tu s = ceil(n/3B) den VALID dau tien -> m trong [2B,3B).
# Thu hep: giu s ~ 2B/w (w = do rong khoang chua m) thi moi WINDOW
#   [(2B+rn)/s, (3B-1+rn)/s] rong ~ w/2: bat ky hit nao cung cat khoang
#   xuong con ~w/2. Quet state-free giua cac hit (khong cap nhat M — chi
#   intersect khi hit) de toc do moi truy van ~ oracle thuan.
# Tong so truy van ~ (bits can thu hep) x (n/B).
import sys
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "_lib"))

import challenge as CH

n, e, ct = CH.n, CH.e, CH.ct
oracle = CH.oracle
K = CH.K
B = 1 << (8 * (K - 2))

queries = 0


def oracle_s(s):
    global queries
    queries += 1
    return oracle((ct * pow(s, e, n)) % n)


def ceil_div(x, y):
    return -((-(x)) // y)


def windows(s, a, b):
    res = []
    r_lo = max(0, -((-(a * s - 3 * B + 1)) // n))
    r_hi = (b * s - 2 * B) // n
    for r in range(r_lo, r_hi + 1):
        lo = max(a, ceil_div(2 * B + r * n, s))
        hi = min(b, (3 * B - 1 + r * n) // s)
        if lo <= hi:
            res.append((lo, hi))
    return res


def maxwidth(M):
    return max(b - a for (a, b) in M) if M else 0


t0 = time.time()

# ---- Buoc 2a: quet tuan tu den hit dau tien ----
s = max(1, n // (3 * B))
while not oracle_s(s):
    s += 1
M = windows(s, 2 * B, 3 * B - 1)
print(f"[+] hit dau tien: s = {s}, q = {queries}, |M| = {len(M)}, "
      f"wbits = {maxwidth(M).bit_length()} ({time.time()-t0:.0f}s)", flush=True)

# ---- Thu hep: giu s ~ 2B/w, moi hit cat nua khoang ----
rounds = 0
while M and maxwidth(M) > 8:
    rounds += 1
    if rounds > 500:
        raise RuntimeError("qua nhieu vong")
    w = maxwidth(M)
    s = max(s + 1, ceil_div(2 * B, w))
    # quet state-free den hit
    while True:
        ok = oracle_s(s)
        if ok:
            break
        s += 1
        if queries % 500000 == 0:
            print(f"[*] dang quet: s = {s}, q = {queries} ({time.time()-t0:.0f}s)", flush=True)
    newM = []
    for (a, b) in M:
        newM.extend(windows(s, a, b))
    M = newM
    print(f"[*] vong {rounds}: hit s = {s}, |M| = {len(M)}, "
          f"wbits = {maxwidth(M).bit_length()}, q = {queries} ({time.time()-t0:.0f}s)", flush=True)

print(f"[+] xong: rounds = {rounds}, queries = {queries}, {time.time()-t0:.0f}s", flush=True)
for (a, b) in M:
    for cand in range(a, b + 1):
        blk = cand.to_bytes(K, "big")
        if blk[0:2] == b"\x00\x02":
            msg = blk[blk.find(b"\x00", 2) + 1:] if b"\x00" in blk[2:] else b""
            if msg.startswith(b"crypto{"):
                print(f"queries tong = {queries}")
                print("FLAG:", msg.decode())
                raise SystemExit(0)
raise RuntimeError("khong tim duoc flag trong cac khoang cuoi")
