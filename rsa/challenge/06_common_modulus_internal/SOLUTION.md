# Lời giải — 06 Common Modulus (internal / Simmons)

## Ý tưởng

Survey §2.1 (Simmons): một mô-đun RSA **không bao giờ** được dùng chung —
người dùng hợp lệ có thể phá người dùng khác. Cơ chế: từ cặp `(e, d)` của mình
tìm được `phi(N) = N - p - q + 1`, từ đó sinh được `d` cho **mọi** số mũ khác
trên cùng N.

Cách 1 (theo HackMD doc — dùng trong solve.py): vì `e·d = 1 + k·phi(N)` với
`0 < k ≤ e`, chỉ có tối đa `e` ứng viên `k`. Với mỗi `k` chia hết
`(ed−1) % k == 0`, ứng viên `phi = (ed−1)/k` được kiểm tra hợp lệ bằng cách
giải phương trình bậc hai `x² − (n − phi + 1)x + n = 0` (nghiệm phải là p, q —
kiểm tra biệt thức chính phương).

Cách 2 (Mệnh đề 1 trong survey — phân tích N trực tiếp từ d):
`k = ed − 1 = 2^t·r` (r lẻ). Với g ngẫu nhiên, dãy `g^{k/2}, g^{k/4}, …`
chứa căn bậc hai khác ±1 của 1 theo mod N (xác suất ≥ 1/2);
`gcd(x−1, N)` lộ một thừa số. Code:

```python
k = e*d - 1
t = 0
while k % 2 == 0: k //= 2; t += 1
while True:
    g = random.randrange(2, n-1)
    x = pow(g, k, n)
    for _ in range(t):
        y = pow(x, 2, n)
        if y == 1 and x != 1 and x != n - 1:
            p = math.gcd(x - 1, n); print(p, n // p); return
        x = y
```

## Các bước (cách 1)

```python
ed1 = e*d - 1
k = ed1 // n
while k <= e:
    if ed1 % k == 0:
        phi = ed1 // k
        ... kiem tra chinh phuong ...
    k += 1
d_boss = pow(e_boss, -1, phi)
m = pow(c_boss, d_boss, n)
```

Ví dụ số học nhỏ: n = 77 = 7·11, phi = 60, e = 5 → d = 5·12+1?? tính:
d·5 ≡ 1 (mod 60) → d = 5? 5·5 = 25 ≠ 1 mod 60. d = 5·13 = 65... đúng: d = 5
không đúng; tìm d: 5d ≡ 1 (60) → d = 5·(5^{-1} mod 60)?? 5d = 1 + 60k →
d = 5, k... 5·5−1 = 24 = k·60? 24/60 không nguyên. d = 5·13−... d = 77? Thử
d = 5·k+... thực tế d = 5^{-1} mod 60: 5·12 = 60 ≡ 0; 5·5 = 25; 5·17 = 85 ≡ 25;
dùng Euclid: 60 = 12·5 + 0 → 5 và 60 KHÔNG nguyên tố cùng nhau (gcd=5) → ví
dụ này không hợp lệ; chọn e = 7: 7d ≡ 1 (60) → d = 43 (7·43 = 301 = 5·60+1 ✓),
k = 5. Từ (7, 43): ed1 = 300 → k ∈ {300//77=3..7}: k=5 → phi = 60 ✓
(kiểm tra: s = 77−60+1 = 18, Δ = 324−308 = 16 = 4² ✓). d_boss = 65537^{-1}...\
với e_boss = 13: d_boss = 37 (13·37 = 481 = 8·60+1 ✓).

## Flag

```
crypto{ins1d3r_j0b_pr0p0s1t10n_1_fact0r}
```

## Cách phòng thủ

Không dùng chung N; mỗi người dùng một mô-đun độc lập.
