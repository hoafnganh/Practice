# bai-01-vigenere-key-phan-so

**Thể loại:** crypto / cổ điển

## Đề bài

Một ciphertext thuần chữ thường; **tên file** là một chuỗi base64 — giải ra chính là hint: "The key is hidden in one in a prime number".

## Lời giải

- Key là biểu diễn thập phân tuần hoàn (repetend) của một phân số có mẫu số nguyên tố: 1/17 = 0.0588235294117647…
- Đề dùng key là **6 chữ số đầu được cắt ra rồi lặp**: `058823` — chứ KHÔNG phải repetend đầy đủ 16 chữ số (dùng đủ 16 số chỉ giải được đúng 6 chữ "verysi" đầu rồi gãy).
- Giải Vigenère (chỉ áp cho chữ thường) ra: `verysimplecryptochallengewasntit`.

Xem `solve.py`.

## Flag

```
XHM{verysimplecryptochallengewasntit}
```
