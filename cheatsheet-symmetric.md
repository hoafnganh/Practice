# Cheatsheet — Symmetric Ciphers

Tổng hợp kỹ thuật giải mật mã đối xứng (AES, DES, mode of operation, stream cipher, oracle) theo hướng "nhận diện → ý tưởng → code → bẫy". Nội dung chính lấy từ bộ 29 bài Symmetric Ciphers của CryptoHack (cryptohack.org/challenges/aes) cộng thêm kinh nghiệm giải các đề tương tự.

Tài liệu đi kèm trong repo:

- Sơ đồ quyết định dạng bài: `Symmetric Cipher - Sơ đồ nhận diện dạng bài.md` — đọc sơ đồ trước khi vào đây tra công thức.
- Solve mẫu chạy được: `Cryptohack/<tên bài>/solve.py` (CTRIME, Dancing Queen, ECB CBC WTF, ECB Oracle, Lazy CBC, Logon Zero, Oh SNAP, Pad Thai, Stream of Consciousness…).
- Bộ tool mật mã cổ điển: `classical/` (xem `tools.md` để biết lệnh).

## 0. Chuẩn bị nhanh

```python
from Crypto.Cipher import AES
AES.new(key, AES.MODE_ECB)                       # tự bỏ qua phần block lẻ
AES.new(key, AES.MODE_CBC, iv=iv)
AES.new(key, AES.MODE_CTR, nonce=nonce)          # counter tự tăng
AES.new(key, AES.MODE_GCM, nonce=nonce)          # .encrypt/.digest/.update(aad)
from Crypto.Cipher import DES, DES3              # khối 8 byte
from Crypto.Util.Padding import pad, unpad       # PKCS7
from Crypto.Hash import MD5, SHA256

xor = lambda a, b: bytes(x ^ y for x, y in zip(a, b))   # helper dùng nhiều nhất
```

Giao tiếp với server dạng REST của CryptoHack: `requests.get(url + "/" + payload.hex())` rồi `r.json()`; mọi giá trị hex đều `bytes.fromhex(...)` trước khi dùng. Với socket dùng pwntools (`remote`, `sendline`, `recvline`).

## 1. AES internals (How AES Works 01–07)

Bảy bài đầu là bài học tự implement AES-128; giá trị lâu dài là **thuộc thứ tự các phép biến đổi để đọc code AES bị sửa sai**.

- **State** là ma trận 4×4 byte, nạp theo **CỘT**: `state[r][c] = b[r + 4c]`; đọc ngược lại là `matrix2bytes`.
- AES-128: 10 vòng; key schedule sinh 44 word (11 round key).
- Mỗi vòng mã hóa: `SubBytes → ShiftRows → MixColumns → AddRoundKey(k_i)`; vòng cuối **không có MixColumns**.
- **Thứ tự GIẢI MÃ 1 block** (dùng nhiều lần khi đọc code đảo):
  1. `AddRoundKey(k10)`
  2. lặp i = 9 → 1: `InvShiftRows → InvSubBytes → AddRoundKey(k_i) → InvMixColumns`
  3. `InvShiftRows → InvSubBytes → AddRoundKey(k0)`
- InvShiftRows: hàng r quay **phải** r vị trí. InvMixColumns nhân với ma trận `{0e,0b,0d,09}`.
- MixColumns là nhân ma trận trong GF(2⁸) mod x⁸+x⁴+x³+x+1 (0x11B); phép nhân 1 byte = chuỗi `xtime`: `xtime(x) = (x<<1) ^ (0x11B nếu tràn bit 8)`.
- 01 · Keyed Permutations: block cipher là **hoán vị có key** — ánh xạ 16 byte → 16 byte phải song ánh thì mới giải mã được.
- 02 · Resisting Bruteforce: tấn công tốt nhất công bố trên AES nguyên bản là **biclique cryptanalysis** (nhanh hơn vét cạn một chút, không thực tế) —AES vẫn an toàn về mặt vét cạn.
- 03 · Structure of AES:.flatten ma trận theo cột là xong.
- 04 · Round Keys: `AddRoundKey` = XOR state với round key (16 byte).
- 05 · Confusion through Substitution: `sub_bytes` dùng S-box; giải mã áp **S-box đảo** từng byte.
- 06 · Diffusion through Permutation: áp ngược `inv_shift_rows` + `inv_mix_columns`.
- 07 · Bringing It All Together: ghép tất cả — implement key schedule + vòng giải mã như trên.

Gotcha hay gặp khi đọc code AES bị biến dạng: đổi chỗ SubBytes/ShiftRows trong vòng lặp, quên InvMixColumns ở đúng vòng, hoặc nạp state theo **hàng** thay vì cột — decrypt ra rác đều đặn. So từng dòng với chuẩn FIPS-197.

## 2. Bảng mode → bug đặc trưng

| Mode | Công thức | Bug hay gặp |
|---|---|---|
| ECB | C_i = E(P_i) | block lặp lộ pattern (penguin); byte-at-a-time oracle |
| CBC | C_i = E(P_i ⊕ C_{i−1}) | padding oracle; bit-flip (sửa C_{i−1} đổi P_i, hỏng block trước); IV = key |
| CFB | P_i = C_i ⊕ E(C_{i−1}) | stream hóa; CFB8 = feedback từng byte → Zerologon |
| OFB | ks_i = E(ks_{i−1}), ks_0 = E(IV) | IV = key ⇒ encrypt = decrypt |
| CTR | ks_i = E(nonce ∥ counter_i) | nonce reuse ⇒ keystream dùng lại (MTP) |
| GCM | CTR + GHASH tag | nonce reuse ⇒ forbidden attack (lộ H, forge tag) |
| IGE | P_i = D(C_i) ⊕ P_{i−1} ⊕ C_{i−1} | padding oracle biến thể (kiểu Telegram) |

Nguyên tắc chung: **mode chỉ là cách đóng gói block cipher**. Mọi bug đều rơi vào 1 trong 3 nhóm: (a) keystream lặp (OFB/CTR/GCM nonce), (b) oracle cho mình chọn input của E hoặc D (ECB/CBC), (c) tính xác thực yếu (tag GCM với nonce lặp).

## 3. 29 bài — chi tiết từng bài

### 3.1 How AES Works (01–07)

Xem mục 1. Không có tấn công; mục đích là thành thạo internals để các bài sau đọc code là biết chỗ sai.

### 3.2 Symmetric Starter (08–09)

**08 · Modes of Operation Starter (15)** — gọi API `encrypt_flag` nhận `{ciphertext, iv}`, rồi gọi `decrypt` trả key/ct về. Làm quen JSON + hex thôi. Gotcha: hex decode trước khi `unpad`.

**09 · Passwords as Keys (50)** — key = `MD5(word).digest()` với `word` trong danh sách từ cho sẵn.

```python
for word in WORDLIST:
    key = MD5(word.encode()).digest()
    try:
        pt = AES.new(key, AES.MODE_ECB).decrypt(ct)
        if pt.startswith(b"crypto{"): print(pt)   # check prefix thay vì unpad
    except Exception: pass
```

Gotcha: decrypt xong `unpad` có thể ném exception vì padding rác — check bằng prefix flag sẽ sạch hơn.

### 3.3 Block Ciphers 1 (10–14)

**10 · ECB CBC WTF (55)** — server encrypt bằng CBC nhưng endpoint decrypt chỉ làm ECB từng block (quên XOR). Tự XOR phía client:

```python
prev = iv
for i in range(0, len(ct), 16):
    pt_block = xor(dec_ecb(ct[i:i+16]), prev)
    prev = ct[i:i+16]
```

**11 · ECB Oracle (60)** — server encrypt `input || FLAG` bằng ECB. Vì ECB deterministic, cùng block input → cùng block output.

```python
def attack(oracle, N=16):
    flag = b""
    while True:
        p = N - 1 - len(flag) % N
        idx = (len(p*"A") + len(flag) + 1) // N      # block chứa byte unknown
        target = oracle(b"A"*p)[:idx*N]
        for c in range(256):
            if oracle(b"A"*p + flag + bytes([c]))[:idx*N] == target:
                flag += bytes([c]); break
        else:
            return flag
```

Ý tưởng: đệm input sao cho **byte cuối của flag rơi vào cuối block**; block đó mã hóa `A*…A + flag_known + x` — brute 256 giá trị x, block trùng khớp là byte đúng. Gotcha: khi flag dài hơn 1 block, `idx` phải tăng đúng; dùng dict `{block: byte}` build từ các query trước sẽ nhanh hơn nhiều.

**12 · Flipping Cookie (60)** — cookie `admin=False;…` mã hóa CBC, server chỉ check plaintext.

```python
iv = bytearray(iv)
i = cookie.find(b"False")
iv[i:i+5] = xor(iv[i:i+5], xor(b"False", b"True;"))   # False → True;
```

Sửa plaintext block 0 ⟹ sửa **IV** cùng vị trí. Sửa block i (i>0) ⟹ sửa block ciphertext i−1 và **chấp nhận hỏng plaintext block i−1**. Gotcha: giữ nguyên độ dài chuỗi thay thế (`False`→`True;`) để phần sau không xô lệch.

**13 · Lazy CBC (60)** — `iv = KEY`. Gửi `ct = C0 || 00*16 || C0`:

- P0 = D(C0) ⊕ key
- P2 = D(C0) ⊕ 0

⟹ `key = P0 ⊕ P2`. Server trả plaintext (qua chính error message của endpoint nhận dữ liệu) — đọc hex là có key, decrypt nốt flag.

**14 · Triple DES (60)** — được **chọn key** cho DES3. 4 weak keys:

```
0101010101010101  FEFEFEFEFEFEFEFE  E0E0E0E0F1F1F1F1  1F1F1F1F0E0E0E0E
```

Với weak key, `E(E(x)) = x` (E là đối hợp). 3DES(K1,K2,K1) = E1∘D2∘E1; khi cả hai đều weak, **áp chuỗi 2 lần = identity** ⟹ "encrypt" ciphertext một lần nữa trả lại plaintext. Gotcha: DES3 cần key 16 byte dạng `K1 || K2` (K1 dùng lại cho vị trí 3).

### 3.4 Stream Ciphers (15–21)

**15 · Symmetry (50)** — OFB với `iv = KEY`. OFB chỉ XOR plaintext với keystream ⟹ **encrypt chính là decrypt**. Gửi ciphertext vào endpoint encrypt là nhận lại flag.

**16 · Bean Counter (60)** — ảnh PNG mã hóa bằng CTR tự chế có counter reset ⟹ keystream chu kỳ 16 byte.

```python
hdr = bytes.fromhex("89504e470d0a1a0a0000000d49484452")   # PNG magic + IHDR
ks = xor(ct[:16], hdr)
pt = xor(ct, (ks * (len(ct)//16 + 1))[:len(ct)])
```

Gotcha: plaintext là ảnh — giải xong lưu thành file rồi **mở ảnh mà nhìn**, đừng soi hex.

**17 · CTRIME (70)** — plaintext bị `zlib.compress` trước khi encrypt bằng CTR ⟹ **độ dài ciphertext là oracle** (CRIME/BREACH cùng họ).

```python
flag = "crypto{"
while not flag.endswith("}"):
    base = len(enc(flag))
    for c in string.printable:
        if len(enc(flag + c)) <= base:    # nén tốt hơn = đoán đúng
            flag += c; break
```

Ý tưởng: đoán đúng ký tự tiếp theo làm nội dung nén được nhỏ hơn ⟹ ct ngắn đi hoặc giữ nguyên; đoán sai thì phình ra. Gotcha: gửi `guess + c` lặp 2 lần giúp hiệu ứng nén rõ hơn; thử theo thứ tự `string.printable`.

**18 · Logon Zero (80)** — CFB8 + reset password theo token mình gửi (bối cảnh Netlogon / Zerologon CVE-2020-1472).

CFB8: `pt[i] = AES(state)[0] ^ ct[i]`, `state = state[1:] + ct[i]` — IV nằm **trong** ciphertext mình gửi. Gửi token toàn `00` × 29: state ≡ 0 ⟹ `pt = E(0)[0]` lặp cả 29 byte. Xác suất 1/256 mỗi key: `E(0)[0] = 0` ⟹ 4 byte cuối (password_length) = 0 ⟹ password rỗng ⟹ đăng nhập bằng chuỗi rỗng. Fail thì reset connection (key mới) thử lại ~256 lần. Đây chính là lỗ hổng "session key không xác thực" của Netlogon Secure Channel.

**19 · Stream of Consciousness (80)** — keystream cố định; server nói 1 câu từ danh sách lyric biết trước, flag mã hóa cùng keystream.

Cách giải: thử từng câu `s`: `ks = xor(ct_song, s)` → `flag = xor(ct_flag, ks)`, check `crypto{`. Gotcha (bẫy thật): 2 câu cùng prefix → XOR 2 ciphertext ở phần prefix chung = 0 → **crib bị echo lại** tạo false positive `crypto{` — phải verify flag ĐẦY ĐỦ có `}` khớp, hoặc ưu tiên câu dài/độc nhất.

**20 · Dancing Queen (120)** — ChaCha20 tự implement **thiếu feed-forward** (không cộng state ban đầu vào cuối).

Block function chuẩn cuối vòng cộng state gốc; thiếu bước này ⟹ chuỗi quarter-round thuần túy **khả nghịch**. Known-plaintext lấy keystream block → đảo ngược từng phép (`+`→`−` mod 2³², `<<<r`→`>>>r`, XOR tự đảo, **đảo thứ tự các thao tác trong quarter-round**) về state ban đầu → **key = state[4:12]** (state layout: 4 constant + 8 key + counter + nonce). Solve mẫu: `Cryptohack/Dancing Queen/solve.py`.

**21 · Oh SNAP (120)** — RC4, `key = IV(3 byte tự chọn) || FLAG`; error `Unknown command: ...` leak keystream byte đầu → **FMS attack** (WEP-style, 2001).

Ba bước:
1. Đo độ dài flag bằng binary search: `ARC4.new` raise (HTTP 500) khi `len(nonce) + len(FLAG) > 256`.
2. Thu thập keystream[0] với IV dạng `(a+3, 255, x)`, đủ 256 giá trị x cho mỗi vị trí a.
3. Majority vote (thuật toán FMS chuẩn — dùng sẵn `fms.attack` của crypto-attacks).

```python
import sys
sys.path.insert(0, "<đường dẫn tới bản clone của github.com/jvdsn/crypto-attacks>")
from fms import attack
ivs = [bytes([a + 3, 255, x]) for a in range(flag_len) for x in range(256)]
# leak(iv) = bytes.fromhex(err[17:]) từ error "Unknown command: <hex>"
flag = attack(encrypt_oracle, flag_len)
```

Gotcha: gửi plaintext `\x00` để error message echo đúng keystream; chạy đa luồng + cache vì cần ~256×len query.

### 3.5 Padding Attacks (22–26)

**22 · Pad Thai (80)** — padding oracle CBC kinh điển (Vaudenay 2002). Submit `(fake_prev_block, cur_block)` → True/False theo PKCS7 hợp lệ.

```python
def dec_block(query, prev, cur, HEX=False):
    D = bytearray(16)
    for i in range(15, -1, -1):
        pv = 16 - i                                  # giá trị padding cần tạo
        for g in (b"0123456789abcdef" if HEX else range(256)):
            fake = bytearray(prev)
            for j in range(i+1, 16):
                fake[j] = prev[j] ^ D[j] ^ pv
            fake[i] = prev[i] ^ g ^ pv
            if query(bytes(fake), cur):
                if i > 0:                            # giết false positive n>=2:
                    fake[i-1] ^= 1                   # flip bit, query lại vẫn True mới nhận
                    if not query(bytes(fake), cur): continue
                D[i] = g; break
    return bytes(D)                                    # plaintext = D ^ prev_thật
```

Ý tưởng: giải mã từng block bằng cách **tự chế prev block** sao cho padding hợp lệ; đi từ byte cuối (padding 1) lùi lên, mỗi byte đã biết được "ghim" vào fake block cho bước sau. Gotcha của chính bài này: server chỉ nhận payload **đúng 2 block** (dài hơn thì ngắt kết nối), và check sai chỉ trả error chứ không chết connection ⟹ pipeline query theo lô được; plaintext dạng hex ⟹ chỉ 16 ứng viên/byte thay vì 256.

**23 · Rhetorical Oracle (100)** — ra mắt 10/2026, **chưa có writeup public** (10/2026). Dạng "thuyết phục admin": biến thể Flipping Cookie khi oracle trả lời có error handling. Hướng thử: đọc kỹ toàn bộ response (kể cả error) tìm kênh leak, thử bit-flip IV nhiều vị trí, xem server check theo prefix/suffix nào. Giải xong nên ghi bổ sung vào bảng ở sơ đồ nhận diện.

**24 · The Good, The Pad, The Ugly (100)** — padding oracle **nhiễu OR**: `good | (rng.random() > 0.4)`.

- Noise `rng() > 0.4`=True với xác suất 0.6, và OR chỉ biết nâng 0→1 ⟹ câu trả lời **False luôn đúng**, True thì nghi ngờ.
- Mỗi hit True **xác nhận lại ×23** (0.6²³ ≈ 10⁻⁵ — sai số chấp nhận được). Budget 12000 query.
- Plaintext hex ⟹ 16 ứng viên/byte, đủ dùng.

**25 · Oracular Spectacular (150)** — nhiễu **XOR**: `good ^ (rng.random() > 0.4)` — không tin được câu trả lời nào (mỗi câu đúng 60%).

Chiến lược thống kê:
- Mỗi ứng viên gán n query; đếm t lần True; **LLR = t·ln(0.4/0.6) + (n−t)·ln(0.6/0.4)** — ứng viên đúng có LLR tăng tuyến tính theo n.
- Dồn query cho **top-2** ứng viên, không loại vĩnh viễn (ứng viên "tồi" có thể chỉ đang xui).
- Xác suất thành công mỗi run thấp → **reconnect làm lại** là chiến lược chính, không phải cố một connection.

**26 · Rhetorical Oracle 2 (150)** — phần 2 của 23, cùng trạng thái **TBD** (chưa có writeup public 10/2026). Cùng hướng điều tra: sự khác biệt giữa các nhánh error của oracle.

### 3.6 Authenticated Encryption (27–28)

**27 · Paper Plane (120)** — mode **IGE** (Telegram từng dùng): `M_i = D(C_i) ⊕ C_{i−1} ⊕ M_{i−1}` với 2 block khởi tạo (m0, c0) công khai.

Padding oracle chuẩn nhưng khối sau chain theo **plaintext khối trước** ⟹ giải theo thứ tự đặc biệt: brute block cuối với `(c0', m0')` tự chọn trước, giải xong block sau thì dùng plaintext vừa giải làm `m0` cho block trước nó. Error "Can't decrypt" = oracle bit.

**28 · Forbidden Fruit (150)** — GCM, nonce dùng lại cho 2 lần encrypt plaintext mình chọn.

Cùng nonce, không AAD, 1 block: `tag = c·H² + X` (H = E(0), X phụ thuộc độ dài) ⟹

- `H² = (t1 − t2)·(c1 − c2)⁻¹` trong GF(2¹²⁸)
- `X = t1 − c1·H²`

Encrypt plaintext cần gửi, forge `tag' = c₃·H² + X`. Field GCM: đa thức `x¹²⁸ + x⁷ + x² + x + 1`, **bit-reverse từng byte** khi đổi bytes ↔ phần tử field (quy ước reflected). Sage:

```python
R.<x> = GF(2)[]; F = R.quotient(x^128 + x^7 + x^2 + x + 1)
# bytes→field: mỗi byte đảo bit, byte thấp = hệ số cao — kiểm chứng 2 chiều
# bằng 1 cặp (c, t) tự encrypt trước khi tin kết quả
```

### 3.7 Linear Cryptanalysis (29)

**29 · Beatboxer (150)** — cipher dựa trên AES nhưng S-box lạ. Test 1 dòng:

```python
all(sbox[a^b] == sbox[a]^sbox[b]^sbox[0] for a in range(256) for b in range(256))
```

Nếu đúng: S-box affine ⟹ **cả cipher thành ánh xạ affine** `E(x) = M·x ⊕ c` trên GF(2)¹²⁸, trong đó **M không phụ thuộc key** (key chỉ đổi hằng số c qua AddRoundKey; SubBytes/ShiftRows/MixColumns đều tuyến tính-tuyến tính-affine).

```python
E = cipher_with(bat_ky_key); c0 = E(b"\0"*16)
cols = [xor(E(e_j), c0) for j in range(128)]     # e_j = block đúng bit j = 1
# dựng ma trận M 128x128 bit từ các cột, khử Gauss GF(2) tìm M^{-1}
# 1 query server encrypt(block 0) → c_server (chính là hằng số c của server)
# flag_block = M^{-1}·(ct_block ⊕ c_server)
```

Đây là ví dụ gọn nhất của "tuyến tính hóa cipher": bỏ tính phi tuyến là mất toàn bộ an toàn.

## 4. Thấy gì trong source → làm gì

| Tín hiệu | Hướng giải |
|---|---|
| `zlib.compress` trước encrypt | length oracle (17) |
| `AES.MODE_ECB` + secret nối input | byte-at-a-time (11) |
| `MODE_CBC` + try/except unpad trả lỗi khác nhau | padding oracle (22) |
| `iv = KEY` | CBC: recover key bằng C0∥0∥C0 (13); OFB: enc=dec (15) |
| decrypt endpoint thiếu XOR | tự XOR CBC (10) |
| cookie `admin=False` CBC | bit-flip IV (12) |
| `good \| noise` / `good ^ noise` | xác nhận ×23 (24) / LLR top-2 (25) |
| CFB8 + password từ token | Zerologon token 00 (18) |
| ảnh + stream cipher | known header (16) |
| cùng keystream 2 bản mã | MTP / xác định plaintext (19) |
| nonce GCM lặp | forbidden attack (28) |
| S-box lạ | test affine (29) |
| 3DES chọn key | weak keys (14) |
| `key = md5(password)` | brute wordlist, check prefix (9) |
| ChaCha tự implement | so từng dòng với RFC 7539, tìm bước bị bỏ (20) |
| keystream từ RNG có seed biết/khá biết | phục hồi seed hoặc dựng lại keystream |
| counter CTR reset / ngắn | keystream chu kỳ ngắn (16) |

## 5. Kỹ thuật oracle nhiễu & tăng tốc

- **OR-noise** (`good | rand>0.4`): False là bằng chứng, True cần xác nhận bội lần. Số lần xác nhận chọn theo ngân sách: 0.6ⁿ < sai số chấp nhận ⟹ n = 23 cho 10⁻⁵.
- **XOR-noise** (`good ^ rand>0.4`): mọi tín hiệu đều nhiễu ⟹ LLR tích lũy, tập trung resource vào top-2, và coi **mỗi run như một phép thử Bernoulli** — reconnect là mộtnhánh của giải thuật.
- **Pipeline query**: gom 32–256 query một lần gửi (server pty buffer nhỏ thì giảm cỡ lô); kinh nghiệm thực chiến: 16.4k request / 176s với 24 threads.
- Oracle chết connection khi sai: dùng 1 connection end-to-end cho mỗi block, reconnect giữa các block.
- Ưu tiên giảm không gian ứng viên trước khi brute: plaintext hex (16), printable (~95), chỉ chữ+ số (62).

## 6. Checklist 5 phút khi nhận đề symmetric

1. Đọc mode + nguồn entropy: IV/nonce từ đâu, có reuse không, có = key không.
2. Đếm oracle: encrypt-chosen? decrypt-chosen? 1-bit? error-message leak?
3. Nhìn plaintext cấu trúc: hex-only? có prefix biết trước (`crypto{`, PNG header)? có nén?
4. Cipher tự chế? → test S-box affine, đếm vòng, so với chuẩn từng dòng.
5. Noise/rate-limit? → đo trước khi viết vòng brute (budget query, xác suất nhiễu).

## 7. Nguồn tham khảo công khai

- Danh mục bài + điểm: <https://cryptohack.org/challenges/aes>
- Bộ solve script cộng đồng: <https://github.com/onealmond/hacking-lab> (mục cryptohack), <https://github.com/jeonyujin4209/crypto_ctf>
- Ghi chú cộng đồng trên HackMD (nhóm KCSC, CayCon và các collection khác) — tìm `cryptohack symmetric writeup site:hackmd.io`.
- Logon Zero & Zerologon: bài viết phân tích CVE-2020-1472 của Tom Tervoort (Secura) — gốc của kỹ thuật CFB8 token 00.
- Vaudenay, "Security Flaws Induced by CBC Padding" (EUROCRYPT 2002) — gốc họ padding oracle.
- FMS: Fluhrer, Mantin, Shamir, "Weaknesses in the Key Scheduling Algorithm of RC4" (SAC 2001).
- Forbidden attack: Joux, "Comments on the Draft GCM Specification" (2006).
