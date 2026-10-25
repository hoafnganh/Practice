# Lời giải — 16 Coppersmith short-pad attack (survey §4.4, Định lý 8)

## Bối cảnh survey

*"Bob gửi cho Alice một bản mã của M đã được đệm đúng cách. ... Bob quyết định
gửi lại M. Bây giờ Marvin có hai bản mã tương ứng với hai lần mã hóa cùng một
thông điệp bằng hai phần đệm ngẫu nhiên khác nhau. ... mặc dù không biết các
phần đệm đã dùng, Marvin vẫn có thể khôi phục bản rõ."* (survey §4.4)

## 3 bước khai thác

**Bước 1 — Resultant.** `M₁ = M||r₁`, `M₂ = M||r₂`, `M₂ = M₁ + Δ` với
`Δ = r₂ − r₁` (|Δ| < 2³²). Hai đa thức `g₁(x) = x³ − c₁` và
`g₂(x) = (x+y)³ − c₂` có nghiệm chung x = M₁ khi y = Δ ⇒ Δ là nghiệm của

```
h(y) = res_x(g₁, g₂)  — monic, bậc ≤ e² = 9, hệ số mod n
```
(sympy tính resultant trên ℤ rồi reduce mod n.)

**Bước 2 — Coppersmith.** `|Δ| < 2³² = N^{0.0625} ≪ N^{1/9}` → nghiệm nhỏ của
h mod N tìm bằng Howgrave-Graham lattice + LLL (m = 4, t = 0, dim 36).
Đây chính là Định lý 3 trong survey.

**Bước 3 — Franklin-Reiter.** Biết Δ: `gcd((x−Δ)³ − c₁, x³ − c₂) = x − M₂`
(challenge 13) → M₂ → bỏ 32 bit pad → flag.

Survey chứng minh tổng quát: đệm ngắn tới `⌊n/e²⌋` bit đều bị phá (e = 3:
đệm < 1/9 độ dài thông điệp). Với e = 65537, tấn công không khả thi trên
mô-đun chuẩn — cũng là lý do khuyến nghị e = 65537 (survey §4).

## Flag

```
crypto{sh0rt_p4d_r3sult4nt_c0pp3rsm1th}
```

## Cách phòng thủ

Đệm **ngẫu nhiên và đủ dài** (OAEP) — không bao giờ gửi lại thông điệp với
"một chút đệm khác"; hoặc dùng e lớn.
