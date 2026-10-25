import base64
from Crypto.Util.number import *
c = int.from_bytes(base64.b64decode("kPmDFLk5b/torG53sThWwEeNm0AIpEQek0rVG3vCttc="))
e = 65537
n = int("B62DCE9F2581635723DB6B188F12F0469CBEE0CBC5DACB36C36E0C96B6EA7BFC", 16)
bin_n = list(bin(n)[2:])
# print(type(factor(n)))
# for i in range(len(bin_n)):
# print(i)
# bin_n[i] = "1" if bin_n[i] == "0" else "0"
# tmp = int("".join(bin_n), 2)
# f = factor(tmp)
# if (len(f) == 2) and f[0][0].nbits() > 100 and f[1][0].nbits() > 100:
# n = tmp
# print(f)
# break
# bin_n[i] = "0" if bin_n[i] == "1" else "1"
# print()
bin_n[255] = "1" if bin_n[255] == "0" else "0"
n = int("".join(bin_n), 2)
p, q = 279125332373073513017147096164124452877, 295214597363242917440342570226980714417
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
print(long_to_bytes(pow(c, d, n)))
