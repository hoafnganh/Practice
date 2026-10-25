# 02 — Fermat's attack (p và q quá gần nhau)

**Dạng:** Phân tích thừa số Fermat khi `|p - q|` nhỏ
**Độ khó:** ★★☆☆☆
**Nguồn:** `TASK 1 RSA ATTACK - HackMD.pdf` — mục *"Fermat's attack"*

## Câu chuyện

Cùng cơ quan ở challenge 01 đã "rút kinh nghiệm" và dùng N 1024 bit. Nhưng
để tiết kiệm thời gian, dev sinh `p` rồi lấy `q` là số nguyên tố **ngay cạnh**
`p`. Bạn lại chặn được bản mã của thông điệp mật.

## Files phát cho người chơi

- `output.txt` — chứa `n`, `e`, `c`

## Mục tiêu

Giải mã `c` để lấy flag. Flag có dạng `crypto{...}`.

## Gợi ý

1. Nếu `p - q` nhỏ, `n = p·q` nằm rất gần một số chính phương `a²`.
2. Thuật toán Fermat: thử `a = ceil(√n), ceil(√n)+1, …` cho tới khi
   `a² - n` là số chính phương `b²`. Khi đó `p = a - b`, `q = a + b`.
3. Trong challenge này `a - √n` chỉ cỡ vài chục bước.

## Chạy lời giải (để kiểm tra)

```
python solve.py
```
