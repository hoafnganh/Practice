# Lời giải — 05 Common Modulus (external)

## Ý tưởng (theo tài liệu)

Ta có `C_b = m^{e_b} mod n` và `C_c = m^{e_c} mod n` với cùng `m`, cùng `n`,
và `gcd(e_b, e_c) = 1`. Euclid mở rộng cho `u, v` sao cho

```
u·e_b + v·e_c = 1
```

Nhân hai congruence (với số mũ âm dùng nghịch đảo modulo n):

```
C_b^u · C_c^v = m^{u·e_b + v·e_c} = m (mod n)
```

Khá mã không cần biết p, q — tính chất multiplicative của RSA biến hai bản mã
thành bản rõ.

## Các bước + code

```python
u = pow(e_b, -1, e_c)          # Euclid mo rong (Python 3.8+)
v = (1 - u*e_b) // e_c
if u < 0: c_b, u = pow(c_b, -1, n), -u
if v < 0: c_c, v = pow(c_c, -1, n), -v
m = pow(c_b, u, n) * pow(c_c, v, n) % n
```

Ví dụ số học nhỏ (như HackMD doc): n = 1908...283, e_b = 31, e_c = 71 →
u = -16, v = 7 (vì -16·31 + 7·71 = -496 + 497 = 1). Vì u < 0 nên dùng
`inverse(C_b, n)^{16} · C_c^{7} mod n = m`.

## Flag

```
crypto{c0mm0n_m0dulus_n3v3r_sh4r3_N}
```

## Cách phòng thủ

Không bao giờ dùng chung N cho nhiều người dùng — mỗi cặp khóa phải có mô-đun
riêng (survey §2.1: "một mô-đun RSA không bao giờ nên được nhiều hơn một
thực thể sử dụng").
