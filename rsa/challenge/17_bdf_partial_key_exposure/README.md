# 17 — Partial Key Exposure (BDF): lộ bit thấp của d

**Dạng:** Biết các bit thấp nhất của d (e = 3) → phương trình bậc 2 mod 2^s + Coppersmith
**Độ khó:** ★★★★★
**Nguồn:** `RSA-survey-vi.md` §4.5 (Định lý 9 — Boneh, Durfee, Frankel)

## Câu chuyện

Một tiền xử lý side-channel làm lộ **176 bit thấp nhất của d** (N 512-bit, e = 3).
Survey (Định lý 9) nói: chỉ cần ⌈n/4⌉ bit thấp của d là đủ khôi phục toàn bộ.
Bạn có thêm bản mã c của thông điệp mật.

## Files phát cho người chơi

- `output.txt` — chứa `n`, `e = 3`, `d_low` (d mod 2^176), `c`

## Mục tiêu

Khôi phục d (hay p, q) rồi giải mã. Flag dạng `crypto{...}`.

## Gợi ý

1. Từ `ed − k(N − p − q + 1) = 1`, nhân với p, rút gọn mod 2^s (s = 176):

   ```
   k·p² + (ed − kN − k − 1)·p + kN ≡ 0 (mod 2^s)
   ```

2. Với e = 3 chỉ có k ∈ {1, 2, 3}. Giải phương trình bậc hai mod 2^s
   (thư viện: `rsalib.solve_quad_mod_2k`) → ứng viên `p mod 2^s`.
3. Mỗi ứng viên p_low: `p = p_low + 2^s·x`, `x < 2^{80}` → Coppersmith
   (tương tự challenge 15) tìm x → p | N.

## Chạy lời giải (để kiểm tra)

```
python solve.py
```
