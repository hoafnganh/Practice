# 05 — Common Modulus (kẻ tấn công bên ngoài)

**Dạng:** Cùng mô-đun N, hai số mũ khác nhau, cùng thông điệp
**Độ khó:** ★★☆☆☆
**Nguồn:** `TASK 1 RSA ATTACK - HackMD.pdf` — mục *"Common Modulus — As an External Attacker"*

## Câu chuyện

Alice gửi **cùng một** thông điệp cho Bob và Cock. Do lỗi cấu hình, cả hai
dùng **cùng mô-đun N** (nhưng khác số mũ: e_b = 17, e_c = 23). Bạn chặn được
cả hai bản mã C_b, C_c cùng khóa công khai.

## Files phát cho người chơi

- `output.txt` — chứa `n`, `e_b`, `e_c`, `c_b`, `c_c`

## Mục tiêu

Khôi phục thông điệp của Alice (chứa flag, dạng `crypto{...}`) **mà không cần
phân tích N**.

## Gợi ý

1. `gcd(e_b, e_c) = 1` → Euclid mở rộng tìm `u, v`: `u·e_b + v·e_c = 1`.
2. `C_b^u · C_c^v = m^(u·e_b + v·e_c) = m^1 (mod n)`.
3. Nếu `u < 0`, thay `C_b^u` bằng `inverse(C_b, n)^{|u|}`.

## Chạy lời giải (để kiểm tra)

```
python solve.py
```
