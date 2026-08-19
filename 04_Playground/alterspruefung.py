schlage_alter = [14, 19, 16, 22, 18, 30, 15]

zaehler = 0  # Wir starten bei 0 volljährigen Personen

for alter in schlage_alter:
    # WENN das alter größer oder gleich 18 ist...
    if alter >= 18:
        # ...DANN erhöhe den zaehler um 1
        zaehler = zaehler + 1

print("Anzahl der volljährigen Personen:", zaehler)
