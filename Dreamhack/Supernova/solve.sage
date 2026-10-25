from pwn import *
import re
context.log_level = 'error'

io = remote("host3.dreamhack.games", 18028)
N  = int(io.recvline())
c  = int(io.recvline())
e  = 0x10001
K  = 512

# --- 1) Sinh trọn bộ query phía client; nhân tử tính ĐỆM (1 phép nhân/vòng,
#        thay vì pow(4, i*e, N) — full modexp — cho từng i)
step = pow(4, e, N)                    # 4^e mod N, tính đúng một lần
t, queries = 1, []
for i in range(K):
    queries.append(str(c * t % N).encode())   # giải mã ra 4^i·m mod N
    t = t * step % N                          # 4^((i+1)·e)

# --- 2) PIPELINE: bắn cả K dòng trong một lần, không chờ trả lời từng dòng
io.send(b"\n".join(queries) + b"\n")

# --- 3) Gom đáp án: mỗi chữ số đứng sau prompt "> " (input() in không kèm \n)
buf = b""
while True:
    buf += io.recv(8192, timeout=5)
    digits = re.findall(rb"(?m)^([0-3])\r?\n", buf.replace(b"> ", b""))
    if len(digits) >= K:
        break
digits = list(map(int, digits[:K]))

# --- 4) Ghép chữ số, dựng m, TỰ KIỂM TRA trước khi đi nước cuối
A = 0
for a in digits:
    A = 4*A + a
m = -(-N * A // 4**K)
assert pow(m, e, N) == c, "chưa chính xác — tăng K rồi kéo thêm chữ số"

io.sendline(str(m).encode())
print(io.recvall(timeout=5).decode())