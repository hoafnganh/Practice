# bai-07-shutdown-chain

**Thể loại:** privesc / cloud config

## Đề bài

Mục tiêu: tắt máy chủ.

## Lời giải

EC2 user-data script (được lộ trong `linpeas.txt` — output quét cấu hình) tiết lộ toàn bộ setup:

- Tồn tại user local `user` với password `IamTheUser!`, và SSH bật chế độ đăng nhập bằng password.
- `/etc/pam.d/su` được thêm rule `pam_succeed_if` sao cho khi `user` chạy `su shutdown` thì xác thực thành công **không cần mật khẩu**.
- Login shell của user `shutdown` là `/sbin/system/shutdown.sh`, chỉ chạy đúng một lệnh `sudo poweroff -i`.
- sudoers cấp cho `shutdown ALL=NOPASSWD: /usr/sbin/poweroff -i`.

Vậy chuỗi khai thác: đăng nhập bằng `user`, chuyển sang `shutdown`, shell của nó sẽ tắt máy.

```bash
ssh user@<target>          # password: IamTheUser!
su shutdown                # không cần password nhờ PAM -> chạy shutdown.sh -> sudo poweroff -i
```

Máy chủ tắt.
