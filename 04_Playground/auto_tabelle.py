import pandas as pd

# Wir bauen die Tabelle direkt Zeile für Zeile auf – das verhindert Syntax-Fehler!
df_autos = pd.DataFrame([
    {"kilometerstand": 60000, "ps": 150, "marke": "BMW"},
    {"kilometerstand": 80000, "ps": 110, "marke": "Audi"},
    {"kilometerstand": 90000, "ps": 90, "marke": "VW"}
])

print("--- VORHER (Mit Text-Marke) ---")
print(df_autos)
print("\n" + "="*40 + "\n")

# Wir zwingen Pandas, echte Zahlen (0 und 1) statt True/False zu generieren
tabelle_mit_zahlen = pd.get_dummies(df_autos, columns=['marke'], dtype=int)

print("--- NACHHER (Für die KI umgewandelt) ---")
print(tabelle_mit_zahlen)
