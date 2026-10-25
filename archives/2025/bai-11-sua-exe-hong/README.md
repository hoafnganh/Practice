# bai-11-sua-exe-hong

**Thể loại:** RE

## Đề bài

Nhận được `corrupted.exe` — không chạy được. Hãy khôi phục file và chạy nó (không tham số) để lấy flag.

## Lời giải

File là một PE với header bị can thiệp. Nhìn vào phần đầu:

```
corrupted: 00 04 99 01 40 01 b1 a3 00 00 5a 5a 90 00 03 00 ...
restored: 4d 5a 90 00 03 00 00 00 04 00 ... -> "MZ"
```

Có hai lỗi: **10 byte rác được chèn lên đầu**, và magic `MZ` bị phá. `fix_corrupted.py` sửa cả hai — bỏ 10 byte đầu, rồi ép byte đầu tiên về `'M'` — thu được file PE32 console hợp lệ.

```bash
python3 fix_corrupted.py # corrupted.exe -> restored.exe
```

Chạy `restored.exe` không tham số sẽ in flag. Trong disassembly, `main` dựng flag từ một format string:

```c
printf("XHM{%sing_%s_%s_%s!}\n", "find", "the", "magic", "now");
```

`%sing` = `find` + `ing` = `finding`, vậy kết quả là:

## Flag

```
XHM{finding_the_magic_now!}
```
