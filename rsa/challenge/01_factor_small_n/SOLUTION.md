# Lời giải — 01 Factorizing the public key

## Ý tưởng (theo tài liệu)

TASK 1 RSA ATTACK viết: *"Nếu số n quá nhỏ (ít hơn 256 bits), ta sẽ factor được
số n này."* Toàn bộ an toàn của RSA nằm ở việc không phân tích được `n = p·q`.
Với n nhỏ, bài toán phân tích thừa số trở nên khả thi → toàn hệ thống sụp đổ.

Chuỗi khai thác:

1. `n` = 224 bit, thừa số nhỏ nhất chỉ ~48 bit → thuật toán Pollard rho
   (bên trong `sympy.factorint`) tìm được trong vài chục giây
   (độ phức tạp ~ O(p^{1/2}) = 2^24 phép tính).
2. Có `p, q` → `phi(n) = (p-1)(q-1)`.
3. `d = e^{-1} mod phi(n)` (nghịch đảo modulo qua Euclid mở rộng).
4. `m = c^d mod n` → flag.

## Các bước + code

```python
from sympy import factorint
from Crypto.Util.number import long_to_bytes

n = ...; e = ...; c = ...   # từ output.txt
p, q = factorint(n)         # {'p':1,'q':1} — lấy 2 khóa
phi = (p-1)*(q-1)
d = pow(e, -1, phi)
print(long_to_bytes(pow(c, d, n)))
```

Ví dụ số học cỡ nhỏ (minh họa cơ chế, không phải số của challenge):
n = 15 = 3·5, phi = 8, e = 3 → d = 3 (3·3 = 9 ≡ 1 mod 8).
m = 4 → c = 4³ mod 15 = 64 mod 15 = 4. Giải mã: 4³ mod 15 = 4 = m. ✓

## Flag

```
crypto{sm4ll_n_g0_brrr}
```

## Cách phòng thủ

Dùng N ≥ 2048 bit (khuyến cáo trong tài liệu) và sinh p, q ngẫu nhiên độc lập.
