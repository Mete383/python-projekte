# 1. Eingaben holen (Mit Schutz vor falschen Eingaben)
try:
    Gesamt_betrag = float(input("Wie viel ist euer Gesamtbetrag? "))
except ValueError:
    print("❌ Bitte gib nur Zahlen ein (z. B. 45.50 ohne €-Zeichen)!")
    exit()

Personen = int(input("Wie viele Personen teilen sich die Rechnung auf? "))
Trinkgeld_prozent = int(input("Wie viel Prozent Trinkgeld möchtet ihr geben? "))

# 2. Berechnung 
Trinkgeld_euro = Gesamt_betrag * (Trinkgeld_prozent / 100)
Endbetrag = Gesamt_betrag + Trinkgeld_euro
Betrag_pro_person = Endbetrag / Personen

# 3. Ausgabe
print(f"Jede Person muss {Betrag_pro_person:.2f} Euro bezahlen.")
