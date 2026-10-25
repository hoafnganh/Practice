# L03 — Tin nhắn khuôn mẫu (RSA e=3, biết phần lớn bản rõ)

> Dạng: **RSA stereotyped message — Coppersmith univariate** (paper 2023/032, mục 5.1)
> Challenge thật cùng dạng: Squ1rrel CTF 2024 — *"Partial RSA"*; rất phổ biến trên CTF

## Đề bài

Server gửi mã kích hoạt bằng RSA **e = 3** và bản rõ có khuôn mẫu cố định:

```
m = "Hello agent. Your one-time activation code is: crypto{??????????????????}"
```

Chỉ 18 ký tự cuối (bên trong `crypto{...}`) là ngẫu nhiên.

```
N = ...
e = 3
c = ...
```

**Khôi phục bản rõ đầy đủ.**

## File

- `output.txt` / `gen.py` / `solve.py` / `SOLUTION.md`

## Gợi ý

1. Viết $m = m' + x$ với $m' = $ phần biết, $x <$ phần ẩn.
2. $f(x) = (m' + x)^3 - c \equiv 0 \pmod N$ — monic bậc 3.
3. Coppersmith: tìm được nghiệm tới $\frac12 N^{1/3}$. Với $N$ 768-bit: $\approx 2^{255}$ — phần ẩn chỉ 144 bit.
