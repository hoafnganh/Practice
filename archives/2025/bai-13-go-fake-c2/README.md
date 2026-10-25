# bai-13-go-fake-c2

**Thể loại:** RE

## Đề bài

- **Mục tiêu:** phân tích binary và trích flag.
- **Binary:** `fakeC2.exe` (Go binary) — bản mô phỏng đơn giản hóa một implant giao tiếp với C2.

## Hành vi tổng quan

- Entry nhảy tới `main.main`, gọi `main.startServer` (đăng ký route `/check` và `/post`) rồi `main.runClient`.
- Phía client HTTP check tới `http://127.0.0.1:5555/check`, hỏi decrypt key, rồi POST JSON `{ "decryptkey": <key> }` lên `/post` và in phản hồi của server.

## Handler `/post` của server (main.startServer.func2)

- Decode JSON, trích `decryptkey`.
- So với key mong đợi nhúng sẵn trong global `main.expectedKey`.
- Nếu khớp: giải mã RC4 một buffer ciphertext nhúng sẵn rồi trả plaintext; ngược lại trả thông báo lỗi.

## Key và ciphertext

- `main.expectedKey` → "RC4JsonMarshalLocalC2"
- `main.flag` → ciphertext 73 byte (global byte buffer)

## Giải mã

- Thuật toán: RC4 stream cipher, key = `RC4JsonMarshalLocalC2`
- Giải mã 73 byte của `main.flag` thu được JSON chứa flag.

## Flag

```
XHM{go_rev_startingpoint}
```
