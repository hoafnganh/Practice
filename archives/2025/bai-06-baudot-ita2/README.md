# bai-06-baudot-ita2

**Thể loại:** misc / encoding

## Đề bài

Một file text chỉ toàn ký tự `.` và `-`. Mô tả gợi ý về "điện báo / Morse" — nhưng đó là mồi nhử.

## Lời giải

**1. Không phải Morse.** Một dòng `.-` dài, nhịp đều, không tách được thành các chữ A–Z bằng khoảng cách letter/word là dấu hiệu nhận biết. Mã điện báo "cổ hơn Morse" chính là **Baudot / ITA2** — mã khối cố định 5-bit.

**2. Giải mã ITA2.** Loại bỏ mọi thứ trừ `.` và `-`, map hai ký hiệu sang bit, cắt thành nhóm 5-bit, tra bảng *letters* của ITA2. Vì hướng đọc mơ hồ nên thử 4 biến thể — `. -> 1 / - -> 0` và ngược lại, mỗi loại có và không đảo bit trong từng nhóm 5. Một biến thể cho text sạch.

**3. Bảng đánh vần Thụy Điển.** Text giải được là chuỗi từ đánh vần kiểu radio Thụy Điển — `ADAM=A, BERTIL=B, CAESAR=C, DAVID=D, ERIK=E, …, SIGURD=S, GUSTAV=G, …`. Lấy chữ cái đầu mỗi từ được:

```
XHM UNDERSCORE FLAG OPENING BRACE PUNCH CARDS ARE DEAD NOW CLOSING BRACE
```

**4. Chuẩn hoá token** (`UNDERSCORE -> _`, `OPENINGBRACE -> {`, `CLOSINGBRACE -> }`) để ghép flag. `solve.py` chạy toàn bộ pipeline (tự chọn đúng biến thể bit).

## Flag

```
XHM{PUNCHCARDSAREDEADNOW}
```
