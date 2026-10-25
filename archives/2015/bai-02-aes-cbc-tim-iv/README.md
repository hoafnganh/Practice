# bai-02-aes-cbc-tim-iv

**Thể loại:** crypto / AES-CBC

## Đề bài

`chall.py` mã hóa một thông điệp 2 block bằng AES-CBC: key bị che mất 2 byte cuối (biết trước 14 byte `5d6I9pfR7C1JQt`), IV 16 byte không biết. Biết plaintext gốc ("The message is protected by AES!") và block ciphertext cuối còn nguyên.

## Lời giải

Dùng quan hệ giải ngược CBC: `C_(i−1) = D_k(C_i) ⊕ P_i` và `IV = D_k(C_0) ⊕ P_0`.

- Brute 2 byte key còn thiếu (65.536 candidate), **đặt IV = 0 khi brute** (IV chỉ tham gia phép XOR nên không ảnh hưởng việc check).
- Check các byte đã biết của block 1 suy ngược — candidate đúng cho key 16 byte `5d6I9pfR7C1JQt7$`.
- Từ đó giải ngược lấy IV — chính là flag.

Xem `solve.py`.

## Flag

```
XHM{rVFvN9KLeYr6}
```
