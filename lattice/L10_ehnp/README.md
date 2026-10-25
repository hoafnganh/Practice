# L10 — ECDSA Key Disclosure: mảnh rời của nonce VÀ của khóa

> Dạng: **Extended Hidden Number Problem (EHNP)** (paper 2023/032, mục 4.3.2 + 5.3.3 — Hlaváč–Rosa 2007)
> Challenge thật cùng dạng: rất hiếm — side-channel thực tế (Minerva, cache) thường
> lộ các mảnh rời không liền kề; đây là bản luyện tập đúng công thức EHNP

## Đề bài

Thiết bị ký P-192 bị lỗi side-channel:

- Mỗi nonce $k_i$ **lộ trừ bit 4..27** (24 bit giữa bị ẩn, phần cao ≥ bit 28 và
  phần thấp bit 0..3 đã biết): $k_i = \bar k_i + 2^4\,k_{i,1}$, $0 \le k_{i,1} < 2^{24}$.
- Khóa $d$ **lộ trừ bit 60..99** (40 bit): $d = \bar d + 2^{60}d_1$, $0 \le d_1 < 2^{40}$.

20 chữ ký:

```
dbar = ...          (khóa với các bit ẩn = 0)
Qx = ...  Qy = ...
z r s               (20 dòng)
nonce = ...  ct = ...
```

**Tìm $d$** (biết trước $\bar d$ và vị trí các mảnh).

## File

- `output.txt` / `gen.py` / `solve.py` / `SOLUTION.md`

## Gợi ý

1. Thay biểu diễn mảnh vào $s_ik_i \equiv z_i + r_id$ → EHNP đúng công thức:
   $\alpha_i\Sigma 2^{\pi_j}x_j + \sum\rho_{i,j}k_{i,j} \equiv \beta_i - \alpha_i\bar x \pmod n$.
2. Lattice EHNP: các mảnh scale về cùng khoảng $[0, K)$, đích CVP đặt ở "tâm" $K/2$.
3. Dùng `ehnp_solve` — hoặc tự dựng theo mục 4.3.2.
