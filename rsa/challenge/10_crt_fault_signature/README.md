# 10 — Fault attack on RSA-CRT signatures (Bellcore)

**Dạng:** Chữ ký CRT tính sai một bit → `gcd(ŝ^e − m, N)` lộ thừa số
**Độ khó:** ★★☆☆☆
**Nguồn:** `TASK 1 RSA ATTACK - HackMD.pdf` — mục *"Fault attack on signatures"*; `RSA-survey-vi.md` §5.2 (Boneh–DeMillo–Lipton)

## Câu chuyện

Bạn lấy được log của một dịch vụ ký RSA chạy trên server lỗi thời (RAM hay
lỗi bit). Log chứa 8 cặp `(m, chữ ký)` — một số chữ ký **không hợp lệ** vì
phần tính theo CRT bị lỗi. Cuối log là bản mã `c` của thông điệp mật.

## Files phát cho người chơi

- `output.txt` — chứa `n`, `e`, 8 cặp `m_i, s_i`, và `c`

## Mục tiêu

Phân tích N từ chữ ký lỗi rồi giải mã `c`. Flag dạng `crypto{...}`.

## Gợi ý

1. Chữ ký đúng: `s^e ≡ m (mod N)` — không lộ gì.
2. Chữ ký lỗi CRT (chỉ sai theo mod q): `ŝ^e ≡ m (mod p)` nhưng
   `ŝ^e ≠ m (mod q)` → `gcd(ŝ^e − m, N) = p`.
3. Duyệt log, kiểm tra `pow(s, e, n) == m` từng cặp.

## Chạy lời giải (để kiểm tra)

```
python solve.py
```
