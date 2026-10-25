with open("secretMessage.enc", "rb") as f:
    data = f.read()
# print(data)
pt = b""
i = 0
while i < len(data):
    a = data[i]
    if i + 1 < len(data) and a == data[i + 1]:
        count = data[i + 2] + 2
        pt += (bytes([a]) * count)
        i += 3
    else:
        pt += bytes([a])
        i += 1
# print(pt)

with open("secretMessage.raw", "wb") as f:
    f.write(pt)