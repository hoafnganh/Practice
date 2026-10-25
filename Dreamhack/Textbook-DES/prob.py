#!/usr/bin/env python3
from cipher import TDES
import os


def pad(plaintext):
    padding_len = 16 - len(plaintext) % 16
    padding = bytes([padding_len]) * padding_len
    return plaintext + padding

def menu():
    print("1. Encrypt message")
    print("2. Encrypt flag")
    print("3. Exit")
    print("> ", end="")


if __name__ == "__main__":
    with open("flag", "rb") as f:
        flag = pad(f.read())

    key1 = os.urandom(8)
    key2 = os.urandom(8)
    tdes = TDES(key1, key2)

    print("DES is no longer safe?")
    print("How about Triple-DES?")
    while True:
        menu()
        action = int(input())
        if action == 1:
            print("send your message(hex) > ", end="")
            msg = bytes.fromhex(input())
            print("send your mode > ", end="")
            mode = input()
            if mode == "DED":
                print("forbidden mode!")
                break
            print(f"encrypted message > {tdes.encrypt(msg, mode).hex()}")

        elif action == 2:
            print(f"encrypted flag > {tdes.encrypt(flag, 'EDE').hex()}")

        elif action == 3:
            print("Good Bye!")
            break

        else:
            print("invalid")
            break
