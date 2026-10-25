# Lời giải — 18 Timing attack (Kocher, survey §5.1)

## Ý tưởng (survey §5.1)

Thẻ ký bằng bình phương lặp LSB-first; phép nhân `C·z` **chỉ xảy ra khi bit
d_j = 1** còn bình phương luôn xảy ra. Thời gian mỗi phép nhân phụ thuộc giá
trị (ở đây: `40 + 30·popcount(kết quả)` μs — giả định reduction thực mất thời
gian theo giá trị). Kocher: đo T_i cho hàng loạt thông điệp M_i, rồi quyết định
từng bit của d bằng tương quan.

## Thuật toán trong solve.py

1. Ngoại tuyến theo dõi `C_i = M_i^{d mod 2^j}` và `z_i = M_i^{2^j}` (biết các
   bit < j) — tính được chi phí mọi phép toán đã chắc chắn, dồn vào `acc_i`.
2. Tại bit j: `residual_i = T_i − acc_i`. Nếu d_j = 1 thì residual chứa thêm
   `cost(C_i·z_i)` — **tương quan dương**; nếu d_j = 0 thì độc lập.
3. Hệ số tương quan Pearson trên 8192 cặp; bit 0 biết chắc = 1 (d lẻ);
   ngưỡng 0.034 phân biệt bit 1 (corr đo được ≥ 0.037) với bit 0 (≤ 0.030,
   trung bình ~0).
4. Cập nhật acc (chi phí bình phương luôn, cộng nhân nếu bit = 1), chuyển bit.
5. Sau ~264 bit: kiểm chứng `(M^e)^d ≡ M` rồi giải mã c.

Kocher thật dùng chính kỹ thuật này (CRYPTO '96); survey còn nhấn mạnh: với
e nhỏ, chỉ cần khôi phục ¼ bit của d rồi chuyển sang partial key exposure
(challenge 17). Phòng thủ: làm mù (Rivest — nhân trước với r^e, chia r sau)
hoặc thời gian không đổi — đúng như survey §5.1 trình bày.

## Flag

```
crypto{t1m1ng_s1d3_ch4nn3l}
```
