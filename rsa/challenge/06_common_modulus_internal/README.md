# 06 — Common Modulus (kẻ tấn công bên trong / Simmons)

**Dạng:** Dùng `d` của mình để phân tích N chung (Proposition 1), rồi khôi phục `d` của người khác
**Độ khó:** ★★★☆☆
**Nguồn:** `TASK 1 RSA ATTACK - HackMD.pdf` — mục *"Common Modulus — Internal Attacker"*; `RSA-survey-vi.md` §2.1 + Mệnh đề 1

## Câu chuyện

Công ty cấp cho mọi nhân viên khóa trên **cùng một mô-đun N** (để "dễ quản lý").
Bạn là nhân viên, biết cặp khóa của chính mình `(N, e, d)`. Sếp mã hóa thông
điệp mật bằng khóa riêng của ông `(N, e_boss)` và bạn có được bản mã `c_boss`
cùng khóa công khai `(N, e_boss)`.

## Files phát cho người chơi

- `output.txt` — chứa `n`, `e` (của bạn), `d` (của bạn), `e_boss`, `c_boss`

## Mục tiêu

Đọc thông điệp của sếp (chứa flag, dạng `crypto{...}`).

## Gợi ý

1. `e·d = 1 + k·phi(N)` với `k` nguyên, `1 ≤ k ≤ e` (vì `d < phi(N)`).
2. Như HackMD doc: bắt đầu `k = (e·d - 1) // n` rồi tăng dần; khi
   `k·phi == e·d - 1` (chia hết) và `phi` hợp lệ (kiểm tra `Δ = (n - phi + 1)² - 4n`
   là số chính phương) thì đã tìm được `phi(N)`.
3. `d_boss = inverse(e_boss, phi)` → giải mã.
4. Cách khác (Mệnh đề 1 trong survey): từ `d` phân tích trực tiếp N
   (`k = ed-1 = 2^t·r`, tìm căn bậc hai khác ±1 của 1, `gcd(x-1, N)`).

## Chạy lời giải (để kiểm tra)

```
python solve.py
```
