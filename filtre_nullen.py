zahlen = [0, 1, 0, 3, 12, 0, 9]
bereinigte_liste = []

for z in zahlen:
    if z != 0:
        bereinigte_liste.append(z)

print("Ohne Nullen:", bereinigte_liste)
