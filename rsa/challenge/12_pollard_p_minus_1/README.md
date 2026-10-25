# 12 — Pollard's p−1 (p−1 là B-smooth)

**Dạng:** `p−1` chỉ có thừa số nguyên tố nhỏ → nhân `a ← a^j mod N` cho j = 2..B
**Độ khó:** ★★☆☆☆
**Nguồn:** `RSA-survey-vi.md` §1.1 ("nếu p−1 là tích của các thừa số nguyên tố nhỏ hơn B, thì N có thể bị phân tích trong thời gian nhỏ hơn B³")

## Câu chuyện

Một dev "tự sinh số nguyên tố" bằng cách lấy `p = M + 1` với `M` là tích các
lũy thừa số nguyên tố nhỏ (để "dễ kiểm tra"). Không ai nhận ra điều đó khiến
`p − 1` cực kỳ smooth. Bạn có khóa công khai và bản mã.

## Files phát cho người chơi

- `output.txt` — chứa `n`, `e`, `c`

## Mục tiêu

Phân tích N rồi giải mã. Flag dạng `crypto{...}`.

## Gợi ý

1. Nếu mọi thừa số của `p−1` đều ≤ B thì `(p−1) | B!` → theo Fermat nhỏ:
   `2^{B!} ≡ 1 (mod p)`.
2. Tính dần `a ← 2^j mod N` cho j = 2..B (mỗi bước `a = pow(a, j, N)`),
   định kỳ lấy `gcd(a − 1, N)` — khi hết "makan" các lũy thừa sẽ ra p.
3. B = 65536 là quá đủ cho challenge này.

## Chạy lời giải (để kiểm tra)

```
python solve.py
```
