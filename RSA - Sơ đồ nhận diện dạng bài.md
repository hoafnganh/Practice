# RSA — Sơ đồ nhận diện dạng bài

> **Cách dùng:** nhận source chall RSA → đọc sơ đồ **từ node đầu xuống dưới**, trả lời lần lượt các câu hỏi (hình diamond). Lá xanh lục = kết luận dạng bài + công thức giải. Bộ 18 dạng chuẩn nằm tại `rsa/challenge/` (lời giải mẫu `rsa/solves/`, thư viện `rsa/challenge/_lib/rsalib.py`, lý thuyết: `rsa/RSA-survey-vi.md`).

## Sơ đồ quyết định (tuần tự từ trên xuống)

```mermaid
flowchart TD
    START(["NHẬN SOURCE CHALL RSA"]):::start --> Q1{"Có service phải tương tác?<br>(nc / server.py / oracle)"}

    Q1 -->|"CÓ"| QOR{"Oracle / service trả về gì?"}
    QOR -->|"Bản rõ đầy đủ m = ...<br>nhưng từ chối nếu kết quả là flag"| R07(["07 · BLINDING<br>gửi c·rᵉ mod n → oracle trả m·r<br>→ nhân r⁻¹ mod n lấy m"]):::res
    QOR -->|"Chỉ 1 bit: Even / Odd"| R11(["11 · PARITY ORACLE<br>gửi ct·(2^k)ᵉ → m·2^k mod n<br>Even/Odd = binary search m"]):::res
    QOR -->|"Đúng/sai đệm PKCS#1 v1.5<br>(2 byte đầu = 00 02 ?)"| R14(["14 · BLEICHENBACHER BB'98<br>quét s: ct·sᵉ conform [2B,3B)<br>→ thu hẹp khoảng chứa m"]):::res
    QOR -->|"Danh sách thông điệp kèm<br>thời gian ký (M_i, T_i)"| R18(["18 · TIMING ATTACK (Kocher)<br>khôi phục d từng bit từ LSB:<br>corr(T_i, cost(C_i·z_i))"]):::res

    Q1 -->|"KHÔNG — chỉ chall.py / output.txt"| Q2{"Dữ liệu cho có gì<br>NGOÀI (n, e, c)?"}
    Q2 -->|"Cho sẵn d của mình<br>+ (e₂, c₂) trên cùng n"| R06(["06 · COMMON MODULUS (trong)<br>từ (n,e,d) suy phi(n)<br>k=(ed−1)//n tăng dần, kiểm Δ chính phương<br>→ d₂ = e₂⁻¹ mod phi"]):::res
    Q2 -->|"p_high — bit CAO của p"| R15(["15 · COPPERSMITH bit cao p<br>p = p_high·2^u + x, x nhỏ hơn N^(1/4)<br>→ LLL tìm x · rsalib.coppersmith_known_high_bits"]):::res
    Q2 -->|"d_low — bit THẤP của d"| R17(["17 · PARTIAL KEY EXPOSURE (BDF)<br>pt bậc 2 mod 2^s → p mod 2^s<br>rồi Coppersmith như 15"]):::res
    Q2 -->|"Nhiều cặp (m_i, s_i) — chữ ký"| R10(["10 · CRT FAULT (Bellcore)<br>duyệt log: gcd(ŝᵉ − m, n) = p<br>với chữ ký lỗi"]):::res
    Q2 -->|"≥ 2 ciphertext"| Q3{"Các bản mã<br>khác nhau chỗ nào?"}
    Q2 -->|"Không — chỉ đúng (n, e, c)"| Q5{"Nhìn vào e<br>và cỡ của n"}

    Q3 -->|"Khác n, cùng e, cùng m<br>(đủ e bản mã)"| R04(["04 · HÅSTAD BROADCAST<br>CRT ghép → C = mᵉ trên nguyên<br>→ gmpy2.iroot(C, e)"]):::res
    Q3 -->|"Cùng n, khác e,<br>gcd(e1,e2) = 1"| R05(["05 · COMMON MODULUS (ngoài)<br>Bézout u·e1 + v·e2 = 1<br>m = c1ᵘ · c2ᵛ mod n"]):::res
    Q3 -->|"Cùng n, cùng e —<br>HIỆU m2−m1 BIẾT TRƯỚC<br>(m2 = m1+1, serial tăng)"| R13(["13 · FRANKLIN–REITER<br>gcd(xᵉ−c1, (x+h)ᵉ−c2) = x−m2<br>trong Z_n[x] · rsalib.poly_gcd_mod"]):::res
    Q3 -->|"Cùng n, cùng e=3 — cùng m,<br>chỉ khác pad ngẫu nhiên ngắn<br>(HIỆU KHÔNG biết trước)"| R16(["16 · SHORT-PAD (Coppersmith)<br>resultant(x³−c1, (x+y)³−c2) → Δ=r2−r1<br>rồi Franklin–Reiter lấy m"]):::res

    Q5 -->|"e nhỏ (3), bản rõ ngắn<br>→ mᵉ chưa wrap mod n"| R03(["03 · e NHỎ, căn nguyên<br>gmpy2.iroot(c, e) = m"]):::res
    Q5 -->|"e KHỔNG LỒ:<br>bit(e) ≈ bit(n)"| R08(["08 · WIENER (d nhỏ)<br>phân số liên tục e/n → hội tụ (k,d)<br>phi=(ed−1)/k, Δ=s²−4n chính phương<br>· rsalib.wiener_attack"]):::res
    Q5 -->|"e DÀI BẤT THƯỜNG:<br>bit(e) ≈ bit(n)/2"| R09(["09 · d_p NHỎ (~20 bit)<br>brute dp: gcd(r − (rᵉ)^dp mod n, n) = p<br>(source: e = dp⁻¹ mod p−1)"]):::res
    Q5 -->|"n nhỏ hơn 300 bit"| R01(["01 · N QUÁ NHỎ<br>sympy.factorint / factordb<br>→ p,q → d → giải mã"]):::res
    Q5 -->|"n bình thường 512–1024 bit<br>không dấu hiệu gì"| F1["① factordb.com / sympy.factorint(n)"]:::ladder

    F1 -->|"n có sẵn trong DB"| R01b(["giải mã chuẩn<br>d = e⁻¹ mod (p−1)(q−1)"]):::res
    F1 -->|"không có"| F2["② FERMAT (source: p,q sinh gần nhau —<br>next_prime(p) / cùng base)<br>a = ⌈√n⌉, tăng dần tới a²−n = b²"]:::ladder
    F2 -->|"vài chục bước ra"| R02(["02 · FERMAT p ≈ q<br>p = a−b, q = a+b"]):::res
    F2 -->|"không ra"| F3["③ POLLARD p−1 (source: p−1 smooth —<br>p = M+1 với M tích prime nhỏ)<br>a ← a^j mod n (j = 2..B), gcd(a−1, n)"]:::ladder
    F3 -->|"ra p"| R12(["12 · POLLARD p−1<br>B = 65536 thường đủ<br>· rsalib.pollard_p1"]):::res
    F3 -->|"không ra"| F4["④ ECM / RsaCtfTool / sage<br>— vẫn chết? quay lại nhánh trên,<br>đề ắt còn tín hiệu chưa thấy —"]:::ladder

    classDef res fill:#1a7f37,stroke:#0f5132,color:#fff
    classDef start fill:#0d6efd,stroke:#084298,color:#fff
    classDef ladder fill:#fff3cd,stroke:#997404,color:#212529
```

## Tra ngược: tín hiệu trong source/output → dạng

Nhận source thì grep/dò các mẫu này trước — ra ngay dạng bài:

| Thấy gì trong chall | Dạng | Bài |
|---|---|---|
| `getPrime(48)`, n < 300 bit | N quá nhỏ → factor trực tiếp | 01 |
| `next_prime(p)`, `gen_prime_near`, q sinh từ cùng base | Fermat p ≈ q | 02 |
| `e = 3`, không pad, flag ngắn, `assert m**3 < n` | Căn bậc e nguyên | 03 |
| Nhiều dòng `n1..ne` + `c1..ce`, cùng e | Håstad broadcast | 04 |
| Cùng n, hai `e_b`, `e_c` coprime | Common modulus ngoài | 05 |
| **Cho sẵn `d`** (+ e₂, c₂ cùng n) | Common modulus trong → suy phi | 06 |
| Server hỏi `Text to decrypt:` | Blinding oracle | 07 |
| `e.bit_length()` ≈ `n.bit_length()` (e ~ 1024 bit) | Wiener d nhỏ | 08 |
| `e = pow(dp, -1, p-1)` — e ~ 512 bit khi n 1024 bit | Brute d_p nhỏ | 09 |
| Log nhiều cặp `m_i`, `s_i` chữ ký | CRT fault — gcd(ŝᵉ−m, n) | 10 |
| Server trả `Even` / `Odd` | Parity oracle | 11 |
| `p = m + 1` với m = tích các prime nhỏ | Pollard p−1 | 12 |
| 2 ct, `M2 == M1 + 1` (serial/counter tăng) | Franklin–Reiter | 13 |
| `block[0:2] == b"\x00\x02"`, PKCS#1 conform oracle | Bleichenbacher | 14 |
| `p_high = p >> U` cho kèm trong output | Coppersmith bit cao | 15 |
| `M = (msg << 32) \| r` gửi 2 lần với r khác nhau | Short-pad attack | 16 |
| `d_low = d % 2^s` cho kèm | Partial key exposure BDF | 17 |
| Hàng nghìn dòng `M_i T_i` (thời gian µs) | Timing attack Kocher | 18 |

## 18 dạng — điều kiện toán & lệnh giải

| # | Dạng | Điều kiện | Giải (1 dòng) | Tool |
|---|---|---|---|---|
| 01 | N quá nhỏ | n < ~300 bit | `sympy.factorint(n)` → d | factordb / factorint |
| 02 | Fermat | \|p−q\| nhỏ, n gần a² | a=⌈√n⌉ dần lên, b²=a²−n | ~20 dòng python |
| 03 | e nhỏ | mᵉ < n (chưa wrap) | `gmpy2.iroot(c, e)` | gmpy2 |
| 04 | Håstad | cùng m, e bản mã, khác n_i | CRT → iroot(C, e) | CRT tay / gmpy2 |
| 05 | CM ngoài | cùng n, gcd(e1,e2)=1 | Bézout: m = c1ᵘ·c2ᵛ | xgcd (lưu ý u âm → inverse) |
| 06 | CM trong | biết (n,e,d) | k=(ed−1)//n++ → phi (Δ chính phương) | python thuần |
| 07 | Blinding | oracle giải mã trừ flag | c·rᵉ → m·r → ·r⁻¹ | 1 query |
| 08 | Wiener | d < ⅓·N^¼ (e cực lớn) | liên tục e/n → (k,d) → phi | `rsalib.wiener_attack` |
| 09 | d_p nhỏ | d_p ~ 2²⁰ (e ~ n/2 bit) | brute dp, gcd(r−r^{e·dp}, n) | pow nhanh (rᵉ)^dp |
| 10 | CRT fault | 1 chữ ký sai mod q | gcd(ŝᵉ − m, n) = p | duyệt log |
| 11 | Parity | oracle chẵn/lẻ | ct·(2^k)ᵉ, halve khoảng | ~log₂n query |
| 12 | Pollard p−1 | p−1 B-smooth | a←a^j, gcd(a−1,n) | `rsalib.pollard_p1` |
| 13 | Franklin–Reiter | m2 = m1 + h (h biết) | gcd đa thức mod n | `rsalib.poly_gcd_mod` |
| 14 | Bleichenbacher | oracle conform 00 02 | BB'98: quét s, intersect khoảng | ~1.4M query offline |
| 15 | Coppersmith cao | biết ≥ n/4 bit cao của p | p_high·2^u + x → LLL | `coppersmith_known_high_bits` |
| 16 | Short-pad | cùng m ± pad ngắn, e=3 | resultant → Δ → FR | `coppersmith_small_roots` + FR |
| 17 | BDF bit thấp d | biết ≥ ⌈n/4⌉ bit thấp d | quad mod 2^s → p_low → 15 | `solve_quad_mod_2k` + Cop |
| 18 | Timing | T_i phụ thuộc phép nhân | corr(T, cost(C·z)) từng bit d | numpy corr, 8192 mẫu |

## Khi (n, e, c) "sạch sẽ" — thang phân tích N

Theo thang bậc trong `tools.md` (factordb trước, Fermat ngay sau):

1. **factordb** (qua `factordb-python`) — n nằm sẵn trong DB thì xong ngay.
2. **Fermat** — p, q gần nhau (việc này rẻ, cứ chạy 1–2 phút trước khi nghĩ tiếp).
3. **Pollard p−1** — p−1 smooth; kèm **p+1 (Williams)** nếu đề sinh prime đặc biệt.
4. **ECM** (PARI `factorint` flag 2 / sage `ecm`) — thừa số nhỏ hơn ~60 digit.
5. **RsaCtfTool** (Win-WSL) — quay đại các attack phổ thông.
6. Vẫn chết → **quay lại đọc source lần 2**: đề 18/18 dạng nào cũng có tín hiệu ở nhánh trên của sơ đồ.

## Phân biệt các cặp dễ nhầm

- **03 vs 04**: cùng e=3 — chỉ 1 bản mã thì m³ phải *nhỏ hơn* n mới iroot được; có đủ e bản mã *khác n* thì CRT trước rồi iroot.
- **08 vs 09**: e đều "dài bất thường" — **bit(e) ≈ bit(n)** → d nhỏ (Wiener); **bit(e) ≈ bit(n)/2** → d_p nhỏ (e sinh theo p−1). Wiener fail nhưng e vẫn ~ n bit → d tới N^0.292: **Boneh–Durfee** (solve mẫu trong `lattice/L11_boneh_durfee/`).
- **05 vs 06**: cùng modulus — không có d → Bézout hai bản mã; **có d của mình** →factor N / suy phi, mạnh hơn nhiều.
- **13 vs 16**: 2 bản mã cùng n cùng e — biết *chính xác* quan hệ m2−m1 → Franklin–Reiter; cùng m nhưng *chỉ khác pad ngẫu nhiên* (không biết hiệu) → short-pad (resultant trước, FR sau).
- **15 vs 17**: đều kết thúc bằng Coppersmith — leak ở **p** (bit cao, shift trái `2^u`) vs leak ở **d** (bit thấp, giải pt bậc 2 mod `2^s` chuyển leak sang p trước).
- **06 và mọi nhánh "có thêm dữ liệu"**: luôn ưu tiên nhánh có dữ liệu lạ (d, p_high, d_low, chữ ký, nhiều ct) TRƯỚC khi đánh giá (n,e,c) — đó là lý do Q2 đứng trên Q5 trong sơ đồ.
