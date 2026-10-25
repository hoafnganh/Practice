# bai-02-batch-alphabet

**Thể loại:** RE / scripting

## Lời giải

`data.txt` là Base64 lồng hai lần. Giải hai lượt thu được chuỗi các codepoint Unicode dạng `U+HHHH` ghép thành một [batch script](command.txt) của Windows.

Batch script này dựng lại các chuỗi bằng cách tra `%VAR:~offset,1%` và tự sinh thêm vài bộ alphabet; lệnh `echo` cuối cùng index vào các alphabet đó để ghép ra password.

## Flag

```
F1r3NIc3$4Lyfe
```
