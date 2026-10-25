# L05 — Bài toán số ẩn (Hidden Number Problem)

> Dạng: **HNP gốc của Boneh–Venkatesan** (paper 2023/032, mục 4.3) — nền của L06, L08, L09, L12
> Challenge thật cùng tinh thần: Ledger Donjon CTF "Projective Signatures" (lộ bit nonce),
> nhiều bài DLP side-channel

## Đề bài

Một hệ Diffie–Hellman dùng số nguyên tố $p$ 256-bit và bí mật $\alpha$. Server tính

$$v_i = t_i \cdot \alpha + r_i \bmod p$$

với $t_i$ ngẫu nhiên **công khai**, nhưng bản vá lỗi khiến $r_i$ luôn nằm trong
$[0, 2^{40})$ thay vì $[0, p)$. Bạn nhận được 24 cặp $(t_i, v_i)$ và bản mã flag:

```
p = ...
t[0] = ...   v[0] = ...
...
nonce = ...  ct = ...     (AES-CTR, key = sha256(alpha))
```

**Tìm $\alpha$.**

## File

- `output.txt` / `gen.py` / `solve.py` / `SOLUTION.md`

## Gợi ý

1. Đặt $k_i = v_i - t_i\alpha \bmod p$ — mỗi $k_i < 2^{40}$ là "phần bị che".
2. Đây chính là HNP: $\beta_i - t_i\alpha + a_i \equiv 0 \pmod p$, $|\beta_i| < B$.
3. Hai cách giải: CVP/Babai (mục 4.3.1) hoặc Kannan embedding thành SVP (mục 4.3.1 — thường mạnh hơn).
4. Vector đích trong lattice embedding: $(\beta_1, \dots, \beta_m, \pm B)$.
