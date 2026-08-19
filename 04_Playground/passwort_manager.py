import random

passwort = 'hanzpeter2010'
versuche = 1

while versuche <= 3:
    eingabe = input(f"Versuch {versuche}/3 - Bitte Passwort eingegeben: ")
    if eingabe.lower() == passwort:
        print("Passwort korrekt! Zugriff erlaubt.")
        break
    else:
        print("Passwort falsch!")
    versuche = versuche + 1

if versuche > 3:
    print("Zu viele Versuche. Programm wird beendet.")


