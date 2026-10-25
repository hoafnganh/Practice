# L02 — SOLUTION

## Pipeline

```
200 phương trình 1 bit  →  "tổng con có nghiệm 0/1"  →  lattice CJLOSS 200+1 chiều
                        →  SVP_γ                     →  LLL  →  vector ±1 | 0
```

## Lattice CJLOSS (mục 4.2.2 của paper)

$$
B = \begin{pmatrix}
2 & & & & N a_1\\
& 2 & & & N a_2\\
& & \ddots & & \vdots\\
& & & 2 & N a_n\\
1 & \cdots & 1 & & N s
\end{pmatrix}, \qquad N > \sqrt n
$$

Tổ hợp $(e_1, \dots, e_n, -1)$ cho $(2e_i - 1,\ 0)$ — toàn $\pm 1$ và một $0$,
chuẩn $\sqrt{160} \approx 12{,}6$, trong khi định thức lattice $\approx 2^{160}N^{161}\max(a)$
cho vector "ngẫu nhiên" cỡ $2^{1024}$ — lệch chuẩn cực lớn nên LLL tìm được ngay.

**Vì sao cần "CJLOSS" thay vì lattice thô (Lagarias–Odlyzko)?** Cách làm thô dùng
vector $(e_i, 0)$ có chuẩn thay đổi theo nghiệm; CJLOSS "căn giữa" ($e_i - \tfrac12$)
để chuẩn đích cố định $\tfrac12\sqrt n$, chứng minh được nghiệm là vector ngắn
**duy nhất** khi mật độ $d = n/\log_2\max(a_i) < 0{,}9408$.

Ở đây $d = 160/1024 = 0{,}156$ — dư địa rất lớn. (Lưu ý thực hành: với dim lớn
— n ≥ 200 — hệ số xấp xỉ của LLL yếu đi; giữ mật độ ≲ 0.2 hoặc nâng cấp BKZ.)

## Flag

**Flag: `crypto{kn4ps4ck_r3d}`**

## Nguồn

- Paper 2023/032, mục 4.2 (LO85, CJLOSS92, PZ16)
- Challenge thật: SECCON CTF 2021 (https://rkm0959.tistory.com/244 — giải modular
  subset sum bằng CJLOSS); BackdoorCTF 2023 "Knapsack" là ví dụ ngược (density > 1
  → LLL thất bại, phải meet-in-the-middle)
