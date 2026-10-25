# L09 — ECDSA nonce chia sẻ bit cao (không biết giá trị)

> Dạng: **ECDSA biased nonce — biến thể "Shared MSB"** (paper 2023/032, mục 5.3.2)
> Thực tế: PRNG chết sau khi sinh bit cao, bộ lọc/vi điều khiển tái dùng bộ sinh
> cùng tầng ngẫu nhiên, v.v.

## Đề bài

Thiết bị ký secp256k1 với nguồn entropy nghèo: **40 bit cao của mọi nonce giống
hệt nhau** nhưng ta không biết chúng là gì:

$$k_i = 2^{216}\,t + k_i', \qquad 0 \le k_i' < 2^{216}$$

14 chữ ký:

```
Qx = ...  Qy = ...
z r s     (14 dòng)
nonce = ...  ct = ...
```

**Tìm $d$.**

## File

- `output.txt` / `gen.py` / `solve.py` / `SOLUTION.md`

## Gợi ý

1. Trừ phương trình 1 cho các phương trình còn lại — thành phần $t$ **triệt tiêu**.
2. Sai khác $k_i' - k_1'$ nhỏ → HNP với $\ell - 1 = 13$ phương trình.
3. Cẩn thận dấu: $k_i' - k_1'$ có thể âm → recenter về $[0, B)$ với $B = 2^{217}$.
