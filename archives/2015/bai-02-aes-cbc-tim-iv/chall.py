#!/usr/bin/env python

from Crypto.Cipher import AES
import sys
import binascii

# Predefine
KEY= b"5d6I9pfR7C1JQt"

# Replace with random number
IV= "??" # 16 byte

# Encrypt function
def encrypt(message, passphrase):
    aes = AES.new(passphrase, AES.MODE_CBC, IV)
    return aes.encrypt(message)

# Check argument
if len(sys.argv) <2:
    print("Please input your data!")
    sys.exit

# Output result
print("encrypted Data: " + binascii.hexlify(encrypt(sys.argv[1], KEY)))

# python encrypt.py "The message is protected by AES\!"

# encrypted Data:
# fe000000000000000000000000009ec3
# 307df037c689300bbf2812ff89bc0b49