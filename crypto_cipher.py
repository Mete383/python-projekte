# =====================================================================
# PROJEKT: KRYPTOGRAPHIE & MODULO-VERSCHLÜSSLER (CAESAR-CIPHER)
# =====================================================================

def code_verarbeiten(text, schluessel, modus):
    """
    Verarbeitet einen gesamten Text Buchstabe für Buchstabe.
    Nutzt das mathematische Modulo-Prinzip, um das Alphabet im Kreis zu drehen.
    """
    ergebnis = ""
    
    # Wenn der Modus auf Entschlüsseln steht, drehen wir das Vorzeichen des Schlüssels um.
    # Aus einer Verschiebung von +3 nach rechts wird so eine Verschiebung von -3 nach links.
    if modus == "entschluesseln":
        schluessel = -schluessel

    # Wir gehen den eingegebenen Text Buchstabe für Buchstabe ab
    for zeichen in text:
        # Wir prüfen, ob es sich um ein echtes Zeichen des Alphabets handelt
        if zeichen.isalpha():
            
            # MATHE-KERN: ASCII-Startwert bestimmen
            # A = 65 für Großbuchstaben, a = 97 für Kleinbuchstaben
            # Da der Computer bei 0 anfängt zu zählen, rutschen alle Buchstaben um 1 nach hinten (t ist die 19)
            basis = 65 if zeichen.isupper() else 97
            
            # DIE KREIS-MATHEMATIK:
            # 1. ord() zieht den Buchstaben in eine Zahl (z.B. 'A' -> 65)
            # 2. Wir ziehen die Basis ab, damit wir auf einer Skala von 0 bis 25 rechnen (z ist die 25)
            # 3. Wir addieren unseren geheimen Schlüssel
            # 4. Der Modulo-Befehl (%) fängt die Zahlen ab 26 ab und setzt sie zurück auf die 0 (a)
            neuer_wert = (ord(zeichen) - basis + schluessel) % 26
            
            # chr() wandelt den berechneten Zahlenwert zurück in ein echtes Zeichen
            ergebnis += chr(basis + neuer_wert)
        else:
            # Leerzeichen, Zahlen und Sonderzeichen (z. B. "!", "?") überspringen die Mathe-Maschine
            ergebnis += zeichen
            
    return ergebnis


def main():
    """
    Hauptmenü zur Steuerung des Krypto-Tools im Terminal.
    """
    while True:
        print("\n--- 🔐 GEHEIMCODE-GENERATOR (MODULO-MATHE) ---")
        print("1. Nachricht verschlüsseln")
        print("2. Nachricht entschlüsseln")
        print("3. Programm beenden")
        
        auswahl = input("Wähle eine Option (1-3): ")
        
        if auswahl == "1":
            text = input("Gib deinen geheimen Text ein: ")
            try:
                zahl = int(input("Gib eine Schlüsselzahl ein (z. B. 5): "))
                geheimtext = code_verarbeiten(text, zahl, "verschluesseln")
                print(f"\n🔒 Verschlüsselter Code: {geheimtext}")
            except ValueError:
                print("🔴 Fehler: Der Schlüssel muss eine ganze Zahl sein!")
            
        elif auswahl == "2":
            text = input("Gib den verschlüsselten Code ein: ")
            try:
                zahl = int(input("Gib die passende Schlüsselzahl ein: "))
                klartext = code_verarbeiten(text, zahl, "entschluesseln")
                print(f"\n🔓 Entschlüsselter Text: {klartext}")
            except ValueError:
                print("🔴 Fehler: Der Schlüssel muss eine ganze Zahl sein!")
            
        elif auswahl == "3":
            print("Programm beendet. Bleib sicher!")
            break  # Bricht die Endlosschleife ab und schließt das Programm
        else:
            print("🔴 Ungültige Eingabe! Bitte wähle 1, 2 oder 3.")

# Der Einstiegspunkt für Python
if __name__ == '__main__':
    main()
