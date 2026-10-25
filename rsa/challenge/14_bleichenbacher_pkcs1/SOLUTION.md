# Lời giải — 14 Bleichenbacher PKCS#1 v1.5 (survey §5.3)

## Bối cảnh survey

Ứng dụng trả về thông báo lỗi *"bản mã không hợp lệ"* khi 16 bit đầu của bản
rõ ≠ `02` — biến dịch vụ thành **oracle**: với mọi `r`, kẻ tấn công biết được
16 bit cao của `D(r·C mod n)` có bằng `02` hay không. Bleichenbacher (CRYPTO
'98) chứng minh oracle đó đủ để giải mã C.

## Thuật toán triển khai trong solve.py

Phát biểu bằng khoảng: `B = 2^{8(K−2)}`; block hợp lệ ⇔ `2B ≤ m < 3B`.
Gửi `c' = c·s^e mod n` — hợp lệ ⇔ `m·s mod n ∈ [2B, 3B)` ⇔
`m ∈ [(2B+rn)/s, (3B−1+rn)/s]` với `r = ⌊m·s/n⌋` (window).

1. **Bước 2a:** quét `s = ⌈n/3B⌉, +1, …` tới hit đầu tiên (kỳ vọng n/3B ≈ 2^15
   truy vấn). Hit cho window đầu tiên chứa m.
2. **Thu hẹp hình học:** giữ `s ≈ 2B/w` (w = độ rộng khoảng chứa m). Khi đó
   window rộng ~w/2 — **hit nào cũng cắt khoảng xuống ~w/2**, bất kể hit rơi
   ở đâu trong khoảng. Giữa hai hit chỉ quét "state-free" (không cập nhật
   khoảng — tốc độ mỗi truy vấn ≈ tốc độ oracle thuần); khi có hit, intersect
   khoảng với window của hit. Mỗi hit tốn kỳ vọng n/B truy vấn quét.
3. Sau ~log₂(w) hit, khoảng hẹp ≤ 8 → quét từng ứng viên: block có tiền tố
   `0x00 0x02`, tách phần sau `0x00` đầu tiên → flag.

Kết quả chạy thật (khóa 128-bit, e = 3): **~69 vòng halving, ~1.4 triệu truy
vấn, ~5 giây** (oracle cục bộ). Với RSA-1024/2048 thật, cùng thuật toán cần
~2^20 truy vấn qua mạng — đúng cỡ số liệu mà BB'98/ROBOT báo cáo.

Ví dụ trực quan: `m·s mod n ∈ [2B, 3B)` nghĩa là `m·s − r·n ∈ [2B, 3B)` với
`r = ⌊m·s/n⌋` — mỗi truy vấn "hỏi" xem m có nằm trong một dải nghiêng (theo s)
của không gian (m, r); đủ nhiều dải, chỉ còn một điểm m.

## Flag

```
crypto{bb98}
```

## Cách phòng thủ

Kiểm tra đệm phải **đồng nhất** (không phân biệt loại lỗi, constant-time),
và tốt nhất là dùng **RSA-OAEP**. Đây là bài học đẩy ngành sang "mã hóa xác
thực trước khi giải mã" — thông điệp kết luận của survey.
