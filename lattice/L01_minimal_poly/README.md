# L01 — Đa thức tối tiểu ẩn trong một con số thập phân

> Dạng: **Khôi phục đa thức tối tiểu từ xấp xỉ** (paper 2023/032, mục 3.6 — Kannan–Lenstra–Lovász 1984)
> Challenge thật cùng dạng: UIUCTF 2025 — *"Back to Roots"* (giải bằng LLL tìm minimal polynomial)

## Đề bài

Một "số huyền bí" $\alpha$ được ký hiệu bởi đa thức tối tiểu (minimal polynomial) $f(x) \in \mathbb{Z}[x]$
— đa thức monic bậc thấp nhất mà $\alpha$ là nghiệm. Chúng ta chỉ còn lại xấp xỉ thập phân sau:

```
alpha ≈ 6.673681168671
```

Biết rằng $f$ có **bậc 3** và mọi hệ số đều nhỏ (giá trị tuyệt đối < 1000).

**Tìm $f(x)$.** Flag là danh sách hệ số của $f$ theo thứ tự hệ số tự do → hệ số bậc cao:

```
crypto{[a0,a1,a2,a3]}
```

## File

- `output.txt` — xấp xỉ thập phân của α
- `gen.py` — sinh lại output (seed cố định)
- `solve.py` — lời giải mẫu (LLL theo paper)
- `SOLUTION.md` — phân tích lời giải

## Gợi ý

1. Viết $f(\beta) \approx 0$ thành **một phương trình tuyến tính gần đúng** theo các hệ số $a_0, a_1, a_2$ (hệ số $a_3 = 1$ vì monic).
2. Nhân với $10^{12}$ để làm việc trên số nguyên.
3. Dựng lattice 4×4 như mục 3.6 của paper: mỗi hàng = (lũy thừa β·scale, vector đơn vị), hàng cuối = (β³·scale, 0…0).
4. LLL — hàng đầu chính là $(\approx 0, a_0, a_1, a_2)$.
