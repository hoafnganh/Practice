# bai-03-tranh-cat-vigenere

**Thể loại:** forensics / stego

## Lời giải

**1. Tách archive nhúng.** JPEG đi kèm (`cover.jpg`) có một file ZIP nối đuôi. `binwalk` tách ra được; archive có mật khẩu, giải nén thành 12 mảnh ảnh của bức tranh *The Death of Socrates* (Jacques-Louis David).

**2. Thu hồi các mảnh.** Chạy `strings` trên từng mảnh thu được một đoạn text ngắn bị xáo trộn:

```
q-pvothd   ef!-Ooas   g-aeq-sh   eeq-cvbh   rd-iaeiq   ocressgl
uemthdag   guoae!!}   {Ynk!==Yb   qd-Iugrz   OST_RLNS   yk-drooq
```

**3. Sắp thứ tự mảnh.** Ghép hình lại bức tranh nguyên vẹn sẽ suy ra đúng thứ tự các mảnh (và do đó thứ tự các đoạn text):

```
11 - 9 - 3 - 6 - 12 - 10 - 4 - 5 - 1 - 2 - 7 - 8
```

Nối các đoạn theo thứ tự đó được:

```
OST_RLNS{Ynk!==Ybg-aeq-shocressglyk-drooqqd-Iugrzeeq-cvbhrd-iaeiqq-pvothdef!-Ooasuemthdagguoae!!}
```

**4. Vigenère.** Kết quả là **ciphertext Vigenère**; giải mã ra văn bản đọc được và flag.

## Flag

```
XHM{Yay!==You-are-successfully-decoded-Vigenere-cipher-inside-pictures!-Congratulations!!}
```
