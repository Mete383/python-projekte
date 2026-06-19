count = int(input("Gib eine Startzahl ein: "))
count += 4
count *= 2
count -= 1

if count % 2 == 0:
    status = "Gerade"
else:
    status = "Ungerade"

print(f"Endergebnis: {count} (Diese Zahl ist {status}!)")        