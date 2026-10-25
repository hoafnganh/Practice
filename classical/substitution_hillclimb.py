#!/usr/bin/env python3
"""Monoalphabetic substitution solver: hill-climbing with quadgram statistics.

Needs english_quadgrams.txt next to this script (already downloaded from the
practicalcryptography.com mirror). Works on letters-only text; non-letters are
stripped. Run several times if the first attempt stalls (random restarts).

Usage:
    python substitution_hillclimb.py ciphertext.txt
    python substitution_hillclimb.py "ciphertext string"
"""
import os
import random
import string
import sys

from _lib.cipherlib import only_letters

QUAD_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'english_quadgrams.txt')
ALPHABET = string.ascii_uppercase


def load_quadgrams():
    table = {}
    total = 0
    with open(QUAD_FILE, encoding='utf-8') as fh:
        for line in fh:
            parts = line.split()
            if len(parts) != 2:
                continue
            count = int(parts[1])
            table[parts[0]] = count
            total += count
    logt = {}
    for k, v in table.items():
        logt[k] = __import__('math').log10(v / total)
    floor = __import__('math').log10(0.01 / total)
    return logt, floor


def make_scorer(quad, floor):
    def score(text):
        t = only_letters(text)
        s = 0.0
        for i in range(len(t) - 3):
            s += quad.get(t[i:i + 4], floor)
        return s / max(len(t) - 3, 1)
    return score


def apply_key(text, key):
    """key maps A..Z -> chosen cipher-plain letters; text is letters-only."""
    table = str.maketrans(ALPHABET, key)
    return text.translate(table)


def hillclimb(cipher, score, restarts=12, steps=3000):
    t = only_letters(cipher)
    best_overall = (float('-inf'), None, '')
    for _ in range(restarts):
        key = list(ALPHABET)
        random.shuffle(key)
        key = ''.join(key)
        best = (score(apply_key(t, key)), key)
        improved = True
        it = 0
        while improved and it < steps:
            improved = False
            it += 1
            for i in range(25):
                for j in range(i + 1, 26):
                    cand = list(best[1])
                    cand[i], cand[j] = cand[j], cand[i]
                    cand = ''.join(cand)
                    s = score(apply_key(t, cand))
                    if s > best[0]:
                        best = (s, cand)
                        improved = True
            if best[0] > best_overall[0]:
                best_overall = (best[0], best[1], apply_key(t, best[1]))
    return best_overall


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    data = open(args[0], encoding='utf-8', errors='replace').read() \
        if os.path.exists(args[0]) else args[0]
    if not os.path.exists(QUAD_FILE):
        sys.exit(f'missing {QUAD_FILE} — see README to re-download it')
    quad, floor = load_quadgrams()
    scorer = make_scorer(quad, floor)
    s, key, plain = hillclimb(data, scorer)
    print(f'score={s:.4f}')
    print(f'cipher->plain key: {key}')
    print(plain[:600])
