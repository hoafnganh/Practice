# Lời giải — 12 Pollard's p−1

## Ý tưởng (survey §1.1)

Survey: *"nếu p−1 là tích của các thừa số nguyên tố nhỏ hơn B, thì N có thể bị
phân tích trong thời gian nhỏ hơn B³."*

Cơ chế: nếu mọi thừa số nguyên tố của `p−1` ≤ B thì `(p−1) | B!` (vì B! chứa
mọi lũy thừa cần). Theo Fermat nhỏ, với mọi a: `a^{B!} ≡ 1 (mod p)`.
Tính `A = 2^{B!} mod N` dần bằng `a ← a^j mod N` (j = 2..B — mỗi bước "bổ sung"
lũy thừa j). Khi đó `p | A − 1` nhưng thường `q ∤ A − 1`:

```
gcd(A − 1, N) = p
```

## Các bước + code

```python
a = 2
for j in range(2, B+1):
    a = pow(a, j, n)
    if j % 64 == 0:
        g = math.gcd(a - 1, n)
        if 1 < g < n: p = g; break
```

Ví dụ số học nhỏ: p = 211 (p−1 = 210 = 2·3·5·7 — 7-smooth), q = 331,
N = 211·331 = 69841. Với B = 10: A = 2^{10!} mod N — 10! = 3628800 chia hết
cho 210 → A ≡ 1 (mod p); A − 1 mod N → gcd → 211. (Thử bằng code:
`pollard_p1(69841, B=20)`.)

## Flag

```
crypto{p0ll4rd_p_m1nus_1_sm00th}
```

## Cách phòng thủ

Sinh p sao cho p−1 có thừa số lớn (vd p = 2p' + 1 với p' nguyên tố lớn —
"số nguyên tố an toàn"), hoặc dùng thư viện chuẩn có kiểm tra.
Williams p+1 / ECM là các biến thể tấn công khi p±1 smooth.
