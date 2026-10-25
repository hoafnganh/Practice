#!/usr/bin/env python3
"""Brute-force the whole Caesar/ROT/Atbash/Affine family and rank by English-likeness.

Usage:
    python rot_family.py "RJXXFJ AY"          # tries rot 0..25, rot47, atbash, affine
    python rot_family.py ciphertext.txt
"""
import sys

from _lib.cipherlib import (affine, atbash, caesar_shift, chi_squared,
                            english_score, read_input, word_coverage)


def combined_score(text):
    """Sort key: most dictionary words first, then best chi-squared."""
    return (-word_coverage(text), chi_squared(text))


def rank(label_results, top=8, extra_note=''):
    scored = sorted(((combined_score(p), label, p) for label, p in label_results))
    for (cov, chi), label, p in scored[:top]:
        print(f'[words {-cov:4.0%} chi {chi:6.1f}] {label:<14} {p[:100]}')
    if extra_note:
        print(extra_note)


def rot47_shift(text, k):
    return ''.join(chr(33 + ((ord(c) - 33 + k) % 94)) if 33 <= ord(c) <= 126 else c
                   for c in text)


def main(data):
    print('--- Caesar/ROT-N (letters) ---')
    rank([(f'ROT-{k:02d}', caesar_shift(data, k)) for k in range(26)])

    print('--- ROT47 family (ascii 33..126, all shifts) ---')
    rank([(f'ROT47+{k:02d}', rot47_shift(data, k)) for k in range(94)], top=3)

    print('--- Atbash ---')
    rank([('atbash', atbash(data))], top=1)

    print('--- Affine (a,b) best 4 ---')
    affines = []
    for a in (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25):
        for b in range(26):
            if (a, b) == (1, 0):
                continue
            try:
                affines.append((f'affine {a},{b}', affine(data, a, b)))
            except ValueError:
                pass
    rank(affines, top=4)

    print(f'(plain english_score={english_score(data):.2f}; '
          f'read candidates whose output looks like words — score is just a hint)')


if __name__ == '__main__':
    data = read_input(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin.read()
    main(data)
