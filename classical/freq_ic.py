#!/usr/bin/env python3
"""Triage an unknown ciphertext: is it transposition/substitution/polyalphabetic?

Usage:
    python freq_ic.py ciphertext.txt
    python freq_ic.py "KHOOR ZRUOG"
    type ciphertext.txt | python freq_ic.py -

Prints printable ratio, letter stats, IC, chi-squared and a suggestion of the
cipher family — the offline replacement for eyeballing on dCode.
"""
import sys
from collections import Counter

from _lib.cipherlib import (ENGLISH_IC, PRINTABLE, avg_column_ic, chi_squared,
                            index_of_coincidence, only_letters, read_input)


def analyze(text):
    letters = only_letters(text)
    n = len(letters)
    printable = sum(1 for c in text if c in PRINTABLE) / max(len(text), 1)
    ic = index_of_coincidence(text)
    chi = chi_squared(text)
    counts = Counter(letters)
    top = ', '.join(f'{c}:{v * 100 // max(n, 1)}%' for c, v in counts.most_common(6))
    charset = 'ascii-extended' if any(ord(c) > 126 for c in text) else 'ascii'
    report = [
        f'length: {len(text)} (letters: {n})   charset: {charset}   printable: {printable:.1%}',
        f'top letters: {top}',
        f'IC: {ic:.4f}   chi2-vs-english: {chi:.1f}',
    ]
    if charset == 'ascii' and printable < 0.6:
        report.append('>> many non-printables -> NOT a text cipher; try XOR / encodings (baudot, base-x)')
    elif ic >= 0.060:
        report.append('>> IC high (~English) -> mono substitution / transposition / Caesar-ROT family')
        report.append('   next: rot_family.py, then substitution_hillclimb.py')
    elif ic >= 0.048:
        report.append('>> IC middle -> short text or polyalphabetic with short key')
        report.append('   next: vigenere_keyless.py')
    else:
        best = sorted(range(1, 21), key=lambda p: -avg_column_ic(text, p))[:3]
        report.append(f'>> IC low (flat) -> polyalphabetic (Vigenere) or XOR multi-byte; candidate periods: {best}')
        report.append('   next: vigenere_keyless.py, xor_tool.py')
    groups5 = n % 5 == 0 and all(len(w) == 5 for w in text.split() if w) if text.split() else False
    if groups5 and set(text) <= set('01'):
        report.append('>> binary text, multiple of 5 -> try baudot.py (5-bit ITA2)')
    elif len(set(text)) <= 33 and set(text) <= set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
        report.append('>> digits/letters only: try a1z26 / polybius / adfgvx / base32 (misc_classical.py)')
    return '\n'.join(report)


if __name__ == '__main__':
    data = read_input(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin.read()
    print(analyze(data))
