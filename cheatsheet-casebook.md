# Casebook — Sổ tay case study

Tập hợp các "dạng đề" nằm ngoài hai mảng chính (symmetric thuần và RSA thuần): encoding lạ, cipher tự chế, đa lớp forensics/stego, RE nhẹ. Mỗi case ghi theo khuôn **Nhận diện → Cách giải → Bẫy**, mục đích là khi gặp lại đúng "mùi" thì nhớ ra đường đi ngay.

Nguyên tắc chung khi gặp đề lai (crypto + forensics + RE): **xác định lớp ngoài cùng trước, bóc từng lớp một, mỗi lớp dùng đúng tool chuyên dụng** — đừng cố viết script tổng từ đầu.

## 1. Encoding & mật mã cổ điển

### 1.1 Base64 — ký tự không thể xuất hiện

- **Nhận diện:** câu hỏi dạng "ký tự base64 nào KHÔNG THỂ bao giờ xuất hiện trong output" (với một tập input ràng buộc, ví dụ chỉ chữ cái).
- **Cách giải:** Base64 gom 3 byte → 4 ký tự. Với input chỉ gồm A–Z/a–z (byte luôn bắt đầu `01…`), duyệt toàn bộ chuỗi A-Za-z độ dài 1–3 (52 + 52² + 52³ ≈ 143.000) là phủ mọi vị trí output có thể; phần bù của tập xuất hiện (trừ `=`) chính là đáp án. Ví dụ classic với input thuần chữ cái: `+` và `/` (index 62/63 cần bit đầu = 1), `f` (cần byte 0x7C–0x7F), `7` (low6 = 111011 > max 111010) → `+/7f` → thường đề yêu cầu SHA1 của chuỗi đó.
- **Bẫy:** nhớ trừ `=`; tính SHA1 của chuỗi **xếp theo ASCII tăng dần** đúng format đề.

### 1.2 Chuỗi chỉ có `.` và `-` nhóm 5 — Baudot/ITA2

- **Nhận diện:** text toàn `.`/`-`, hint "telegraph/Morse" nhưng KHÔNG có separator Morse và nhịp chia đều theo nhóm 5 → Morse là mồi nhử, thật ra là mã khối 5-bit ITA2/Baudot.
- **Cách giải:** lọc chỉ giữ `.`/`-` → chia nhóm 5 bit → thử 4 biến thể {`.` = 1 hay 0} × {đảo bit trong nhóm hay không} → lookup bảng ITA2 letters, chọn biến thể cho text sạch nhất. Kết quả có thể là các từ đánh vần kiểu NATO/Thụy Điển (Adam=A, Bertil=B, Caesar=C…) → lấy chữ cái đầu mỗi từ ghép lại. Tool sẵn: `classical/baudot.py`.
- **Bẫy:** token điều khiển LTRS/FIGS trông như từ thật nhưng phải loại trước khi ghép chữ đầu.

### 1.3 Vigenère giấu trong các mảnh ảnh cắt

- **Nhận diện:** ảnh JPEG + `binwalk` thấy ZIP appended + nhiều mảnh ảnh cắt từ cùng một bức tranh → stego đa lớp; text thu được có pattern `XXXX_XXXX{...}` đặc trưng Vigenère.
- **Cách giải:** `strings` từng mảnh ra 1 đoạn; **thứ tự mảnh phải tự ghép lại bức tranh nguyên vẹn** (không theo filename). Nối đúng thứ tự thành ciphertext; decrypt Vigenère (chỉ áp chữ cái, giữ nguyên ký tự khác). Key có thể suy ngược từ crib = prefix format flag: dịch 3 chữ đầu ra shift lần lượt → key lặp.
- **Bẫy:** ghép sai thứ tự mảnh = ciphertext vô nghĩa, tưởng sai hướng mã; ZIP thường có password (tìm trong metadata ảnh hoặc hint đề).

### 1.4 Vigenère key = thập phân tuần hoàn của phân số

- **Nhận diện:** plaintext English bình thường rồi đột ngột "gãy" KeyStream-like; key stream dài ~16+ nhưng lặp; các con số "đẹp" xuất hiện trong hint (phân số kiểu 1/17).
- **Cách giải:** key = **chu kỳ thập phân** (repetend) của phân số, thường bị CẮT ngắn (1/17 = 0.0588235294117647… → chu kỳ 0588235294117647, đề có thể chỉ lấy 6 chữ số "058823" lặp). Nếu đã biết dạng phân số, sinh repetend đầy đủ rồi brute các độ dài cắt.
- **Bẫy:** repetend ĐẦY ĐỦ có thể fail dù đúng hướng — đề đã cắt ngắn; luôn brute biến thể cắt. Digit-key bị một số toolkit bỏ im lặng → chuyển sang chữ (tra bảng A=0..9=I) nếu tool bắt buộc.

### 1.5 OTP tự nhúng key

- **Nhận diện:** ciphertext dài bất thường kèm cặp (cipher, plaintext) mẫu để đối chiếu → cấu trúc nhúng key vào chính ciphertext: `cipher = [base64(pt) ⊕ key] || [key]`, hai nửa bằng nhau.
- **Cách giải:** XOR byte-wise hai nửa → thu lại chuỗi base64 → decode:
  ```python
  h = len(c) // 2
  b64 = bytes(a ^ b for a, b in zip(c[:h], c[h:]))
  print(base64.b64decode(b64))
  ```
- **Bẫy:** XOR thực hiện trên byte của chuỗi BASE64, không phải plaintext thô; verify công thức trên cặp mẫu trước khi chạy bản thật.

### 1.6 Stream cipher tự chế `c_i = m_i + 2·m_{i+1}`

- **Nhận diện:** cipher tự chế mà mỗi byte mã hóa phụ thuộc 2 byte plaintext liên tiếp (tuyến tính theo cặp).
- **Cách giải:** giải **NGƯỢC từ ký tự cuối biết trước** (`}` của format flag) — mỗi bước chỉ có 1 nghiệm:
  ```python
  out = ['}']
  for c in cipher[::-1]:
      out.append(chr((ord(c) - 2*ord(out[-1])) & 0xFF))
  flag = "".join(reversed(out))
  ```
- **Bẫy:** giải từ ĐẦU bất định vì `2b mod 256` có 2 nghiệm (b và b+128); plaintext thường có prefix random (bỏ N byte đầu theo đề).

### 1.7 Enigma + gói IPsec/ESP

- **Nhận diện:** pcap có gói ESP (IPsec) + chuỗi chữ hoa A–Z vô nghĩa kèm dòng cấu hình rotor → giải mã ESP trước, Enigma sau.
- **Cách giải:** sửa magic file giả (ZIP giả header MS-DOS, pcap bị phá `PK`/`\xd4\xc3`…) → Wireshark decrypt ESP bằng key tìm được → HTML chứa ciphertext + cấu hình Enigma (reflector, wheel, vị trí, plugboard) → nhập đúng vào simulator (Enigma đối xứng: encrypt = decrypt). Việc của solver là NHẬN RA và nhập đúng cấu hình, không phải crack.
- **Bẫy:** kiểm tra magic byte mọi file trước khi tin extension; EXIF ảnh chứa pass ZIP.

## 2. Symmetric tự chế / implement sai

### 2.1 ChaCha — nonce 8 byte vs 12 byte

- **Nhận diện:** hint vui kiểu "chacha... 20 years old" + đề cho ĐỦ key 256-bit + nonce + ciphertext → không phải tấn công, chỉ cần implement cipher ĐÚNG.
- **Cách giải:** state 16 word = 4 hằng số "expand 32-byte k" (`0x61707865, 0x3320646e, 0x79622d32, 0x6b206574`) + key 8 word + counter + nonce. 20 vòng = 10 double round (column + diagonal), mỗi vòng 4 QUARTERROUND (XOR, cộng mod 2³², rotl 16/12/8/7); cuối CỘNG feed-forward state gốc rồi XOR với ciphertext.
- **Bẫy:** nonce 8 byte = ChaCha gốc (DJB), KHÔNG phải RFC 7539 (12 byte) — thư viện mặc định 12 byte phải chỉnh; ciphertext ngắn hơn 1 block 64 byte thì khỏi tăng counter.

### 2.2 CBC — thiếu 2 byte key, suy IV

- **Nhận diện:** CBC + cho trước plaintext nguyên vẹn ≥ 2 block + biết prefix key + block ciphertext CUỐI nguyên vẹn → giải ngược CBC để vừa validate key vừa suy IV.
- **Cách giải:** quan hệ `C_(i−1) = D_k(C_i) ⊕ P_i` và `IV = D_k(C_0) ⊕ P_0`. Brute 2 byte thiếu (65.536 candidate), **đặt IV = 0 khi brute** (IV chỉ tham gia XOR, không ảnh hưởng check), check các byte đã biết của block 1 suy ngược.
- **Bẫy:** XOR đúng chiều `decrypt ⊕ plain` chứ không phải encrypt; chỉ check offset đã biết nên có thể còn candidate sót — dùng block 2 kiểm thêm.

### 2.3 Malware exfil — encoding 2 byte/1 byte + XOR/ADD word key

- **Nhận diện:** dữ liệu exfil "như base64" nhưng dài GẤP ĐÔI (2 byte cho 1 byte plaintext) + binary có mảng key ~40 byte nhúng.
- **Cách giải:** thường là encoding 2-byte-có-random mà **mỗi byte output leak đúng 4 bit**: `m[i] = (src[2i+1] & 0xf) | ((src[2i] & 0xf) << 4)` → khỏi cần brute seed. Sau đó giải ngược layer mã hóa tự chế (mỗi block 8 byte: word 32-bit đầu XOR key, word thứ hai CỘNG key; key chu kỳ 10 word) → phục hồi file. Định danh file thật (XLSX không phải XLS — header khác nhau!) trước khi viết đường brute.
- **Bẫy:** định danh sai header (XLS vs XLSX) khiến đường brute vô dụng; phân tích cấu trúc leak-bit trước khi brute seed 32-bit.

### 2.4 Feistel round function = XOR

- **Nhận diện:** cho cặp plaintext–ciphertext + cipher "Feistel N vòng" mà round function yếu (XOR/ADD) và số vòng không nói trước → khai triển đại số tìm tính TUẦN HOÀN, không cần recover từng round key.
- **Cách giải:** với F = XOR round key deterministic (key tái dùng giữa các message), khai triển cho thấy mỗi nửa ciphertext chỉ thuộc tập hữu hạn {pt1, pt2, pt1⊕pt2} ⊕ (tổng XOR nào đó của round keys), trạng thái lặp chu kỳ ngắn theo số vòng. Brute tổ hợp XOR của các ứng viên plaintext × ứng viên ciphertext × ứng viên round-key-XOR → lọc kết quả printable.
- **Bẫy:** đừng đi hướng recover round key — đề không cho đủ dữ liệu; nghĩ "tập giá trị có thể" thay vì "giá trị đúng".

### 2.5 CBC cut & paste (craft block thành admin)

- **Nhận diện:** 2 cookies/tickets mã hóa AES-CBC với plaintext gần giống nhau (challenge và ticket), login cho kiểm soát trường username.
- **Cách giải:** chọn username có độ dài khớp để block hóa đẹp: `'X'*k + '{"user":"x","groups":["admin"]}'`; lấy cookie challenge, **cắt block đầu (IV)** đi, phần còn lại decrypt thành ticket admin hợp lệ (server tin plaintext ticket).
- **Bẫy:** cần biết chính xác format JSON server kiểm; độ dài username phải đẩy JSON payload lên đúng biên block.

## 3. RSA & số học

### 3.1 Modulus bị lật 1 bit

- **Nhận diện:** hint "lost 1 bit" + factor n ra nhiều hơn 2 thừa số (không phải semiprime) → đề đã lật 1 bit trong n; ciphertext mã hóa bằng n THẬT.
- **Cách giải:** brute 256 vị trí bit, candidate đúng = cái factor ra đúng 2 prime. **Mẹo parity:** modulus RSA thật luôn LẺ → n trong đề mà chẵn thì thử `n | 1` (set bit cuối) NGAY trước khi brute 256 vị trí.
- **Bẫy:** decrypt textbook không padding (có PKCS#1 v1.5 thì cắt sau byte 0x00); với n ~256 bit thì factordb/sage factor gần như instant — đừng tự viết factor.

### 3.2 Key RSA lộ công khai / default

- **Nhận diện:** thấy `rsautl -encrypt` + hint trỏ tool/project nổi tiếng (keystore, snakeoil CA, packet analyzer, Python, Debian RNG) → đừng "phá RSA", đi tìm **private key công khai** tương ứng.
- **Cách giải (chuỗi lồng nhau điển hình):** zip password = default password nổi tiếng của Java keystore (dùng lại mọi level); key "snakeoil CA" trong repo apache-mod-ssl; key `rsa-p-lt-q.key` trong repo Wireshark (chọn theo điều kiện p<q); `Lib/test/ssl_key.pem` trong repo CPython; level cuối = bộ key Debian-OpenSSL weak PRNG (tarball nổi tiếng) — phải thử hàng nghìn key, bỏ lỗi bằng `2>/dev/null` rồi `sort -u` kết quả.
- **Bẫy:** thứ tự và điều kiện chọn key (p<q) nằm trong hint; tarball Debian key phải lấy bản chuẩn theo năm bản ghi trong đề.

### 3.3 Modulus khổng lồ cân bằng → Fermat

- **Nhận diện:** modulus RSA khổ LỚN bất thường (8192-bit) mà factordb không có → thử **Fermat** (p, q gần nhau) TRƯỚC khi nghĩ tới attack cấu trúc phức tạp. Thường đề sinh `q = next_prime(p)`.
- **Cách giải:** Fermat từ `a = ceil(√N)`, N = a²−b² hội tụ sau rất ít bước (p−q chỉ khác vài nghìn). Xem code 5 dòng trong `cheatsheet-asymmetric.md` mục 2.2. Sau đó `d = e⁻¹ mod lcm(p−1, q−1)`; `pow(c, d, N)` → hex → ASCII.
- **Bẫy:** PARI/GP `factorint` KHÔNG có bước Fermat đầu tiên — với N cân bằng 8192-bit nó treo vĩnh viễn; phải chạy Fermat python riêng.

### 3.4 Nhiều modulus cấp phát chung prime

- **Nhận diện:** nhiều public key (PEM) phát cho nhiều "thiết bị" + entropy nguồn sinh prime kém.
- **Cách giải:** batch GCD từng cặp; gcd ≠ 1 → p → q = n/p → decrypt cả hai key. Code trong `cheatsheet-asymmetric.md` mục 3.
- **Bẫy:** một số cặp chia nhau hơn 1 prime → gcd composite; kiểm `bit_length`/`isprime` trước khi dùng.

### 3.5 md5 từ hexdump lines

- **Nhận diện:** mỗi dòng của file (hexdump text) được coi như 1 "hash MD5" để tra DB ngược → brute từng dòng qua dịch vụ băm ngược cục bộ.
- **Cách giải:** tách dòng → query reverse-hash (rockyou cục bộ) → ghép kết quả theo thứ tự.
- **Bẫy:** dòng trùng lặp; kết quả cần strip whitespace.

## 4. Forensics & stego đa lớp

### 4.1 VM Windows + BitLocker + JS obfuscate + stego

- **Nhận diện:** đĩa VM Windows có BitLocker + trang HTML có JS obfuscate với mảng số → deobfuscate JS (XOR) TRƯỚC khi nghĩ tới stego.
- **Cách giải (chuỗi điển hình):** Ophcrack crack password user (KHÔNG reset password — mất khả năng giải mã BitLocker) → JS XOR key = từng char của chuỗi fingerprint môi trường (`navigator.platform + ...`) → plaintext decode ASCII85 (`<~...~>`) ra tên tool stego → trích file .doc bằng tool đó (pass = password admin dùng lại) → không có Word thì chạy trong sandbox lấy dump → tìm chuỗi base64.
- **Bẫy:** hai lớp encoding nối tiếp (XOR rồi ASCII85); fingerprint phụ thuộc môi trường phải dựng đúng chuỗi.

### 4.2 QR code hỏng một phần

- **Nhận diện:** ảnh QR bị cháy/rời góc → luôn nghĩ **reconstruction + Reed-Solomon error correction**, đừng đi tìm flag ẩn bằng stego.
- **Cách giải:** QRazyBox (web tool): chọn đúng version (đếm số module mỗi cạnh), vẽ lại tay các module còn nhìn thấy (finder/timing/alignment + vùng data) → RS decoder của tool tự sửa phần còn lại. zbar/zxing đọc ảnh gốc fail thẳng là bình thường.
- **Bẫy:** chọn sai version QR = decoder nối lại sai data; vẽ marking pattern đúng trước, data sau.

### 4.3 PyInstaller exe

- **Nhận diện:** exe Windows có dấu vết PyInstaller (magic MEI/pyi-) → unpack lấy .pyc rồi `strings`/`xxd` TRƯỚC khi cố decompile.
- **Cách giải:** pyinstxtractor → pyc → `uncompyle6`/`decompyle3` (python 3.8-); nếu decompile fail, hexdump pyc — flag thường nằm nguyên dạng chuỗi constant trong bytecode.
- **Bẫy:** pyc bị STRIP magic header → prepend lại magic đúng version (nhận diện qua `python3x.dll` đi kèm) rồi mới decompile; extension file trong pcap có thể giả.

### 4.4 Boot sector giấu trong PDF

- **Nhận diện:** PDF mà quét thấy boot signature (kết thúc `55AA`) → carve image filesystem ra phân tích, không phải phân tích PDF bình thường.
- **Cách giải:** carve sector/đĩa từ offset tìm được → duyệt FS tìm binary lạ → RE hàm check với chuỗi magic + tham số ẩn (so sánh với bản gốc công khai của tool) → kết quả là giá trị trả về của hàm.
- **Bẫy:** đáp án có thể KHÔNG có format flag — là số thập phân (đổi từ hex trả về của hàm); đọc kỹ câu hỏi.

### 4.5 Port knocking

- **Nhận diện:** pcap có các kết nối rải rác vào port số nhỏ, lạ lùng → port-knocking; **port number chính là dữ liệu**.
- **Cách giải:** sort packet theo destination port (hoặc theo thời gian tùy đề) → map số port → ký tự ASCII → ghép.
- **Bẫy:** thứ tự đúng là theo timestamp, không phải số port tăng dần — đọc narrative của đề.

### 4.6 Yara rule biến thành exfil oracle

- **Nhận diện:** giao diện chỉ có "submit Yara rule → hit/no-hit" trên binary build RANDOM mỗi query → đây là oracle; phải leak từng byte bằng chính điều kiện của rule.
- **Cách giải:** match nop-sled 16×`90` + chuỗi byte đặc trưng trước lời gọi hàm decode; đọc tham số bằng `uint32(@nops[1]+off)`; đổi địa chỉ virtual → file offset qua module `pe` (image_base, virtual_address, raw offset của `.data`); mỗi guess kiểm `uint8(flag_raw+i) ^ uint8(key_raw+(i%key_size)) == guess` → hit = đúng byte. Lặp hết flag_len.
- **Bẫy:** đa số chỉ biết Yara khớp string/hex — dạng này bắt dùng arithmetic + `@`/`[1]` + module `pe`; binary mới mỗi query nên phải quy everything về 1 rule duy nhất đọc được cả key lẫn flag offset.

### 4.7 Zero-width steganography

- **Nhận diện:** base64 decode ra đoạn text "Hello, ..." dài BẤT THƯỜNG → check zero-width characters ngay (U+200B/200C/200D).
- **Cách giải:** lọc bỏ ký tự thường → tách theo U+200D (separator), map U+200C=0, U+200B=1 → mỗi 8 bit → ASCII.
- **Bẫy:** đôi khi phải tìm bản archive/lưu cũ của site (qua stego ảnh chỉ điểm sự tồn tại) — bản chính đã vá.

### 4.8 RFID Tag EM4100

- **Nhận diện:** file rawbits kiểu output ProxMark (`Using Clock:64 / Invert:0 / Bits Found:625`, `ASK/Manchester`) → thẻ RFID 125 kHz chuẩn **EM4100**; tool demod xong cho 1 khối 64 bit lặp nhiều lần (thẻ truyền lặp liên tục).
- **Cách giải:**
  - Manchester nhanh: mỗi bit chia 2 nửa, LUÔN có transition ở giữa bit; hướng transition = giá trị bit. EM4100 theo phe IEEE 802.3: cạnh LÊN = 1, XUỐNG = 0 (G.E. Thomas ngược lại) — decode không ra khung thì lật toàn bộ (chính là tham số `Invert`).
  - Layout EM4100 đúng 64 bit: `9 bit '1' (header)` + `10 hàng × (4 bit data + 1 parity hàng)` + `4 parity cột` + `1 stop bit 0`.
  - Decode: tìm header `data.index("1"*9)` → xoay vòng `data[off:] + data[:off]` → cắt 10 nhóm 5 bit từ vị trí 9, mỗi nhóm lấy 4 bit đầu → hex → UID:
    ```python
    off = data.index("1" * 9)
    r = (data[off:] + data[:off])[:64]
    assert r[:9] == "1"*9 and r[63] == "0"
    uid = "".join("%X" % int(r[9+5*i:13+5*i], 2) for i in range(10))
    ```
- **Bẫy:** parity trong đề có thể sinh TÙY Ý (lẫn even/odd) → đừng validate bằng parity; chốt alignment bằng header 9×'1' + stop bit 0 + UID đọc được.
- Tài liệu: Manchester code (Wikipedia, 2 convention), priority1design.com.au (EM4100 protocol), datasheet EM4200.

## 5. Mini-cases (một dòng mỗi kiểu)

| Tín hiệu | Đường giải |
|---|---|
| binary check flag, đo được instruction count (Valgrind callgrind) | side-channel: brute từng vị trí, chọn ký tự cho count cực đại |
| request chứa base64, 40 ký tự hex đầu = key | RC4 decrypt phần còn lại → id/key/iv → AES-CBC giải file |
| `binwalk -eM` bóc archive lồng nhau | trong cùng thường là zip chứa flag |
| tọa độ điểm trong ICMP payload | plot scatter → chữ hiện ra |
| Java deserialize (Commons Collections) | gadget chain, flag ném ra trong stacktrace |
| ảnh + EXIF base64 | pass cho lớp trong cùng (zip/stego) |
| exe + chuỗi "cookie" không decode kiểu nào | tính hiệu `ord()` với known prefix: lệch hằng số → ROT-n/ROT47 |
| UPX pack nhưng ĐỔI TÊN sections | sửa tên section chuẩn → `upx -d` được |
| DNS tunnel exfil trong pcap | tách subdomain → decode base32/hex |
| visual cryptography (2 ảnh chồng nhau) | XOR/collage 2 lớp ảnh |

## 6. Nguyên tắc chung

1. **Magic bytes trước, extension sau** — mọi file lạ đều hexdump 16 byte đầu.
2. Đề lai N lớp thì giải từng lớp, **mỗi lớp dùng tool chuyên dụng** (binwalk, strings, Wireshark, simulator...), không viết script tổng.
3. Hint văn bản thường chỉ THẲNG vật dùng (tên người/quote/tool) — Google nó trước khi "phá mã".
4. Khi mọi hướng chết: quay lại đọc đề lần 2 — 9/10 có tín hiệu đã bỏ qua.
