# 04 — Håstad's broadcast attack (cùng thông điệp, nhiều người nhận)

**Dạng:** Broadcast cùng `m` với `e` số mũ giống nhau, đủ `e` bản mã
**Độ khó:** ★★☆☆☆
**Nguồn:** `TASK 1 RSA ATTACK - HackMD.pdf` — mục *"Hastad's Broadcast Attack"*; `RSA-survey-vi.md` §4.2

## Câu chuyện

Bob muốn gửi **cùng một** lệnh khởi động tới 3 trạm điều khiển. Ba trạm dùng
ba khóa RSA khác nhau nhưng đều chọn e = 3 (cho nhanh). Bob không đệm thông
điệp. Bạn nghe lén được cả 3 bản mã.

## Files phát cho người chơi

- `output.txt` — chứa `n1, n2, n3`, `e = 3`, và `c1, c2, c3`

## Mục tiêu

Khôi phục thông điệp `m` (chứa flag, dạng `crypto{...}`).

## Gợi ý

1. `c_i = m³ mod n_i` — với cùng một `m` nhưng ba mô-đun khác nhau.
2. CRT ghép ba congruence thành `C ≡ m³ (mod n1·n2·n3)`.
3. Vì `m < min(n_i)`, ta có `m³ < n1·n2·n3` → `C = m³` **trên số nguyên**.
4. Căn bậc ba nguyên của C chính là m.

## Chạy lời giải (để kiểm tra)

```
python solve.py
```
