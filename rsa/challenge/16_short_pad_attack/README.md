# 16 — Coppersmith short-pad attack (đệm ngắn, gửi lại)

**Dạng:** Cùng thông điệp, hai phần đệm ngẫu nhiên khác nhau → resultant + Coppersmith + Franklin-Reiter
**Độ khó:** ★★★★★
**Nguồn:** `RSA-survey-vi.md` §4.4 (Định lý 8)

## Câu chuyện

Alice gửi cho Bob bản mã của `M₁ = (flag << 32) | r₁` (32 bit đệm ngẫu nhiên
ở cuối). Không thấy phản hồi, Bob gửi lại `M₂ = (flag << 32) | r₂` với **một
phần đệm ngẫu nhiên khác**. Bạn chặn được CẢ HAI bản mã (e = 3) nhưng KHÔNG
biết r₁, r₂ hay flag.

## Files phát cho người chơi

- `output.txt` — chứa `n`, `e = 3`, `c1`, `c2`, và ghi chú định dạng
  `M = (msg << 32) | r`

## Mục tiêu

Khôi phục flag (dạng `crypto{...}`).

## Gợi ý (survey Định lý 8)

1. `Δ = r₂ − r₁` (|Δ| < 2³²) là nghiệm nhỏ của **resultant**
   `h(y) = res_x(x³ − c₁, (x+y)³ − c₂)` — đa thức monic bậc 9 mod n.
   (Tính bằng `sympy.resultant` trên đa thức hệ số nguyên.)
2. Tìm nghiệm nhỏ của h bằng Coppersmith (Howgrave-Graham + LLL, thư viện
   `_lib/rsalib.py` đã có: `coppersmith_small_roots(h, n, 2**32, m=4, t=0)`).
3. Có Δ → Franklin-Reiter (challenge 13):
   `gcd((x−Δ)³ − c₁, x³ − c₂) = x − M₂` → M₂ → flag = M₂ >> 32.

## Chạy lời giải (để kiểm tra)

```
python solve.py
```
