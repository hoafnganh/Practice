# L11 — SOLUTION

## Pipeline

```
RSA, d ≈ N^0.25 (vượt Wiener)
   → ed − 1 = k(N + 1 − 2s)        [s = (p+q)/2]
   → f(x, y) = 1 + (N+1)x − 2xy ≡ 0 (mod e), nghiệm (k, s) nhỏ
   → bivariate modular Coppersmith (shift BD)  →  LLL
   → 2 đa thức triệt tiêu trên Z  →  resultant  →  s  →  k  →  d
```

## Biến đổi (mục 5.2.1 của paper)

$ed = 1 + k\varphi(N)$, $\varphi(N) = N + 1 - 2s$ với $s = \frac{p+q}{2}$ (chẵn hóa):

$$1 + 2k\Bigl(\frac{N+1}{2} - s\Bigr) \equiv 0 \pmod e
\;\Longleftrightarrow\; f(x, y) = 1 + (N+1)x - 2xy \equiv 0 \pmod e$$

**Kích thước nghiệm:** $k = \frac{ed-1}{\varphi} < d \approx 2^{128}$;
$s \approx \sqrt N = 2^{256}$. So với mô-đun $e \approx 2^{512}$: cả hai "nhỏ" —
đúng khung Coppersmith bivariate.

## Lattice Boneh–Durfee

Shift polynomial: $x^i f^k e^{m-k}$ ($0 \le k \le m$, $0 \le i \le m-k$) và
$y^j f^m$ ($1 \le j \le t$). Với $m=4, t=1$: 16 shift, 20 monomial, dim 20.
Mọi shift triệt tiêu mod $e^m$ tại nghiệm. Sau LLL, các hàng ngắn (chuẩn
$\lesssim e^m/\sqrt\omega$ — Howgrave-Graham) triệt tiêu **trên $\mathbb{Z}$**;
lấy 2 đa thức → **resultant theo $x$** → đa thức 1 biến theo $y$ → nghiệm
$y_0 = s$ → $k$ từ $f$ (tuyến tính theo $x$ tại $y_0$) →
$d = \frac{1 + k\varphi}{e}$.

**Tại sao vượt Wiener?** Wiener chỉ dùng liên phân số $\frac e N \approx \frac k d$
với $k < d$, cho ra điều kiện $d < \frac13 N^{1/4}$. BD thay bằng lattice
2 biến ⇒ đạt $d < N^{0.292}$ — mốc 25 năm chưa ai vượt.

## Thực nghiệm trong thư viện

`boneh_durfee_attack(N, e, 128, m=4, t=1)` chạy 0.3 giây cho $N$ 512-bit, δ=0.25.

## Flag

**Flag: `crypto{b0n3h_durf33_b3y0nd_w13n3r}`**

## Nguồn

- Paper 2023/032, mục 5.2.1 (BD99)
- Script Sage chuẩn: https://github.com/mimoo/RSA-and-LLL-attacks
- Tham số CTF thực: 春秋杯 2023 (d ≈ N^0.273)
