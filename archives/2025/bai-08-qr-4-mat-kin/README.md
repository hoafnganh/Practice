# bai-08-qr-4-mat-kin

**Thể loại:** crypto / misc

## Đề bài

Cho một file `index.html` — phân tích nó để tìm flag.

## Lời giải

HTML vẽ một bảng 4 ô, nền mỗi ô là một PNG nhúng base64 (`.bg1`..`.bg4`). Từng ảnh riêng lẻ trông như một mã QR bị nhiễu.

`extract_decode.py`:

1. Trích 4 ảnh base64 khỏi HTML (`data:image/...;base64,...`) và lưu thành `img1.png`..`img4.png`.
2. Sinh các biến thể để khôi phục QR: denoise/threshold/invert cho từng ảnh, cộng các tổ hợp cả bốn ảnh (median / min / max / XOR / std-dev), rồi thêm vài mức upscale. Một trong các tổ hợp đó "gộp" được nhiễu share thành một QR sạch.
3. Tự giải mã mọi biến thể bằng `QRCodeDetector` của OpenCV. Các biến thể tổ hợp giải mã thành công.

```bash
uv run extract_decode.py
# Found 4 embedded images
# Saved: img1.png, img2.png, img3.png, img4.png
# DECODED from var_14.png: (link da bo)
```

Mã QR trỏ tới một file text được host trên S3 — nơi chứa flag.

## Vượt SSE-C

Gọi thẳng URL S3 sẽ không được — object được lưu bằng **SSE-C** (mã hóa phía server với key AES-256 do phía khách cung cấp) nên một GET bình thường trả về:

```
InvalidRequest: The object was stored using a form of Server Side Encryption.
The correct parameters must be provided to retrieve the object.
```

Hướng vượt dự kiến là tận dụng proxy `fetch.php`.
