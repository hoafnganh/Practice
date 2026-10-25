# L08 — SOLUTION

## Pipeline

```
40 chữ ký, k_i < 2^200  →  k_i ≡ s_i⁻¹z_i + s_i⁻¹r_i·d (mod n)   [HNP]
                        →  lattice embedding 42 chiều  →  LLL  →  d
```

## Biến đổi (mục 5.3.2, biến thể "Zero MSB" của paper)

$$s_i k_i \equiv z_i + r_i d \;\Longrightarrow\; k_i \equiv s_i^{-1}z_i + s_i^{-1}r_i\,d \pmod n$$

Đặt $t_i = s_i^{-1}r_i$, $a_i = s_i^{-1}z_i$: **$k_i = t_i d + a_i \bmod n$ với
$k_i < B = 2^{200}$** — đúng định nghĩa HNP (mục 4.3). Lattice (mục 4.3.1, bản
Howgrave-Graham–Smart nguyên hóa):

- $m$ hàng $n\cdot e_i$;
- hàng $a = (a_i + B/2 \dots, B)$;
- hàng $t = (t_i \dots, 0)$.

Tổ hợp $(-\ell_i, d, 1)$ cho vector $(k_i - B/2,\ B)$ — chuẩn $\le \sqrt{41}\cdot 2^{199}
= 2^{202.7}$, trong khi $\det^{1/42} = (n^{40}B)^{1/42} = 2^{(10240+200)/42} = 2^{248.6}$.
Lệch chuẩn 45 bit → LLL bắt ngay.

## Đọc kết quả & kiểm chứng

Hàng có **cột cuối $\pm B$**: $k_i = \pm(\text{tọa độ}) + B/2$; rồi
$d = (k_i - a_i)t_i^{-1} \bmod n$ (bỏ phiếu đa số giữa các $i$). Cuối cùng
**xác minh bằng khóa công khai** $dG \overset{?}{=} Q$.

## Thực trạng thực tế

"Lệch dưới 1 bit cũng chết" — LadderLeak (CCS 2020) phá ECDSA với chỉ MSB luôn = 0
trong less than one bit of leakage. Minerva, OpenSSH CVE-2023-27632, các ví Bitcoin
lỗi PRNG — đều về cùng một HNP.

## Flag

**Flag: `crypto{b14s3d_n0nc3_l34ds_t0_d00m}`**

## Nguồn

- Paper 2023/032, mục 5.3.2 (HS01; Ara+20)
- Donjon CTF: https://blog.cryptohack.org/ecdsa-side-channel-attack-projective-signatures-donjon-ctf-writeup
- LadderLeak: https://eprint.iacr.org/2020/615 ; Biased Nonce Sense: https://eprint.iacr.org/2019/023
