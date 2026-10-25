# L04 — Partial Key Exposure: lộ bit cao của d

> Dạng: **Partial key exposure attack** (paper 2023/032, mục 5.2.2 — Ernst et al. 2005,
> giản lược theo Sarkar–Sen Gupta–Maitra 2010)
> Dạng thật trên CTF: hiếm (thường gặp biến thể LSB của d — xem bộ RSA challenge 17);
> đây là bản "khoảng lõm" để tập trung đúng ý tưởng **xấp xỉ k**

## Đề bài

Khóa RSA 512-bit dùng số mũ bí mật $d$ chỉ dài 183 bit (đáng lẽ phải ≥ $\varphi/2$).
Một side-channel rò rỉ **bit cao của $d$**: bạn biết $d_0$ sao cho phần thiếu chỉ là
8 bit cuối:

```
N = ...
e = ...
d0 = ...          (d = d0 + x, |x| < 256)
```

**Khôi phục $d$** → giải mã flag (AES-CTR, key = sha256(d)).

## File

- `output.txt` / `gen.py` / `solve.py` / `SOLUTION.md`

## Gợi ý

1. Từ $ed = 1 + k\varphi(N)$, $\varphi(N) = N + 1 - 2s$ với $s = \frac{p+q}{2}$.
2. $k = \frac{ed-1}{\varphi} \approx \frac{e\,d_0}{N}$ (lấy phần nguyên) — chỉ sai khác
   một vài đơn vị khi phần ẩn của $d$ nhỏ.
3. Thử từng ứng viên $k$: từ $2ks \equiv 1 + k(N+1) \pmod e$ suy ra $s$ — rồi
   $z^2 - 2sz + N = 0$ cho $p, q$.
4. Với phần ẩn LỚN hơn (vài chục đến vài trăm bit), cặp $(k_1, s)$ trở thành nghiệm
   nhỏ của đa thức 2 biến $1 + 2(k_0+x)(\frac{N+1}{2} - y) \equiv 0 \pmod e$ —
   đúng khung Boneh–Durfee (xem SOLUTION).
