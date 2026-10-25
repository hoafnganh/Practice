# L01 — SOLUTION

## Pipeline (theo paper §3.6)

```
xấp xỉ β ≈ α  →  f(β) ≈ 0 (phương trình tuyến tính theo hệ số)
              →  lattice 4×4 (mỗi hàng = 1 lũy thừa β)
              →  SVP_γ  →  LLL  →  vector (≈0, a0, a1, a2)
```

## Lời giải chi tiết

$f(x) = a_0 + a_1x + a_2x^2 + a_3x^3$ monic ($a_3 = 1$), $f(\beta) \approx 0$. Nhân $10^{12}$:

$$10^{12}a_0 + \lfloor 10^{12}\beta\rfloor a_1 + \lfloor 10^{12}\beta^2\rfloor a_2 + \lfloor 10^{12}\beta^3\rfloor \approx 0$$

Dựng lattice (hàng):

```
[10^12          1 0 0]
[⌊10^12β⌋       0 1 0]
[⌊10^12β²⌋      0 0 1]
[⌊10^12β³⌋      0 0 0]
```

Tổ hợp $(a_0, a_1, a_2, 1)$ cho vector $(\approx 0,\ a_0,\ a_1,\ a_2)$ — vector ngắn
vì $|a_i| < 1000$ trong khi cột đầu cỡ $10^{12}\beta^3$. Chạy LLL, đọc hàng đầu
có tọa độ đầu "gần 0" (so với $10^{12}$).

## Kiểm tra chất lượng trước khi chạy

Công thức ngón tay cái (Hệ quả 3.15): LLL tìm vector tới $\approx 1.02^4\cdot(10^{12})^{1/4}\cdot\sqrt4 \approx 3700$.
Vector đích $\approx \sqrt{3\cdot 1000^2} \approx 1730$ — dư địa thoải mái ✓.

## Flag

Vector trả về: `[-144, 75, -15, 1]` → $f(x) = x^3 - 15x^2 + 75x - 144$.

**Flag: `crypto{[-144,75,-15,1]}`**

## Nguồn

- Paper 2023/032, mục 3.6 (Kannan–Lenstra–Lovász 1984)
- Challenge thật cùng dạng: UIUCTF 2025 — *Back to Roots*
  (https://awrreny.github.io/posts/uiuctf25-writeup-back-to-roots/)
