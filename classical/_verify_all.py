#!/usr/bin/env python3
"""Self-test every tool in the classical/ toolkit. Run from the classical/ folder:

    python _verify_all.py
"""
import base64
import os
import random
import string
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _lib.cipherlib import (affine, atbash, caesar_shift, chi_squared,
                            english_score, index_of_coincidence, rot47,
                            vigenere, word_coverage)

PASS = 0
FAIL = 0


def check(name, cond, detail=''):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f'  PASS  {name}')
    else:
        FAIL += 1
        print(f'  FAIL  {name}  {detail}')


PLAIN = ('THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG AND THIS IS A SOMEWHAT '
         'LONGER ENGLISH SENTENCE WITH COMMON WORDS TO MAKE STATISTICS WORK')

print('== _lib/cipherlib ==')
check('caesar roundtrip', caesar_shift(caesar_shift(PLAIN, 7), -7) == PLAIN)
check('vigenere roundtrip',
      vigenere(vigenere(PLAIN, 'LEMON', decrypt=False), 'LEMON') == PLAIN)
check('atbash self-inverse', atbash(atbash(PLAIN)) == PLAIN)
check('rot47 self-inverse', rot47(rot47('Hello FLAG{abc_123}!')) == 'Hello FLAG{abc_123}!')
check('affine roundtrip',
      affine(affine(PLAIN, 7, 11, decrypt=False), 7, 11) == PLAIN)
check('IC english > flat', index_of_coincidence(PLAIN) > 0.05 >
      index_of_coincidence(''.join(string.ascii_uppercase * 10)))
check('chi2 english < shift', chi_squared(PLAIN) < chi_squared(caesar_shift(PLAIN, 13)))
check('word_coverage hits english', word_coverage('the flag is here') > 0.7)

print('== rot_family ==')
from rot_family import combined_score  # noqa: E402
ct = caesar_shift(PLAIN, -11)          # encrypt: shift FORWARD 11
cands = [(combined_score(caesar_shift(ct, k)), k) for k in range(26)]
check('rot brute finds shift 11', min(cands)[1] == 11, f'got {min(cands)}')
r47 = rot47(PLAIN[:40])
check('rot47 undo scores better', combined_score(rot47(r47)) < combined_score(r47))

print('== vigenere_keyless ==')
import vigenere_keyless as vk  # noqa: E402
long_plain = (PLAIN + ' ') * 6
ct = vigenere(long_plain, 'PATTERN', decrypt=False)
solved_key, plain = vk.keyless(ct)
check('vigenere keyless: key length 7', len(solved_key) == 7, f'key={solved_key}')
from _lib.cipherlib import substring_word_score  # noqa: E402
check('vigenere keyless: plaintext readable', substring_word_score(plain) > 40,
      plain[:80])

print('== custom_b64_recover ==')
import custom_b64_recover as cb  # noqa: E402
std_alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
alphabet = list(std_alphabet)
random.Random(42).shuffle(alphabet)
custom = ''.join(alphabet)
# known pair covering ALL 64 symbols -> complete bijection (like several known
# plaintext segments concatenated together)
known_plain_bytes = base64.b64decode(std_alphabet)
known_cipher = std_alphabet.translate(str.maketrans(std_alphabet, custom))
target_plain = 'FLAG{custom_alphabet_recovered}'
target_cipher = base64.b64encode(target_plain.encode()).decode().translate(
    str.maketrans(std_alphabet, custom))
out = cb.recover(known_plain_bytes, known_cipher, target_cipher)
check('custom b64 recovers target', out.decode('utf-8', 'replace') == target_plain,
      f'got {out!r}')

print('== baudot ==')
import baudot as bd  # noqa: E402
bits = bd.encode('HELLO WORLD 123')
check('baudot encode->decode (MSB, LTRS start)',
      bd.decode_stream(bits, msb_first=True, start_ltrs=True) == 'HELLO WORLD 123')
check('baudot wrong reading differs',
      bd.decode_stream(bits, msb_first=False, start_ltrs=True) != 'HELLO WORLD 123')
check('baudot decode5', bd.decode5('00000 00101') == 'AF')

print('== xor_tool ==')
import xor_tool as xt  # noqa: E402
key = bytes([0x2a, 0x13, 0x99])
pt = (b'The flag is FLAG{xor_repeating_key_found} and the rest is padding '
      b'to make sure several blocks are present for statistics to work well.')
data = xt.xor(pt, key)
best_key = bytes(xt.solve_key_column(data[i::3])[1] for i in range(3))
check('xor multi recovers key', best_key == key, f'got {best_key!r} want {key!r}')
check('xor to_bytes hex path', xt.to_bytes(data.hex()) == data)

print('== misc_classical ==')
import misc_classical as mc  # noqa: E402
check('a1z26', mc.a1z26('8 5 12 12 15') == 'HELLO')
check('polybius', mc.polybius('23 15 31 31 34') == 'HELLO')
check('morse', mc.morse('... --- ... / .... . .-.. .-.. ---') == 'SOS HELLO')
check('bacon', mc.bacon('ABABA ABBAB BAABB AABAA') == 'LOVE')
RF_CT = 'WECRLTEERDSOEEFEAOCAIVDEN'          # wikipedia rail fence example
check('railfence 3 known vector', mc.railfence(3, RF_CT) == 'WEAREDISCOVEREDFLEEATONCE')
check('railfence brute finds it', 'WEAREDISCOVEREDFLEEATONCE' in
      [out for _, out in mc.railfence_brute(RF_CT)])

print('== CLI smoke tests (each tool once with inline text) ==')
import subprocess  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def run_cli(args, stdin=None):
    return subprocess.run([sys.executable] + args, input=stdin,
                          capture_output=True, text=True, cwd=HERE)


r = run_cli(['rot_family.py', 'KHOOR ZRUOG'])
check('rot_family inline arg', r.returncode == 0 and 'Caesar' in r.stdout,
      r.stderr[-200:])
r = run_cli(['rot_family.py', '-'], stdin='KHOOR ZRUOG')
check('rot_family stdin -', r.returncode == 0, r.stderr[-200:])

tmp = os.path.join(HERE, '_tmp_ct.txt')
with open(tmp, 'w', encoding='utf-8') as fh:
    fh.write('KHOOR ZRUOG')
r = run_cli(['rot_family.py', tmp])
check('rot_family file path', r.returncode == 0 and 'Caesar' in r.stdout,
      r.stderr[-200:])
r = run_cli(['freq_ic.py', tmp])
check('freq_ic file path', r.returncode == 0 and 'IC:' in r.stdout,
      r.stderr[-200:])
r = run_cli(['freq_ic.py', 'KHOOR ZRUOG'])
check('freq_ic inline arg', r.returncode == 0, r.stderr[-200:])
os.remove(tmp)

ct = vigenere('ATTACK AT DAWN ' * 4, 'LEMON', decrypt=False)
r = run_cli(['vigenere_keyless.py', ct])
check('vigenere inline recovers LEMON', r.returncode == 0 and 'LEMON' in r.stdout.upper(),
      (r.stdout + r.stderr)[-200:])

enc = run_cli(['baudot.py', 'encode', 'HELLO WIFI'])
r = run_cli(['baudot.py', 'decode', '-'], stdin=enc.stdout.strip())
check('baudot encode inline / decode stdin', r.returncode == 0 and 'HELLO WIFI' in r.stdout,
      r.stdout[:160] + r.stderr[-200:])

r = run_cli(['xor_tool.py', 'single',
             xt.xor(b'the flag is here and some more text to score against',
                    b'\x2a').hex()])
check('xor_tool single inline hex', r.returncode == 0, r.stderr[-200:])

r = run_cli(['misc_classical.py', 'a1z26', '8 5 12 12 15'])
check('misc a1z26 inline', r.returncode == 0 and 'HELLO' in r.stdout, r.stderr[-200:])

SMOKE_PLAIN = 'smoke test forty two with some words'
SMOKE_B64 = base64.b64encode(SMOKE_PLAIN.encode()).decode()
r = run_cli(['custom_b64_recover.py', '--known-plain', SMOKE_PLAIN,
             '--known-cipher', SMOKE_B64, '--target', SMOKE_B64])
check('custom_b64 identity roundtrip', r.returncode == 0 and SMOKE_PLAIN in r.stdout,
      r.stdout[-200:] + r.stderr[-200:])

if os.path.exists(os.path.join(HERE, 'english_quadgrams.txt')):
    r = run_cli(['substitution_hillclimb.py', caesar_shift(PLAIN[:80], -5)])
    check('substitution_hillclimb inline arg', r.returncode == 0 and 'score=' in r.stdout,
          r.stderr[-200:])
else:
    check('substitution_hillclimb quadgram file', False, 'english_quadgrams.txt missing')

print(f'\n{PASS} passed, {FAIL} failed')
sys.exit(1 if FAIL else 0)
