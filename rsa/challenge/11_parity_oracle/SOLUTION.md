# Lời giải — 11 Parity (LSB) Oracle

## Ý tưởng (theo tài liệu)

Oracle trả về chẵn/lẻ của `D(x)` cho mọi x ta chọn. Nhân bản rõ bằng 2:

```
D(ct·2^e mod n) = 2m mod n
```

Vì `n` lẻ: `2m mod n` chẵn ⇔ `2m < n` (tức `m < n/2`); lẻ ⇔ `m > n/2`.
Lặp lại với 4, 8, 16, …: parity của `m·2^k mod n` cho biết `m·2^{k−1} mod n`
nằm trong nửa nào → **tìm kiếm nhị phân** m trong [0, n). Sau ⌈log₂ n⌉ ≈ 512
truy vấn, khoảng thu hẹp về đúng m.

## Các bước + code

```python
lb, ub = 0, n
cq = ct
c2e = pow(2, e, n)
for i in range(n.bit_length() + 8):
    cq = cq * c2e % n               # ban ro nhan 2
    mid = (lb + ub) // 2
    if oracle(cq) == "Even":
        ub = mid
    else:
        lb = mid
# quet [lb-2, ub+2] tim m voi pow(m, e, n) == ct
```

Ví dụ số học nhỏ: n = 143 = 11·13 (lẻ), m = 100. 2m = 200 > n →
2m mod n = 57 → lẻ ⇒ m > n/2 ✓ (100 > 71.5). Tiếp: 4m mod n = 400 − 2·143
= 114 → chẵn... chuỗi parity quyết định từng bit của 100/n.

## Flag

```
crypto{lsb_0r4cl3_b1n4ry_s34rch}
```

## Cách phòng thủ

Không bao giờ trả về **bất kỳ** thông tin nào về bản rõ cho ciphertext không
được xác thực (mã xác thực AEAD, không dùng raw RSA). Cùng họ với Bleichenbacher
(challenge 14): chỉ cần một bit thông tin mỗi truy vấn là đủ phá toàn hệ thống.
