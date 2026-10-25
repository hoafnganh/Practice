# Cryptohack Libs cần dùng

## Intro to Crypto

- base64: thư viện `base64`
- `from Crypto.Util.number import *`
- `^` chỉ làm việc với số, output là số.
- Với 1 biến là byte thì khi gọi index nó sẽ trả về integer 0 đến 255.
- pwntools: kết nối netcat.

## Symmetric

```python
import requests, json, string
from pwn import *
from Crypto.Cipher import AES
```

## Public key / ECC

```python
import fastecdsa
from fastecdsa.point import Point
from fastecdsa.curve import P256
from ecdsa.ecdsa import Public_key, Private_key, Signature, generator_192
```

## Tools

- RsaCtfTool: <https://github.com/RsaCtfTool/RsaCtfTool>
- padding-oracle-attacker: <https://github.com/KishanBagaria/padding-oracle-attacker>
- SageMath: <https://doc.sagemath.org/html/en/installation/index.html>
- yafu: <https://github.com/bbuhrow/yafu>

## Cài Sage trong WSL (Kali)

```bash
wsl --install -d kali-linux
# cài conda:
cd ~
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-Linux-x86_64.sh
# rồi tạo env sage:
conda create -n sage sage python=3.12 -c conda-forge
```

Sau khi bật sage (`conda activate sage`), cài thêm libs cho python trong env:

```bash
pip install z3-solver libnum factordb-py pyOpenSSL hlextend
pip install py_ecc fastecdsa coincurve gmssl gmpy2
```

```bash
python -m pip install -U \
  pycryptodome cryptography \
  sympy gmpy2 \
  z3-solver \
  fpylll \
  galois \
  py_ecc ecdsa \
  numpy scipy mpmath \
  pwntools requests
python -m pip install -U \
  networkx ortools \
  randcrack mnemonic owiener libnum primefac \
  coincurve pynacl \
  argon2-cffi bcrypt \
  python-flint \
  scapy pillow \
  phe pqcrypto
python -m pip install cypari2
```
