import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from AES import AES_implemented

class NoShift(AES_implemented):
    # ghi de thanh ghi de, giong dung chall.py lam
    def _shift_rows(self): pass
    def _shift_rows_inv(self): pass

def diff(a, b):
    return sum(x != y for x, y in zip(a, b))

key = os.urandom(16)
P   = os.urandom(16)
P2  = bytes(b ^ 1 if i == 0 else b for i, b in enumerate(P))  # dao 1 byte

print("=" * 62)
print("THU 1: Dam vat (avalanche) - dao 1 byte plaintext")
print("=" * 62)
c_full = AES_implemented(key).encrypt(P), AES_implemented(key).encrypt(P2)
c_cut  = NoShift(key).encrypt(P), NoShift(key).encrypt(P2)
print(f"AES DU          : enc(P) vs enc(P^1bit) khac {diff(*c_full)}/16 byte ciphertext")
print(f"THIEU ShiftRows : enc(P) vs enc(P^1bit) khac {diff(*c_cut)}/16 byte ciphertext")

print()
print("=" * 62)
print("THU 2: So byte state khac nhau THEO TUNG VONG (dao 1 byte)")
print("=" * 62)

def rounds_trace(cls, pt):
    a = cls(key)
    a._state = a._transpose(pt)
    a._add_round_key(0)
    snaps = [bytes(a._state)]
    for rn in range(1, 10):
        a._sub_bytes(); a._shift_rows(); a._mix_columns(); a._add_round_key(rn)
        snaps.append(bytes(a._state))
    a._sub_bytes(); a._shift_rows(); a._add_round_key(10)
    snaps.append(bytes(a._state))
    return snaps

t_full = rounds_trace(AES_implemented, P), rounds_trace(AES_implemented, P2)
t_cut  = rounds_trace(NoShift, P), rounds_trace(NoShift, P2)
print(f"{'vong':5} {'CO ShiftRows':>14} {'THIEU ShiftRows':>17}")
for i in range(11):
    print(f"R{i:<4} {diff(t_full[0][i], t_full[1][i]):>12} {diff(t_cut[0][i], t_cut[1][i]):>15}")

print()
print("=" * 62)
print("THU 3: 4 nhom byte doc lap (thieu ShiftRows)")
print("=" * 62)
base = NoShift(key).encrypt(P)
aes  = NoShift(key)
for g in range(4):
    pt = bytearray(P); pt[4*g] ^= 1          # dao 1 byte trong nhom g
    ct = aes.encrypt(bytes(pt))
    changed = [i for i in range(16) if base[i] != ct[i]]
    print(f"dao byte {4*g} (nhom {g}) -> ciphertext chi thay doi tai: {changed}")
