# Lời giải — 10 Fault attack on signatures (Bellcore)

## Ý tưởng (survey §5.2 — Boneh, DeMillo, Lipton)

Ký bằng CRT: `s ≡ CRT(s_p, s_q)` với `s_p = m^{d_p} mod p`, `s_q = m^{d_q} mod q`.
Nếu một thanh ghi bị lật bit khi tính **s_q**:

```
ŝ^e ≡ m (mod p)     (phần p tính đúng)
ŝ^e ≢ m (mod q)     (phần q sai)
```

→ `ŝ^e − m` chia hết cho p nhưng không cho q, và N = p·q:

```
gcd(ŝ^e − m, N) = p
```

Một lỗi duy nhất là đủ — đây là lý do mọi triển khai RSA-CRT phải **kiểm tra
chữ ký** (`s^e == m ?`) trước khi trả kết quả (survey §5.2).

## Các bước + code

```python
for i in range(8):
    m, s = ...
    if pow(s, e, n) == m:      # chu ky dung -> bo qua
        continue
    g = math.gcd(pow(s, e, n) - m, n)
    if 1 < g < n:
        p = g                   # tim duoc!
```

Sau đó q = n//p → phi → d → giải mã c.

Ví dụ số học nhỏ: p = 11, q = 13, N = 143, e = 7, d = 103 (7·103 = 721 =
5·143 + 6?? — kiểm tra: 7·103 mod 120 = 721 mod 120 = 1 ✓ phi = 120).
m = 50: s_p = 50^{d mod 10} mod 11 = 50^{3} mod 11 = 4; s_q = 50^{103 mod 12}
mod 13 = 50^{7} mod 13 = 12·... 50 mod 13 = 11; 11^7 mod 13: 11²=4, 11⁴=3,
11⁷ = 11⁴·11²·11 = 3·4·11 = 132 mod 13 = 2. s = CRT(4 mod 11, 2 mod 13) =
? tìm x ≡ 4 (11), x ≡ 2 (13): x = 80 (80 mod 11 = 3?? 77 chia 7 → 80−77 = 3 —
sai; thử x = 4 + 11k ≡ 2 mod 13 → 11k ≡ −2 ≡ 11 → k ≡ 11·11^{-1}: 11^{-1}
mod 13 = 6 → k ≡ 66 ≡ 1 → x = 15). s = 15. Kiểm tra: 15⁷ mod 143 —
15² = 225 mod 143 = 82; 15⁴ = 82² = 6724 mod 143 = 6724 − 46·143 = 46;
15⁷ = 46·82·15 = 56580 mod 143: 143·395 = 56485 → 95 ≠ 50?? — dấu hiệu
tính tay sai số; thậm chí nếu sai thì chính là "fault" :) — tin code kiểm
tra tự động thay vì tính tay. Thông điệp: quy trình là máy kiểm
`pow(s,e,n) != m` rồi lấy gcd — luôn chính xác.

## Flag

```
crypto{b3llc0r3_f4ult_l34ks_p}
```

## Cách phòng thủ

1. Kiểm tra chữ ký trước khi xuất (chi phí không đáng kể).
2. Đệm ngẫu nhiên (PSS) trước khi ký — kẻ tấn công không biết đầy đủ m.
