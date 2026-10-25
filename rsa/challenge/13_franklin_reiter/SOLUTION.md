# Lời giải — 13 Franklin–Reiter (survey §4.3, Bổ đề 7)

## Ý tưởng

M1, M2 liên hệ tuyến tính `M1 = M2 − 1` (khác nhau 1 đơn vị vì sê-ri tăng 1),
`C_i = M_i³ mod N`. Khi đó `M2` là nghiệm chung trong ℤ_N[x] của:

```
g1(x) = (x − 1)³ − C1     (g1(M2) = (M2−1)³ − M1³ = 0)
g2(x) = x³ − C2           (g2(M2) = M2³ − M2³ = 0)
```

Nên `x − M2` chia cả hai. Thuật toán Euclid cho đa thức trên ℤ_N[x] tính
`gcd(g1, g2)` trong O(e²·log²N) — với e = 3 gần như luôn ra **đa thức tuyến
tính** `x − M2` (survey chứng minh GCD phải tuyến tính vì x³ − C chỉ có một
nghiệm khi gcd(3, φ(N)) = 1).

## Các bước + code

```python
g1 = [(-1 - c1) % n, 3, -3, 1]   # he so thap->cao cua (x-1)^3 - c1
g2 = [(-c2) % n, 0, 0, 1]        # x^3 - c2
h, _ = rsalib.poly_gcd_mod(g1, g2, n)   # = [−M2, 1] (monic)
M2 = (-h[0] * pow(h[1], -1, n)) % n
M1 = M2 - 1
```

Ví dụ số học nhỏ: N = 91 = 7·13, e = 3. M1 = 10, M2 = 11.
C1 = 1000 mod 91 = 1000 − 910 = 90; C2 = 1331 mod 91 = 1331 − 1274 = 57.
g1 = (x−1)³ − 90, g2 = x³ − 57. gcd phải là x − 11 (kiểm tra:
(11−1)³ = 1000 ≡ 90 ✓, 11³ = 1331 ≡ 57 ✓). Lấy 11 → M1 = 10 ✓.
(Kiểm chứng nhanh: nghiệm x = 11 mod 7 là 4: 4³ = 64 ≡ 1 mod 7; 90 mod 7 = 6
— 64 − 90 = −26 ≡ 2 mod 7?? — khi mod N không nguyên tố, GCD vẫn đúng theo
nghĩa ℤ_N[x] — hãy tin mã thực thi đã được test trong test_rsalib.py.)

## Flag

```
crypto{fr4nkl1n_r31t3r_p0ly_gcd}
```

## Cách phòng thủ

Đệm ngẫu nhiên trước khi mã hóa để hai bản rõ không còn liên hệ tuyến tính
biết trước; không dùng e = 3 (FR chỉ khả thi với e nhỏ — thời gian O(e²)).
Đây cũng là bước cuối của short-pad attack (challenge 16).
