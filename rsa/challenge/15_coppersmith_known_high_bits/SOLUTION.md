# Lời giải — 15 Coppersmith: known high bits of p

## Ý tưởng (survey §4.1 Định lý 3 + §4.5 Định lý 10)

Survey (Định lý 10): *"Cho N = pq là mô-đun RSA dài n bit. Khi biết n/4 bit
có trọng số thấp nhất của p hoặc n/4 bit có trọng số cao nhất của p, ta có
thể phân tích N thành thừa số một cách hiệu quả."*

Cụ thể: `p = p_high·2^u + x` với `x < 2^u ≈ N^{1/4}`. Đa thức
`f(x) = p_high·2^u + x` (monic) có nghiệm `x₀ = x` **theo modulo p** — tức là
theo modulo một thừa số N^{1/2} của N.

**Howgrave-Graham:** dựng các đa thức `g_{i}(x) = N^{m−i}·f(x)^i` (mọi chứng
thức đều ≡ 0 mod p^m tại x₀ vì N ≡ 0 và f(x₀) ≡ 0 mod p) cùng các shift
`x^a·f(x)^m`. Xếp thành lattice (cột = hệ số của `g(xX)`), chạy LLL: vector
ngắn ⇒ đa thức h với `|h(x₀)| < p^m` và `h(x₀) ≡ 0 mod p^m` ⇒ `h(x₀) = 0`
**trên số nguyên** ⇒ phân tích thừa số h (flint `fmpz_poly.factor`) lấy nghiệm.

Điều kiện nghiệm: `2^{w/4}·det(L)^{1/w} < p^m/√w` — với m = t = 8, u = 116
(N 512-bit) cận được thỏa dư ~200 bit → LLL chạy < 0.1 s.

## Các bước + code

```python
import rsalib as R
p = R.coppersmith_known_high_bits(n, p_high, U, m=8, t=8)[0]
q = n // p
phi = (p-1)*(q-1)
d = pow(e, -1, phi)
print(long_to_bytes(pow(c, d, n)))
```

Ví dụ số học nhỏ (cùng cơ chế, kiểm chứng được bằng tay): N = 91 = 7·13.
p = 7, biết p_high·2^1 = 6 (bit cao của 7 = 1... minh họa 7 = 6 + 1:
p_high = 3, u = 1, x₀ = 1). f(x) = 6 + x có nghiệm 1 mod 7. Với N to, lattice
thay cho việc thử tay — nguyên lý giống hệt bổ đề Howgrave-Graham: poly chuẩn
nhỏ + nghiệm mod N^m ⇒ nghiệm nguyên.

## Flag

```
crypto{c0pp3rsm1th_kn0wn_h1gh_b1ts}
```

## Cách phòng thủ

Không bao giờ để rò rỉ một phần khóa — survey §4.5 (Boneh–Durfee–Frankel)
chứng minh mạnh hơn: chỉ cần ¼ bit của **d** cũng đủ khôi phục toàn bộ khóa
(khi e < √N) — xem challenge 17.
