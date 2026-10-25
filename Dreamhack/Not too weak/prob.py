#! /usr/bin/env python3
import os
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad

with open('flag', 'rb') as f:
    FLAG = f.read()
IV = os.urandom(8)
USED_KEYS = []

def menu():
    print("1. Encrypt message")
    print("2. Encrypt flag")
    print("3. Exit")

def bye(m):
    print(m)
    exit()

def chk_key(key):
    if len(key) != 8:
        return False
    if key in USED_KEYS:
        return False
    return True

def xor(a,b):
    return bytes([x^y for x,y in zip(a,b)])

def encrypt(k, m):
    cipher = DES.new(k, mode=DES.MODE_ECB)
    m = pad(m, 8)
    m = xor(m, IV*(len(m)//8))
    c = cipher.encrypt(m)
    c = xor(c, IV*(len(c)//8))
    return c # m -> m' -> DES -> c' -> c

if __name__ == "__main__":
    while True:
        menu()
        i = int(input("> "))
        if i == 1:
            key = bytes.fromhex(input("key(hex)> "))
            if not chk_key(key):
                bye("invalid key")
            USED_KEYS.append(key)
            msg = bytes.fromhex(input("msg(hex)> "))
            enc = encrypt(key, msg)
            print(f'enc(hex)> {enc.hex()}')
        elif i == 2:
            key = bytes.fromhex(input("key(hex)> "))
            if not chk_key(key):
                bye("invalid key")
            USED_KEYS.append(key)
            enc_flag = encrypt(key, FLAG)
            print(f'enc_flag(hex)> {enc_flag.hex()}')
        elif i == 3:
            bye("ok bye")
        else:
            bye("invalid option")
