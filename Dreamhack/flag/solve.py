flag = b""



for i in range(10):
    with open(f"flag.png.0{i}", "rb") as f:
        data = f.read()
        flag += data

with open("flag.png", "wb") as f:
    f.write(flag)