# 13 — Franklin–Reiter: thông điệp liên quan (e = 3)

**Dạng:** Hai bản mã của hai thông điệp liên hệ tuyến tính → GCD đa thức tìm m
**Độ khó:** ★★★☆☆
**Nguồn:** `RSA-survey-vi.md` §4.3 (Bổ đề 7)

## Câu chuyện

Hệ thống báo động gửi trạng thái kèm **số sê-ri 4 byte big-endian** ở cuối
thông điệp. Hai báo động liên tiếp được mã hóa cùng khóa e = 3:

- `M1 = bytes_to_long(flag_bytes + (1).to_bytes(4,'big'))`
- `M2 = bytes_to_long(flag_bytes + (2).to_bytes(4,'big'))` → `M2 = M1 + 1`

Bạn chặn được cả hai bản mã. Không cần khóa riêng, khôi phục cả hai.

## Files phát cho người chơi

- `output.txt` — chứa `n`, `e = 3`, `c1`, `c2`

## Mục tiêu

Khôi phục flag (dạng `crypto{...}`).

## Gợi ý

1. `M2` là nghiệm chung của `g1(x) = (x−1)³ − C1` và `g2(x) = x³ − C2`
   trong ℤ_N[x].
2. `x − M2` chia hết cả hai → `gcd(g1, g2)` là đa thức **tuyến tính**.
3. Thuật toán Euclid trên ℤ_N[x] (monic hóa bằng nghịch đảo hệ số đầu).

## Chạy lời giải (để kiểm tra)

```
python solve.py
```
