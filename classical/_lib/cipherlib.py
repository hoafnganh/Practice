"""Shared helpers for the classical-cipher toolkit. Stdlib only.

Run tests:  python _verify_all.py   (from the classical/ folder)
"""
import math
import os
import re
import string
import sys
from collections import Counter

UPPER = string.ascii_uppercase
ENGLISH_FREQ = {  # percent
    'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702, 'F': 2.228,
    'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153, 'K': 0.772, 'L': 4.025,
    'M': 2.406, 'N': 6.749, 'O': 7.507, 'P': 1.929, 'Q': 0.095, 'R': 5.987,
    'S': 6.327, 'T': 9.056, 'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150,
    'Y': 1.974, 'Z': 0.074,
}
ENGLISH_IC = 0.0667
PRINTABLE = set(string.printable[:-5])  # no trailing \t\n\r\x0b\x0c


def read_input(arg):
    """arg is a file path, '-' for stdin, or the ciphertext text itself."""
    if arg == '-':
        return sys.stdin.read()
    if os.path.exists(arg):
        return open(arg, encoding='utf-8', errors='replace').read()
    return arg


def only_letters(text, keep_case=False):
    t = text.upper() if not keep_case else text
    return ''.join(c for c in t if c.upper() in UPPER)


def index_of_coincidence(text):
    """IC of the letters in text (0..1). English mono-substitution ~0.066,
    flat/random ~0.038, polyalphabetic trends toward flat."""
    t = only_letters(text)
    n = len(t)
    if n < 2:
        return 0.0
    counts = Counter(t)
    total = sum(c * (c - 1) for c in counts.values())
    return total / (n * (n - 1))


def chi_squared(text):
    """Chi-squared of letter distribution vs English (lower = more English)."""
    t = only_letters(text)
    n = len(t)
    if n == 0:
        return float('inf')
    counts = Counter(t)
    chi = 0.0
    for letter in UPPER:
        expected = ENGLISH_FREQ[letter] * n / 100.0
        chi += (counts.get(letter, 0) - expected) ** 2 / max(expected, 0.01)
    return chi


def english_score(text):
    """Quick heuristic English-likeness in [0,1]: letters+digits+space/punct mix."""
    if not text:
        return 0.0
    good = sum(1 for c in text if c.isalnum() or c in " ._-'{}!?;:,()/")
    printable = sum(1 for c in text if c in PRINTABLE)
    return (0.7 * good + 0.3 * printable) / len(text)


def avg_column_ic(text, period):
    """Average IC across the columns of a given period (Vigenere key length)."""
    t = only_letters(text)
    if len(t) < period * 4:
        return 0.0
    vals = []
    for i in range(period):
        col = t[i::period]
        if len(col) > 1:
            vals.append(index_of_coincidence(col))
    return sum(vals) / len(vals) if vals else 0.0


def best_key_periods(text, max_period=30, top=6):
    """Rank candidate Vigenere key lengths by how close column IC is to English."""
    t = only_letters(text)
    scored = []
    for p in range(1, min(max_period, len(t) // 8) + 1):
        scored.append((abs(avg_column_ic(t, p) - ENGLISH_IC), p))
    scored.sort()
    # prefer smallest period when several multiples of the true one all score well
    picked, out = [], []
    for _, p in scored:
        if any(p % q == 0 for q in picked):
            continue
        picked.append(p)
        out.append(p)
        if len(out) >= top:
            break
    return out


def caesar_shift(text, k):
    out = []
    for c in text:
        if 'A' <= c <= 'Z':
            out.append(chr((ord(c) - 65 - k) % 26 + 65))
        elif 'a' <= c <= 'z':
            out.append(chr((ord(c) - 97 - k) % 26 + 97))
        else:
            out.append(c)
    return ''.join(out)


def vigenere(text, key, decrypt=True):
    """Classic Vigenere over letters only; non-letters pass through untouched."""
    k = only_letters(key)
    if not k:
        return text
    out, i = [], 0
    for c in text:
        if c.upper() in UPPER:
            base = 65 if c.isupper() else 97
            kk = ord(k[i % len(k)]) - 65
            shift = kk if not decrypt else -kk
            out.append(chr((ord(c) - base + shift) % 26 + base))
            i += 1
        else:
            out.append(c)
    return ''.join(out)


def rot47(text):
    return ''.join(chr(33 + ((ord(c) - 33 + 47) % 94)) if 33 <= ord(c) <= 126 else c
                   for c in text)


def atbash(text):
    out = []
    for c in text:
        if c.upper() in UPPER:
            base = 65 if c.isupper() else 97
            out.append(chr(base + 25 - (ord(c) - base)))
        else:
            out.append(c)
    return ''.join(out)


def affine(text, a, b, decrypt=True):
    if math.gcd(a, 26) != 1:
        raise ValueError('a must be coprime with 26')
    a_inv = pow(a, -1, 26)
    out = []
    for c in text:
        if c.upper() in UPPER:
            base = 65 if c.isupper() else 97
            x = ord(c) - base
            out.append(chr(base + (a_inv * (x - b) if decrypt else a * x + b) % 26))
        else:
            out.append(c)
    return ''.join(out)


ENGLISH_WORDS = frozenset("""
the be to of and a in that have i it for not on with he as you do at this but his
by from they we say her she or an will my one all would there their what so up out
if about who get which go me when make can like time no just him know take people
into year your good some could them see other than then now look only come its over
think also back after use two how our work first well way even new want because any
these give day most us is are was were been has had flag the you your secret message
cipher key text encryption decrypt code secretcode hidden attack signal traffic enemy
is are this that with have from
password secret flag found hello world example test sample result final answer value
number letter figure symbol plain plaintext ciphertext shift substitution polyalphabetic
""".split())

WORDBREAK = re.compile(r'[A-Za-z]+')


def word_coverage(text):
    """Fraction of alphabetic tokens found in the embedded mini wordlist."""
    words = WORDBREAK.findall(text)
    if not words:
        return 0.0
    hits = sum(1 for w in words if w.lower() in ENGLISH_WORDS)
    return hits / len(words)


def substring_word_score(text):
    """For letters-only (spaceless) text: total length of mini-wordlist words
    found as substrings. Longer hits dominate, so real English outranks noise."""
    t = text.upper()
    return sum(len(w) for w in ENGLISH_WORDS if len(w) >= 2 and w.upper() in t)
