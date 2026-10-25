# 11 — Parity Oracle (LSB oracle)

**Dạng:** Oracle chỉ trả về chẵn/lẻ của bản rõ → tìm nhị phân m trong log₂(n) truy vấn
**Độ khó:** ★★★☆☆
**Nguồn:** `TASK 1 RSA ATTACK - HackMD.pdf` — mục *"Parity Oracle"*

## Dịch vụ

```
python server.py 1337
```

Dịch vụ cho `n, e, ct` (bản mã của flag). Bạn gửi ciphertext tùy ý — dịch vụ
chỉ trả về **Even** (bản rõ chẵn) hoặc **Odd** (lẻ). Nếu bạn gửi đúng `ct`,
dịch vụ tự đóng kết nối (không đấy, không phải vậy đâu).

```
n = ...
e = 65537
ct = ...
> ...
Even
> ...
```

## Mục tiêu

Khôi phục flag (dạng `crypto{...}`) chỉ bằng oracle chẵn/lẻ.

## Gợi ý

1. RSA multiplicative: bản rõ của `ct·(2^k)^e mod n` là `m·2^k mod n`.
2. `n` lẻ → `2x mod n` chẵn ⇔ `2x < n` (không rơi vòng). Dò `m·2^k mod n`
   tương đương tìm nhị phân vị trí của m trong [0, n).
3. Cứ nhân đôi: mỗi lần nhận Even/Odd thu hẹp khoảng một nửa.
   Sau ~log₂(n) truy vấn khoảng còn độ rộng < 1 → lấy m.

## Chạy lời giải (để kiểm tra)

```
python solve.py            # tu dong khoi dong server o port rong
```
