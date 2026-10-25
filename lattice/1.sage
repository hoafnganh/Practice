beta = RealField(100)("8.70997594")

c = 10 ^ 8

b1 = floor(c * beta)
b2 = floor(c * beta ^ 2)
b3 = floor(c * beta ^ 3)

B = Matrix(ZZ, [
    [c,  1, 0, 0],
    [b1, 0, 1, 0],
    [b2, 0, 0, 1],
    [b3, 0, 0, 0]
])
LLL_reduced = B.LLL()

print(LLL_reduced)
v = LLL_reduced[0]
c = v[0]
a0 = v[1]
a1 = v[2]
a2 = v[3]

PR.<x> = PolynomialRing(ZZ)
f = x ^ 3 + a2 * x ^ 2 + a1 * x ^ 1 + a0
print(f)