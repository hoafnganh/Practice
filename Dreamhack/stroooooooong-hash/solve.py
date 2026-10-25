#!/usr/bin/env python3
"""
stroooooooong-hash -- solve

Yeu diem: stronghash(m) = G( F(pad(m)[:16])[:2] )
  F = chuoi 10 vong AES tren block X, moi vong key = chinh block do (Y khong tham gia)
  G = chuoi md5/sha256 cong khai, chi doc 2 byte dau cua X10

Cach giai:
  CP1  tach stronghash thanh F + G, verify khop ban goc
  CP2  G_rev : hash 32B -> v (2B)          65536 gia tri, dung 1 lan
  CP3  cover : v -> X0 (16B msg)           coupon collector ~730k lan (~40s), dung 1 lan
  CP4  moi stage: hash -> v -> X0 -> gui X0.hex() (32 ky tu hex)

Usage:
  python solve.py test                 # CP1 + chay end-to-end voi deploy/prob.py (pipe)
  python solve.py remote HOST PORT     # danh bai that (vi du: python solve.py remote host3.dreamhack.games 14448)
"""
import hashlib
import os
import pickle
import re
import socket
import subprocess
import sys
import time

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "solve_cache.pkl")

STAGES = 100
HASH_RE = re.compile(rb"My hashed password : ([0-9a-fA-F]{64})")


# ------------------------------------------------------------------ CP1 --
def stronghash(msg: bytes) -> bytes:
    """Copy y nguyen deploy/prob.py -- chi dung de verify, khong dung de solve."""
    hashed_msg = pad(msg, 16)
    for _ in "Stronger!!":
        hashed_msg = AES.new(hashed_msg[:16], AES.MODE_ECB).encrypt(hashed_msg)
    for length in range(2, 16):
        hashed_msg = hashlib.md5(hashed_msg[:length]).digest()
    for length in range(16, 32):
        hashed_msg = hashlib.sha256(hashed_msg[:length]).digest()
    return hashed_msg


def F(x: bytes) -> bytes:
    """Chuoi AES 10 vong tren block X: x = E_key=x(x). Y khong anh huong X."""
    for _ in range(10):
        x = AES.new(x, AES.MODE_ECB).encrypt(x)
    return x


def G(v: bytes) -> bytes:
    """Chuoi md5/sha256 -- vong dau md5(v[:2]) nen input chi can 2 byte."""
    h = v
    for length in range(2, 16):
        h = hashlib.md5(h[:length]).digest()
    for length in range(16, 32):
        h = hashlib.sha256(h[:length]).digest()
    return h


def cp1_decomposition(rounds: int = 100) -> None:
    for i in range(rounds):
        m = os.urandom((i * 7 + 5) % 17)            # do dai 0..16 byte
        assert stronghash(m) == G(F(pad(m, 16)[:16])[:2]), m
    print(f"[CP1] decomposition OK ({rounds} msg, moi do dai)")


# ------------------------------------------------------------------ CP2 --
def build_G_rev() -> dict:
    g_rev = {}
    for i in range(65536):
        v = i.to_bytes(2, "big")
        g_rev[G(v)] = v
    # G KHONG don anh: buoc md5 thu 2 lay md5(h[:3]) nen ~128 cap v (birthday 24-bit)
    # cung prefix 3 byte -> cung state -> cung hash. Khong anh huong: moi hash
    # van tra duoc MỘT v, va cover phu moi v.
    assert len(g_rev) > 65536 - 2048, f"G_rev mat qua nhieu bucket: {len(g_rev)}"
    print(f"[CP2] G_rev: {len(g_rev)} hash rieng biet (merge ~{65536 - len(g_rev)} cap v)")
    return g_rev


# ------------------------------------------------------------------ CP3 --
def build_cover() -> dict:
    cover = {}
    i = 0
    t0 = time.time()
    while len(cover) < 65536:
        head = F(i.to_bytes(16, "big"))[:2]
        if head not in cover:
            cover[head] = i.to_bytes(16, "big")
        i += 1
        if i % 200_000 == 0:
            print(f"      ... {i} thu, {len(cover)}/65536 bucket, {time.time() - t0:.0f}s")
    print(f"[CP3] cover du 65536 bucket sau {i} lan thu ({time.time() - t0:.0f}s)")
    return cover


def load_or_build():
    if os.path.exists(CACHE):
        with open(CACHE, "rb") as f:
            g_rev, cover = pickle.load(f)
        print(f"[cache] nap lai G_rev ({len(g_rev)}) + cover ({len(cover)})")
        return g_rev, cover
    g_rev = build_G_rev()
    cover = build_cover()
    with open(CACHE, "wb") as f:
        pickle.dump((g_rev, cover), f)
    return g_rev, cover


# ------------------------------------------------------------------ CP4 --
class LineReader:
    """Doc theo dong tu socket hoac subprocess pipe.
    Parse bang content (regex), khong dua vao vi tri dong -- chong pty echo."""

    def __init__(self, f):
        self.f = f
        self.buf = b""

    def _read(self, n=4096):
        if hasattr(self.f, "recv"):          # socket
            return self.f.recv(n)
        if hasattr(self.f, "read1"):         # subprocess pipe: read() se block den du n byte!
            return self.f.read1(n)
        return self.f.read(n)

    def readline(self) -> bytes:
        while b"\n" not in self.buf:
            chunk = self._read()
            if not chunk:
                raise EOFError("ket thuc du lieu giua chung, buffer: " + repr(self.buf))
            self.buf += chunk
        line, self.buf = self.buf.split(b"\n", 1)
        return line

    def readall(self, timeout=None) -> bytes:
        if timeout is not None and hasattr(self.f, "settimeout"):
            self.f.settimeout(timeout)
        out, self.buf = self.buf, b""
        while True:
            try:
                chunk = self._read()
            except (socket.timeout, TimeoutError, OSError):
                break
            if not chunk:
                break
            out += chunk
        return out


def answer_for(target_hash: bytes, g_rev: dict, cover: dict) -> bytes:
    if target_hash not in g_rev:
        raise KeyError(f"hash khong nam trong G_rev: {target_hash.hex()}")
    return cover[g_rev[target_hash]]


def solve_stages(r: LineReader, send, g_rev: dict, cover: dict) -> None:
    for stage in range(1, STAGES + 1):
        target = None
        while target is None:
            m = HASH_RE.search(r.readline())
            if m:
                target = bytes.fromhex(m.group(1).decode())
        send(answer_for(target, g_rev, cover).hex().encode() + b"\n")
        if stage % 20 == 0:
            print(f"      stage {stage}/{STAGES}")


def local_test() -> None:
    """End-to-end voi deploy/prob.py thong qua pipe -- test parser va luong giai."""
    g_rev, cover = load_or_build()
    p = subprocess.Popen(
        [sys.executable, "-u", "prob.py"],
        cwd=os.path.join(HERE, "deploy"),
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )

    def send(b):
        p.stdin.write(b)
        p.stdin.flush()

    r = LineReader(p.stdout)
    t0 = time.time()
    solve_stages(r, send, g_rev, cover)
    print("[CP4-local] xong 100 stage,", f"{time.time() - t0:.0f}s")
    print("[CP4-local] du lieu cuoi:", r.readall().decode(errors="replace"))
    p.wait()


def remote(host: str, port: int) -> None:
    g_rev, cover = load_or_build()
    s = socket.create_connection((host, port), timeout=60)
    r = LineReader(s)
    t0 = time.time()
    solve_stages(r, s.sendall, g_rev, cover)
    print(f"[remote] xong {STAGES} stage ({time.time() - t0:.0f}s), cho flag...")
    print("[FLAG]", r.readall(timeout=10).decode(errors="replace"))


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "test"
    if mode == "test":
        cp1_decomposition()
        local_test()
    elif mode == "remote":
        remote(sys.argv[2], int(sys.argv[3]))
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
