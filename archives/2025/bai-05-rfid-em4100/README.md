# bai-05-rfid-em4100

**Thể loại:** hardware / RFID

## Đề bài

File `rawbits.txt` là output dạng bit thô của tool demod (ASK/Manchester, clock 64) đối với một thẻ RFID 125 kHz chuẩn **EM4100**. Thẻ truyền đi lặp liên tục nên toàn bộ thông điệp nằm gọn trong một khối 64 bit.

## Lời giải

- **Manchester:** mỗi bit chia 2 nửa, luôn có transition ở giữa bit; hướng transition = giá trị bit (EM4100 theo quy ước IEEE: cạnh LÊN = 1, XUỐNG = 0).
- **Layout EM4100 64 bit:** `9 bit '1' (header)` + `10 hàng × (4 bit data + 1 bit parity hàng)` + `4 bit parity cột` + `1 stop bit 0`.
- Tìm header bằng `data.index("1"*9)` → xoay vòng stream về đúng khung → cắt 10 nhóm 5 bit từ vị trí 9, mỗi nhóm lấy 4 bit đầu → hex → UID.

```bash
python3 solve.py
```

## Lưu ý

- Parity trong đề sinh tùy ý (lẫn even/odd) — đừng validate bằng parity; hãy chốt alignment bằng header 9×'1' + stop bit 0 + UID đọc được.
- Output demod có thể bị ngược bit tuỳ quy ước của tool — decode không ra khung thì lật toàn bộ.
