# L12 — Bleichenbacher PKCS#1 v1.5... bản LATTICE

> Dạng: **Bleichenbacher padding oracle — formulation HNP của Nguyễn 2009** (paper 2023/032, mục 5.4)
> Challenge thật: các CTF có oracle đệm PKCS rất nhiều (bộ RSA challenge 14 là bản
> Bleichenbacher cổ điển); phiên bản **lattice/HNP** hiếm — đây là bản luyện tập

## Đề bài

Server RSA 512-bit, e = 3, có **oracle đệm PKCS#1 v1.5**: cho ciphertext $c'$,
trả về 1 nếu bản rõ bắt đầu `00 02`. Ta đã hỏi **60 câu** $r_i^e\,c$ với $r_i$
ngẫu nhiên và nhận đủ 60 lần "đúng đệm":

```
N = ...
e = 3
c = ...
r = [r_1, ..., r_60]     (60 giá trị được oracle chấp nhận)
ct = ...                  (AES-CTR, key = sha256(m))
```

**Tìm bản rõ $m$** (mã hóa flag theo PKCS: `00 02 || padding || 00 || flag`).

## File

- `output.txt` / `gen.py` / `solve.py` / `SOLUTION.md`

## Gợi ý

1. $O_B(r_i^e c) = 1$ nghĩa là $r_i m \bmod N$ bắt đầu `00 02`:
   $2B \le r_i m \bmod N < 3B$ với $B = 2^{496}$.
2. Viết $r_i m \bmod N = 2B + k_i$, $0 \le k_i < B$ →
   $k_i \equiv r_i\,m - 2B \pmod N$ — **HNP với ẩn $m$**, $B = 2^{496}$!
3. Điều kiện giải được: $l \ll 16\ell$ (paper mục 5.4.2) — với $l = 512$ cần $\ell \gtrsim 32$; ta có 60.
