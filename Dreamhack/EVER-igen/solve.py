from string import ascii_lowercase, ascii_uppercase, digits

words = ascii_uppercase + ascii_lowercase + digits # 62 ký tự

def shift(a, d):
    if a not in words:
        return a
    index = words.index(a)
    return words[(index + d) % len(words)]
def decrypt(key):
    pt = ""
    for i in range(len(ct)):
        pt += shift(ct[i], -key[i % len(key)])
    return pt


ct = "39 2YAx k5LgCy iP Aj9geVQy nEvXnd3Je c kX9P 8z uZ7dbErYRAyegw Ona3Js eRcKyO u7 ffFTl70 TH9ScB – M0HbNuV HDd 4yk TE c3uVU 8Y D1Q ZDNhBpRc 9WY27fjiF – dVWNBP D1Q NAZsM fW bPlBI N3e p8 6i97Nc. FmP HjIjVi 7Zu 4Zth9 bL kYD Gg0yZjc0 dBrYVQ, f8GQ0PD, Bu kGue 8BUlT9FmE0 UDCNp2vQi xd jkfm97 9uDfndFF egcc9CZ 27 mTE 2Y7u A8Zi fM N4Ks3 UVK Dg0. LTAabG 2RSDTqDu GP7QbLq. qy ZE2Xy GUpG kYD eYvEXf DJdMc fE Ep2DTjX4Zt dlk uObyx f DJq7ckZM0 \"w8gse0WtBie\" (L 4yk) FT LyZkB1 a29Tjc FmIjRSDDd yFQwj QfMvVi. 9I, Tjc0 dHoVj DSc zXfR. Ek{sreSsZxMq8OPf37BwUdvpZKzQ8oNg7Z8rwASqbxQsBl0g935rwDLQaNxNCnxK44g}"
def score(a):
    s = 0
    for i in a:
        if i in "etaoinshrdlu":
            s += 4
        elif i == " ":
            s += 3
        elif i.islower(): s += 2
        elif i.isdigit(): s -= 4
    return s

key = []
for j in range(16):
    best_key = 0
    best_score = -99999
    for k in range(63):
        col_pt = ""
        for i in range(j, len(ct), 16):
            col_pt += shift(ct[i], -k)
        if score(col_pt) > best_score:
            best_score = score(col_pt)
            best_key = k
    key.append(best_key)
print(*key) # 51 22 45 60 29 2 53 53 35 20 47 57 20 20 48 1
for round in range(10):
    changed = False
    for j in range(16):
        old = key[j]
        best_k, best_s = old, score(decrypt(key))
        for k in range(63):
            key[j] = k
            s = score(decrypt(key))
            if s > best_s:
                best_s = s
                best_k = k
        key[j] = best_k
        if best_k != old:
            changed = True
    if not changed:
        break

print("key =", key)
