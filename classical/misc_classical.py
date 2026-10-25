#!/usr/bin/env python3
"""Small encoders/decoders that CyberChef also covers — kept here for offline use.

    python misc_classical.py a1z26 "8 5 12 12 15"
    python misc_classical.py polybius "23 15 34 34 15"       # 5x5, I/J merged
    python misc_classical.py tapcode "43 15 11 44"           # tap code, no K
    python misc_classical.py morse "... --- ... / ... --- ..."
    python misc_classical.py bacon "AABBB ABABA ..."         # 24-letter Bacon
    python misc_classical.py railfence 3 "WECRLTEERDSOEEFEAOCAIVDEN"
    python misc_classical.py railfence_brute "ciphertext"
"""
import re
import sys

MORSE = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F',
    '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
    '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R',
    '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
    '-.--': 'Y', '--..': 'Z', '-----': '0', '.----': '1', '..---': '2',
    '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7',
    '---..': '8', '----.': '9', '.-.-.-': '.', '--..--': ',', '..--..': '?',
    '-..-.': '/', '-....-': '-', '-.--.': '(', '-.--.-': ')',
}
_ROWS = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'          # I/J merged (classic 5x5)
POLYBIUS = {f'{i + 1}{j + 1}': _ROWS[i * 5 + j] for i in range(5) for j in range(5)}
TAP = {k: ('C' if v == 'K' else v) for k, v in POLYBIUS.items()}  # tap code drops K
_ALPHA24 = 'ABCDEFGHIKLMNOPQRSTVWXYZ'        # Bacon: 24 letters (I/J, U/V merged)


def a1z26(text):
    return ''.join(chr(int(x) + 64) if 1 <= int(x) <= 26 else '?'
                   for x in re.findall(r'\d+', text))


def polybius(text):
    return ''.join(POLYBIUS.get(p, '?') for p in re.findall(r'[1-5][1-5]', text))


def tapcode(text):
    return ''.join(TAP.get(p, '?') for p in re.findall(r'[1-5][1-5]', text))


def morse(text):
    out = []
    for word in text.strip().split('/'):
        out.append(''.join(MORSE.get(tok, '?') for tok in word.split() if tok))
    return ' '.join(out)


def bacon(text):
    groups = re.findall(r'[ABab01]{5}', text.replace(' ', ''))
    out = []
    for g in groups:
        b = g.upper().replace('A', '0').replace('B', '1')
        v = int(b, 2)
        out.append(_ALPHA24[v] if v < len(_ALPHA24) else '?')
    return ''.join(out)


def railfence(rails, text):
    if rails < 2:
        return text
    pattern = list(range(rails)) + list(range(rails - 2, 0, -1))
    positions = [pattern[i % len(pattern)] for i in range(len(text))]
    order = sorted(range(len(text)), key=lambda i: positions[i])
    result = [''] * len(text)
    for pos, i in enumerate(order):
        result[i] = text[pos]
    return ''.join(result)


def railfence_brute(text, max_rails=10):
    for r in range(2, max_rails + 1):
        yield r, railfence(r, text)


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    mode, args = sys.argv[1], sys.argv[2:]
    if mode == 'a1z26':
        print(a1z26(args[0]))
    elif mode == 'polybius':
        print(polybius(args[0]))
    elif mode == 'tapcode':
        print(tapcode(args[0]))
    elif mode == 'morse':
        print(morse(args[0]))
    elif mode == 'bacon':
        print(bacon(args[0]))
    elif mode == 'railfence':
        print(railfence(int(args[0]), args[1]))
    elif mode == 'railfence_brute':
        for r, out in railfence_brute(args[0]):
            print(f'rails={r}: {out[:120]}')
    else:
        sys.exit(__doc__)


if __name__ == '__main__':
    main()
