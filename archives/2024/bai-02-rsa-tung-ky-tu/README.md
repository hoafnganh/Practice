# bai-02-rsa-tung-ky-tu

**Thể loại:** crypto / RSA

## Đề bài

Flag bị mã hóa **từng ký tự một** bằng RSA không padding: mỗi ký tự `l` cho `format(pow(ord(l), E, N), '08X')` với N = p·q sinh từ `getPrime(12)` → N < 2²⁴ (xem `chall.py` và `text.txt`).

## Lời giải

- N quá nhỏ: brute mọi cặp prime trong `primerange(2, 4096)` (564 số) sao cho `n = p·q > max(ciphertext)` và **decrypt toàn bộ các khối đều ra ký tự printable** (32..126) — điều kiện này lọc gần hết ứng viên sai.
- Bộ thoả mãn: n = 1429 × 1531; tính `d = e⁻¹ mod (p−1)(q−1)` rồi giải từng khối 8 hex ra ký tự và ghép lại.

Xem `solve.sage` (chạy dưới 1 phút). `test.py` minh hoạ phép format 08X trên số nhỏ.

## Flag

Chạy `solve.sage`, flag là chuỗi ký tự in ra cuối.
