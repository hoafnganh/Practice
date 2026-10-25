#!/usr/bin/env python3
"""Baudot / ITA2 (5-bit telegraph) decode & encode.

Tries all 4 interpretations (2 bit orders x 2 start states) because challenge
files rarely document them:

    python baudot.py decode bits.txt        # raw 0101... bits, spaces ignored
    python baudot.py decode "01010 00110"   # 5-bit groups or a continuous stream
    python baudot.py encode "HELLO WORLD"   # emits ITA2 bits (MSB first, ltrs mode)
    python baudot.py decode5 file.txt       # one 5-letter group per code (A=0..Z=25 style)
"""
import re
import sys

from _lib.cipherlib import read_input

ITA2 = {
    0b00000: ('\x00', '\x00'), 0b00001: ('E', '3'), 0b00010: ('\n', '\n'),
    0b00011: ('A', '-'), 0b00100: (' ', ' '), 0b00101: ('S', "'"),
    0b00110: ('I', '8'), 0b00111: ('U', '7'), 0b01000: ('\r', '\r'),
    0b01001: ('D', '$'), 0b01010: ('R', '4'), 0b01011: ('J', '\a'),
    0b01100: ('N', ','), 0b01101: ('F', '!'), 0b01110: ('C', ':'),
    0b01111: ('K', '('), 0b10000: ('T', '5'), 0b10001: ('Z', '"'),
    0b10010: ('L', ')'), 0b10011: ('W', '2'), 0b10100: ('H', '#'),
    0b10101: ('Y', '6'), 0b10110: ('P', '0'), 0b10111: ('Q', '1'),
    0b11000: ('O', '9'), 0b11001: ('B', '?'), 0b11010: ('G', '&'),
    0b11011: ('^F', '^F'), 0b11100: ('M', '.'), 0b11101: ('X', '/'),
    0b11110: ('V', ';'), 0b11111: ('^L', '^L'),  # ^F=FIGS shift, ^L=LTRS shift
}
LTRS, FIGS = 0b11111, 0b11011
REVERSE5 = {i: int(f'{i:05b}'[::-1], 2) for i in range(32)}


def decode_stream(bits, msb_first=True, start_ltrs=True):
    codes = []
    for i in range(0, len(bits) - 4, 5):
        raw = int(bits[i:i + 5], 2)
        codes.append(raw if msb_first else REVERSE5[raw])
    out, state = [], (0 if start_ltrs else 1)
    for code in codes:
        if code == LTRS:
            state = 0
            continue
        if code == FIGS:
            state = 1
            continue
        out.append(ITA2.get(code, ('\x1a', '\x1a'))[state])
    return ''.join(out)


def encode(text, msb_first=True):
    out, state = [], 0  # 0=LTRS
    for c in text.upper():
        code = None
        want = 0
        for b, (ltr, fig) in ITA2.items():
            if c == ltr:
                code, want = b, 0
                break
            if c == fig:
                code, want = b, 1
                break
        if code is None:
            continue
        if want != state:
            out.append(LTRS if want == 0 else FIGS)
            state = want
        out.append(code)
    bits = ''.join(f'{b:05b}' if msb_first else f'{REVERSE5[b]:05b}' for b in out)
    return bits


def decode5(text):
    """Alternative reading: each 5-char group is a letter index (A=0, B=1, ...)."""
    groups = re.findall(r'[01]{5}', ''.join(text.split()))
    return ''.join(chr(int(g, 2) + ord('A')) for g in groups)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    data = read_input(sys.argv[2]) if len(sys.argv) > 2 else sys.stdin.read()
    if mode == 'encode':
        print(encode(data))
        return
    if mode == 'decode5':
        print(decode5(data))
        return
    bits = re.sub(r'[^01]', '', data)
    for msb in (True, False):
        for ltrs in (True, False):
            label = f"[{'MSB' if msb else 'LSB'} first, start {'LTRS' if ltrs else 'FIGS'}]"
            print(f'{label} {decode_stream(bits, msb, ltrs)[:160]}')


if __name__ == '__main__':
    main()
