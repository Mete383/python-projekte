# Variabel (Speicherbox)
startkapital = float(input("Sag mir dein Startkapital!"))
zinssatz = float(input("Gib den Zinssatz in Prozent ein (z.B. 5):"))
jahre = int(input("Gib die Laufzeit in Jahren ein (z.B. 10):"))

# Loop-Schleife
for jahr in range(1, jahre + 1):
    endkapital = startkapital * (1 + zinssatz / 100) ** jahr
    
    # NEU: Diese Zeile zeigt dir den Kontostand für JEDES Jahr an!
    print(f"Jahr {jahr}: {endkapital:.2f} Euro")

# Gibt das Endkapital auf dem Bildschirm am Ende aus
print(f"\nNach {jahre} Jahren hast du ein Endkapital von: {endkapital:.2f} Euro.")
