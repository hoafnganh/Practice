# 15 — Coppersmith: phân tích N khi biết phần cao của p (Định lý 10)

**Dạng:** Biết ~n/4 bit (ở đây 140 bit đầu của p 256-bit) → LLL/Howgrave-Graham tìm phần còn lại
**Độ khó:** ★★★★☆
**Nguồn:** `RSA-survey-vi.md` §4.1 (Định lý 3 — Coppersmith) + §4.5 (Định lý 10)

## Câu chuyện

Một thiết bị HSM rò rỉ_SIDE-channel: bạn đo được **140 bit cao nhất** của thừa
số p (trong 256 bit). Khóa dùng N 512-bit, e = 65537.

## Files phát cho người chơi

- `output.txt` — chứa `n`, `e`, `p_high` (140 bit cao của p), `c`

## Mục tiêu

Khôi phục p, q rồi giải mã. Flag dạng `crypto{...}`.

## Gợi ý

1. `p = p_high·2^116 + x` với `x < 2^116 ≈ N^{0.227} < N^{1/4}`.
2. Đa thức `f(x) = p_high·2^116 + x` có nghiệm `x₀` **mod p** (thừa số của N).
3. Howgrave-Graham: dựng lattice gồm `N^{m−i}·f^i` và các shift `x^a·f^m`;
   LLL (flint) cho đa thức h có nghiệm nguyên = x₀.
4. Thư viện: `_lib/rsalib.py` đã có `coppersmith_known_high_bits(N, p_high, u, m, t)`.

## Chạy lời giải (để kiểm tra)

```
python solve.py
```
