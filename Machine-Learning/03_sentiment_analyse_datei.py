import os
from transformers import pipeline 

# 1. Deutsches Modell definieren und laden
deutsch = "oliverguhr/german-sentiment-bert"
ki = pipeline("sentiment-analysis", model=deutsch) 

# ZAUBERTRICK: Python findet den aktuellen Ordner automatisch heraus
aktueller_ordner = os.path.dirname(os.path.abspath(__file__))
pfad_eingabe = os.path.join(aktueller_ordner, "kunden.txt")
pfad_ausgabe = os.path.join(aktueller_ordner, "ergebnisse.txt")

# 2. Datei einlesen mit dem automatischen Pfad
with open(pfad_eingabe, "r", encoding="utf-8") as datei:
    bewertungen = datei.read().splitlines()

# 3. KI füttern und Stimmung berechnen
antwort = ki(bewertungen)

# 4. Ergebnisse elegant verknüpfen und untereinander abspeichern
with open(pfad_ausgabe, "w", encoding="utf-8") as ausgabe_datei:
    # zip() verbindet jede Bewertung direkt mit dem passenden KI-Ergebnis
    for satz, ergebnis in zip(bewertungen, antwort):
        stimmung = ergebnis['label']
        zeile = f"{satz} -> {stimmung}\n"
        ausgabe_datei.write(zeile)

print("Die Ergebnisse wurden wunderschön in 'ergebnisse.txt' gespeichert!")
