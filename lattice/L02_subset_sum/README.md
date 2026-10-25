# L02 — Balô mật mã (low-density subset sum)

> Dạng: **Knapsack / subset sum mật độ thấp giải bằng LLL** (paper 2023/032, mục 4.2 — CJLOSS)
> Challenge thật cùng dạng: SECCON CTF 2021 (rkm0959's writeup, CJLOSS), cùng nhiều bài knapsack low-density khác

## Đề bài

Chúng tôi mã hóa flag bằng một balô:

- 160 trọng số $a_i$ (mỗi cái 1024 bit)
- $s = \sum e_i a_i$ với $e_i \in \{0,1\}$ là các bit của flag

```
a[0] = ...
a[1] = ...
s = ...
```

**Tìm lại các bit $e_i$** → flag.

File `output.txt`: 160 trọng số + tổng $s$. Mật độ $d = 160/1024 = 0{,}156$.

## File

- `output.txt` / `gen.py` / `solve.py` / `SOLUTION.md`

## Gợi ý

1. Mật độ $d < 0{,}9408$ → lattice CJLOSS (nâng cấp của Lagarias–Odlyzko).
2. Vector đích: $(2e_1 - 1, \dots, 2e_n - 1, 0)$ — chuẩn $\sqrt{160} \approx 12{,}6$.
3. Sau LLL, đọc hàng đầu: $\pm 1$ tại $n$ tọa độ đầu, $0$ ở cột cuối.
