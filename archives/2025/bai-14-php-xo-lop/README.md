# bai-14-php-xo-lop

**Thể loại:** RE / web misc

## Đề bài

Một PHP script bị obfuscate nhiều lớp (kiểu búp bê lồng nhau). Mỗi lớp khi chạy chỉ decode rồi `eval` lớp kế tiếp — lồng nhau cho tới tận flag.

## Các file

- Lớp ngoài cùng có kích thước **~130 MB** (một khối `eval(hex2bin("…"))` khổng lồ).
- `final.php` — một lớp trung gian/cuối nhỏ hơn hẳn (146 byte), chứa flag.

## Mẫu obfuscate

Mỗi lớp là lớp kế tiếp được bọc trong một hoặc nhiều phép biến đổi PHP đảo ngược được, rồi `eval`. Bóc vài lớp đầu thấy được các khối dựng:

```
eval(hex2bin("6261736536345f6465636f6465..."))      # hex2bin -> ASCII
   -> base64_decode("aGV4MmJpbigiNjc3YTY5...")       # base64  -> ASCII
      -> hex2bin("677a696e666c617465286865...")      # "gzinflate(hex..."
         -> gzinflate(hex2bin("..."))                # giải nén
            -> eval(... lớp kế tiếp ...)
```

Bộ phép bọc gồm: `hex2bin(...)` (giải hex), `base64_decode` (giải base64), `gzinflate(...)` (giải nén DEFLATE thô), `eval(...)` (chạy kết quả).

## Lớp cuối / flag

Script trong cùng là một đoạn mồi + flag:

```php
<?php $s='print("I have a flag!\n"); /* XHM{A_Matryoshka_Obfuscated_Script} */ print("Congrats!!\n");';
$s=substr($s, 0, 27); eval($s); ?>
```

Điểm mấu chốt: `$s` bị cắt chỉ còn 27 ký tự trước khi `eval`, nên đoạn code thực sự chạy chỉ là `print("I have a flag!\n")`. Còn flag nằm trong comment của chuỗi gốc.

## Flag

```
XHM{A_Matryoshka_Obfuscated_Script}
```
