v1 = vector(QQ, [4, 1, 3, -1])
v2 = vector(QQ, [2, 1, -3, 4])
v3 = vector(QQ, [1, 0, -2, 7])
v4 = vector(QQ, [6, 2, 9, -5])
vectors = [v1, v2, v3, v4]
u = []
u1 = v1
u.append(u1)
for i in range(1, 4):
    u_i = vectors[i]
    for j in range(0, i):
        muy = (vectors[i] * u[j]) / (u[j] * u[j])
        u_i -= muy * u[j]
    u.append(u_i)