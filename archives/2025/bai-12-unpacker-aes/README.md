# bai-12-unpacker-aes

**Thể loại:** RE

## Đề bài

`packed.exe` (PE32+) là một packer tự chế mang theo payload được mã hóa.

## Lời giải

Đọc stub cho thấy nó giải mã một blob nhúng bằng **AES-128 ECB** với key bị hardcode, rồi nạp kết quả như một DLL. Các hằng số quan trọng rút ra từ binary:

- Vị trí payload: RVA `0xF370`, kích thước `0x19A00`
- AES key: `49 6D 6C 39 43 90 AF 04 DD 0A BF D8 DF F1 9F B9`

`decrypt_payload.py` tái hiện quá trình: đọc blob tại RVA đó, giải AES-ECB, kiểm tra output là PE hợp lệ (`MZ` / `PE\0\0`). Script ghi ra `payload.dll` rồi tìm flag bên trong.

```bash
python3 decrypt_payload.py      # cần: pefile, pycryptodome
# Wrote payload.dll (104960 bytes)
strings payload.dll | grep XHM
```

Flag là một chuỗi nằm thẳng trong DLL đã giải mã.

## Flag

```
XHM{packer_daisuki}
```
