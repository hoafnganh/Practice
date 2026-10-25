# Lattice Challenge Collection

Bộ challenge lattice tổng hợp từ tài liệu **`lattice-theory-vi.md`** (ngay trong thư mục này) —
bản biên soạn thuần Việt của paper *"A Gentle Tutorial for Lattice-Based Cryptanalysis"*
(Surin & Coheny, ePrint 2023/032). Mỗi challenge = một dạng tấn công trong paper.

Flag format: **`crypto{...}`**.

## Cách dùng

**Lời giải mẫu** nằm ở `lattice/solves/` (file phẳng `<tên_challenge>.py`, tự
`chdir` về folder challenge khi chạy — chạy được từ bất kỳ đâu), tách khỏi folder
challenge để luyện tập đúng cách (không nhìn giải trước):

```
cd <thu_muc_challenge>
python gen.py                          # sinh lại output.txt từ seed cố định
python ..\solves\L01_minimal_poly.py   # lời giải mẫu — in ra flag
```

Chạy kiểm thử toàn bộ: `python _verify_all.py` (hoặc liệt kê tên thư mục để chạy một phần).

## Danh sách challenge (12 dạng)

| # | Challenge | Dạng tấn công | Mục paper | Challenge thật cùng dạng | Độ khó |
|---|-----------|---------------|-----------|--------------------------|--------|
| L01 | `L01_minimal_poly` | Đa thức tối tiểu từ xấp xỉ (KLL84) | §3.6 | UIUCTF 2025 "Back to Roots" | ★★ |
| L02 | `L02_subset_sum` | Balô mật độ thấp — CJLOSS | §4.2 | SECCON CTF 2021 | ★★ |
| L03 | `L03_stereotyped` | RSA e=3 tin nhắn khuôn mẫu (Coppersmith) | §5.1 | Squ1rrel CTF 2024 "Partial RSA" | ★★★ |
| L04 | `L04_partial_key` | Partial key exposure — xấp xỉ k từ MSB của d | §5.2.2 | (hiếm; biến thể LSB = RSA-17) | ★★★ |
| L05 | `L05_hnp_basic` | Hidden Number Problem thuần | §4.3 | Donjon CTF (Projective Signatures) | ★★ |
| L06 | `L06_truncated_lcg` | LCG cụt bit → HNP | Hình 2 | DownUnderCTF 2020; RCTF | ★★★ |
| L07 | `L07_ecdsa_xor_nonce` | ECDSA k = z⊕d → subset sum kiểu TSJ | §5.3.1 | **TSJ CTF 2022 "Signature"** | ★★★★★ |
| L08 | `L08_ecdsa_biased` | ECDSA nonce lệch (zero MSB) → HNP | §5.3.2 | Donjon CTF; TBTL 2023; LadderLeak | ★★★ |
| L09 | `L09_ecdsa_shared_msb` | ECDSA nonce chia sẻ MSB → HNP | §5.3.2 | biến thể của trên | ★★★★ |
| L10 | `L10_ehnp` | EHNP — mảnh rời của nonce VÀ khóa | §4.3.2, §5.3.3 | hiếm (Minerva-style) | ★★★★ |
| L11 | `L11_boneh_durfee` | Boneh–Durfee d < N^0.25+ | §5.2.1 | 春秋杯 2023 v.v. | ★★★★ |
| L12 | `L12_bleichen_lattice` | Bleichenbacher PKCS#1 bản lattice (HNP) | §5.4 | (bản cổ điển = RSA-14) | ★★★★ |

## Cấu trúc

- `_lib/latlib.py` — thư viện chung: LLL (flint + pure-Python fallback), Babai CVP,
  Kannan embedding, HNP, CJLOSS + subset-sum modular kiểu TSJ, EHNP,
  bivariate modular small roots (Boneh–Durfee), Coppersmith univariate (từ bộ RSA),
  ECDSA cơ bản (secp256k1 / P-192), LCG, AES-flag helper.
  Kiểm thử đầy đủ: `_lib/test_latlib.py` — **17/17 OK**.
- `_verify_all.py` — chạy gen + solve toàn bộ, đối chiếu flag.

## Ghi chú kỹ thuật

- Môi trường: Python 3.14 + `gmpy2` + `pycryptodome` + `sympy` + `python-flint` + `flint`.
- Lỗi đã chốt 1-1 trong lúc phát triển (đều có trong SOLUTION/latlib docstring):
  flint `fmpz_mat.lll` mặc định `gram='approx'` có thể trả vector ngoài lattice
  (dùng `gram='exact'` cho entry lớn); vector đích luôn có 2 dạng ± trong cơ sở
  reduced — phải xử lý dấu khi đọc nghiệm; ma trận chữ nhật (rows≠cols) cần cẩn thận.
- Thời gian solve: 0.1–6 giây (L07 ~29 giây do lattice 263 chiều).
