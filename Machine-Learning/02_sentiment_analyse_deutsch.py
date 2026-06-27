import numpy as np
from transformers import pipeline

# 1. Das KI-Modell für Sentiment-Analyse (Stimmung) laden
# Dieses Modell erkennt, ob ein Satz POSITIV oder NEGATIV ist
ki = pipeline("sentiment-analysis", model="oliverguhr/german-sentiment-bert")

# HIER WURDEN DIE KOMMAS ERGÄNZT:
bewertungen = [
    "Ich finde die App super habe meine Steuererklärun in Rekordzeit erledigt.",
    "Ich habe keine Probleme mehr mit Steuernerklärungen!",
    "Ich finde die App hat zu viele Werbungen.",
    "Habe durch die App 1067€ zurückbekommen. Danke dir!"
]

antwort = ki(bewertungen)
print(antwort)
