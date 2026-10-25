# 07 — Decipher Oracle / Blinding attack

**Dạng:** Oracle giải mã không cho giải mã flag → dùng tính multiplicative (làm mù)
**Độ khó:** ★★☆☆☆
**Nguồn:** `TASK 1 RSA ATTACK - HackMD.pdf` — mục *"Decipher oracle"*; `RSA-survey-vi.md` §2.2 (Làm mù)

## Dịch vụ

```
python server.py 1337
```

Dịch vụ cho bạn `n, e, c` (bản mã của flag). Bạn có thể gửi **bất kỳ** ciphertext
nào để dịch vụ giải mã — trừ khi kết quả chính là flag (khi đó nó từ chối).

```
n = ...
e = 65537
c = ...
Text to decrypt: ...
```

## Mục tiêu

Dùng oracle giải mã flag `c` mà không bị từ chối. Flag dạng `crypto{...}`.

## Gợi ý

1. RSA là multiplicative: `D(A·B) = D(A)·D(B) mod n`.
2. Gửi `c' = c · r^e mod n` → dịch vụ trả về `m·r mod n`.
3. Chia lại cho r (`inverse(r, n)`) để lấy m.

## Chạy lời giải (để kiểm tra)

```
python solve.py            # tu dong khoi dong server o port rong
```
