# 01 — Factorizing the public key (mô-đun quá nhỏ)

**Dạng:** Phân tích thừa số khóa công khai khi N quá nhỏ
**Độ khó:** ★☆☆☆☆
**Nguồn:** `TASK 1 RSA ATTACK - HackMD.pdf` — mục *"Factorizing the public key"*; `RSA-survey-vi.md` §1.1

## Câu chuyện

Một cơ quan "tiết kiệm chi phí" đã sinh khóa RSA với mô-đun N chỉ 224 bit.
Họ cho rằng "chưa ai rảnh phá nó". Bạn có bản mã của thông điệp mật. Hãy khôi phục.

## Files phát cho người chơi

- `output.txt` — chứa `n`, `e`, `c`

## Mục tiêu

Giải mã `c` để lấy flag. Flag có dạng `crypto{...}`.

## Gợi ý

1. `n` chỉ 224 bit — nhỏ hơn ngưỡng 256 bit được nhắc trong tài liệu.
2. Thử `sympy.factorint(n)` hoặc submit `n` lên factordb.com.
3. Có `p, q` → có `phi(n) = (p-1)(q-1)` → có `d = e^-1 mod phi(n)` → giải mã.

## Chạy lời giải (để kiểm tra)

```
python solve.py
```
