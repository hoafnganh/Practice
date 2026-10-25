# Cheatsheet Crypto

Thư viện đi kèm khi luyện tập CryptoHack: `Cryptohack Libs cần dùng.md`.

# Chap 1

## Số nguyên tố, Phân tích thừa số nguyên tố, Trường hữu hạn

Thông thường: trong mod m, a có nghịch đảo trong Z/mZ khi và chỉ khi gcd(a,m)=1

Tuy nhiên, nếu m là nguyên tố, thì ta có mọi phần tử khác 0 trong Z/mZ đều có nghịch đảo

Khi làm 1 bài liên quan đến số nguyên tố, hãy check nó có phải là thặng dư bậc hai, hoặc có tính chất gì đặc biệt không.

# Modular arithmetic

Extended GCD:

```python
def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

print(egcd(26513, 32321))
```

# Modulo nghịch đảo

Sage

```python
a = 3
m = 11

kq = inverse_mod(a, m)
print(kq)  # Kết quả: 4 (vì 3 * 4 = 12 ≡ 1 mod 11)
```

hoặc:

```python
a = 3
m = 11

# Sử dụng Zmod
kq1 = Zmod(m)(a)^-1

# Hoặc sử dụng hàm mod()
kq2 = mod(a, m)^-1
```

# Thặng dư bậc hai

```python
p = 29
ints = [14,6,11]

for x in ints:
    if Mod(x, p).is_square():
        print(x)
        print(Mod(x, p).sqrt(), p - Mod(x, p).sqrt())
        
# Bạn cũng có thể dùng ký hiệu Legendre (Kronecker symbol)
# Trả về 1 (có), -1 (không), hoặc 0 (x chia hết cho p)
leg = kronecker(x, p) 
print(f"Ký hiệu Legendre: {leg}")
```

Quadratic Residue * Quadratic Residue = Quadratic Residue

Quadratic Residue * Quadratic Non-residue = Quadratic Non-residue

Quadratic Non-residue * Quadratic Non-residue = Quadratic Residue

# Đối tượng Mod()

```python
a = Mod(6, 29) # Output: obj
b = Mod(31, 29)
print(1 / a) # Nếu như không có sẽ trả về ZeroDivisionError: inverse of Mod(x, p) does not exist
print(b) # Trả về 2
```

# CRT

```python
# Danh sách các số dư (a_i)
rem = [2, 3, 2]

# Danh sách các modulo (m_i)
mod = [3, 5, 7]

# Tính nghiệm x dương nhỏ nhất
x = crt(rem, mod) # tra ve Sage Integer -> doi thanh int(x)

print(f"Nghiệm của hệ là: {x}")
```

# Public key

```python
import hashlib
```

```bash
pip install git+https://github.com/elliptic-shiho/primefac-fork@master
```

# Căn bậc n

```python
ct = <int>
print(long_to_bytes(ct.nth_root(3)))
```

# Căn nguyên thuỷ

Cấp của a modulo n là d min sao cho $a^d \equiv 1$ mod n

Căn nguyên thuỷ g là số có thể biểu diễn trường hữu hạn p (p: prime) dạng: $g^1,g^2,...,g^{p-1}$

Vậy cấp của g phải là p - 1.

Công thức tính cấp của g theo p - 1:

$$
ord(g)=\frac{p-1}{gcd(k,p-1)}
$$

```python
# Khai báo số nguyên tố p
p = 17

# 1. Tìm một căn nguyên thủy đầu tiên
g = primitive_root(p)

# 2. Tạo danh sách tất cả các căn nguyên thủy
# Bằng cách tính g^k mod p với những k nguyên tố cùng nhau với p-1
all_roots = [power_mod(g, k, p) for k in range(1, p) if gcd(k, p - 1) == 1]
```

# DLP

$$
base^x = target
$$

```python
discrete_log(target, base) # BSGS

Alice_pub = E(public_x, public_y) # Pohlig / BSGS

# Hàm .log() của SageMath tự động áp dụng Pohlig-Hellman / BSGS
n = Alice_pub.log(G) # G: generator
```

# Elliptic

```python
p = 97 # Khai báo số nguyên tố
F = GF(p) # Khởi tạo trường hữu hạn F_97
    
# Đường cong y^2 = x^3 + 2x + 3 trên modulo 97
E_finite = EllipticCurve(F, [2, 3])
    
# Đếm tổng số điểm (Order) trên đường cong theo Định lý Hasse
print("Số điểm trên đường cong:", E_finite.cardinality())
    
# Sinh một điểm ngẫu nhiên
G = E_finite.random_point()
print("Điểm ngẫu nhiên G:", G)
    
# Phép nhân vô hướng (Scalar multiplication) - Cốt lõi của ECC
k = 15
print("15 * G =", k * G)
# Point in ECC
P = E_finite(100, 100)
```

Khai báo mỗi G.x để tự tìm điểm y:

```python
G.lift_x(<x>)

```

# Montgomery

```python
# Montgomery curve: By^2 = x^3 + Ax^2 + x
p = 2 ** 255 - 19
A, B = 486662, 1
# [1, a2, a3, a4, a6] ứng với y^2 + a1xy + a3y = x^3 + a2x^2 + a4x + a6 Nếu B = 1
E = EllipticCurve(GF(p), [0, A, 0, 1, 0])
G = E.lift_x(9)
k = bin(0x1337c0decafe)[2:] # class 'sage.rings.integer.Integer'>

def add(P, Q):
    x1, y1 = P.xy()
    x2, y2 = Q.xy()
    alpha = (y2 - y1) / (x2 - x1)
    x3 = alpha ** 2 - A - x1 - x2
    y3 = alpha * (x1 - x3) - y1
    return E(x3, y3)
def doubling(P):
    x1, y1 = P.xy()
    alpha = (3 * x1 ** 2 + 2 * A * x1 + 1) / (2 * y1)
    x3 = alpha ** 2 - A - 2 * x1
    y3 = alpha * (x1 - x3) - y1
    return E(x3, y3)

def algo(P, k): # Q = kP
    R0, R1 = P, doubling(P)
    for i in k[1:]:
        if i == '0':
            R0, R1 = doubling(R0), add(R0, R1)
        else: R0, R1 = add(R0, R1), doubling(R1)
    return R0

print(algo(G, k).xy())

```