# bai-01-rsa-mat-1-bit

**Thể loại:** crypto / RSA

## Đề bài

Cho một public key PEM 256-bit (`PublicKey.pem`) và một ciphertext. Hint của đề: modulus "mất 1 bit" — nghĩa là n trong file PEM đã bị lật đúng 1 bit so với n thật dùng để mã hóa.

## Lời giải

- Thử factor n của PEM: kết quả ra nhiều hơn 2 thừa số (không phải semiprime) → xác nhận n đã bị sửa.
- **Mẹo parity:** modulus RSA thật luôn LẺ → nếu n trong đề là chẵn thì thử ngay `n | 1` (set bit cuối) trước khi brute 256 vị trí bit.
- Candidate đúng là cái factor ra đúng 2 prime ~128 bit. Sau đó giải RSA textbook: `d = e⁻¹ mod (p−1)(q−1)` rồi `long_to_bytes(pow(c, d, n))`.

`solve.sage` chốt luôn vị trí bit 255 (bit cuối).

## Flag

```
XHM{$@!zbo4+qt9=5}
```
