# bai-04-hta-md5-password — Writeup

**Thể loại:** RE / cracking

## Đề bài

**File:** `crackme.HTA` — ứng dụng HTA kiểm tra password.

### Cơ chế
1. Validation bằng JavaScript dùng băm MD5
2. Password tách thành 3 thành phần (h1, h2, h3) qua phép hoán vị ký tự
3. Mỗi thành phần được băm MD5, đảo chuỗi, rồi so sánh với giá trị đã obfuscate

### Biến chính
```javascript
nl = [0, 6, 17, 14, 1, 18, 16, 7, 11, 13, 8, 12, 2, 3, 0, 15, 4, 0, 9, 5, 0, 0, 10, 0, 0]
ko = "58b4cb64f141e5c914640c5c8cc8e5d5"  // h1: 8 chữ số
ka = "8a1828526galf607b8257cb552b0e6c8"  // h2: 4 ký tự alphanumeric
kq = "z99za5c140689zc2d2a1052c8z5e4b9d"  // h3: 6 ký tự alphanumeric
```

## Lời giải

### Bước 1: đảo chiều phép biến đổi
```python
# Áp dụng substitution rồi đảo chuỗi
target_h1 = ko.replace('4','a').replace('d','3').replace('e','7')[::-1]
target_h2 = ka.replace('f','3').replace('l','d').replace('g','9')[::-1]
target_h3 = kq.replace('2','f').replace('b','7').replace('z','3')[::-1]
```

Hash MD5 đích:
- h1: `53578cc8c5c0a6a19c571a1fa6bcab85`
- h2: `8c6e0b255bc7528b7063da96258281a8`
- h3: `d974e538cf501afdfc3986041c5a3993`

### Bước 2: crack hash

**Brute force bằng Python** (cho h1 & h2):
```python
import hashlib, itertools

def md5(s): return hashlib.md5(s.encode()).hexdigest()

# h1: 8 chữ số — tìm được 20231114
# h2: 4 alphanumeric — tìm được fL46
```

**Hashcat** (cho h3):
```bash
hashcat -m 0 -a 3 hash.txt ?1?1?1?1?1?1 -1 ?u?l?d
# Kết quả: Dec0d3
```

### Bước 3: ghép lại password

Dùng bảng vị trí `nl`:

```
Vị trí  1: h1[1]=0  |  Vị trí  2: h3[3]=0  |  Vị trí  3: h1[4]=1
Vị trí  4: h1[5]=1  |  Vị trí  5: h1[6]=1  |  Vị trí  6: h1[0]=2
Vị trí  7: h1[2]=2  |  Vị trí  8: h1[3]=3  |  Vị trí  9: h3[5]=3
Vị trí 10: h1[7]=4  |  Vị trí 11: h2[2]=4  |  Vị trí 12: h2[3]=6
Vị trí 13: h3[2]=c  |  Vị trí 14: h3[0]=D  |  Vị trí 15: h3[4]=d
Vị trí 16: h3[1]=e  |  Vị trí 17: h2[0]=f  |  Vị trí 18: h2[1]=L
```

**Các thành phần:**
- h1 = `20231114`
- h2 = `fL46`
- h3 = `Dec0d3`

**Password:** `001112233446cDdefL`

`carve_png.py` là phần phân tích thêm: carve các PNG nhúng trong chính file HTA (scan chunk PNG hợp lệ kết thúc đúng IEND).

## Flag

```
XHM{001112233446cDdefL}
```

## Tool đã dùng
- Python 3 (brute force h1, h2)
- Hashcat (crack h3)
