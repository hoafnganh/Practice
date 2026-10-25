from fastecdsa.curve import Curve
from fastecdsa.point import Point
import string

p  = 0xF1FD178C0B3AD58F10126DE8CE42435B3961ADBCABC8CA6DE8FCF353D86E9C03
a  = 0xF1FD178C0B3AD58F10126DE8CE42435B3961ADBCABC8CA6DE8FCF353D86E9C00
b  = 0xee353fca5428a9300d4aba754a44c00fdfec0c9ae4b1a1803075ed967b7bb73f
n  = 0xf1fd178c0b3ad58f10126de8ce42435b53dc67e140d2bf941ffdd459c6d655e1
Gx = 0xB6B3D4C356C139EB31183D4749D423958C27D2DCAF98B70164C97A2DD98F5CFF
Gy = 0x6142e0f7c8b204911f9271f0f3ecef8c2701c307e8e4c9e183115a1554062cfb

# G = FRP256v1.G
F = GF(p)
E = EllipticCurve(F, [a, b])
G = E(Gx, Gy)

# FCSC{Dl0G_S0lV1ng!}

X = 0xbba2fac88d029643d8557b9850255c516d1851bad36184718ae3e416a5362b3
Y = 0xdddac00e5bf9d3ec2d5d472756cc3ee38b229118eafb9aacc2466d7673fe4ed4

pt = E(X, Y)
alpha = string.printable
flag = ""
for ch in alpha:
    pt = ord(ch) * G
    
    if pt.x() == X and pt.y() == Y:
        flag += ch
        print(flag)
        break
