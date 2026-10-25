# Lời giải — 09 Brute force small CRT-exponent (d_p)

## Ý tưởng (theo tài liệu)

`d_p = d mod (p−1)` nên `e·d_p = 1 + k·(p−1)`. Với mọi `r` nguyên tố cùng
nhau với p, định lý Fermat nhỏ cho:

```
r^{e·d_p} = r·(r^{p−1})^k ≡ r (mod p)
→ p | (r − r^{e·d_p} mod n)
→ gcd(r − r^{e·d_p} mod n, n) = p   (nếu cùng lúc ≡ r mod q thì được n — hiếm)
```

`d_p` nhỏ (~20 bit) → vét cạn toàn bộ. Mẹo quan trọng về hiệu năng:
`r^{e·d_p} = (r^e)^{d_p}` — tính `r^e mod n` **một lần**, mỗi ứng viên chỉ cần
lũy thừa với số mũ 20 bit (~30 phép nhân) thay vì số mũ e·d_p (~530 bit).

## Các bước + code

```python
import gmpy2
r_e = gmpy2.powmod(r, e, n)
for dp in range(1, 1 << 21):
    g = gmpy2.gcd(int(r - gmpy2.powmod(r_e, dp, n)), n)
    if 1 < g < n:
        p = int(g); break
```

Chạy ~20–60s với 2^20 ứng viên (gmpy2). Sau đó q = n/p, phi, d, giải mã.

Ví dụ số học nhỏ: p = 11, d_p = 3, e = 3^{-1} mod 10 = 7 (7·3 = 21 ≡ 1 mod 10).
e·d_p = 21 = 1 + 2·(p−1) ✓. r = 2: r^{21} mod p = 2^{21} mod 11 = 2097152 mod 11
= 2 (vì 2^{10} ≡ 1) ✓ → p | r − r^{e·d_p}: lấy n = p·13 = 143,
r − r^{21} mod n: r^{21} mod 143 = 12 → 2 − 12 = −10; gcd(10, 143) = 1?? —
cẩn thận: gcd phải tính với giá trị (r − r^{e·dp}) mod n: (2 − 12) mod 143 =
133; gcd(133, 143) = 11 = p ✓.

## Flag

```
crypto{sm4ll_dp_crt_brut3f0rc3}
```

## Cách phòng thủ

Sinh e chuẩn (65537) rồi suy ra d; sau đó kiểm tra `d_p = d mod (p−1)` và
`d_q = d mod (q−1)` phải lớn (thực tế chúng ~ n/2 bit nên an toàn). Survey §3
cũng lưu ý: nếu d_p, d_q quá nhỏ, có tấn công thời gian O(√d_p) tốt hơn cả
vét cạn (Boneh–Durfee–Frankel), nên tuyệt đối không để CRT exponent nhỏ.
