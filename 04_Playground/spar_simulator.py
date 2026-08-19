import random

ziel_budget = 1115
aktueller_sparnis = 0
wochen_zaehler = 0

def generiere_spargeld():
    betrag = random.randint(4, 40)
    if betrag >= 40:
        print("Super Woche!")
    return betrag

while aktueller_sparnis < ziel_budget:
    wochen_zaehler += 1
    aktueller_sparnis += generiere_spargeld()

print("Ziel erreicht! Du hast", wochen_zaehler, "Wochen gebraucht.")
