# Cheatsheet — RSA & mật mã bất đối xứng

Tổng hợp kỹ thuật đánh RSA theo hướng "tín hiệu trong đề → dạng tấn công → công thức → code → bẫy". Phần lớn ví dụ lấy từ bộ 29 bài RSA của CryptoHack (cryptohack.org/challenges/rsa) và 18 dạng chuẩn có solve mẫu trong repo.

Tài liệu đi kèm trong repo:

- Lý thuyết nền: `rsa/RSA-survey-vi.md` — bản dịch tiếng Việt bài "Twenty Years of Attacks on the RSA Cryptosystem" (Dan Boneh, 1999), đọc khi cần hiểu **vì sao** mỗi attack hoạt động.
- 18 dạng chuẩn kèm generator + solve: `rsa/challenge/` (solve mẫu `rsa/solves/`, thư viện `rsa/challenge/_lib/rsalib.py`).
- Phần lattice (Coppersmith, Boneh–Durfee, Bleichenbacher): `lattice/` (12 bài L01–L12 có SOLUTION.md).
- Sơ đồ quyết định dạng bài: `RSA - Sơ đồ nhận diện dạng bài.md`.
- Tooling: `tools.md`.

## 0. Nền tảng 60 giây

```python
pow(a, e, n)                 # modexp gốc — KHÔNG BAO GIỜ dùng a**e % n với số lớn
d = pow(e, -1, phi)          # python 3.8+; gcd(e, phi) phải = 1
from Crypto.Util.number import long_to_bytes, bytes_to_long
m = pow(c, d, n); print(long_to_bytes(m))
```

**φ theo cấu trúc của n** — bước đầu tiên luôn là hỏi "n thật sự là gì":

| n | φ(n) | Ghi chú |
|---|---|---|
| p·q (khác nhau) | (p−1)(q−1) | chuẩn |
| p (n nguyên tố) | n − 1 | đề lừa bằng n "không phân tích được" |
| p² | p·(p−1) | **KHÔNG PHẢI (p−1)²**; p = isqrt(n) |
| Π pᵢ (nhiều prime) | Π (pᵢ − 1) | nhân theo ĐỦ thừa số, kể cả bội |

d chỉ cần thoả mãn mod lcm(p−1, q−1) cũng decrypt được — Useful khi đề cho d lỗi một chút.

## 1. Bản đồ 29 bài RSA CryptoHack → kỹ thuật

| Section | Bài | Kỹ thuật |
|---|---|---|
| Starter (6) | Modular Exponentiation, Public Keys, Euler's Totient, Private Keys, RSA Decryption, RSA Signatures | pow / φ / d / sign cơ bản |
| Primes Part 1 (5) | Factoring, Inferius Prime, Monoprime, Square Eyes, Manyprime | factordb; φ biến thể |
| Public exponent (6) | Salty, Modulus Inutilis, Everything is Big, Crossed Wires, Everything is Still Big, Endless Emails | e=1; căn nguyên; Wiener; factor-N-từ-d; Boneh–Durfee; Håstad |
| Primes Part 2 (5) | Infinite Descent, Marin's Secrets, Fast Primes, "Ron was Wrong, Whit is Right", RSA Backdoor Viability | Fermat; Mersenne; ROCA; batch GCD; Cheng 4p−1 |
| Padding (2) | Bespoke Padding, Null or Never | Franklin–Reiter; small-e + wrap |
| Signatures 1 (3) | Signing Server, Let's Decrypt, Blinding Light | sign=decrypt; chosen-modulus e=1; blinding |
| Signatures 2 (2) | Vote for Pedro, Let's Decrypt Again | căn bậc e mod 2^k; smooth modulus + dlog |

## 2. Phân tích N — thang bậc

Thứ tự thử **luôn luôn** là: nhãn đặc biệt → factordb → Fermat → p−1 → ECM → tool tổng hợp. Đề nào "sạch sẽ" cũng có tín hiệu ở source (xem bảng mục 11).

### 2.1 factordb

```python
from factordb.factordb import FactorDB
f = FactorDB(n); f.connect()
print(f.get_status(), f.get_factor_list())   # status 'C' = chưa factor xong
# list có thể chứa thừa số GHÉP — luôn tự kiểm p*q == n và isprime từng thừa số
```

n dưới ~256 bit thường nằm sẵn trong DB. 150-bit thì gần như chắc chắn.

### 2.2 Fermat (p ≈ q)

```python
from gmpy2 import isqrt
def fermat(n, max_iter=10**6):
    a = isqrt(n)
    if a*a < n: a += 1
    for _ in range(max_iter):
        b2 = a*a - n
        b = isqrt(b2)
        if b*b == b2: return int(a-b), int(a+b)
        a += 1
```

Tín hiệu: `next_prime(p)`, q sinh từ cùng base, n cân bằng lớn mà DB không có. Chạy 1–2 phút trước khi nghĩ tiếp — rẻ vô cùng so với scaffold attack khác. Gotcha: PARI/GP `factorint` **không** có bước Fermat đầu tiên (chuỗi thật: trial division → Rho/SQUFOF → ECM → MPQS) — với N cân bằng 8192-bit nó treo vĩnh viễn, trong khi python 5 dòng trúng vòng 1. Flags PARI nếu cần ép: 1=avoid MPQS, 2=avoid ECM giai đoạn 1, 4=avoid Rho/SQUFOF, 8=bỏ ECM cuối.

### 2.3 Pollard p−1 (p−1 smooth)

```python
def pollard_p1(n, B=65536):
    a = 2
    for j in range(2, B):
        a = pow(a, j, n)
        g = gcd(a - 1, n)
        if 1 < g < n: return g
```

Tín hiệu: `p = M + 1` với M = tích các prime nhỏ. Kèm p+1 (Williams) nếu đề sinh prime kiểu đặc biệt. B = 65536 thường đủ cho đề CTF.

### 2.4 Dạng đặc biệt của N

- **N gần luỹ thừa 2 / dạng đa thức**: chuyển sang đa thức theo cơ số 2 rồi factor đa thức (Sage):
  ```python
  poly = sum(e * x^i for i, e in enumerate(n.digits(2)))
  print(poly.factor())     # thừa số đa thức → thử lại mod 2^k cơ số
  ```
- **Mersenne primes**: p, q ∈ danh sách ~51 prime Mersenne 2^k − 1 biết trước → trial division cả danh sách (k đến 82589933).
- **N lặp bit/đẹp**: thử chia cho các số repunit, 2^k±1.

### 2.5 ECM / tool tổng hợp

- PARI: `factor(n)` tốt tới thừa số ~60–70 chữ số; sage có `ecm(B1)`.
- RsaCtfTool: `--attack all` chậm vài phút — đoán được heuristic thì chỉ định đúng attack.

## 3. Sinh prime có cấu trúc = tự sát

- **ROCA (Infineon)**: `p = k·M + 65537^a mod M`, M = primorial 40 prime đầu. Primes sống trong tập con nhỏ có cấu trúc ⟹ Coppersmith khai thác (`rocapolice`/crypto-attacks). N nhỏ (511 bit) thì factordb có sẵn.
- **Cheng 4p−1**: `4p − 1 = D·s²` (D squarefree, class number nhỏ, vd 427) → factor bằng phương pháp nhân phức (complex multiplication, Lucas sequence + gcd): `crypto-attacks/attacks/factorization/complex_multiplication.py`. Đây là dạng "backdoor có chủ ý".
- **Chung prime giữa các key (entropy kém)**: batch GCD —
  ```python
  for i, j in combinations(range(len(ns)), 2):
      g = gcd(ns[i], ns[j])
      if g != 1: p, q = g, ns[i] // g     # factor xong 2 key cùng lúc
  ```
  Gotcha: ~vài chục cặp có thể chia nhau >1 prime (gcd composite) — lọc `g.bit_length() == n.bit_length()//2` hoặc kiểm `isprime(g)` rồi mới tin.

## 4. e nhỏ & không padding

- **e = 1**: `c = m mod n` — không mã hóa gì cả, `long_to_bytes(c)` xong.
- **m^e < n** (chưa wrap): `m, ok = gmpy2.iroot(c, e); assert ok` — **luôn kiểm tra cờ exact**, iroot không exact nghĩa là đã wrap (hoặc đề sai hướng).
- **Håstad broadcast**: cùng m, cùng e, ≥ e modulus đôi một nguyên tố cùng nhau:
  ```python
  from itertools import combinations
  for grp in combinations(zip(ns, cs), e):
      N = prod(n for n, _ in grp)
      M = sum(c * pow(N//n, -1, n) * (N//n) for n, c in grp) % N   # CRT
      m, ok = gmpy2.iroot(M, e)
      if ok: print(long_to_bytes(m))
  ```
  Gotcha: không phải bộ nào cũng cùng m — nếu đề trộn nhiễu, brute mọi tổ hợp e phần tử và check prefix flag.
- **Padding null (đã biết trước)**: m = FLAG ∥ 0^k ⟹ c ≡ FLAG³·256^{3k}: nhân với `pow(256**(3*k), -1, n)`, sau đó true value là `t + j·n` với j nhỏ — brute j rồi `iroot`:
  ```python
  for flag_len in range(20, 81):
      t = c * pow(256**(3*(100-flag_len)), -1, n) % n
      for j in range(2**24):
          m, ok = gmpy2.iroot(t + j*n, 3)
          if ok and long_to_bytes(m).startswith(b"crypto{"): ...
  ```
  Tương đương Coppersmith stereotyped message (x³ − t, sage `small_roots`) — bản brute j dễ viết hơn và đủ nhanh khi khối wrap ít.

## 5. e KHỔNG LỖ ⇒ d nhỏ

Dấu hiệu: `e.bit_length() ≈ n.bit_length()` ⟹ d được sinh trước (đề chọn d nhỏ rồi tính e = d⁻¹ mod φ).

### 5.1 Wiener (d < N^0.25/3)

Liên phân số của e/N cho các hội tụ (k, d); với mỗi hội tụ tính φ = (e·d − 1)/k, giải p+q = n − φ + 1, kiểm Δ = (p+q)² − 4n là chính phương. Tool: `pip install owiener; owiener.attack(e, n)`. Logic tự viết: `rsalib.wiener_attack` (`rsa/challenge/_lib/`).

### 5.2 Boneh–Durfee (d < N^0.292)

Wiener fail nhưng e vẫn ~ bit(n) ⟹ thử Boneh–Durfee (Coppersmith 2 biến: x(A+y)+1 mod e với A = N+1). Solve mẫu chạy được: `lattice/L11_boneh_durfee/`; hoặc `crypto-attacks/shared/boneh_durfee.py`. Chậm hơn Wiener nhiều (cần LLL nhiều lần).

### 5.3 d_p nhỏ (~20 bit)

Tín hiệu: `e = pow(dp, -1, p-1)` trong source ⟹ e ~ bit(n)/2. Brute dp:
```python
for dp in range(1, 2**20):
    r = 2
    if 1 < gcd(r - pow(pow(r, e, n), dp, n), n) < n:   # = p
```
Chuẩn hơn: kiểm `pow(2, e·dp, p) == 2` với candidate p thu được.

## 6. Cùng modulus N

- **Không có d** (2 bản mã, gcd(e1,e2)=1): Bézout a·e1 + b·e2 = 1 ⟹ m = c1^a · c2^b mod n.
```python
a, b = xgcd(e1, e2)[:2]
assert a*e1 + b*e2 == 1                  # Bézout THẬT, hệ số âm cũng được
m = pow(c1, a, n) * pow(c2, b, n) % n    # py3.8+: pow mũ âm tự dùng nghịch đảo (cần gcd(c,n)=1)
```
  **Bẫy kinh điển**: dùng `pow(e1,-1,e2)` và `pow(e2,-1,e1)` ghép lại cho ra m^(1+e1·e2) — không phải m. Phải dùng Bézout thật (đúng đẳng thức = 1, kể cả hệ số âm).
- **Có d của mình**: mạnh hơn nhiều —
  - Cách 1 (suy φ): k = (e·d − 1)//n, tăng dần tới khi (e·d−1) chia hết cho k và φ = (e·d−1)/k cho Δ = (n − φ + 1)² − 4n chính phương → p, q.
  - Cách 2 (factor xác suất, tổng quát cho mọi cấu trúc N): viết e·d − 1 = 2^s·t; chọn g ngẫu nhiên, x = g^t, bình phương liên tiếp tới khi gặp 1; gcd(x − 1, n) tại bước trước đó cho thừa số không tầm thường.
- Sau khi có φ: mọi "bạn bè" dùng cùng N với e_i khác → decrypt bằng `d_i = pow(e_i, -1, phi)`. Nếu đề mã hóa **tuần tự qua nhiều lớp** (m^(e1·e2·…)), decrypt theo **thứ tự ngược lại** và cập nhật c mỗi vòng.

## 7. Bản tin liên quan nhau

- **Franklin–Reiter** (mã hóa cùng N, cùng e, quan hệ tuyến tính biết trước m2 = a·m1 + b): gcd đa thức trong Z_n[x] của f1(x) = (x)^e − c1 và f2(x) = (a·x+b)^e − c2 bằng (x − m1). Implement: khai triển (a·x+b)^e bằng **định lý nhị thức** (C(e,k)·a^k·b^(e−k)), Euclid đa thức mod n (chuẩn hóa monic bằng nghịch đảo hệ số dẫn; nghịch đảo không tồn tại ⟹ đã factor được N ngay tại đó). Solve mẫu: `rsa/challenge/13_franklin_reiter/`.
- **Short-pad** (cùng m ± pad ngắn, e=3, không biết hiệu pad): resultant của x³ − c1 và (x+y)³ − c2 theo x cho đa thức theo y = r2 − r1 → tìm y (Coppersmith small_roots) → về Franklin–Reiter.
- **Coppersmith bit cao của p** (biết ≥ n/4 bit cao): `p = p_high·2^u + x`, tìm x bằng `small_roots` (sage):
  ```python
  R.<x> = PolynomialRing(Zmod(n))
  f = p_high*2^u + x
  roots = f.small_roots(X=2^u, beta=0.4)   # X = chặn trên của x
  ```

## 8. Oracle & chữ ký

- **Signing server = decryption oracle**: RSA textbook ký s = m^d — gửi **chính ciphertext của secret** vào endpoint sign là nhận lại plaintext. Đây là lý do chữ ký thật phải hash trước.
- **Blinding**: (r^e·m)^d = r·m^d ⟹ sign bản che m·r rồi nhân r⁻¹. Vừa là tấn công (vượt filter nội dung), vừa là kỹ thuật phòng thủ chống timing. r ngẫu nhiên, nguyên tố cùng nhau với n.
- **Parity oracle** (server trả chẵn/lẻ của pow(c, d, n)): gửi c·(2^k)^e → m·2^k mod n; bit parity = bit cao nhất của m → binary search toàn bộ m sau log₂(n) query.
- **Bleichenbacher BB'98** (oracle conform PKCS#1 v1.5, 2 byte đầu = 00 02): quét s sao cho c·s^e conform [2B, 3B), thu hẹp khoảng chứa m. Chi tiết implementation + solve mẫu: `lattice/L12_bleichen_lattice/` và `rsa/challenge/14_bleichenbacher_pkcs1/`.
- **Chosen-modulus, e = 1**: verify tự cho mình chọn N, e ⟹ chọn e=1, N = SIGNATURE − digest sao cho `sig mod N == digest`. Cần reproduce đúng encoding EMSA-PKCS1-v1.5 (khối 256 byte).
- **Chosen-modulus smooth + dlog**: N = p^k với p nhỏ (vd 41^144) → nhóm nhân smooth → Pohlig–Hellman (có Hensel lift cho phần p^(k−1)) tính **e sao cho** sig^e == digest với digest bất kỳ ⟹ "chữ ký" hợp lệ cho mọi message. Cần sig là phần tử sinh (kiểm `pow(g, 20, P) != 1` và `pow(g, 8, P) != 1` cho P=41; không thì reconnect lấy sig khác).
- **Căn bậc e mod 2^k** (unpadding kiểu "cắt sau byte 00 cuối"): verify chỉ nhìn giá trị mod 256^len — với e lẻ, luỹ thừa bậc e là song ánh trên nhóm lẻ mod 2^k ⟹ giải x^e ≡ target (mod 2^k) bằng Sage `Mod(target, 256**15).nth_root(3)` — không cần d, không cần N.
- **CRT fault** (1 chữ ký sai): gcd(ŝ^e − m, n) = p với chữ ký lỗi (Bellcore). Duyệt log các cặp (m_i, s_i).
- **Timing (Kocher)**: T_i tương quan với cost phép nhân theo từng bit của d — hồi quy bit-by-bit từ LSB.
- **Partial key exposure (BDF)**: biết ≥ ⌈n/4⌉ bit thấp của d → giải phương trình bậc 2 mod 2^s thu p mod 2^s → Coppersmith bit thấp. `rsa/challenge/17_bdf_partial_key_exposure/`.

## 9. Padding trong thực tế

- **OAEP** (PKCS#1 v2): decrypt bằng `PKCS1_OAEP.new(key).decrypt(ct)` — KHÔNG dùng pow trực tiếp.
- **PKCS#1 v1.5 decrypt**: pow xong cắt phần sau byte 0x00 đầu tiên.
- **EMSA-PKCS1-v1.5 encode** (khi cần tự dựng khối verify): `00 01 FF..FF 00 || HashInfo || H(msg)` đủ độ dài khối.
- RSA.construct cần **int thuần python** — kết quả gmpy2 mpz phải `int()` lại.
- `Crypto.Util.number.inverse` theo phiên bản pycryptodome: ≤3.16 trả về 0 khi không khả nghịch (im lặng!), 3.17–3.21 raise, ≥3.22 ổn. Trong môi trường lạ, ưu tiên `pow(x, -1, m)` (py3.8+).

## 10. Gotchas tổng hợp

- Sage: `^` là **lũy thừa** (preparser), `^^` mới là XOR — ngược hoàn toàn với python thuần.
- `gmpy2.iroot` trả tuple (nghiệm, cờ exact) — quên kiểm cờ là nhận nghiệm sát số.
- Mọi phép "gcd(x^e − c_i, y^e − c_j)" kiểu known-plaintext RSA: chạy gcd trên nhiều cặp, thừa số chung t·n có thể kèm hệ số t — chia thử.
- CRT yêu cầu các modulus **nguyên tố cùng nhau từng cặp** — gặp cặp không coprime thì chính gcd đó là thừa số (tấn công luôn).
- `long_to_bytes` số 0 đầu bị mất — khi cần độ dài cố định, `rjust(n, b'\0')`.
- Wiener fail ⟹ đừng tăng số hội tụ vô hạn; chuyển sang Boneh–Durfee hoặc kiểm tra nhánh d_p nhỏ (nhìn bit-length của e để chọn).
- Sau khi factor bằng bất kỳ cách nào: luôn `assert p*q == n` trước khi tính d.

## 11. Bảng tra: tín hiệu trong source → dạng tấn công

| Thấy gì trong đề | Dạng | Mục |
|---|---|---|
| n < 300 bit | factor trực tiếp / factordb | 2 |
| `next_prime(p)`, q gần p | Fermat | 2.2 |
| `p = M+1` với M tích prime nhỏ | Pollard p−1 | 2.3 |
| nhiều key, entropy kém | batch GCD | 3 |
| prime từ danh sách đặc biệt | Mersenne / ROCA / 4p−1 | 2.4, 3 |
| e = 1 | identity | 4 |
| e = 3, không pad, m ngắn | iroot | 4 |
| cùng m nhiều modulus | Håstad | 4 |
| m + padding null biết trước | shift + brute wrap | 4 |
| bit(e) ≈ bit(n) | Wiener → Boneh–Durfee | 5 |
| bit(e) ≈ bit(n)/2 | d_p nhỏ | 5.3 |
| cùng N khác e | common modulus ngoài | 6 |
| cho sẵn d | common modulus trong / factor từ d | 6 |
| m2 = a·m1 + b | Franklin–Reiter | 7 |
| cùng m ± random pad ngắn | short-pad | 7 |
| p_high / d_low leak | Coppersmith / BDF | 7, 8 |
| server ký tùy ý | sign = decrypt / blinding | 8 |
| verify cho chọn N, e | e=1 / smooth+dlog / mod 2^k | 8 |
| chữ ký lỗi trong log | CRT fault | 8 |
| Oracle chẵn/lẻ | parity | 8 |
| conform 00 02 oracle | Bleichenbacher | 8 |

## 12. Nguồn tham khảo công khai

- Danh mục bài: <https://cryptohack.org/challenges/rsa>
- Boneh, *Twenty Years of Attacks on the RSA Cryptosystem* (bản dịch trong repo: `rsa/RSA-survey-vi.md`).
- Bộ solve cộng đồng: <https://github.com/onealmond/hacking-lab> (mục cryptohack), <https://github.com/jeonyujin4209/crypto_ctf>; ghi chú HackMD nhóm KCSC (RSA 1/2), CayCon.
- Thư viện attack: <https://github.com/jvdsn/crypto-attacks> (wiener, boneh_durfee, bleichenbacher, franklin-reiter, complex_multiplication…).
- Batch GCD & shared primes: Lenstra et al., "Ron was wrong, Whit is right", eprint 2012/064.
- ROCA: Nemec et al., "The Return of Coppersmith's Attack" (eprint 2017/675).
- 4p−1: Sedlacek et al., "I Want to Break Square-free" (SECRYPT 2019).
