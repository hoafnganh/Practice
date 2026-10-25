# 09 — Brute force trên CRT exponent nhỏ (d_p)

**Dạng:** `d_p = d mod (p−1)` nhỏ → vét cạn `d_p`, phân tích N qua `gcd`
**Độ khó:** ★★★☆☆
**Nguồn:** `TASK 1 RSA ATTACK - HackMD.pdf` — mục *"Brute force attack on small secret CRT-Exponents"*

## Câu chuyện

Để tăng tốc giải mã CRT, một thư viện cũ chọn `d_p = d mod (p−1)` **trước**
rồi tính ngược `e = d_p^{-1} mod (p−1)` — vô tình khiến `d_p` chỉ ~20 bit.
Bạn có khóa công khai `(n, e)` (e rất dài!) và bản mã.

## Files phát cho người chơi

- `output.txt` — chứa `n`, `e`, `c`

## Mục tiêu

Khôi phục flag (dạng `crypto{...}`).

## Gợi ý

1. `e·d_p = 1 + k·(p−1)` → với mọi `r`: `r^{e·d_p} ≡ r (mod p)`
   (định lý Fermat nhỏ).
2. Suy ra `p | r − r^{e·d_p} (mod n)` → `gcd(r − r^{e·d_p} mod n, n)` trả về p.
3. Vét cạn `d_p` từ 1 đến 2^20. Mẹo tính nhanh:
   `r^{e·d_p} = (r^e mod n)^{d_p} mod n` — lũy thừa chỉ với số mũ 20 bit!

## Chạy lời giải (để kiểm tra)

```
python solve.py
```
