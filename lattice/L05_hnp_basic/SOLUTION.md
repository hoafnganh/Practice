# L05 — SOLUTION

## Pipeline

```
24 phương trình  v_i = t_i·α + r_i (mod p), r_i < 2^40
                 →  HNP (Boneh–Venkatesan 1996)
                 →  lattice embedding (m+1) chiều  →  LLL
                 →  vector (−k_1, ..., −k_m, ±B)  →  α
```

## Lattice (mục 4.3.1 của paper — biến thể SVP)

Với $k_i = t_i'\alpha + a_i \bmod p$ ($t_i' = -t_i$, $a_i = v_i$), $0 \le k_i < B$:

$$
\begin{pmatrix}
p & & & \\
& \ddots & & \\
t_1' & \cdots & t_m' & B\\
a_1 & \cdots & a_m & 0
\end{pmatrix}
\quad\text{— hàng } p\cdot e_i,\ \text{hàng } (t', B),\ \text{hàng } (a, 0)
$$

Tổ hợp $(\ell_1..\ell_m, \alpha, 1)$: tọa độ đầu $= \ell_ip + t_i'\alpha + a_i = k_i$ (nhỏ!),
cột cuối $= B$. Vector đích chuẩn $\le \sqrt{m+1}\,B = 2^{42}$, trong khi
$\det^{1/(m+1)} = (p^m B)^{1/25} = 2^{(256\cdot24+40)/25} = 2^{247}$ — lệch chuẩn
khủng khiếp, LLL bắt được ngay.

Đọc kết quả: hàng có **cột cuối $\pm B$**, đổi dấu nếu cần, rồi
$\alpha = (k_i - a_i)\cdot t_i'^{-1} \bmod p$ (lấy "phiếu chiếu" đa số từ các $i$).

## Vì sao chỉ cần 40 bit "bị che"?

Điều kiện thành công (mục 4.3.1): $B \ll p^{m/(m+1)}$ — tức số bit lộ
$\log_2 p - \log_2 B \gtrsim \frac{\log_2 p}{m+1}$. Với $m = 24$: chỉ cần lộ
$\ge 11$ bit; ở đây lộ 216 bit — dư địa cực lớn.

## Flag

**Flag: `crypto{h1dd3n_numb3r_bv96_l0c4t3d}`**

## Nguồn

- Paper 2023/032, mục 4.3 (BV96; Babai 1986; Kannan 1987)
- Cùng tinh thần: Ledger Donjon CTF "Projective Signatures"
  (https://blog.cryptohack.org/ecdsa-side-channel-attack-projective-signatures-donjon-ctf-writeup)
