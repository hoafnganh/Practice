# Lời giải — 02 Fermat's attack

## Ý tưởng (theo tài liệu)

HackMD doc: *"Nếu p và q đều có độ dài bit như nhau, và nếu chọn quá gần nhau,
thì sẽ bị tấn công Fermat."*

Cơ sở toán học:

```
n = p·q = ((p+q)/2)² − ((p−q)/2)² = a² − b²
```

Nếu `|p−q|` nhỏ thì `a = (p+q)/2` chỉ hơi lớn hơn `√n`. Thuật toán Fermat
thử lần lượt `a = ⌈√n⌉, ⌈√n⌉+1, …` và kiểm tra `a² − n` có chính phương không.
Số bước cần ≈ `(p−q)²/(8·√n)` — với p, q cách nhau ~2^260 bit trên N 1024 bit,
số bước chỉ cỡ vài trăm.

## Các bước + code

```python
import gmpy2
a = gmpy2.isqrt(n)
if a*a < n: a += 1
while True:
    b2 = a*a - n
    b = gmpy2.isqrt(b2)
    if b*b == b2: break
    a += 1
p, q = int(a-b), int(a+b)   # p*q == n
```

Sau đó như thường lệ: `phi = (p-1)(q-1)`, `d = e^{-1} mod phi`, giải mã.

Ví dụ số học nhỏ: n = 5183. √n ≈ 72.0 → thử a = 72: 72²−5183 = 1 = 1² →
b = 1 → p = 71, q = 73 (hai số nguyên tố sinh đôi — đúng tình huống tệ nhất).

## Flag

```
crypto{f3rm4t_tw1n_pr1m3s_s1t_cl0s3}
```

## Cách phòng thủ

Sinh p, q độc lập ngẫu nhiên; kiểm tra `|p−q|` đủ lớn (thực tế khóa chuẩn
luôn thỏa). Đây cũng là lý do không dùng `q = next_prime(p)`.
