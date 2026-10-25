#!/usr/bin/env python3
"""XOR tool: single-byte brute and multi-byte key recovery (repeating-key).

    python xor_tool.py single ct.txt
    python xor_tool.py single "1b37373331363f78151b7f2b783431333d"
    python xor_tool.py multi ct.txt            # repeating-key, auto keysize 2..40
    python xor_tool.py multi --keylen 11 ct.txt
"""
import argparse
import base64
import binascii
import sys

from _lib.cipherlib import english_score

PLAIN_PREF = (' the ', ' flag', 'FLAG{', 'flag{', ' and ', 'ing ')


def to_bytes(s):
    s = s.strip()
    try:
        return binascii.unhexlify(s)
    except (binascii.Error, ValueError):
        pass
    if all(c in '0123456789abcdefABCDEF \n' for c in s) and len(s.replace('\n', '').replace(' ', '')) % 2 == 0:
        return binascii.unhexlify(''.join(s.split()))
    try:
        return base64.b64decode(s, validate=True)
    except Exception:
        return s.encode('latin-1')


def xor(data, key):
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def single(data, top=6):
    scored = []
    for k in range(256):
        out = bytes(b ^ k for b in data)
        bonus = sum(out.count(p.encode()) for p in (' the ', ' flag', '{', '}', 'flag'))
        scored.append((english_score(out.decode('latin-1')) + bonus * 0.05, k, out))
    scored.sort(reverse=True)
    for s, k, out in scored[:top]:
        print(f'[{s:.3f}] key=0x{k:02x} ({k:3d} {chr(k) if 32 <= k < 127 else "?"!r}) '
              f'{out[:120]!r}')


def hamming(a, b):
    return sum(bin(x ^ y).count('1') for x, y in zip(a, b))


def keysize_candidates(data, lo=2, hi=40, top=4):
    ranked = []
    for ks in range(lo, min(hi, len(data) // 4) + 1):
        blocks = [data[i:i + ks] for i in range(0, len(data) - ks + 1, ks)][:6]
        if len(blocks) < 2:
            continue
        dists = [hamming(blocks[i], blocks[j]) / ks
                 for i in range(len(blocks)) for j in range(i + 1, len(blocks))]
        ranked.append((sum(dists) / len(dists), ks))
    return sorted(ranked)[:top]


def solve_key_column(col):
    best = (float('-inf'), 0)
    for k in range(256):
        out = bytes(b ^ k for b in col)
        s = english_score(out.decode('latin-1'))
        if s > best[0]:
            best = (s, k)
    return best


def multi(data, keylen=None):
    cands = [keylen] if keylen else [ks for _, ks in keysize_candidates(data)]
    for ks in cands:
        key = bytes(solve_key_column(data[i::ks])[1] for i in range(ks))
        out = xor(data, key)
        print(f'--- keylen={ks} key={key!r} score={english_score(out.decode("latin-1")):.2f}')
        print(f'    {out[:200]!r}')


def _isfile(p):
    import os
    return os.path.isfile(p)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['single', 'multi'])
    ap.add_argument('input', help='file path or hex/base64/raw string ("-" = stdin)')
    ap.add_argument('--keylen', type=int)
    a = ap.parse_args()
    data = open(a.input, 'rb').read() if _isfile(a.input) else to_bytes(
        sys.stdin.read() if a.input == '-' else a.input)
    (single if a.mode == 'single' else multi)(data, a.keylen)
