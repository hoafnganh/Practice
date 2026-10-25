# bai-01-otp-nhua-key

**Thể loại:** crypto / stream

## Đề bài

Cho trước vài cặp (ciphertext, plaintext) mẫu và một ciphertext cuối cần giải để lấy flag (xem `chall.txt`).

## Lời giải

Mỗi ciphertext có cấu trúc hai nửa bằng nhau:

- **Nửa sau** chính là keystream (key) nguyên vẹn.
- **Nửa trước** là `base64(plaintext) XOR key`.

Cách giải:

```
nửa_đầu XOR nửa_sau  ->  chuỗi base64  ->  plaintext
```

Kiểm chứng lại với các cặp mẫu đã biết (`Hello? Hello? Anybody home?`, `Great Scott!`), rồi áp dụng cho ciphertext chứa flag.

```bash
python3 solve.py
```

## Flag

```
XHM{Wont_U_make_Lemonade}
```
