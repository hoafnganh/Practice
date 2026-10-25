# L10 — SOLUTION

## Pipeline

```
20 chữ ký + mảnh rời của k_i (24 bit) và của d (40 bit)
   → EHNP (Hlaváč–Rosa 2007):  r_i·2^60·d_1 − s_i·2^4·k_{i,1}
                               ≡ s_i·k̄_i − z_i − r_i·d̄  (mod n)
   → lattice EHNP 42 chiều: các mảnh scale về [0, K), đích CVP ở tâm K/2
   → embedding → LLL  →  d_1  →  d = d̄ + 2^60·d_1
```

## Lattice EHNP (mục 4.3.2 của paper)

Tổng quát: $x = \bar x + \sum 2^{\pi_j}x_j$; phương trình thứ $i$:
$\alpha_i\sum 2^{\pi_j}x_j + \sum_j \rho_{i,j}k_{i,j} \equiv \beta_i - \alpha_i\bar x \pmod p$
với $0 \le x_j < 2^{\nu_j}$, $0 \le k_{i,j} < 2^{\mu_{i,j}}$.

Lattice (kèm embedding): hàng $p\cdot e_i$ (dòng dư $\ell_i$), hàng cho từng mảnh
$x_j$ (cột riêng scale $S_j = K/2^{\nu_j}$), hàng cho từng mảnh nonce
(scale $K/2^{\mu_{i,j}}$), và hàng đích $(\beta_i - \alpha_i\bar x,\ K/2, \dots, K/2)$.
Vector cần tìm: $(0,\dots,0,\ x_jS_j - K/2,\ \dots,\ -K)$ — mọi tọa độ $\le K/2$.

Ở đây $K = 2^{40}$ (mảnh khóa lớn nhất), 20 phương trình — chuẩn đích
$\approx 2^{41.7}$ so với $\det^{1/42} = (n^{20}\cdot 1\cdot(2^{16})^{20}\dots)^{1/42} \approx 2^{101}$
— LLL xử lý gọn.

## Vì sao L08/L09 không đủ?

Side-channel thật (Minerva, cache timing) lộ các bit **rời rạc, không liền kề** —
cả trên nonce lẫn trên khóa. HNP chỉ mô tả được "một khối liên tục"; EHNP khái
quát: nhiều mảnh/ phương trình, mỗi mảnh scale riêng — và **hấp thụ luôn mảnh của
khóa** (HNP không có khái niệm "khóa cũng bị lộ mảnh").

## Flag

**Flag: `crypto{3hnp_chunks_r3v34l_4ll}`**

## Nguồn

- Paper 2023/032, mục 4.3.2 + 5.3.3 (HR07: https://doi.org/10.1007/978-3-540-74462-7_9)
- Bối cảnh thực: Minerva (https://minerva.crocs.fi.muni.cz/)
