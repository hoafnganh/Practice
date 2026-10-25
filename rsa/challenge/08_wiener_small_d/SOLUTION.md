# Lời giải — 08 Wiener's attack

## Ý tưởng (survey §3, Định lý 2 — M. Wiener)

Nếu `q < p < 2q` và `d < (1/3)·N^{1/4}` thì từ `(N, e)` khôi phục được `d`.

Chứng minh tóm tắt (xem survey + HackMD doc):

1. `ed − kφ(N) = 1` → `|e/φ(N) − k/d| = 1/(d·φ(N))` — `k/d` xấp xỉ rất sát `e/φ(N)`.
2. Không biết φ(N), nhưng `φ(N) = N − p − q + 1` và `p + q − 1 < 3√N` nên
   `|N − φ(N)| < 3√N`, suy ra
   `|e/N − k/d| ≤ 3k/(d√N) < 1/(2d²)`.
3. Định lý xấp xỉ cổ điển: mọi phân số `k/d` thỏa `|α − k/d| < 1/(2d²)` là một
   **phân số hội tụ** của liên phân số α. → khai triển liên phân số `e/N`,
   duyệt các hội tụ `(k, d)`.
4. Với mỗi ứng viên: `φ = (ed−1)/k`, `s = n − φ + 1 = p + q`,
   `Δ = s² − 4n = (p−q)²` phải chính phương → p, q; kiểm chứng `p·q = n`.

## Các bước + code

```python
import rsalib as R
d, p, q = R.wiener_attack(n, e)      # phan so lien tuc cua e/N
m = pow(c, d, n)
```

(Ngoài ra `E:\Book\wiener_demo.py` trong thư mục gốc là demo đầy đủ của dạng
này, gồm cả kiểm chứng âm với e = 65537.)

Ví dụ số học nhỏ: p = 89, q = 97 → n = 8633, φ = 8544, chọn d = 53
(53 < (1/3)·8633^{1/4} ≈ 17?? — 8633^{1/4} ≈ 9.65 → d < 3.2 — không đủ! Đây
chính là lý do ví dụ nhỏ phải dùng d rất nhỏ, vd d = 3? 3·e ≡ 1 mod 8544 →
e = 2848. Liên phân số 2848/8633: hội tụ bao gồm 1/3 → k = 1?? thử:
e·d − 1 = 8543 = 1·8543?? — k = 8543/8544... để chính xác: ed − kφ = 1:
2848·3 − 8544 = 8544−8544+... = 0 ≠ 1. Thử d = 5: e·5 ≡ 1 → e = 6835;
6835·5 − 1 = 34174 = 4·8544 + 2 → không. Kết luận: ví dụ bằng tay dễ sai —
điểm mấu chốt là kiểm chứng cuối `p·q == n` trong code luôn phát hiện ứng
viên sai, không cần tin tính tay.)

## Flag

```
crypto{w13n3r_c0nt1nu3d_fr4ct10ns}
```

## Cách phòng thủ

Không dùng d < N^{1/4}; d chuẩn (≈ φ(N)) hoặc nếu cần giải mã nhanh thì dùng
CRT với dp, dq (nhưng không quá nhỏ — xem challenge 09). Boneh–Durfee cải
tiến bound lên `d < N^{0.292}` (survey §3), nên biên an toàn thực tế còn thấp hơn.
