from fastecdsa.curve import Curve
from fastecdsa.point import Point
from hashlib import sha256, sha512
from base64 import b64encode as b64e, b64decode as b64d
from pwn import *

def sign(C, sk, msg):
	ctx = sha256()
	ctx.update(msg.encode())
	k = int(ctx.hexdigest(), 16)

	ctx = sha512()
	ctx.update(msg.encode())
	h = int(ctx.hexdigest(), 16)

	P = k * C.G
	r = P.x
	assert r > 0, "Error: cannot sign this message."

	s = (pow(k, -1, C.q) * (h + sk * r)) % C.q
	assert s > 0, "Error: cannot sign this message."

	return (r, s)

def verify(C, Q, msg, r, s):

	if Q.IDENTITY_ELEMENT == Q:
		return False

	if not C.is_point_on_curve((Q.x, Q.y)):
		return False

	if r < 1 or r > C.q - 1:
		return False

	if s < 1 or s > C.q - 1:
		return False

	ctx = sha512()
	ctx.update(msg.encode())
	h = int(ctx.hexdigest(), 16)

	s_inv = pow(s, -1, C.q)
	u = h * s_inv % C.q
	v = r * s_inv % C.q
	P = u * C.G + v * Q
	return r == P.x

re = remote("localhost", 4000)

C = Curve(
            "ANSSIFRP256v1",
            0xF1FD178C0B3AD58F10126DE8CE42435B3961ADBCABC8CA6DE8FCF353D86E9C03, # p
            0xF1FD178C0B3AD58F10126DE8CE42435B3961ADBCABC8CA6DE8FCF353D86E9C00, # a
            0xEE353FCA5428A9300D4ABA754A44C00FDFEC0C9AE4B1A1803075ED967B7BB73F, # b
            0xF1FD178C0B3AD58F10126DE8CE42435B53DC67E140D2BF941FFDD459C6D655E1, # q
            0xB6B3D4C356C139EB31183D4749D423958C27D2DCAF98B70164C97A2DD98F5CFF, # gx
            0x6142E0F7C8B204911F9271F0F3ECEF8C2701C307E8E4C9E183115A1554062CFB # gy
        )

re.recvline()
re.recvline()
re.recvline()
re.recvline()
re.recvline()
Qx = int(re.recvline().decode().strip().split(": ")[1], 16)
Qy = int(re.recvline().decode().strip().split(": ")[1], 16)
Q = Point(Qx, Qy, curve=C)

re.recvuntil(b">>> ")
# print(Qx, Qy)
re.sendline(b'admin')
re.recvline()
token = [b64d(re.recvline().decode()).decode() for _ in range(4)]
# print(token)
# for i in range(4):
#     uid, r, s = token[i].split('|')
#     # print(uid, r, s)
uid, r, s = token[0].split('|')
r, s = int(r), int(s)
ctx = sha256()
ctx.update(uid.encode())
k = int(ctx.hexdigest(), 16)
ctx = sha512()
ctx.update(uid.encode())
h = int(ctx.hexdigest(), 16)
sk = ((s * k - h) * pow(r, -1, C.q)) % C.q

re.recvline()
re.recvline()
re.recvuntil(b">>> ")

r, s = sign(C, sk, 'admin')
# print(verify(C, Q, 'admin', r, s))
payload = b64e(b'admin|' + str(r).encode() + b"|" + str(s).encode())
re.sendline(payload)
print(re.recvall(timeout=5))
 