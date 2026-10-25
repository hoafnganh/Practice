# tools — Hộp công cụ crypto

Sổ tay cài đặt + câu lệnh cho bộ tool giải crypto: môi trường Python/Sage, factoring, RSA all-in-one, OpenSSL, hash, stego, forensic. Nguyên tắc chung: **ưu tiên tool offline** — không upload dữ liệu nhạy cảm (đề bài, secrets, dump) lên dịch vụ web công cộng; khi bắt buộc dùng web (tra cứu công khai như factordb.com) thì chỉ gửi các giá trị "vô hại" (số n công khai).

## Sage trên WSL

Cách tạm (chỉ phiên hiện tại):
```bash
source ~/miniforge3/etc/profile.d/conda.sh
conda activate sage
```
Cách vĩnh viễn (khuyên dùng):
```bash
~/miniforge3/bin/conda init bash
exec bash          # hoặc thoát SSH rồi vào lại
conda activate sage
```

## Môi trường Python 3 (WSL / Linux)

```bash
python3 -m venv v && source v/bin/activate
pip install pycryptodome gmpy2 sympy pwntools
# hoặc với uv:
uv venv && uv pip install pycryptodome gmpy2 && uv run solve.py
```
Máy có `python2` riêng thì dùng cho chall cũ (script thế hệ cũ in không dấu ngoặc).

## factordb-python

Tra N vào FactorDB không cần mở web.
```python
from factordb.factordb import FactorDB
f = FactorDB(n); f.connect()
print(f.get_status(), f.get_factor_list())
```
Lưu ý: status `C` = composite chưa factor xong, list có thể chứa thừa số ghép → tự kiểm `p*q == n` và `isprime` từng thừa số.

## Fermat (p ≈ q) — tự viết, LUÔN thử trước khi nghĩ đến ECM

N to (≥2048 bit) cân bằng mà FactorDB không có → p có thể sát √N. **PARI `factor()` KHÔNG có bước này** (chuỗi của nó: trial division → Rho/SQUFOF → ECM → MPQS) → treo vô hạn: ECM không với nổi thừa số 4096-bit (record ~275 bit), MPQS chết ở ~130 chữ số. Python 5 dòng thì tức thì:
```python
from gmpy2 import isqrt
def fermat(n, max_iter=10**6):
    a = isqrt(n)
    if a*a < n: a += 1
    for _ in range(max_iter):
        b2 = a*a - n
        b = isqrt(b2)
        if b*b == b2: return int(a-b), int(a+b)   # None = không phải p≈q
        a += 1
```
Ví dụ thật: RSA-8192 cân bằng với p−q = 2886 → Fermat trúng ngay vòng 1 (0.000s), PARI treo mãi.

## SymPy

Số học cho SỐ NHỎ (brute, tìm prime, factor ≤ ~40 bit, đồng dư, Diophantine/Pell). N lớn (2048 bit) thì ĐỪNG — đi theo chain factordb → Fermat → PARI/Sage. ĐÃ TEST trên sympy 1.14 — **3 hàm KHÔNG nằm ở top-level** (xem import dưới).
```python
from sympy import (primerange, isprime, nextprime, prevprime, prime, primepi,
                   randprime, factorint, divisors, mod_inverse, gcd, lcm,
                   sqrt_mod, legendre_symbol, is_quad_residue,
                   n_order, primitive_root, discrete_log, diophantine)
# 3 hàm này KHÔNG top-level (sympy 1.13/1.14):
from sympy.core.intfunc import igcdex                 # (x, y, g) : a*x + b*y = g
from sympy.ntheory.modular import crt                 # -> (x, M)
from sympy.solvers.diophantine.diophantine import diop_DN

list(primerange(2, 4096))        # primes TRONG [2,4096) — nửa mở, KHÔNG gồm 4096 -> 564 số
isprime(n); nextprime(n); prevprime(n); prime(100); primepi(4096)   # 541; 564
randprime(a, b)                  # prime ngẫu nhiên trong [a,b)

factorint(n)                     # {p: k, ...}  vd {1429:1, 1531:1}
factorint(n, limit=10**5)        # trial division tới limit; phần CHƯA factor nằm
                                 # trong dict như một "thừa số" — PHẢI isprime() lại!

mod_inverse(e, phi)              # = pow(e,-1,phi); ValueError nếu không khả nghịch
igcdex(a, b)                     # Bézout (x, y, g) với a*x + b*y = g — x TRƯỚC g
                                 # gmpy2.gcdext(a,b) là (g, x, y) — NGƯỢC THỨ TỰ!
crt([2, 3, 5], [1, 2, 3])        # -> (23, 30) — TUPLE (nghiệm, modulus); moduli NTLCN cặp đôi
sqrt_mod(a, p, all_roots=True)   # căn bậc 2 mod p nguyên tố -> [r1, p-r1] (Tonelli-Shanks)
legendre_symbol(a, p); is_quad_residue(a, p)
n_order(g, p)                    # cấp của g: n_order(10,17)=16 -> 1/17 reptend 16 chữ số
primitive_root(p); discrete_log(n, a, b)   # giải b^x ≡ a (mod n), group ≤ ~40 bit

diop_DN(D, N)                    # nghiệm gốc (x1,y1) của x²-Dy²=N; vd diop_DN(7,1)=(8,3)
                                 # nghiệm kế: (x1+y1√D)^k — tự viết vòng nhân trong Z[√D]
diophantine(expr, syms=[x, y])   # dạng symbolic; THAM SỐ PHẢI là syms= (đưa list vào
                                 # vị trí 2 = TypeError); output = họ nghiệm theo t — rối,
                                 # Pell thực tế dùng diop_DN + tự sinh
```

Lưu ý:
- Thang tốc độ: sympy chậm hơn gmpy2 (sympy cho KHÁI NIỆM — prime/factor/order/diophantine; gmpy2 cho cộng nhân số khổng lồ). Một script có thể trộn cả hai.
- `discrete_log(n, a, b)` nhầm thứ tự a/b là chạy mãi không xong — luôn ghi chú `b^x = a mod n` bên cạnh lời gọi.
- sympy trả `Integer` riêng của nó (chậm hơn int khi tính thuần); vòng brute nặng thì `int()` lại trước khi mũ.

## crypto-attacks

Thư viện hàng trăm attack (RSA, lattice, DH, ECC…). Mỗi attack = 1 hàm Python có docstring. Trên máy Kali thường nằm `/opt/tools/crypto-attacks`; không có thì clone từ <https://github.com/jvdsn/crypto-attacks>.
```bash
ls /opt/tools/crypto-attacks/attacks/rsa/        # wiener.py, common_modulus.py, ...
```
```python
import sys; sys.path.insert(0, "/opt/tools/crypto-attacks")
from attacks.rsa.wiener import attack
d = attack(n, e)
```
Lưu ý: kiểm tên module/hàm/tham số bằng docstring từng file trước khi dùng.

## RsaCtfTool (Windows/WSL)

RSA all-in-one: tự chạy bộ attack từ public key.
```bash
python3 RsaCtfTool.py --publickey key.pub --uncipherfile flag.enc --attack all
python3 RsaCtfTool.py -n <N> -e 65537 --private
python3 RsaCtfTool.py --publickey key.pub --attack wiener
```
Lưu ý: `all` chậm (vài phút); đoán được heuristic thì chỉ định.

## PARI/GP

```bash
gp -q
```
```
factor(n)                        ~ ECM+MPQS, tốt tới ~60-70 bit thừa số
isprime(n); znorder(Mod(g,p))
znlog(Mod(h,p), Mod(g,p))        ~ DLP (p-1 mượt)
msqrt(a,p)                       ~ sqrt mod p (Tonelli-Shanks)
Mod(c,n)^d                       ~ pow
E=ellinit([a,b],p); ellmul(E,G,k); elllog(E,P,G)
```
One-liner: `gp -q <<<'print(factor(2^67-1))'`
Lưu ý: ECDLP chỉ khả thi khi order nhỏ (vài chục bit).

## OpenSSL

```bash
openssl rsa -in key.pem -text -noout          # xem tham số key
openssl pkeyutl -decrypt -in ct.bin -inkey key.pem
openssl enc -aes-256-cbc -d -K <hexkey> -iv <hexiv> -in f.enc
openssl dgst -sha256 -verify pub.pem -signature sig.bin file
openssl x509 -in cert.pem -text -noout

# Trích n, e từ PUBLIC KEY
openssl rsa -pubin -in PublicKey.pem -text -noout      # Public-Key: (bit) + Modulus hex + Exponent
openssl rsa -pubin -in PublicKey.pem -modulus -noout   # n hex liền, không ':' (Modulus=00b6...)
openssl rsa -pubin -in PublicKey.pem -modulus -noout | cut -d= -f2 \
  | xargs -I{} python3 -c "print(int('{}',16))"        # n thập phân, ném thẳng vào python/sage
python3 -c "from Crypto.PublicKey import RSA; k=RSA.import_key(open('PublicKey.pem','rb').read()); print('n =', k.n); print('e =', k.e)"   # gọn nhất: n,e decimal
```
Lưu ý: `-K/-iv` (HOA) = raw key hex, không KDF; `-k` thường = password (có KDF/salt). `-pubin` = input là public key (`BEGIN PUBLIC KEY`); nếu là `BEGIN CERTIFICATE` thì `openssl x509 -in cert.pem -noout -modulus`. PEM lỗi parse → thử thêm `-inform DER`. Mẹo đo size key từ chiều dài base64: `modulus_bytes ≈ DER_bytes − 30` (vd ~2 dòng base64 = ~62 byte DER = modulus 256 bit; 162 byte DER = 1024 bit) → modulus nhỏ bất thường thì factor ngay.

Gotcha từng gặp: PEM công khai có thể chủ ý SAI 1 bit trong n (hint kiểu "lost 1 bit") — ciphertext mã hoá bằng n thật = n PEM với bit bị lật lại; brute 256 vị trí bit, chọn candidate là semiprime đúng 2 thừa số. Modulus RSA thật luôn LẺ → n chẵn thì thử `n | 1` trước.

Chi tiết đầy đủ 14 mục lệnh openssl: `cheatsheet-openssl.md`.

## hlextend

Hash length extension khi biết `hash(secret‖msg)` + độ dài secret.
```python
import hlextend
h = hlextend.new('sha256')
data = h.extend(b'&admin=1', b'user=x', 16, known_hash_hex)   # bytes gửi đi
print(data, h.hexdigest())
```
Lưu ý: secret length phải đúng — chưa biết thì brute 8..64.

## padding-oracle-attacker

Tự động hoá CBC padding oracle qua HTTP.
```bash
padding-oracle-attacker --help
padding-oracle-attacker -u http://t/dec -e <hexct> --block-size 16 --error "Padding"
```
Lưu ý: tool này kén server; tự viết script 16×256 request cũng rất nhanh (xem `cheatsheet-symmetric.md` mục 3.5).

## jwt_tool

```bash
jwt_tool <token>              # audit tự động
jwt_tool <token> -T           # tamper tương tác
jwt_tool <token> -X k -pk pub.pem   # attack mode (alg confusion, none, ...)
```

## hashid / hashcat / John

```bash
hashid '$6$abc...'                        # đoán format hash
hashcat -m 1800 -a 0 h.txt /usr/share/wordlists/rockyou.txt
john --wordlist=/usr/share/wordlists/rockyou.txt h.txt
john --show h.txt
```
`-m` hay dùng: `0` MD5, `100` SHA1, `1400` SHA256, `1000` NTLM, `1800` sha512crypt `$6$`, `3200` bcrypt.
Lưu ý: check GPU (`nvidia-smi`) trước khi kỳ vọng hashcat nhanh; bcrypt gần như bỏ trên CPU.

## zsteg

```bash
zsteg -a file.png                  # quét mọi channel/bit-order
zsteg -E b1,rgb,lsb,xy file.png    # extract đúng 1 mode
```

## rockyou + SecLists

```
/usr/share/wordlists/rockyou.txt
/usr/share/seclists/Passwords/Common-Credentials/
```
Gotcha file wordlist lớn: dòng trống giữa file làm script EOF sớm nếu chỉ check `if line`; đọc binary `latin-1` để không crash trên byte lạ.

## Classical toolkit

Folder `classical/` — thuần stdlib, không cần cài gì. Chạy thử sau khi copy đi máy khác: `python _verify_all.py` → phải ra `24 passed`. Thay thế nhu cầu các web solver (dCode...) bằng bản offline + CyberChef local.

```bash
cd classical/

# MỌI tool dưới đây nhận cả 3 kiểu input: text inline "..." | file | stdin "-"
#   (arg KHÔNG trùng tên file thật = hiểu là text inline; "-" = stdin)

# BƯỚC 1 LUÔN CHẠY: chẩn đoán IC/chi2 -> gợi ý họ cipher
python freq_ic.py ct.txt        # hoặc: python freq_ic.py "Khoor Zruog"
#   IC ~0.066  -> mono substitution / ROT  -> rot_family.py -> substitution_hillclimb.py
#   IC ~0.04   -> polyalphabetic           -> vigenere_keyless.py / xor_tool.py
#   binary, bội của 5 -> baudot.py; nhiều non-printable -> xor_tool.py

# ROT family: brute ROT-N (26) + ROT47 (94 shift) + Atbash + Affine (312 key)
python rot_family.py "Khoor Zruog"
python rot_family.py ct.txt

# Vigenère KHÔNG key: tự tìm độ dài key (IC) + key (chi2 từng cột)
python vigenere_keyless.py ct.txt
python vigenere_keyless.py --keylen 7 ct.txt      # ép độ dài
python vigenere_keyless.py --key LEMON ct.txt     # decrypt có key

# Substitution mono: hill-climb quadgram (kẹ local optimum thì chạy lại)
python substitution_hillclimb.py ct.txt

# Base64 bảng alphabet CUSTOM từ known-plaintext
# Nối MỌI đoạn known lại thành 1 cặp duy nhất để phủ đủ 64 ký tự
python custom_b64_recover.py --known-plain "known..." --known-cipher "8kP3..." --target "Xy..."

# Baudot/ITA2 5-bit — tự thử 4 kiểu đọc (MSB/LSB x start LTRS/FIGS)
python baudot.py decode bits.txt
python baudot.py decode5 file.txt        # biến thể: mỗi nhóm 5 bit = 1 chữ cái (A=0)
python baudot.py encode "HELLO"

# XOR: 1-byte brute / repeating-key (nhận hex, base64, raw, file)
python xor_tool.py single "1b37373331363f78..."
python xor_tool.py multi ct.bin
python xor_tool.py multi --keylen 11 ct.bin

# Lẻ: A1Z26 / Polybius / Tap code / Morse / Bacon / Rail fence
python misc_classical.py a1z26 "8 5 12 12 15"
python misc_classical.py polybius "23 15 31 31 34"
python misc_classical.py morse "... --- ... / .... . .-.. .-.. ---"
python misc_classical.py bacon "ABABA ABBAB BAABB AABAA"
python misc_classical.py railfence_brute "WECRLTEERDSOEEFEAOCAIVDEN"
```

Lưu ý:
- Convention: `caesar_shift(ct, k)` dịch LÙI k = decrypt; encrypt dùng `-k`.
- `vigenere_keyless` giả định plaintext tiếng Anh; chọn keylen = **period nhỏ nhất có IC cao** (bội của period thật cũng IC cao — đừng chọn dài hơn).
- `substitution_hillclimb` cần `english_quadgrams.txt` (đã nằm trong folder; mất thì re-download theo README).
- CyberChef LOCAL phủ: ROT brute, Atbash, Affine, Vigenère có key, XOR, Rail fence, Bifid/Trifid, Morse, Bacon, **Enigma** (op riêng: rotor/reflector/plugboard), Base64/32/58/85 kèm **alphabet custom**. Auto-solve không key → toolkit trên.
- Optional pip: `pip install py-enigma pycipher xortool`.

## CRC của PNG (khi cần sửa header/chiều rộng ảnh)

```python
import struct, zlib
width, height = 1500, 1125
data = (b'IHDR' + struct.pack(">I", width) + struct.pack(">I", height)
        + bytes.fromhex("08 06 00 00 01"))
crc = zlib.crc32(data) & 0xffffffff
print(f"CRC32 = {crc:08X}")
```

## STEGO / MEDIA

| Tool | Lệnh | Khi nào |
|------|------|---------|
| binwalk | `binwalk -Me file` | tách file nhúng, firmware |
| ExifTool | `exiftool img.jpg` | metadata, comment |
| strings | `strings -n 6 file; strings -el file` | ASCII + UTF-16 |
| xxd | `xxd file \| head`; `xxd -r -p hex.txt > out.bin` | hex view / reverse hex |
| steghide | `steghide info -sf a.jpg`; `steghide extract -sf a.jpg -p pass` | JPEG/BMP passphrase |
| stegseek | `stegseek a.jpg rockyou.txt -xf out` | crack passphrase steghide (nhanh) |
| stegsnow | `stegsnow -C -p pass f.txt` | stego whitespace trong text |
| StegSolve | `java -jar StegSolve.jar` | browse LSB plane, data extract |
| pngcheck | `pngcheck -v f.png` | PNG malformed / chunk lạ |
| ZBar | `zbarimg -q qr.png` | đọc QR |
| ImageMagick | `identify -verbose i.png`; `magick compare a.png b.png d.png` | so ảnh, alpha channel |
| FFmpeg | `ffmpeg -i f.mp4 -vn out.wav`; `ffmpeg -i f.mp4 fr/%05d.png` | tách audio/frame |
| SoX | `sox f.wav -n spectrogram -o s.png` | spectrogram (flag trong phổ) |
| sstv | `sstv -d audio.wav -o img.png` | decode SSTV |
| multimon-ng | `multimon-ng -t wav audio.wav` | AFSK/POCSAG/DTMF |
| Sonic Visualiser / Audacity | GUI | phân tích audio thủ công |
| qpdf | `qpdf --decrypt locked.pdf out.pdf`; `qpdf --show-object=N f.pdf` | PDF unlock, xem object |
| mutool | `mutool clean -d in.pdf out.pdf` | giải nén stream PDF ẩn JS |
| peepdf-3 | `peepdf -i file.pdf` | phân tích PDF interactive |
| pdfid / pdf-parser | `pdfid f.pdf`; `pdf-parser -o N f.pdf` | scan `/JS /OpenAction`, dump object |
| AperiSolve | chạy local `/opt/tools/AperiSolve` (docker) | all-in-one stego (chậm, dùng cuối) |

## FORENSIC

| Tool | Lệnh | Khi nào |
|------|------|---------|
| volatility3 | `vol -f mem.raw windows.info` ; `windows.pslist`; `windows.cmdline`; `windows.netscan`; `windows.filescan`; `windows.dumpfiles --virtaddr 0x…` | memory dump Windows |
| Volatility 2 | `vol.py -f mem.raw --profile=Win7SP1x64 pslist` | dump cũ |
| OpenSSH-Session-Key-Recovery | plugin vol3 (WSL) | khôi phục key phiên SSH từ memory |
| The Sleuth Kit | `fls disk.raw`; `icat disk.raw inode > out` | duyệt FS, trích file theo inode |
| foremost | `foremost -i disk.img -o out/` | carve theo signature |
| PhotoRec/TestDisk | `photorec disk.img` | carve interactive, sửa partition |
| bulk_extractor | `bulk_extractor -o out/ dump.raw` | quét email/url/credential trong dump |
| Plaso | `log2timeline.py t.plaso img`; `psort.py -w tl.txt t.plaso` | timeline toàn hệ thống |
| Chainsaw | `chainsaw hunt evtx/ -s sigma/ --mapping sigma_default.yml` | hunt EVTX bằng sigma |
| Hayabusa | `hayabusa -d evtx/` | phân tích EVTX nhanh |
| RegRipper | `rip.pl -r NTUSER.DAT -f all` | parse registry hive |
| ALEAPP/iLEAPP/mac_apt/Hindsight/FQLite | chạy theo `-h` | parse Android/iOS/macOS/Chrome/SQLite |
| ewf-tools / libesedb / pff-tools | `ewfexport img.E01`; `esedbexport -t out ntds.dit`; `pffexport mail.pst` | E01 / ESE (NTDS) / PST |
| qemu-img | `qemu-img convert -O raw d.qcow2 d.raw` | đổi format disk trước parse |
| dwarf2json | `dwarf2json linux --elf vmlinux --systemmap map > json` | tự build symbol vol3 |
| Autopsy / EZ Tools / HxD / DB Browser / DBeaver / Zui | GUI | duyệt evidence trực quan |
| gitleaks | `gitleaks detect --source repo/` | quét secret trong git repo |
| YARA | `yara -r rule.yar dir/` | match pattern |

## Checklist 5 phút đầu phiên làm bài crypto

1. `sage --version` — nếu lỗi, ghi nhớ dùng PARI/GP + crypto-attacks thay.
2. `uv venv && uv pip install pycryptodome gmpy2 sympy pwntools` (env sạch).
3. Check `ls /opt/tools/crypto-attacks/attacks/` + `gp --version`.
4. Factor N theo thang: factordb-python → **Fermat tự viết** (N cân bằng) → RsaCtfTool / PARI/GP / Sage.
5. RsaCtfTool chỉ trên Windows/WSL — đoán đúng heuristic RSA thì chạy ở đó.
