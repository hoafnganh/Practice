# L11 — Boneh–Durfee: RSA với d < N^0.25 (vượt Wiener)

> Dạng: **Boneh–Durfee — bivariate modular small roots** (paper 2023/032, mục 5.2.1)
> Challenge thật cùng dạng: rất nhiều (thường gặp trong CTF Trung Quốc, vd. 春秋杯 2023
> với d ≈ N^0.273); script chuẩn: mimoo/Boneh-Durfee on Sage

## Đề bài

Khóa RSA 512-bit sinh với số mũ bí mật $d \approx 2^{128} \approx N^{0.25}$ —
**vượt ngưỡng Wiener** ($d < \frac13 N^{1/4} \approx 2^{126.4}$): liên phân số
cổ điển vô dụng. $e$ tương ứng lớn (cỡ $N$):

```
N = ...
e = ...
(hint: d < N^0.25 * 4/3)
```

**Tìm $d$** → flag (AES-CTR, key = sha256(d)).

## File

- `output.txt` / `gen.py` / `solve.py` / `SOLUTION.md`

## Gợi ý

1. $ed = 1 + k\varphi(N)$ → $1 + k(N+1) - 2ks \equiv 0 \pmod e$ với $s = \frac{p+q}{2}$.
2. Đa thức 2 biến mod e: $f(x,y) = 1 + (N{+}1)x - 2xy$, nghiệm nhỏ
   $(k, s)$ với $k < 2^{132}$, $s < 2^{258}$.
3. Shift polynomial kiểu BD: $x^i f^k e^{m-k}$ + $y^j f^m$ → LLL → 2 đa thức
   "vanish" trên $\mathbb{Z}$ → resultant → $s$ → $k$ → $d$.
4. Trong thư viện: `boneh_durfee_attack(N, e, d_bits=128, m=4, t=1)`.
