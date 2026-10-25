# L03 — SOLUTION

## Pipeline

```
RSA e=3 + biết prefix  →  f(x) = (m' + x)^3 − c ≡ 0 (mod N)   [nghiệm nhỏ x0]
                       →  bài toán "tìm nghiệm nhỏ" (Coppersmith)
                       →  lattice tam giác (d+1) chiều  →  LLL  →  đa thức h(x)
                       →  nghiệm nguyên của h  →  x0  →  flag
```

## Chi tiết

Biết trước 42 byte đầu, ẩn 26 byte cuối: $m = m' + x_0$ với
$m' = \text{prefix} \cdot 2^{208}$, $x_0 < 2^{208}$. Đa thức
$f(x) = (m'+x)^3 - c$ là monic bậc 3 trên $\mathbb{Z}_N$.

**Lattice** (mục 5.1.1 của paper): 4 hàng — ba hàng $N(Bx)^i$ ($i<3$) và hàng
$f(Bx)$; định thức $= N^3 B^{6}$, chiều 4. Với $B = 2^{208}$:

$$\|b_1\| \lesssim 2^{1}\sqrt 4 \cdot B^{3/2} N^{3/4} \approx 2^{208+576} \cdot \dots$$

— mỗi hệ số của đa thức thu được nhỏ hơn $N/(d{+}1)$ nên $h(x_0) = 0$ **trên số
nguyên** (bất đẳng thức Howgrave-Graham, mục 5.1.3). Giải $h$ bằng cách tìm
nghiệm nguyên (flint factor) rồi kiểm tra $f(x_0) \equiv 0 \pmod N$.

Điều kiện tồn tại nghiệm nhỏ: $|x_0| \le \frac12 N^{1/e} = \frac12 N^{1/3} = 2^{255}$
— phần ẩn 208 bit thoải mái.

## Phòng thủ

Padding ngẫu nhiên (OAEP) trước khi mã hóa; hoặc dùng e ≥ 65537 với bản rõ dài.

## Flag

**Flag: in ra bởi `solve.py`** (dạng `crypto{...18 ký tự...}` — xem output.txt sau khi gen).

## Nguồn

- Paper 2023/032, mục 5.1 (Coppersmith 1997)
- Challenge thật: Squ1rrel CTF 2024 "Partial RSA"
  (https://nightxade.github.io/ctf-writeups/writeups/2024/squ1rrel-CTF-2024/crypto/partial-rsa.html)
