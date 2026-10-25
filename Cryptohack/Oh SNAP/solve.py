import sys
from concurrent.futures import ThreadPoolExecutor

import requests

sys.path.insert(0, r"E:\Jeopardy\crypto-attacks")
from fms import attack  # noqa: E402

BASE = 'https://aes.cryptohack.org/oh_snap/send_cmd'

session = requests.Session()
adapter = requests.adapters.HTTPAdapter(pool_connections=32, pool_maxsize=32)
session.mount('https://', adapter)


def leak(nonce, ciphertext=b'\x00'):
    """Server 'decrypts' ciphertext under ARC4(nonce || FLAG) and leaks the
    result -> for RC4 this IS the ciphertext of that plaintext."""
    for _ in range(5):
        try:
            r = session.get(f'{BASE}/{ciphertext.hex()}/{nonce.hex()}/', timeout=15)
            if r.status_code != 200:
                return None
            err = r.json().get('error', '')
            if err.startswith('Unknown command: '):
                return bytes.fromhex(err[17:])
            return None
        except requests.RequestException:
            continue
    raise RuntimeError('network failure')


def probe_flag_length():
    # ARC4.new raises (-> HTTP 500) when len(nonce) + len(FLAG) > 256
    lo, hi = 0, 254
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if leak(b'\x00' * mid) is not None:
            lo = mid
        else:
            hi = mid
    return 256 - lo


flag_len = probe_flag_length()
# Code chạy đa luồng
ivs = [bytes([a + 3, 255, x]) for a in range(flag_len) for x in range(256)]
with ThreadPoolExecutor(max_workers=32) as ex:
    results = list(ex.map(leak, ivs))
cache = dict(zip(ivs, results))


def encrypt_oracle(iv, plaintext):
    assert plaintext == b'\x00'
    return cache[bytes(iv)]  # iv arrives as bytearray -> unhashable as-is


flag = attack(encrypt_oracle, flag_len)
print('FLAG:', flag.decode())
