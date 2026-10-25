from pwn import *
ct = "AEF8002C69E37021913A153AB922D853CBEB9DEE"
key = "6b6bf9a226edcf0f77c776e1cb6b6575ff6bcf19"
print(xor(bytes.fromhex(ct), bytes.fromhex(key)).hex())