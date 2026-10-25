from PIL import Image, ImageChops

flag = Image.open("flag_7ae18c704272532658c10b5faad06d74.png").convert("RGB")
lemur = Image.open("lemur_ed66878c338e662d3473f0d98eedbd0d.png").convert("RGB")

res = ImageChops.difference(flag, lemur)
res.save("flag.png")
