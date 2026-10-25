#!/usr/bin/env python3
"""Vigenere solver: finds the KEY LENGTH (IC) and the KEY (chi-squared per column)
with no crib — the offline replacement for dCode's Vigenere auto-solver.
Assumes English plaintext.

Usage:
    python vigenere_keyless.py ciphertext.txt
    python vigenere_keyless.py "Lxfopv Ef Rnhrh"
    python vigenere_keyless.py --keylen 7 ciphertext.txt   # force a length
    python vigenere_keyless.py --key LEMON ciphertext.txt  # plain decrypt
    type ct.txt | python vigenere_keyless.py -
"""
import sys

from _lib.cipherlib import (avg_column_ic, chi_squared, only_letters,
                            read_input, substring_word_score, vigenere)

ENGLISH = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966,
           0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987,
           6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074]


def solve_column(col):
    """Best Caesar shift for one Vigenere column (decryption shift)."""
    n = len(col)
    best = (float('inf'), 0)
    for k in range(26):
        # plaintext letter j comes from ciphertext letter (j + k) mod 26
        chi = sum((col.count(chr((j + k) % 26 + 65)) - ENGLISH[j] * n / 100.0) ** 2
                  / max(ENGLISH[j], 0.01) for j in range(26))
        if chi < best[0]:
            best = (chi, k)
    return best[1]


def solve_key(cipher, keylen):
    t = only_letters(cipher)
    return ''.join(chr(solve_column(t[i::keylen]) + 65) for i in range(keylen))


def keyless(cipher, max_period=30, ic_margin=0.01):
    """Textbook selection: any multiple of the true period also shows high column
    IC (its columns are subsets of true key classes), so take the SMALLEST
    period whose average column IC comes within `ic_margin` of the best."""
    t = only_letters(cipher)
    limit = min(max_period, len(t) // 8)
    scored = sorted(((avg_column_ic(t, p), p) for p in range(1, limit + 1)),
                    reverse=True)
    best_ic = scored[0][0]
    passing = sorted(p for ic, p in scored if ic >= best_ic - ic_margin)
    print(f'candidate key lengths (IC order): {passing}')
    best = None
    for p in passing[:6]:
        key = solve_key(t, p)
        plain = vigenere(t, key, decrypt=True)
        if best is None:
            best = (p, key, plain)  # smallest passing period wins
        print(f'\n[word_score={substring_word_score(plain)}] len={p} key={key}')
        print(f'  {plain[:200]}')
    return best[1], best[2]


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    key = keylen = None
    if '--key' in args:
        i = args.index('--key')
        key = args[i + 1]
        del args[i:i + 2]
    if '--keylen' in args:
        i = args.index('--keylen')
        keylen = int(args[i + 1])
        del args[i:i + 2]
    data = read_input(args[0])
    if key:
        print(vigenere(data, key, decrypt=True))
    elif keylen:
        t = only_letters(data)
        k = solve_key(t, keylen)
        print(f'key={k}\n{vigenere(t, k, decrypt=True)}')
    else:
        keyless(data)
