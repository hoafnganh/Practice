# 03 — Small public exponent (e = 3, không đệm)

**Dạng:** Số mũ công khai nhỏ + bản rõ nhỏ → `m³ < N`
**Độ khó:** ★☆☆☆☆
**Nguồn:** `TASK 1 RSA ATTACK - HackMD.pdf` — mục *"Small public exponent"*; `RSA-survey-vi.md` §4 (mở đầu)

## Câu chuyện

"Ai cũng bảo e=3 làm mã hóa nhanh gấp 20000 lần". Hệ thống mã hóa thông điệp
mật bằng RSA với e = 3 và **không có bất kỳ phép đệm nào**. Bạn chặn được bản mã.

## Files phát cho người chơi

- `output.txt` — chứa `n`, `e`, `c`

## Mục tiêu

Giải mã `c` để lấy flag. Flag có dạng `crypto{...}`.

## Gợi ý

1. Với e = 3, nếu `m³ < n` thì `c = m³ mod n = m³` — phép mod chưa từng diễn ra.
2. Chỉ cần lấy **căn bậc ba nguyên** của c: `gmpy2.iroot(c, 3)`.

## Chạy lời giải (để kiểm tra)

```
python solve.py
```
