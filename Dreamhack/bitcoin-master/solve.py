merkle_root = '4a55e27f5d2760e9083818b1bf8e9e02f67d7e0b75f37f66943a9dc3afaadeb8'
tx_list = ['d629ff44f1185dfdc66f28a130320bbe1191304b0ab907f54850e2f9783c6310', '425b6a69deb3ed5404c2e3f16ca635966dc2506c98a45e0fb98fafdb69e72348', '????????????????????????????????????????????????????????????????', 'a6e05e59c154baba932d6aee9ae3e778c0c317a7af38cfb3a08313e9e85c7c2b', 'c66375ba7d3ccfcd4118f902515335ce72c9a5f7571a06250def8b74198487fd', 'ddf48b45571077646421d9a8a44b382da91853e891da78c4b32f54a6a14b01f5', '4df06fcba00e855b2edacc45fee5922832537aa7976fb4b5323494fc5fd47d92', '59a60d7301bff3c162a2c546082027d6935bd4a00e36564bec12c8e89ab2191d', '37c93c2d966e71f91431cb6ec31c1b965210bb01d37e146c1156c31ee6553044', 'ba4420f7b7047d507fe82f9f72c0144f44cbaeea7cf85054bfd44a1e8c910d79', 'a4177ea5635cfba5f6eecb354635e64668fd9c7ba517c4ea6d8873d768a6450d', 'deeb4bf6cc33100194fd86d5516b0b21ce7f99098f97a92fc003635d4d09d6b0', '3b2f0208e1759a57551af26ef59b32fdc549e1cbd936fe379c1183fb7602a932', '48e435c40bc3b623843fca4667cf19a7b499fe0bbc46356bd76a05a7dab283eb', '501ac17c09169689e0cfcd1ffc8db7a7ee4c3494a889b2a2ac5851e65e87d718', '2d4acfc87ea633a819039a6496ff902fb4d0cf68eb39417e8e8c8c90870f1be6', 'c5835b216696f45bd415ddacc9c47df3eb23b6d57e4bed56f21949549d3e6e8c', '3bfdb32c070c48a974a08e6f6e06c9337890cc604a0921f1b29250d2a6a2436e', 'dcf4a0301d5dd226e4f327d6ea3223329310155ad6b89acd712a8c25308fc756', '514ca0b7e5ca3f89c25f87179de9ccaa035696f4ff76123a2b58757ae6ad3b5d', '30876d7a8126108f3103d860c3789951f02a94835f4d9f8bda9b190a5c17f023', 'd8e50dc2c36260b92be806bbde75a89f98d76c3b6756f9d980e1b14acb415068', 'a51090308de9094e0dd6dfab824b8db48b32e2446210183d4ea1364f0eee524a', '6b16076dac0d4c6cdb4f5d47b4e47593b37ecd675b0dfcafe175c3daf590e4ae', '01ebc005ef09e902904107b1a6b014e81c002ea908491cac8cb9a50ac7140414', '46fbf467216a4c24f3773d5a35dd0cadcfd7dd918a8c08cb911b6ef9433b5bd9', '4c657cc5afd7ceb8ce6b5f8b8f9173d815fdafb222e84dbe85b5d6a942918d10', '2f80fd81451a324e425cff1656bfc3113d91488247ae5ba68815f946f280fa79', '9d5cd49f673e987f9e6dcee77d5dc79ee3c9997f20f9ad1ce8a5247e089d9ee2', 'e417fd57aefe08940e9f5b406860c5a3830a77b3649b98a4217295af01fd77db']

import re, requests, binascii
from hashlib import sha256

host = 'http://host3.dreamhack.games:20388'


def dsha(b):
    return bytes(sha256(sha256(b).digest()).digest())

def hash2(a, b):
    a = bytes.fromhex(a)
    b = bytes.fromhex(b)
    a = a[::-1]
    b = b[::-1]
    r = a + b
    r = dsha(r)
    return r[::-1].hex()

def merkle_root_(hashes):
    if len(hashes) == 1:
        return hashes[0]
    new = list(hashes)
    if len(hashes) % 2 == 1:
        new.append(hashes[-1])
    next_level = []
    for i in range(0, len(new), 2):
        r = hash2(new[i], new[i + 1])
        next_level.append(r)
    return merkle_root_(next_level)

idx = tx_list.index("?" * 64)
cand = None

for i in range(65536):
    raw = i.to_bytes(2, "big")
    cand_i = sha256(raw).digest()[::-1].hex()
    tx_list[idx] = cand_i
    if merkle_root_(tx_list) == merkle_root:
        cand = cand_i
        break

flag = requests.get(f"{host}/check/{tx_list[idx]}")
print(flag.text)



