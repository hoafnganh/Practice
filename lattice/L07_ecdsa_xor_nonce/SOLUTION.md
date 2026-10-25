# L07 — SOLUTION

## Pipeline (chính là lời giải TSJ CTF 2022 "Signature")

```
6 chữ ký ECDSA, nonce k = z ⊕ d
   → XOR theo bit:  k = z + d − 2·Σ 2^j z_[j] d_[j]
   → mỗi chữ ký: Σ_j d_[j]·A_ij + c_i ≡ 0 (mod n)     [tuyến tính theo BIT d_j]
   → lattice TSJ (CJLOSS thế hệ mới): bit là HỆ SỐ TỔ HỢP
   → LLL 263 chiều  →  vector (0…0, d_0..d_255, 1)  →  d
```

## Lattice TSJ (mục 5.3.1 paper + script gốc của maple3142)

Với mỗi bit $j$ một **hàng đơn vị**: $(A_{1j}, \dots, A_{\ell j}, \underbrace{0..1..0}_{j}, 0)$;
một **hàng constant**: $(c_1, \dots, c_\ell, 0..0, 1)$; và $\ell$ **hàng mod-q**
$(n\cdot 2^{64}\cdot e_j)$. Cột mod-q nhân $2^{64}$ để LLL "thích" vector có phần dư = 0:

$$
\begin{pmatrix}
n2^{64} & & & \mathbf{0}\\
& \ddots & & \\
\multicolumn{3}{c}{A \,\big|\, I_{256}} & \\
\multicolumn{3}{c}{c \,\big|\, \mathbf{0}} & 1
\end{pmatrix}
$$

Tổ hợp $(x_j, \underbrace{d_0, .., d_{255}}_{\text{BIT!}}, 1)$ với phần đầu
$= n2^{64}x + (\text{đánh giá affine}) \equiv 0$: vector
$(0,\dots,0,\ d_0, \dots, d_{255},\ 1)$ — toàn bit 0/1, chuẩn $\sqrt{257} \approx 16$,
so với $\det^{1/263} = (n2^{64})^{6/263} = 2^{8.2}$-scale — LLL ăn ngay.

**Điểm mấu chốt:** khác CJLOSS cổ điển (bit là *tọa độ*), ở đây bit là *hệ số tổ hợp* —
lattice chỉ có $263$ chiều thay vì $2^{256}$ tổ hợp, và hàng constant ép nghiệm
"affine" chính xác (xử lý số dư $\ell_i$ một cách tự nhiên).

## Flag

**Flag: `crypto{x0r_n0nc3_1s_subs3t_sum_tsj}`**

## Nguồn

- Paper 2023/032, mục 5.3.1 ("gần giống multiple modular subset sum, giải được khi ℓ ≥ 2")
- TSJ CTF 2022 "Signature" — maple3142 (2/428 solves):
  https://github.com/maple3142/My-CTF-Challenges/tree/master/TSJ%20CTF%202022/Signature
- Writeup phân tích: https://mystiz.hk/posts/2022/2022-03-02-tsjctf-2/
