# 14 — Bleichenbacher: tấn công oracle đệm PKCS#1 v1.5 (BB'98 / ROBOT)

**Dạng:** Oracle "khối đầu có = 0x00 0x02 không" → giải mã bản mã tùy ý
**Độ khó:** ★★★★★
**Nguồn:** `RSA-survey-vi.md` §5.3

## Mô hình

Đúng như survey §5.3 mô tả: ứng dụng giải mã mọi ciphertext gửi lên và **trả
lỗi** khi 16 bit cao của bản rõ ≠ `0x00 0x02` ("khối đầu 02" của PKCS#1 v1.5).
Trong thực tế đây là dịch vụ mạng (SSL/TLS thời 1998, ROBOT 2017); ở đây
oracle là **hàm cục bộ** (`challenge.py`) để có thể chạy hàng triệu truy vấn
offline trong vài giây.

## Files

- `challenge.py` — khóa 128-bit, e = 3, `oracle(x)` và các giá trị `n, e, ct`

## Mục tiêu

Giải mã `ct` (chứa `crypto{...}`) chỉ bằng oracle — không biết p, q, d.

## Gợi ý (thuật toán BB'98)

1. `K = 16` byte, `B = 2^{8(K−2)} = 2^112`. Block hợp lệ ⇔ `m ∈ [2B, 3B)`.
2. **Bước 2a:** quét tuần tự `s = ⌈n/3B⌉, +1, ...` — gửi `ct·s^e mod n`;
   hit đầu tiên xác nhận `m·s mod n ∈ [2B, 3B)` với một `r = ⌊m·s/n⌋`.
3. **Thu hẹp:** giữ `s ≈ 2B/w` (w = độ rộng khoảng chứa m) ⇒ mỗi WINDOW
   `[(2B+rn)/s, (3B−1+rn)/s]` rộng ~w/2 ⇒ **hit nào cũng halve khoảng**.
   Quét state-free giữa các hit; khi hit thì intersect khoảng với window.
4. Lặp tới khi khoảng hẹp (≤ 8) → quét ứng viên lấy block PKCS#1 → flag.

## Chạy lời giải (để kiểm tra)

```
python solve.py
```
