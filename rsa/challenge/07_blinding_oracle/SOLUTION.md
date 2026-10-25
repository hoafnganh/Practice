# Lời giải — 07 Decipher Oracle / Blinding

## Ý tưởng

HackMD doc: dịch vụ giải mã mọi ciphertext trừ khi kết quả chứa flag. Nhưng RSA
là **multiplicative homomorphism**: `D(A)·D(B) ≡ D(A·B) (mod n)`.

Gửi `c' = c·r^e mod n` (r ngẫu nhiên,vd r = 2):

```
D(c') = (c·r^e)^d = c^d · r^{ed} ≡ m·r (mod n)
```

Oracle trả về `m·r` — không phải flag nên không bị chặn. Chia lại cho r:

```
m = m·r · r^{-1} (mod n)
```

Đây chính là kỹ thuật **làm mù** trong survey §2.2 (Bob ký `M' = r^e·M` mà
không hay biết; ở đây vai "Bob" là oracle giải mã).

## Các bước + code

```python
r = 2
c_blind = c * pow(r, e, n) % n      # gui c_blind cho oracle
mp = ...                             # nhan ve m*r
m = mp * pow(r, -1, n) % n
print(long_to_bytes(m))
```

Ví dụ số học nhỏ: n = 91 = 7·13, e = 5, d = 29 (5·29 = 145 ≡ 1 mod 72).
m = 10 → c = 10⁵ mod 91 = 82. Chọn r = 3: c' = 82·3⁵ mod 91 = 82·243 mod 91
= 19926 mod 91 = 88·... tính: 91·218 = 19838, 19926−19838 = 88 → c' = 88.
Oracle: 88²⁹ mod 91 = 10·3 = 30 = m·r. Lấy 30·3^{-1} (3^{-1} mod 91 = 61):
30·61 = 1830 mod 91 = 1830 − 91·20 = 10 = m ✓.

## Flag

```
crypto{bl1nd1ng_0r4cl3_s1gn3d_my_m3ss4g3}
```

## Cách phòng thủ

Oracle giải mã/ký phải đệm ngẫu nhiên bên trong (OAEP cho mã hóa, PSS cho
chữ ký) — khi đó kẻ tấn công không dựng được quan hệ nhân giữa truy vấn và
mục tiêu. Survey §2.2 cũng chỉ ra blinding là công cụ của chữ ký mù (tiền
số ẩn danh) — tính chất vô hại nếu dùng đúng.
