# Classical Cipher Toolkit

Bộ tool mật mã cổ điển chạy offline, thay thế các web solver (dCode...) khi không
muốn đưa dữ liệu lên mạng. Toàn bộ thuần Python stdlib, KHÔNG cần cài gì.

## Kiểm tra bộ toolkit

    python _verify_all.py        # phải in: 24 passed, 0 failed

## Quy trình khi gặp ciphertext lạ

    1. python freq_ic.py ct.txt            # IC + chi2 -> chỉ ra họ cipher
       IC cao (~0.066)  -> mono substitution / ROT family  -> rot_family.py -> substitution_hillclimb.py
       IC thấp (~0.04)  -> polyalphabetic                  -> vigenere_keyless.py / xor_tool.py
       binary, bội của 5 -> Baudot                          -> baudot.py
       nhiều non-printable -> XOR / encoding                -> xor_tool.py

## Các tool

| File | Chức năng | Thay cho dCode |
|---|---|---|
| freq_ic.py | Chẩn đoán: printable, freq, IC, chi2, gợi ý họ cipher | nhận dạng thủ công |
| rot_family.py | Brute ROT-N (26), ROT47 (94), Atbash, Affine (312 keys) | Caesar/ROT47/Affine solver |
| vigenere_keyless.py | Tự tìm độ dài key (IC) + key (chi2 từng cột), không cần crib | Vigenère auto-solver |
| substitution_hillclimb.py | Hill-climb quadgram giải substitution mono | Substitution auto-solver |
| custom_b64_recover.py | Suy bảng Base64 custom từ known-plaintext | — |
| baudot.py | ITA2 5-bit, tự thử 4 kiểu đọc (MSB/LSB x start LTRS/FIGS) | Baudot decoder |
| xor_tool.py | XOR 1-byte brute + repeating-key (hamming + freq) | XorTool/xortool |
| misc_classical.py | A1Z26, Polybius, Tap code, Morse, Bacon, Rail fence (+brute) | từng tool rời rạc |

## Ví dụ

    python freq_ic.py ct.txt
    python rot_family.py "Khoor Zruog"
    python vigenere_keyless.py ct.txt
    python vigenere_keyless.py --key LEMON ct.txt      # decrypt có key
    python substitution_hillclimb.py ct.txt            # chạy vài lần nếu kẹ local optimum
    python custom_b64_recover.py --known-plain "known text" --known-cipher "8kP3..." --target "Xy..."
    python baudot.py decode bits.txt
    python xor_tool.py single ct.txt
    python xor_tool.py multi ct.txt
    python xor_tool.py multi --keylen 11 ct.txt
    python misc_classical.py railfence_brute "WECRLTEERDSOEEFEAOCAIVDEN"

## CyberChef local

CyberChef bản local (tải về chạyoffline, không qua web) làm tốt: ROT13/47 brute,
Atbash, Affine, Vigenère có key, XOR, Rail fence, Bifid, Morse, Bacon, **Enigma**
(op riêng, set rotor/reflector/plugboard), Base64/32/58/85 **kèm bảng alphabet
custom**. Còn auto-solve Vigenère/substitution → dùng toolkit này.

## Optional (pip)

    pip install py-enigma     # Enigma machine nếu CyberChef không đủ
    pip install pycipher      # Playfair, ADFGVX, Columnar...
    pip install xortool       # thay thế xor_tool.py

## Ghi chú quan trọng

- `caesar_shift(text, k)` / `rot_family.py` hiểu k là **lượng dịch vào trong**
  (decrypt). Encrypt = dùng `-k`.
- `vigenere_keyless.py` giả định plaintext tiếng Anh (đa số đề dùng English).
- `substitution_hillclimb.py` cần `english_quadgrams.txt` (3.3MB, đã có sẵn
  trong folder; nguồn: practicalcryptography.com, mirror gibsjose/statistical-attack).
  Nếu thiếu: `curl -L -o english_quadgrams.txt https://raw.githubusercontent.com/gibsjose/statistical-attack/master/english_quadgrams.txt`
- `custom_b64_recover.py`: biết nhiều đoạn known-plaintext thì NỐI LẠI thành 1
  cặp duy nhất trước khi đưa vào, để phủ đủ 64 ký tự bảng.
- Nguyên tắc dữ liệu: mọi thứ làm được offline thì làm offline — không upload
  dữ liệu nhạy cảm (đề bài, secrets, dump) lên dịch vụ web nào.
