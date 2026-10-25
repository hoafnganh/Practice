#!/usr/bin/env python3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os
import hashlib


def give_flag():
    with open("flag", "rb") as f:
        flag = f.read()
    print(flag)


def stronghash(msg: bytes) -> bytes:
    hashed_msg = pad(msg, 16)
    for _ in "Stronger!!":
        hashed_msg = AES.new(hashed_msg[:16], AES.MODE_ECB).encrypt(hashed_msg)

    # Stronger!!!
    for length in range(2, 16):
        md5 = hashlib.md5(hashed_msg[:length])
        hashed_msg = md5.digest()

    # Stronger!!!!
    for length in range(16, 32):
        sha256 = hashlib.sha256(hashed_msg[:length])
        hashed_msg = sha256.digest()

    return hashed_msg


def main():
    print("I invented my custom hash function, which is very very strong")
    print("Can you steal my flag from it?")

    stage = 100
    pw = [os.urandom(16) for _ in range(stage)]
    for i in range(stage):
        print(f"Stage {i + 1}")
        print(f"My hashed password : {stronghash(pw[i]).hex()}")
        msg = bytes.fromhex(input("Guess my password(hex) > "))
        if stronghash(msg) != stronghash(pw[i]):
            exit("Get out stranger! ୧(๑•̀ᗝ•́)૭")
    
    print('Here is your flag, master.')
    give_flag()


if __name__ == "__main__":
    main()