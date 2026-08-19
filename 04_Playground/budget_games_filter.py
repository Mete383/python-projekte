# Eine Liste mit den Preisen verschiedener Videospiele
preise = [15, 45, 0, 25, 60, 12, 0, 29, 35]

# Das maximale Budget, das für ein Spiel ausgegeben werden soll
mein_budget = 30

# Eine leere Liste, in der die bezahlbaren Spiele gespeichert werden
meine_spiele = []

# Wir gehen jeden einzelnen Preis in der Liste durch
for preis in preise:
    # PRÜFUNG: Das Spiel muss im Budget liegen UND darf nicht kostenlos (0) sein
    if preis <= mein_budget and preis != 0:
        # Wenn beide Bedingungen erfüllt sind, fügen wir den Preis der Liste hinzu
        meine_spiele.append(preis)

# Ausgabe der gefilterten Spiele, die gekauft werden können
print("Diese Spiele kaufe ich:", meine_spiele)
