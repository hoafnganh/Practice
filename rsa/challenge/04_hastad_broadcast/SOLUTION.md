# Lời giải — 04 Håstad's broadcast

## Ý tưởng (theo survey §4.2)

Giả sử mọi `e_i = 3` và Bob gửi cùng `m` cho ≥ 3 bên với các mô-đun
`n_1, n_2, n_3` đôi một nguyên tố cùng nhau (nếu không, gcd đã lộ thừa số):

```
C_1 = m³ mod n_1,  C_2 = m³ mod n_2,  C_3 = m³ mod n_3
```

Áp dụng Định lý phần dư Trung Hoa (CRT): tồn tại duy nhất
`C ∈ Z_{n1·n2·n3}` thỏa `C ≡ m³` theo từng mô-đun. Vì `m < min(n_i)`,
`m³ < n1·n2·n3` → **C = m³ trên số nguyên**, không dính mod.
Căn bậc ba nguyên cho ngay m. Tổng quát (Theorem 6 trong survey): với phép
đệm tuyến tính khác nhau, đủ `k > e·deg` bản mã vẫn phá được bằng Coppersmith.

## Các bước + code

```python
from sympy.ntheory.modular import crt
import gmpy2
C, _ = crt([n1, n2, n3], [c1, c2, c3])
m, exact = gmpy2.iroot(int(C), 3)
print(long_to_bytes(int(m)))
```

Ví dụ số học nhỏ: n1 = 5·7 = 35 (giả đơn nguyên tố cùng nhau với n2, n3),
minh họa 2 mô-đun với e=2: n1 = 35, n2 = 11, m = 8 → m² = 64.
c1 = 64 mod 35 = 29, c2 = 64 mod 11 = 9. CRT: x ≡ 29 (35), x ≡ 9 (11) →
x = 64 = m² (nhỏ hơn 35·11 = 385 nên không bị mod) → m = 8. ✓

## Flag

```
crypto{h4st4d_0n3_m3ss4g3_m4ny_b0x3s}
```

## Cách phòng thủ

Đệm **ngẫu nhiên** (không tuyến tính, ví dụ OAEP) cho mỗi lần gửi — phép đệm
cố định hay tuyến tính đều bị survey §4.2 chỉ ra là không an toàn.
