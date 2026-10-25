# Lời giải — 17 Partial Key Exposure (BDF, survey §4.5 Định lý 9)

## Phát biểu trong survey

**Định lý 9 (BDF):** Cho ⟨N, d⟩ khóa riêng RSA, N dài n bit. Khi biết
⌈n/4⌉ bit có trọng số thấp nhất của d, có thể khôi phục toàn bộ d trong thời
gian tuyến tính theo e·log₂e (giả thiết e < √N).

## Chứng minh quy về 2 bước (theo survey §4.5)

**Bước 1 — phương trình bậc hai mod 2^s.** Từ `ed − k(N − p − q + 1) = 1`
với `0 < k ≤ e`. Nhân hai vế với p và dùng pq = N:

```
edp − kNp + kp² + kN − kp = p
⟺ k·p² + (ed − kN − k − 1)·p + kN = 0     (chính xác trên ℤ!)
```

Rút gọn mod 2^s (s = số bit đã lộ): `ed mod 2^s = e·d_low` biết hết ⇒ phương
trình bậc hai **theo p mod 2^s**. Với e = 3 chỉ có k ∈ {1, 2, 3}; giải bậc hai
mod 2^s (Hensel lifting / hoàn thành bình phương + căn mod 2^k) cho vài ứng
viên `p_low = p mod 2^s`. (Survey: tổng số ứng viên ≤ e·log₂e.)

**Bước 2 — Coppersmith với phần cao của p.** `p = p_low + 2^s·x` với
`x < 2^{n/2−s}`. Làm monic: `f̃(x) = x + p_low·(2^s)^{−1} mod N` — nghiệm mod p
(= N^{1/2}). Với s = 176, N 512-bit: `x < 2^80 ≪ N^{1/4}` → lattice nhỏ
(m = t = 6, dim 12) giải tức thì (giống challenge 15).

## Các bước + code

```python
for k in (1, 2, 3):
    roots = R.solve_quad_mod_2k(k, e*d_low - k*n - k - 1, k*n, S)
    for p_low in roots:
        f = [p_low * pow(2**S, -1, n) % n, 1]
        for x0 in R.coppersmith_small_roots(f, n, 1 << (256-S), 6, 6, check_mod_n=False):
            p = p_low + (x0 << S)
            if n % p == 0: -> xong
```

Ví dụ số học của bước 1 (nhỏ, kiểm chứng tay được): p = 11, N = 143, e = 3,
φ = 120, d = 7 (3·7 = 21 = 0·120 + ... — 21 ≡ 21; d = 3^{-1} mod 120 = 87?? —
3·87 = 261 = 2·120 + 21 — không đúng; tính lại: 3d ≡ 1 mod 120 → d = 87:
3·87 = 261 = 2·120 + 21 — 261 mod 120 = 21 ≠ 1. d = 3^{-1} mod 120: 3·x ≡ 1
mod 120 — gcd(3,120) = 3 ≠ 1 — vô nghiệm! e = 3 không hợp lệ với p = 11
(3 | p−1) — đúng như survey nhấn mạnh gcd(e, φ) = 1. Chọn p = 13, q = 17:
φ = 192, gcd(3,192) = 3 lại vô nghiệm... p = 11 bị loại, thử N = 11·17? cùng
vấn đề. → ví dụ tay với e = 3 đòi hỏi p, q ≢ 1 mod 3, vd p = 5, q = 11:
φ = 40, d = 27 (3·27 = 81 = 2·40 + 1 ✓), k = (ed−1)/φ = 2. s = 3 bit:
d_low = 27 mod 8 = 3. Phương trình: 2p² + (81 − 2·55 − 2 − 1)p + 110 ≡ 0
mod 8 → 2p² + 3p + 6 ≡ 0 mod 8 — thử p = 5: 50 + 15 + 6 = 71 ≡ 7 ✗?? —
kiểm chứng: p = 5, bậc hai chính xác: 2·25 + 3·5 + 6 = 71 ≡ 7 mod 8 —
NHƯNG phương trình phải có nghiệm p mod 8 = 5... 71 mod 8 = 7 ≠ 0 — sai chỗ
nào? ed − k(N − p − q + 1) = 81 − 2·(55 − 5 − 11 + 1) = 81 − 2·40 = 1 ✓.
Nhân p: edp − kNp + kp² + kN − kp = p → 2p² + (81 − 110 − 2 − 1)p + 110 − p
= 0?? — chú ý vế phải là p: edp − kNp + kp² + kN − kp − p = 0 → hệ số của p:
ed − kN − k − 1 = 81 − 110 − 2 − 1 = −32 → 2p² − 32p + 110 ≡ 0 mod 8 →
2·25 − 32·5 + 110 = 50 − 160 + 110 = 0 ✓✓ (tôi đã quên dấu −p trước đó).
Ví dụ xác nhận công thức. Trong solve.py: `bb = e*d_low − k*n − k − 1` với
d_low = d mod 2^s — chính xác.)

## Flag

```
crypto{bdf_p4rt14l_k3y_3xp0sur3}
```

## Cách phòng thủ

Bảo vệ toàn bộ d (side-channel countermeasures, constant-time); survey cũng
nhấn mạnh: ElGamal/DSA không bị dạng này (bit của x bị lộ không đủ để khôi phục).
