# bai-15-stego-zip-jpg — writeup nhanh

**Thể loại:** stego

## Lời giải

- Tìm hint qua strings/EXIF: các token P1, P2, P3 → ghép chữ hoa, phân cách bằng gạch nối.
- Carve ZIP nối đuôi JPEG bằng cách dò `PK\x03\x04` và lưu toàn bộ phần đuôi.
- ZIP dùng AES-256; giải nén bằng 7-Zip với password `WATPHO-RECLINING-BUDDHA`.
- Đọc `flag.txt`.

## Flag

```text
XHM{Y0u-Are-Found-Hidd3n-Fi1e}
```
