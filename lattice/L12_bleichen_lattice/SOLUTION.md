# L12 — SOLUTION

## Pipeline (mục 5.4 của paper — formulation của Nguyen 2009)

```
Oracle đệm: O_B(c') = 1 ⟺ bản rõ bắt đầu 00 02
   → thu 60 r_i với O_B(r_i^e·c) = 1  ⟺  2B ≤ r_i·m mod N < 3B, B = 2^496
   → k_i := r_i·m mod N − 2B ∈ [0, B)
   → k_i ≡ r_i·m − 2B (mod N)                       [HNP, ẩn = m]
   → lattice embedding 62 chiều  →  LLL  →  m  →  unpad  →  flag
```

## Điều kiện giải được (mục 5.4.2 của paper)

Vector HNP có chuẩn $\sqrt{\ell+2}\,B$; vector "bình thường" của lattice cỡ
$\sqrt{\ell+2}\,(B^2N^{\ell-1})^{1/(\ell+2)}$. Yêu cầu lệch chuẩn rút gọn về
**$l \ll 16\ell$** — với $l = 512$ bit: cần $\ell \gtrsim 32$ quan hệ. Ta có 60 —
dư địa vừa phải (hệ số xấp xỉ của LLL bắt đầu thấy mồn).

Mỗi truy vấn thành công với xác suất $\approx 1/2^{16}$ → cần
$\ell \cdot 65536 \approx 3{,}9$ triệu truy vấn (bản Bleichenbacher cổ điển
tối ưu hơn về số truy vấn — bản lattice đổi lại là **một phép LLL duy nhất**, song song hóa tốt —
đây chính là hướng khai thác của "The 9 Lives of Bleichenbacher's CAT" 2019).

## Khác biệt với bản Bleichenbacher cổ điển

| | Bleichenbacher 98 | Bản lattice (Nguyen 09) |
|---|---|---|
| Thông tin oracle | "đúng đệm" | y hệt |
| Thuật toán | chia đôi khoảng adaptive | thu thập quan hệ rồi LLL 1 lần |
| Truy vấn | ~465k (512-bit, tối ưu) | ~60·65536 ≈ 3.9M |
| Song song hóa | khó (tự nhiên tuần tự) | dễ (thu thập r độc lập) |

## Flag

**Flag: `crypto{bl31ch3nb4ch3r_4s_hnp}`**

## Nguồn

- Paper 2023/032, mục 5.4 (Ble98; Nguyen 09; Ron+19)
- Bản Bleichenbacher cổ điển: bộ RSA challenge 14 (`challenge/14_bleichenbacher_pkcs1`)
