# Lời giải — 03 Small public exponent

## Ý tưởng (theo tài liệu)

HackMD doc: *"Nếu bạn có 1 quả n rất mạnh và lớn, thế nhưng chỉ lấy e = 3 thì
cũng coi như là không mã hóa"*. Survey §4 cũng mở đầu bằng cảnh báo e nhỏ.

RSA tính `c = m³ mod n`. Nếu `m³ < n` thì phép rút gọn **không xảy ra**:
`c = m³` đúng nghĩa số nguyên. Khôi phục m chỉ là lấy căn bậc ba nguyên —
không cần biết p, q, d hay bất kỳ thông tin bí mật nào.

## Các bước + code

```python
import gmpy2
m, exact = gmpy2.iroot(c, 3)   # exact == True neu can chinh phuong
print(long_to_bytes(int(m)))
```

Ví dụ số học nhỏ: n = 101·103 = 10403, e = 3, m = 15 →
m³ = 3375 < 10403 → c = 3375. Căn bậc ba của 3375 = 15 = m. ✓
Nhưng nếu m = 100 → m³ = 10⁶ > 10403 → c = 10⁶ mod 10403 = 5659 — căn bậc ba
của 5659 không nguyên, tấn công thất bại (đó là lúc cần Hastad/Coppersmith).

## Flag

```
crypto{sm4ll_e_n0_p4dd1ng_3asy_r00t}
```

## Cách phòng thủ

Luôn đệm ngẫu nhiên (OAEP) trước khi mã hóa để bản rõ thực sự chiếm gần hết
kích thước N; hoặc dùng e = 65537 như khuyến nghị trong survey.
