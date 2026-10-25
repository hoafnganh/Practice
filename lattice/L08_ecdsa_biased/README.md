# L08 — ECDSA nonce lệch: 56 bit cao luôn bằng 0

> Dạng: **ECDSA biased nonce → HNP** (paper 2023/032, mục 5.3.2 — Howgrave-Graham–Smart 2001)
> Challenge thật cùng dạng: Ledger Donjon CTF "Projective Signatures";
> TBTL CTF 2023 "Memory Safe ECDSA"; real-world: LadderLeak (CCS 2020), Minerva, Bitcoin wallets

## Đề bài

Ví tiền mã hóa dùng secp256k1, nhưng PRNG của nó bị hỏng: **56 bit cao của mỗi
nonce luôn bằng 0** ($k < 2^{200}$). Ta thu được 40 chữ ký của cùng khóa:

```
Qx = ...  Qy = ...
z r s     (40 dòng)
nonce = ...  ct = ...    (AES-CTR, key = sha256(d))
```

**Khôi phục khóa bí mật $d$.**

## File

- `output.txt` / `gen.py` / `solve.py` / `SOLUTION.md`

## Gợi ý

1. $s_i k_i \equiv z_i + r_i d \pmod n$ → $k_i \equiv s_i^{-1}z_i + s_i^{-1}r_i d$.
2. $k_i$ nhỏ → đúng HNP với $B = 2^{200}$, 40 phương trình.
3. Lattice embedding ~42 chiều — LLL giải trong tích tắc.
