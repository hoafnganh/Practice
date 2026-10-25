# 08 — Wiener's attack (số mũ bí mật nhỏ)

**Dạng:** `d < (1/3)·N^{1/4}` → phân số liên tục của `e/N` lộ `d`
**Độ khó:** ★★★☆☆
**Nguồn:** `RSA-survey-vi.md` §3 (Định lý 2 — M. Wiener); `TASK 1 RSA ATTACK - HackMD.pdf` — mục *"Wiener's attack"*; `wiener_demo.py` (E:\Book)

## Câu chuyện

Một thiết bị IoT yếu muốn giải mã nhanh nên chọn **d rất nhỏ** (250 bit) và
tính `e = d^{-1} mod phi(N)` — khiến `e` chiếm gần đủ 1024 bit của N. Bạn có
khóa công khai và bản mã.

## Files phát cho người chơi

- `output.txt` — chứa `n`, `e`, `c`

## Mục tiêu

Khôi phục `d` và giải mã. Flag dạng `crypto{...}`.

## Gợi ý

1. `ed = 1 + k·phi(N)` → `k/d` xấp xỉ `e/phi(N)`; thay `phi(N)` bằng `N`
   (sai số `< 3√N`) vẫn đủ để `k/d` là một **phân số hội tụ** của `e/N`.
2. Duyệt các phân số hội tụ `(k, d)`; với mỗi cặp tính
   `phi = (ed−1)/k`, rồi `s = n−phi+1 = p+q`;
   `Δ = s² − 4n` phải là số chính phương → giải được p, q.
3. Dấu hiệu nhận biết: `e` chiếm ~100% số bit của `n`.

## Chạy lời giải (để kiểm tra)

```
python solve.py
```
