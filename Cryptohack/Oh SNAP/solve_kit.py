#!/usr/bin/env python3
# Oh SNAP solved with oracle_kit.HttpOracle + crypto-attacks fms.attack.
# Challenge-specific code = the two configs below + the length probe; the rest
# (session pool, retries, caching, 32-thread prefetch) comes from the kit.

import sys

sys.path.insert(0, r'E:\Jeopardy')
sys.path.insert(0, r'E:\Jeopardy\crypto-attacks')

from attacks.rc4.fms import attack
from oracle_kit import HttpOracle


def parse(r):
    """Response -> leaked keystream byte, or None when the query was invalid."""
    try:
        j = r.json()
    except ValueError:
        return None
    err = j.get('error', '') if isinstance(j, dict) else ''
    return bytes.fromhex(err[17:]) if err.startswith('Unknown command: ') else None


oracle = HttpOracle(
    url_template='https://aes.cryptohack.org/oh_snap/send_cmd/{ct}/{nonce}/',
    parse=parse,
)

# 1) flag length: largest nonce that still fits RC4's 256-byte key limit
lo, hi = 0, 254
while lo + 1 < hi:
    mid = (lo + hi) // 2
    if oracle(ct=b'\x00', nonce=b'\x00' * mid) is not None:
        lo = mid
    else:
        hi = mid
flag_len = 256 - lo
print('flag length =', flag_len, flush=True)

# 2) prefetch every iv fms.attack will ever ask: (a+3, 255, x)
print(f'prefetching {flag_len * 256} queries...', flush=True)
oracle.prefetch([dict(ct=b'\x00', nonce=bytes([a + 3, 255, x]))
                 for a in range(flag_len) for x in range(256)])

# 3) adapter to the library contract. RC4 XOR symmetry: the server leaks
#    decrypt(b'\x00') == keystream == ciphertext of b'\x00'.
def encrypt_oracle(iv, plaintext):
    assert plaintext == b'\x00'
    return oracle(ct=b'\x00', nonce=bytes(iv))   # bytes(iv): fms passes bytearray

flag = attack(encrypt_oracle, flag_len)
print('FLAG:', flag.decode())
