# L09 — SOLUTION

## Pipeline

```
14 chữ ký, k_i = 2^216·t + k_i'   (t CHUNG, không biết)
   → trừ phương trình 1:  (k_i' − k_1') ≡ (t_i − t_1)d + (a_i − a_1)  (mod n)
   → HNP với 13 phương trình, "phần bị che" = k_i' − k_1' ∈ (−2^216, 2^216)
   → recenter về [0, 2^217)  →  LLL  →  d
```

## Biến đổi (mục 5.3.2, "Shared MSB" của paper)

Với $t_i = s_i^{-1}r_i$, $a_i = s_i^{-1}z_i$: phương trình 1 là
$k_1' = t_1 d + a_1 - 2^{216}t$. Trừ đi:

$$k_i' - k_1' \equiv (t_i - t_1)d + (a_i - a_1) \pmod n$$

vế trái nằm trong $(-2^{216}, 2^{216})$ — **cộng thêm $2^{216}$ để về $[0, 2^{217})$**
(recentering — mẹo mạnh của Breitner–Heninger "Biased Nonce Sense"). LHS mới là
"phần bị che" của HNP với $B = 2^{217}$.

Điều kiện thành công: $B \ll n^{m/(m+1)}$ với $m = 13$: $2^{217}$ vs
$2^{256\cdot 13/14} = 2^{237.7}$ — dư địa 20 bit ✓ (ít phương trình hơn L08 vì
mỗi cặp chỉ cho một phương trình và mất 1 làm mốc).

## Vì sao không thể "brute force t"?

$t$ có $2^{40}$ giá trị — brute force được, nhưng mỗi giá trị cần một HNP đầy đủ;
lattice khử $t$ trong **một lần** LLL — thanh hơn hàng trăm lần và scale được.

## Flag

**Flag: `crypto{sh4r3d_msb_n0t_s0_s3cr3t}`**

## Nguồn

- Paper 2023/032, mục 5.3.2 (trang 27, đoạn "Shared MSB")
- Recentering: Breitner–Heninger, https://eprint.iacr.org/2019/023
