count = int(input("Gib eine Startzahl ein: "))
count += 7
count *= 6
count -= 7

if count % 2 == 0:
    status = "Gerade"
else:
    status = "Ungerade"

print(f"Endergebnis: {count} (Diese Zahl ist {status}!)")         