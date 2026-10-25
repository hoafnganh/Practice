# Cheatsheet OpenSSL (đầy đủ)

> Test trên OpenSSL 3.6.3 (WSL). Env WSL: `wsl -e bash -lc "..."`.
> `openssl version -a` — xem version + OPENSSLDIR (chỗ nằm openssl.cnf, CA bundle cert.pem).
> Lệnh nào quên option: `openssl <cmd> -help`. Danh sách subcommand: `openssl list` / `openssl help`.
> 3.x: thuật toán "legacy" (DES, RC2, RC4, seed, blowfish...) bị ẩn → thêm `-provider legacy -provider default` vào cuối lệnh.

## 0. Cú pháp chung + mật khẩu

- Input/output: `-in f` `-out f` (không `-in` = đọc stdin); định dạng `-inform PEM|DER` `-outform PEM|DER` (mặc định PEM).
- `-noout` = KHÔNG in object ra stdout (vẫn in `-text` nếu có).
- Mật khẩu: `-passin` (đọc file/mật khẩu của input), `-passout` (đặt cho output), `-pass` (enc dùng cả 2). Nguồn mật khẩu:
  ```bash
  -passin pass:matkhau        # trực tiếp (dễ leak vào history)
  -passin env:MYVAR           # biến môi trường
  -passin file:f.txt          # dòng ĐẦU TIÊN của file (có cả \n nếu không strip!)
  -passin fd:0  /  -passin stdin   # stdin (enc)
  ```
- Lưu ý `-passout pass:x` khi sinh key: x là mật khẩu mã hóa file key.

## 1. Nhận diện file — bảng PEM headers

File PEM = text: `-----BEGIN X-----` + base64 + `-----END X-----`. Header quyết định loại object:

| Header BEGIN | Là gì |
|---|---|
| `CERTIFICATE` | X.509 cert (DER bọc base64) |
| `TRUSTED CERTIFICATE` | cert kèm trust flags (openssl x509 -trustout) |
| `CERTIFICATE REQUEST` / `NEW CERTIFICATE REQUEST` | CSR PKCS#10 |
| `PRIVATE KEY` | PKCS#8 KHÔNG mã hóa |
| `ENCRYPTED PRIVATE KEY` | PKCS#8 CÓ mã hóa (ASN.1, không có Proc-Type) |
| `RSA PRIVATE KEY` | PKCS#1 RSAPrivateKey (kiểu truyền thống; 3.x genrsa mặc định đã đổi ra PKCS#8!) |
| `RSA PUBLIC KEY` | PKCS#1 RSAPublicKey |
| `PUBLIC KEY` | SPKI SubjectPublicKeyInfo (RSA/EC/DSA gì cũng nhét được) |
| `EC PRIVATE KEY` | SEC1 ECPrivateKey (ecparam -genkey / openssl ec ra kiểu này) |
| `DSA PRIVATE KEY` / `DSA PARAMETERS` | SEC1-style DSA |
| `EC PARAMETERS` | tham số đường cong (thường chỉ 1 dòng OID) |
| `DH PARAMETERS` / `X9.42 DH PARAMETERS` | Diffie-Hellman params |
| `PKCS7` / `PKCS #7 SIGNED DATA` | PKCS#7 (.p7b): chuỗi cert, KHÔNG có key |
| `X509 CRL` | Certificate Revocation List |
| `ENCRYPTED DATA` | CMS EnvelopedData dạng PEM (`cms -encrypt -a`) |
| `SSH2 PUBLIC KEY` | RFC 4716 (ssh-keygen -e) |
| `OPENSSH PRIVATE KEY` | format mới ssh-keygen (bcrypt KDF) — **openssl KHÔNG đọc được** |
| `SSH2 ENCRYPTED PRIVATE KEY` | ssh.com format |
| `SSL SESSION PARAMETERS` | session cache |

Key PEM truyền thống CÓ mã hóa thì có 2 dòng header trong base64:
```
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-256-CBC,<IV hex không dấu :>
```

Bảng đuôi file (đuôi KHÔNG quyết định nội dung, `file`/`head -1` mới chuẩn):

| Đuôi | Thường là |
|---|---|
| `.pem` | text base64, 1 file có thể chứa NHIỀU object (openssl thường chỉ đọc object ĐẦU TIÊN) |
| `.der` `.crt` `.cer` | DER nhị phân (Windows hay dùng .cer cho DER) |
| `.key` | private key (PEM hoặc DER) |
| `.csr` | PKCS#10 request |
| `.p12` `.pfx` | PKCS#12 (cert + key + chain, có mật khẩu) |
| `.p7b` `.p7c` | PKCS#7, chỉ cert |
| `.crl` | CRL |
| `.pub` | public key (PEM/SPKI hoặc OpenSSH 1 dòng) |
| `.jks` `.keystore` | Java keystore — openssl KHÔNG đọc; `keytool -list -keystore f.jks` (magic FE ED FE ED; MAGIC = Java-PKCS12) |
| `.pvk` | Windows PVK — openssl không đọc trực tiếp (pvk2pfx / openssl 1.0.2-era tool) |
| `.sst` | MS serialized cert store (`certutil`) |

Phân biệt nhanh:
```bash
file f; head -c 32 f | xxd
# PEM  : ASCII "-----BEGIN"
# DER  : 30 82 xx xx  (ASN.1 SEQUENCE, độ dài long-form) — mọi key/cert/p12 đều bắt đầu 30
# p12  : 30 82 và "PKCS7 Encrypted data" khi asn1parse; thử ngay pkcs12 -info
# enc  : "Salted__" = 53 61 6c 74 65 64 5f 5f rồi 8 byte salt
```

## 2. asn1parse — soi mọi file key/cert/p7 (debug số 1)

```bash
openssl asn1parse -in f.pem                     # PEM; thêm -inform der nếu binary
openssl asn1parse -in f -i                      # -i thụt dòng theo depth
openssl asn1parse -in f -i -dump                # -dump in raw bytes của từng field
openssl asn1parse -in f -i -strparse <offset>   # đào vào object con tại offset (offset cột 1)
openssl asn1parse -in f -i -offset N -length M  # cắt vùng xem
```
Đọc output: `offset:d=depth hl=header-len l=length cons|prim: TYPE :value`
- `INTEGER :0398...` = số (serial/modulus...), `OCTET STRING [HEX DUMP]` = raw, `OBJECT :sha256WithRSAEncryption` = OID.
- PEM hỏng (đề "lost 1 bit"): decode base64 bằng python rồi `asn1parse -inform der` tìm tag lỗi ("wrong tag").

## 3. Keys — sinh / xem / chuyển đổi

```bash
# --- Sinh ---
openssl genrsa -out k.pem 2048                       # 3.x: ra PKCS#8 (BEGIN PRIVATE KEY)
openssl genrsa -out k.pem -aes256 -passout pass:x 2048   # có mã hóa; -3 = e=3, mặc định -f4 (65537)
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 \
        -pkeyopt rsa_keygen_pubexp:65537 -out k.pem       # kiểu hiện đại, cũng ra PKCS#8
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out ec.pem
openssl ecparam -name prime256v1 -genkey -out ec.pem      # ra SEC1 (BEGIN EC PRIVATE KEY)
openssl ecparam -list_curves | grep -i prime
openssl dhparam -out dh.pem 2048                     # chậm; dhparam cũ thường để sẵn trong đề
openssl prime -generate -bits 64 -safe               # sinh số nguyên tố (an toàn thì -safe)

# --- Xem (in n,e,d,p,q,dp,dq,qinv — copy thẳng vào python) ---
openssl rsa -in k.pem -text -noout                   # Private-Key: (2048 bit, 2 primes), modulus: xx:xx:xx...
openssl rsa -in k.pem -noout -modulus                # Modulus=D6DD... (HOA, không ':', có thể leading 00)
openssl rsa -in k.pem -check -noout                  # "RSA key ok"
openssl rsa -pubin -in pub.pem -text -noout          # public key SPKI: Public-Key: (bit) + Modulus + Exponent
openssl pkey -in k.pem -text -noout                  # tổng quát RSA/EC/DSA đều được (3.x khuyến dùng)
openssl pkey -in k.pem -text_pub -noout              # chỉ phần public
openssl ec -in ec.pem -text -noout                   # EC: ASN1 OID: prime256v1, pub, priv
openssl rsa -in k.pem -noout -text | grep -A2 prime1 # p, q

# --- Convert (bảng dưới) ---
openssl rsa -in k.pem -pubout -out spki.pem          # private → BEGIN PUBLIC KEY (SPKI)
openssl rsa -in k.pem -RSAPublicKey_out -out p1.pub  # private → BEGIN RSA PUBLIC KEY (PKCS#1)
openssl rsa -pubin -in spki.pem -RSAPublicKey_out -out p1.pub   # SPKI → PKCS#1 pub
openssl rsa -in p1.pub -RSAPublicKey_in -pubin -out spki.pem    # PKCS#1 pub → SPKI
openssl pkcs8 -topk8 -in k1.pem -nocrypt -out k8.pem # PKCS#1/SEC1 → PKCS#8 (-passout để mã hóa)
openssl rsa -in k8.pem -out k1.pem                   # PKCS#8 → PKCS#1 truyền thống
openssl pkey -in k.pem -aes256 -passout pass:x -out ken.pem     # đặt/thay pass key
```

| Từ → Đến | Header đích | Lệnh |
|---|---|---|
| PKCS#1 priv → PKCS#8 | `PRIVATE KEY` | `pkcs8 -topk8 -nocrypt` (hoặc bất kỳ lệnh `rsa/pkey -out`) |
| PKCS#8 → PKCS#1 priv | `RSA PRIVATE KEY` | `openssl rsa -in k8.pem -out k1.pem` |
| priv → SPKI pub | `PUBLIC KEY` | `rsa -pubout` / `pkey -pubout` |
| SPKI ↔ PKCS#1 pub | `RSA PUBLIC KEY` | `-RSAPublicKey_out` / `-RSAPublicKey_in` |
| OpenSSH pub → PEM | `PUBLIC KEY` | `ssh-keygen -f id_rsa.pub -e -m PKCS8` |
| OpenSSH priv (OPENSSH) → PEM | `RSA PRIVATE KEY` | `ssh-keygen -p -m PEM -f id_rsa` (đổi format tại chỗ) |

Lưu ý:
- 3.x: `genrsa` mặc định ra **PKCS#8** (`BEGIN PRIVATE KEY`) — 1.1.1 trở xuống ra `BEGIN RSA PRIVATE KEY`. Cả hai openssl đều đọc được bằng `rsa` lẫn `pkey`, đừng judging theo header.
- `rsa` đọc được cả PKCS#8 lẫn PKCS#1; phân biệt bằng header khi phải decode tay trong python (PKCS#8 có thêm 1 SEQUENCE version 0 + AlgorithmIdentifier bọc ngoài).
- Input RSA nhỏ/textbook (m < n) thì pkeyutl KHÔNG dùng được (mục 8) — decode tay: base64 → ASN.1 → n,e.

## 4. x509 — certificate

```bash
openssl x509 -in c.pem -text -noout                  # xem tất cả: serial, issuer, subject, validity, SAN, OID sig
openssl x509 -in c.pem -noout -subject -issuer -serial -dates -fingerprint -sha256
openssl x509 -in c.pem -noout -ext subjectAltName    # 1.1.0+: chỉ định extension (x509_extensions tên)
openssl x509 -in c.pem -noout -purpose               # check usage được không
openssl x509 -in c.pem -pubkey -noout > pub.pem      # TRÍCH public key từ cert (rất hay gặp)
openssl x509 -in c.pem -noout -modulus               # Modulus=... (chỉ RSA) — so với key
openssl x509 -in c.pem -outform der -out c.der       # PEM → DER
openssl x509 -inform der -in c.cer -outform pem      # DER → PEM
openssl x509 -in c.pem -checkend 86400               # sắp hết hạn trong 24h không
openssl x509 -in c.pem -noout -subject -nameopt RFC2253   # format subject chuẩn
openssl verify -CAfile ca.pem -untrusted intermediate.pem leaf.pem   # chuỗi verify
# Lấy cert từ server đang chạy:
openssl s_client -connect host:443 -showcerts </dev/null 2>/dev/null > full.txt
awk '/BEGIN CERT/,/END CERT/' full.txt > chain.pem   # tách toàn bộ chain (object đầu = leaf)
```
- So khớp cert ↔ key (cert có đúng là của key này không): so `-modulus` của `x509` với `rsa` — hoặc gọn hơn:
  ```bash
  openssl x509 -in c.pem -pubkey -noout | openssl md5
  openssl pkey -in k.pem -pubout | openssl md5        # hai hash bằng nhau = khớp
  ```
- Tách chuỗi cert trong 1 file PEM nhiều cert: `openssl crl2pkcs7 -nocrl -certfile chain.pem | openssl pkcs7 -print_certs -out certs.pem`.
- CTF hay gặp: n của đề = modulus trong cert (làm việc với cert công khai); extract `pubkey` rồi đẩy n,e vào python; hoặc so modulus phát hiện key/cert mismatch.

## 5. req — CSR (PKCS#10)

```bash
# Sinh key + CSR một phát (-nodes = KHÔNG mã hóa key — "No DES"):
openssl req -new -newkey rsa:2048 -nodes -keyout k.pem -out r.csr -subj "/C=VN/O=x/CN=y"
openssl req -new -newkey ec -pkeyopt ec_paramgen_curve:P-256 -nodes -keyout k.pem -out r.csr -subj "/CN=y"
# Self-signed cert (CTF hay cần cert local):
openssl req -x509 -newkey rsa:2048 -nodes -keyout k.pem -out c.pem -days 365 \
        -subj "/CN=localhost" -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"
openssl req -in r.csr -noout -text                   # xem CSR (subject + pubkey)
openssl req -in r.csr -noout -verify                 # check chữ ký CSR
openssl req -in r.csr -pubkey -noout                 # trích pubkey từ CSR
```

## 6. pkcs12 / pkcs7 / crl

```bash
openssl pkcs12 -in f.p12 -nodes -passin pass:x -out all.pem   # đổ ra PEM: key + cert + chain
openssl pkcs12 -in f.p12 -passin pass:x -nocerts -nodes -out key.pem   # chỉ key
openssl pkcs12 -in f.p12 -passin pass:x -nokeys -clcerts -out cert.pem # chỉ cert user (-cacerts = CA)
openssl pkcs12 -info -in f.p12 -passin pass:x                  # xem cấu trúc (MAC, PBES2, thuật toán)
openssl pkcs12 -legacy -in old.p12 -nodes -passin pass:x ...   # p12 tạo bởi openssl ≤1.1.1 (RC2/3DES)
openssl pkcs12 -export -in c.pem -inkey k.pem -out f.p12 -name alias -certfile chain.pem -passout pass:x
openssl pkcs7 -in p7.pem -print_certs -out certs.pem           # .p7b → các cert rời
openssl pkcs7 -in p7.pem -text -noout                          # xem PKCS#7
openssl crl -in crl.pem -text -noout                           # xem CRL
openssl crl -inform der -in f.crl -out crl.pem                 # DER → PEM
```
- 3.x đổi mặc định pkcs12: PBES2/PBKDF2/AES-256-CBC + MAC sha256. File p12 cũ mở bằng 3.x mà lỗi "unsupported" → thêm `-legacy`; ngược lại p12 tạo bằng 3.x mở trên tool cũ có thể fail.
- p12 không biết pass: thử pass rỗng `-passin pass:`; hoặc `pkcs12 -info -nokeys -nocerts` đôi khi chỉ cần MAC pass.

## 7. enc — mã hóa đối xứng

```bash
openssl enc -aes-256-cbc -salt -pbkdf2 -iter 10000 -in f -out f.enc -pass pass:x
openssl enc -aes-256-cbc -d -in f.enc -out f -pass pass:x          # -d = decrypt
openssl enc -aes-256-cbc -d -K <HEX key> -iv <HEX iv> -in f.enc -out f   # raw key, KHÔNG KDF
openssl enc -aes-128-ecb -K <HEX> -in ...                          # ECB không cần -iv
echo -n data | openssl enc -aes-256-cbc -K ... -iv ... -a          # -a = base64 in/out
openssl list -cipher-algorithms                                    # danh sách (3.x; 1.x: openssl enc -ciphers)
```
- `-K`/`-iv` (HOA) = raw hex: AES-256 key = 64 hex chars, iv = 32 hex chars. `-k` (thường) = password, bật KDF + salt (deprecated cú pháp, vẫn hoạt động).
- Cấu trúc file output khi có salt: `"Salted__"` (8 byte ASCII) + salt (8 byte) + ciphertext. Không có 16 byte này = file thuần (encrypt bằng -K/-iv hoặc -nosalt hoặc tool khác) — **không dùng `enc -d` để decrypt được**, phải raw.
- **"bad decrypt" → đúng key/mode sai KDF.** Thứ tự thử khi đề cho file có `Salted__` + password, không nói version:
  1. `enc -d ... -pass pass:x` (EVP_BytesToKey, SHA-256 — mặc định openssl ≥ 1.1.0)
  2. thêm `-md md5` (file tạo bởi openssl < 1.1.0 — CỰC hay gặp trong CTF)
  3. thêm `-pbkdf2` (+ `-iter N` nếu đề nói)
  4. `-nosalt` nếu không có `Salted__`
- Padding mặc định PKCS#7; `-nopad` nếu đề tự padding.
- `-a` đếm base64: khi decrypt có `-a` mới nhận base64 input.

## 8. dgst — hash / HMAC / ký số

```bash
openssl dgst -sha256 f                       # in "SHA2-256(f)= hex..." ; -md5/-sha1/-sha512/-sha3-256...
openssl dgst -sha256 -binary f | xxd         # -binary raw thay vì -hex (mặc định hex)
openssl dgst -sha256 -hmac "key" f           # HMAC key string; HMAC hexkey: dùng `openssl mac`
openssl mac -digest SHA256 -macopt hexkey:0011.. HMAC -in f   # 3.x
openssl dgst -sha256 -sign k.pem -out sig.bin f        # RSA/EC sign (hash + DigestInfo rồi RSA)
openssl dgst -sha256 -verify pub.pem -signature sig.bin f   # → "Verified OK" / "Verification Failure"
openssl dgst -sha256 -prverify k.pem -signature sig.bin f   # verify bằng PRIVATE key
```
- Khác `pkeyutl -sign`: dgst tự hash + bọc DigestInfo; `pkeyutl -sign` (padding pkcs1 mặc định) ký raw data — với RSA phải tự chuẩn bị DigestInfo, còn `-raw`/`none` thì chính là textbook m^d mod n.
- Verify RSA textbook (đề cho sig nhỏ): decode sig = sig^e mod n bằng python rồi so padding; openssl `pkeyutl -verify` đòi đúng DigestInfo nên hay bị "Signature Verification Failure" dù sig đúng — decode tay khi nghi ngờ.

## 9. pkeyutl / rsautl — RSA/EC operation

```bash
openssl pkeyutl -encrypt -inkey spki.pem -pubin -in m.bin -out c.bin    # mặc định PKCS#1 v1.5
openssl pkeyutl -decrypt -inkey k.pem -in c.bin -out m.bin
openssl pkeyutl -encrypt -inkey pub.pem -pubin -pkeyopt rsa_padding_mode:oaep \
        -pkeyopt rsa_oaep_md:sha256 -pkeyopt rsa_mgf1_md:sha256 -in m.bin
openssl pkeyutl -sign -inkey k.pem -in f -out sig -pkeyopt rsa_padding_mode:pss \
        -pkeyopt rsa_pss_saltlen:-1                                     # pss
openssl pkeyutl -verify -inkey pub.pem -pubin -sigfile sig -in f
openssl pkeyutl -derive -inkey k.pem -peerkey pub.pem -out shared.bin   # ECDH/DH: shared secret
```
- Padding modes: `pkcs1` (mặc định encrypt/decrypt + sign), `oaep` (chỉ encrypt/decrypt), `pss` (chỉ sign), `none` (= textbook).
- **Gotcha lớn: textbook RSA với m nhỏ KHÔNG làm được bằng pkeyutl `-raw`/`rsa_padding_mode:none`** — encrypt input nhỏ hơn modulus → `RSA_padding_add_none:data too small for key size`; decrypt kết quả có leading-zero cũng "data too small". Đề RSA textbook (n,e,c) → **dùng python `pow(c,d,n)`**, openssl chỉ để extract tham số.
- `openssl rsautl` = alias cũ của pkeyutl (deprecated nhưng còn), có thêm `-raw` cổ điển.
- Encrypt ra output luôn dài bằng modulus (đủ padding); nếu file ciphertext dài đúng 128/256 byte = RSA 1024/2048-bit. CT ngắn hơn = không padding = textbook.
- Decrypt PKCS#1 v1.5: plaintext bắt đầu `00 02 <nonzero random> 00 <msg>` — cắt sau byte 0x00 đầu tiên (gotcha từng gặp: msg nhị phân chứa 0x00 thì cắt bằng logic padding, đừng rstrip).

## 10. passwd / rand / prime / lẻ

```bash
openssl passwd -6 -salt saithay matkhau      # $6$saithay$... crypt(3) SHA-512 (shadow linux)
openssl passwd -1 matkhau                    # $1$ MD5 crypt; -5 SHA-256; -apr1 Apache MD5
openssl passwd -salt xyz -6 -verify hash ... # so pass với hash có sẵn (copy salt từ hash)
openssl rand -hex 32                         # 32 byte → 64 hex chars; -base64 32
openssl prime 104729                         # input là DECIMAL → "19919 (104729) is prime" (hex)(dec)
openssl prime -hex 1F                        # -hex: input lẫn output đều hex
openssl prime -checks 20 104729              # tăng số vòng Miller-Rabin
```
- Lưu ý prime: KHÔNG có `-hex` thì nhập decimal; output luôn dạng `<hex> (<số vừa nhập>)`. Nhập chuỗi hex kiểu `1C` khi không -hex → **im lặng, exit 0, không báo lỗi** (3.6.3) — tưởng is prime được là nhầm.
- `openssl speed rsa2048` benchmark; `openssl storeutl certs.pem` liệt kê TẤT CẢ object trong file PEM (x509 chỉ đọc cái đầu).

## 11. s_client / s_server — TLS

```bash
openssl s_client -connect host:443 -servername host          # SNI;Enter rồi gõ HTTP thủ công
openssl s_client -connect host:443 -brief                    # output gọn: version, cipher, cert DN
openssl s_client -connect host:443 -showcerts                # in TẤT CẢ cert server gửi (lấy chain)
openssl s_client -connect host:25 -starttls smtp             # smtp/pop3/imap/ftp/http(post)/xmpp/mysql/postgres...
openssl s_client -connect host:443 -tls1_2 -cipher ECDHE-RSA-AES128-GCM-SHA256   # ép version/cipher
openssl s_client -connect host:443 -crlf -quiet              # -crlf đổi LF→CRLF (HTTP/SMTP thủ công), -quiet + -ign_eof giữ session
openssl s_client -connect host:443 -CAfile ca.pem            # verify qua CA chỉ định; -verify_return_error
openssl s_server -accept 4433 -cert c.pem -key k.pem -www    # server test (GET / trả trang trạng thái)
```
- CTF: dịch vụ HTTPS/STARTTLS → s_client là terminal tương tác; kết hợp `| openssl x509 -text -noout` đọc cert ngay. Cert dạng DER trần (port custom trả 0x30 0x82) → `openssl x509 -inform der -text -noout -in <(nc host port)`.

## 12. cms / smime — S/MIME

```bash
openssl cms -encrypt -in msg.txt -recip cert.pem -aes256 -to a@b -from c@d -subject hi -out msg.cms
openssl cms -decrypt -in msg.cms -recip cert.pem -inkey k.pem -out msg.txt
openssl cms -sign -in msg.txt -signer cert.pem -inkey k.pem -out msg.sig
openssl cms -verify -in msg.sig -CAfile ca.pem -out msg.txt
openssl cms -encrypt -in msg.txt -recip cert.pem -aes256 -outform DER -out msg.der   # nhị phân
# smime = cms bản cũ, cú pháp gần như y hệt; CMS dạng PEM: cms -encrypt ... -outform PEM
```

## 13. Bảng lỗi thường gặp

| Lỗi | Nguyên nhân + xử lý |
|---|---|
| `no start line` / `Could not find private key` | Đọc DER bằng parser PEM → thêm `-inform der`; hoặc header PEM sai/lệch dòng; hoặc file là p12 (`pkcs12 -in`) |
| `unable to load Private Key` | Sai mật khẩu (thiếu `-passin pass:`) hoặc key lẫn giữa PKCS#8/RSA/EC |
| `bad decrypt` (enc) | Sai key/iv/mode hoặc sai KDF → mục 7 (thử `-md md5`, `-pbkdf2`, `-nosalt`) |
| `wrong tag` (asn1parse) | Binary hỏng/đề phá 1 bit — tìm offset bị lỗi, brute flip |
| `data too small for key size` (pkeyutl none) | Textbook RSA m nhỏ → giải bằng python, không dùng openssl |
| `unsupported` (3.x) | Thuật toán legacy → thêm `-provider legacy -provider default` |
| `unable to get local issuer certificate` | verify thiếu chain → `-CAfile` / `-untrusted` |
| `Error reading password from BIO` | Thiếu nguồn mật khẩu; hoặc `-passin file:f` có `\n` cuối → dùng `pass:` |
| `header too long` / junk output | Decrypt nhầm định dạng (đang `-d` file không phải output của enc) |
| p12 mở không được | Sai pass; hoặc thiếu `-legacy` (p12 RC2/3DES cũ) |

## 14. Checklist 2 phút khi gặp file crypto trong đề

1. `file f && head -c 32 f | xxd` → PEM text? DER `30 82`? `Salted__`? p12 (30 82 + thử `pkcs12 -info -passin pass:`)?
2. PEM key → `openssl pkey -in f -text -noout` (n,e,d,p,q → python); PEM cert → `openssl x509 -text -noout`, lấy `-pubkey`, so `-modulus` với key (đề hay giấu mismatch).
3. Key bit nhỏ bất thường (512–1024) → factor ngay (factordb/Fermat) trước khi nghĩ sâu.
4. File có `Salted__` → `enc -d` theo 4 bước KDF mục 7.
5. `.sig` RSA: thử `dgst -verify`; fail → decode textbook bằng python (sig^e mod n, soi padding `00 01 FF..FF 00`).
6. File lạ/base64 rác: `openssl asn1parse -inform der -i -dump` soi; PEM hỏng 1 bit → python decode + brute flip quanh offset lỗi.
7. Server HTTPS/STARTTLS → `s_client -connect -showcerts`, bắt chain, extract cert để lấy n.
