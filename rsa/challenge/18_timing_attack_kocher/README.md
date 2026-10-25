# 18 — Timing attack (Kocher): thẻ thông minh ký RSA

**Dạng:** Tấn công thời gian — khôi phục d bit-by-bit qua tương quan thời gian ký
**Độ khó:** ★★★★☆
**Nguồn:** `RSA-survey-vi.md` §5.1 (Kocher)

## Mô hình (survey §5.1)

Thẻ ký bằng **bình phương lặp** (LSB-first):

```
C = 1, z = M
với mỗi bit d_j của d (j = 0..L-1):
    nếu d_j = 1:  C = C·z mod n   (phép nhân — CHỈ xảy ra khi bit = 1)
    z = z² mod n                  (bình phương — luôn xảy ra)
```

Mô phỏng thời gian: mỗi phép nhân/bình phương mô-đun mất
`40 + 30·popcount(kết quả)` μs (phụ thuộc giá trị — như reduction thực tế),
cộng nhiễu ngẫu nhiên nhỏ cho toàn chữ ký.

## Dịch vụ

```
python server.py 1337
```

Server (khóa 256-bit, e = 65537) ký **8192 thông điệp ngẫu nhiên** M_i và gửi
lại thời gian T_i (μs) của từng chữ ký, cùng `n`, `e`, `c` (bản mã flag).

## Mục tiêu

Dùng tương quan thời gian để khôi phục d rồi giải mã c. Flag `crypto{...}`.

## Gợi ý

1. d lẻ → d₀ = 1. Quyết định từng bit từ LSB lên.
2. Giả sử đã biết các bit < j. Với mỗi thông điệp, trạng thái
   `C_i = M_i^{d mod 2^j}`, `z_i = M_i^{2^j}` tính được **ngoại tuyến**.
3. Nếu d_j = 1 thì thời gian còn lại chứa thêm `cost(C_i·z_i)` — tương quan
   dương với `residual_i = T_i − acc_i`. Nếu d_j = 0: không tương quan.
4. 8192 mẫu đủ tách corr ≈ 0.04-0.1 (bit 1) khỏi nhiễu ±0.011 (bit 0)
   — ngưỡng 0.034.
5. Cập nhật `acc_i` (chi phí bình phương luôn + nhân nếu bit = 1) rồi sang bit kế.

## Chạy lời giải (để kiểm tra)

```
python solve.py            # tu dong khoi dong server o port rong
```
