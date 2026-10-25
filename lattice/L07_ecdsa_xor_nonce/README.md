# L07 — ECDSA với nonce k = z ⊕ d

> Dạng: **ECDSA nonce XOR khóa bí mật → affine modular subset sum** (paper 2023/032, mục 5.3.1)
> Challenge thật: **TSJ CTF 2022 — "Signature"** (maple3142; 2/428 solves)
> https://github.com/maple3142/My-CTF-Challenges/tree/master/TSJ%20CTF%202022/Signature
> Writeup: https://mystiz.hk/posts/2022/2022-03-02-tsjctf-2/

## Đề bài

Chữ ký ECDSA trên **secp256k1**. Định danh nonce "thông minh":

$$k_i = z_i \oplus d$$

với $z_i$ = SHA-256 của thông điệp, $d$ = khóa bí mật. Có vẻ không đoán được —
nhưng XOR **phá vỡ tính tuyến tính theo bit** một cách rất nguy hiểm.

Bạn có 6 chữ ký $(z_i, r_i, s_i)$, khóa công khai $Q = dG$, và flag mã hóa
AES-CTR với key = sha256(d):

```
Qx = ...   Qy = ...
z = ... r = ... s = ...     (6 dòng)
nonce = ...  ct = ...
```

**Tìm $d$.**

## File

- `output.txt` / `gen.py` / `solve.py` / `SOLUTION.md`

## Gợi ý

1. XOR theo bit: $a \oplus b = a + b - 2(a \wedge b)$, và $a \wedge b = \sum_j 2^j a_{[j]}b_{[j]}$.
2. Thay vào $s_i k_i \equiv z_i + r_i d \pmod n$ → mỗi chữ ký là **một phương trình
   tuyến tính theo các BIT $d_{[j]} \in \{0,1\}$** modulo $n$.
3. 6 phương trình × 256 bit ẩn — mật độ $1/6$ — giải được bằng lattice kiểu
   TSJ/CJLOSS mới (`affine_modular_subset_sum_solve`).
