#!/usr/bin/env python3
"""Recover a CUSTOM Base64 alphabet from a known plaintext/ciphertext pair,
then decode the target ciphertext.

Works when the encoder is standard base64 (same grouping/padding) but with a
permuted 64-char alphabet. Pad '=' is kept as-is.

Usage:
    python custom_b64_recover.py --known-plain "known text" \
        --known-cipher "1a2B..." --target "XYz..."
"""
import argparse
import base64
import string

STD = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'


def recover(known_plain, known_cipher, target):
    kb = known_plain if isinstance(known_plain, (bytes, bytearray)) \
        else known_plain.encode('utf-8')
    ref = base64.b64encode(kb).decode().rstrip('=')
    obs = known_cipher.rstrip('=')
    if len(ref) != len(obs):
        raise SystemExit(f'length mismatch: standard-encode of known plain = {len(ref)} '
                         f'chars, observed = {len(obs)} chars (encoder not plain base64?)')
    mapping, conflicts = {}, []
    for s, o in zip(ref, obs):
        if s in mapping and mapping[s] != o:
            conflicts.append((s, mapping[s], o))
        mapping[s] = o
    pad = ''
    if known_cipher.endswith('='):
        pad = '=' * (len(known_cipher) - len(known_cipher.rstrip('=')))
    mapped = set(mapping.values())
    unknown = [c for c in STD if c not in mapping and c not in mapped]
    print(f'recovered {len(mapping)} alphabet positions; '
          f'{len(conflicts)} conflicts; {len(unknown)} unseen standard chars: '
          f'{"".join(unknown) if unknown else "-"}')
    if conflicts:
        print(f'CONFLICTS (standard char -> multiple observed): {conflicts[:10]}')
        print('encoder is NOT a simple permutation; this mapping may be wrong.')
    # translate TARGET from custom-alphabet space back to standard space
    rev = {o: s for s, o in mapping.items()}
    normalized = target.rstrip('=').translate(str.maketrans(rev)) + pad
    normalized += '=' * (-len(normalized) % 4)
    return base64.b64decode(normalized)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--known-plain', required=True)
    ap.add_argument('--known-cipher', required=True)
    ap.add_argument('--target', required=True)
    a = ap.parse_args()
    out = recover(a.known_plain, a.known_cipher, a.target)
    print('--- decoded target ---')
    try:
        print(out.decode('utf-8'))
    except UnicodeDecodeError:
        print(out)
