# RSA Challenge Collection

Bộ challenge RSA luyện tập, mỗi challenge = một "dạng" tấn công. Tài liệu lý
thuyết nền: **`../RSA-survey-vi.md`** — "Twenty Years of Attacks on the RSA
Cryptosystem" (Dan Boneh, bản dịch tiếng Việt).

Flag format: **`crypto{...}`**.

## Cách dùng

```
cd <thu_muc_challenge>
python gen.py        # (challenge offline) sinh lại output.txt từ seed cố định
```

- **Lời giải mẫu** nằm ở `..\solves\<ten_challenge>.py` (mỗi challenge một
  file, gom riêng để luyện tập đúng cách — không nhìn giải trước). Các file
  này là bản tham khảo — chạy được khi đặt lại vào đúng folder challenge
  (tham chiếu `..\_lib`, `output.txt`, `server.py` theo đường dẫn tương đối).
- **Giải thích chi tiết** từng bước: `SOLUTION.md` trong mỗi folder
  (kèm ví dụ số học + cách phòng thủ + flag).

Challenge có oracle dịch vụ (07, 11, 18): chạy tay `python server.py 1337`.
Lời giải tương ứng tự khởi động server ở port ngẫu nhiên, tấn công, rồi tắt.

Challenge 14 (Bleichenbacher): oracle là hàm cục bộ trong `challenge.py`
(mô phỏng dịch vụ kiểm tra đệm PKCS#1) — lời giải chạy ~1.4 triệu truy vấn
offline trong ~5 giây.

Thư viện dùng chung `_lib/rsalib.py` (flint LLL + Coppersmith + Wiener +
GCD đa thức mod N + Pollard p−1; kiểm thử đầy đủ trong `_lib/test_rsalib.py`).

## Danh sách challenge (18 dạng)

| # | Challenge | Dạng tấn công | Nguồn | Độ khó |
|---|-----------|---------------|-------|--------|
| 01 | `01_factor_small_n` | Factorizing the public key (N quá nhỏ) | HackMD | ★ |
| 02 | `02_fermat_close_primes` | Fermat factorization (p, q gần nhau) | HackMD | ★★ |
| 03 | `03_small_e_cuberoot` | Small public exponent, m³ < N | HackMD, survey §4 | ★ |
| 04 | `04_hastad_broadcast` | Håstad broadcast (CRT + căn bậc e) | HackMD, survey §4.2 | ★★ |
| 05 | `05_common_modulus_external` | Common modulus — Extended Euclid | HackMD | ★★ |
| 06 | `06_common_modulus_internal` | Common modulus — nội bộ (Prop. 1, Simmons) | HackMD, survey §2.1 | ★★★ |
| 07 | `07_blinding_oracle` | Decipher oracle / Blinding (multiplicative) | HackMD, survey §2.2 | ★★ |
| 08 | `08_wiener_small_d` | Wiener — phân số liên tục (d < ⅓N^¼) | HackMD, survey §3 | ★★★ |
| 09 | `09_small_dp_bruteforce` | Brute force CRT exponent d_p nhỏ | HackMD | ★★★ |
| 10 | `10_crt_fault_signature` | Fault attack chữ ký CRT (Bellcore) | HackMD, survey §5.2 | ★★ |
| 11 | `11_parity_oracle` | Parity/LSB oracle — tìm nhị phân | HackMD | ★★★ |
| 12 | `12_pollard_p_minus_1` | Pollard p−1 (p−1 B-smooth) | survey §1.1 | ★★ |
| 13 | `13_franklin_reiter` | Franklin–Reiter (thông điệp liên quan, e=3) | survey §4.3 | ★★★ |
| 14 | `14_bleichenbacher_pkcs1` | Bleichenbacher — oracle đệm PKCS#1 v1.5 | survey §5.3 | ★★★★★ |
| 15 | `15_coppersmith_known_high_bits` | Coppersmith — biết bit cao của p (Thm 10) | survey §4.1, §4.5 | ★★★★ |
| 16 | `16_short_pad_attack` | Coppersmith short-pad (resultant + FR) | survey §4.4 | ★★★★★ |
| 17 | `17_bdf_partial_key_exposure` | Partial key exposure — LSB của d (BDF) | survey §4.5 | ★★★★★ |
| 18 | `18_timing_attack_kocher` | Timing attack (Kocher, square-and-multiply) | survey §5.1 | ★★★★ |

Mỗi thư mục con có:

- `README.md` — đề bài + gợi ý
- `gen.py` / `output.txt` — dữ liệu công khai (challenge offline, seed cố định)
- `server.py` hoặc `challenge.py` — dịch vụ / oracle (challenge tương tác)
- `solve.py` — lời giải mẫu, chạy được, in đúng flag
- `SOLUTION.md` — giải thích từng bước + ví dụ số học + cách phòng thủ + flag

## Ghi chú kỹ thuật

- Môi trường: Python 3.14 + `gmpy2` + `pycryptodome` + `sympy` + `python-flint`
  (`pip install gmpy2 pycryptodome sympy python-flint`).
- `_verify_all.py` — chạy gen + solve toàn bộ và đối chiếu flag:
  `python _verify_all.py` (hoặc liệt kê tên thư mục để chạy một phần).
  Kết quả lần cuối: **18 OK, 0 FAIL**.
- Thời gian chạy từng solve.py: từ 0.1 giây (phần lớn) tới ~10 giây
  (parity oracle, timing attack) và ~5 giây (Bleichenbacher, 1.4M truy vấn).
