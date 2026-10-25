# L06 — SOLUTION

## Pipeline (Hình 2 của paper)

```
26 quan sát 40 bit cao  →  x_i = 2^24·y_i + e_i (e_i < 2^24)
                        →  HNP: e_i ≡ a^i·x_0 + (c_i − 2^24·y_i) (mod M)
                        →  lattice embedding 28 chiều  →  LLL  →  x_0
```

## Biến đổi chi tiết

Truy hồi tuyến tính nên $x_i \equiv a^i x_0 + c_i \pmod M$ với
$c_i = \frac{a^i-1}{a-1}b$ (tính bằng vòng lặp). Thay $x_i = 2^{24}y_i + e_i$:

$$e_i \equiv a^i x_0 + \underbrace{(c_i - 2^{24}y_i)}_{a_i} \pmod M$$

— đúng khuôn HNP với "phần bị che" $e_i < 2^{24} = B$: mỗi mẫu lộ 40/61 bit,
cần $m \gtrsim \frac{61}{61-24}$… thực tế 24–26 mẫu là dư ($B = 2^{24} \ll M^{m/(m+1)} = 2^{58.7}$).

Sau LLL: hàng có cột cuối $\pm B$ → $e_i$ → $x_0 = 2^{24}y_0 + e_0$ → kiểm tra lại
cả chuỗi (phòng trường hợp nghiệm dư).

## Bài học nhận dạng

**"Cho các giá trị gần đúng của một chuỗi truy hồi tuyến tính" = HNP trá hình.**
Cùng khuôn: MT19937 tempered output cụt, Java `Random` (48-bit seed, ELTAM),
số dư của phép chia bị che...

## Flag

**Flag: `crypto{trunc4t3d_lcg_1s_hnp_1n_d1sgu1s3}`**

## Nguồn

- Paper 2023/032, Hình 2 + Frieze et al. 1988
- DownUnderCTF 2020 writeup (https://jsur.in) — truncated LCG bằng lattice;
  jvdsn/crypto-attacks có sẵn module `truncated_lcg`
