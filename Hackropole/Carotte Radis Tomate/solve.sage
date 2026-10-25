carotte =  392278890668246705
radis   =  4588810924820033807
tomate  =  17164682861166542664
pomme   =  12928514648456294931
banane  =  5973470563196845286
enc = '2da1dbe8c3a739d9c4a0dc29a27377fe8abc1c0feacc9475019c5954bbbf74dcedce7ed3dc3ba34fa14a9181d4d7ec0133ca96012b0a9f4aa93c42c61acbeae7640dd101a6d2db9ad4f3b8ccfe285e0d'

from Crypto.Cipher import AES
from Crypto.Util.number import *
from Crypto.Util.Padding import unpad

rem = [17488856370348678479, 16548497022403653709, 17646308379662286151, 14933475126425703583, 17256641469715966189]
cer = [carotte, radis, tomate, pomme, banane]

key = crt(cer, rem)
# N = 17488856370348678479 * 16548497022403653709 * 17646308379662286151 * 14933475126425703583 * 17256641469715966189
# print(C)

E = AES.new(long_to_bytes(key), AES.MODE_ECB)

dec = E.decrypt(bytes.fromhex(enc))
print(unpad(dec, 16))