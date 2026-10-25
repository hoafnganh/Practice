# L06 — LCG bị cắt cụt: chỉ thấy bit cao

> Dạng: **Truncated LCG → HNP** (paper 2023/032, Hình 2; Frieze–Håstad–Kannan–Lagarias–Shamir 1988)
> Challenge thật cùng dạng: DownUnderCTF 2020 (jsur.in writeup), RCTF (truncated LCG + LLL),
> tấn công Java `Random` của ELTAM

## Đề bài

Trò chơi dùng LCG:

$$x_{i+1} = a\,x_i + b \pmod M,\qquad M = 2^{61} - 1$$

Tham số $a, b$ công khai. Mỗi lượt server chỉ in **40 bit cao** của trạng thái
(24 bit thấp bị cắt). Bạn thu được 26 quan sát:

```
M = 2305843009213693951
a = ...
b = ...
y[0] = ...     (y_i = x_i >> 24)
...
nonce = ...  ct = ...   (AES-CTR, key = sha256(x_0))
```

**Khôi phục trạng thái đầu $x_0$** → flag.

## File

- `output.txt` / `gen.py` / `solve.py` / `SOLUTION.md`

## Gợi ý

1. Đặt $x_i = 2^{24}y_i + e_i$ với $e_i < 2^{24}$ — phần bị cắt chính là "số bị che".
2. Biểu diễn $x_i$ theo $x_0$: $x_i \equiv a^i x_0 + c_i \pmod M$.
3. Ghép lại thành HNP: $e_i \equiv a^i x_0 + (c_i - 2^{24}y_i) \pmod M$.
4. Dùng `hnp_solve_embedding` — LCG là HNP trá hình.
