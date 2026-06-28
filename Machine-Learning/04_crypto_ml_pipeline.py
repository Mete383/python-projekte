import os  # Schon in Python eingebaut (für Dateien)
import sqlite3  # Schon in Python eingebaut (deine SQL-Datenbank!)
import requests  # Kennst du schon aus Phase 3 (für die API)
import pandas as pd  # Kennst du schon aus Phase 1 (für die CSV-Tabelle)
import numpy as np  # <-- DIESER IMPORT HAT GEFEHLT!
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# 1. LIVE-DATEN VON DER API HOLEN (Richtige API-URL!)
# 1. LIVE-DATEN VON DER NEUEN API HOLEN (CryptoCompare)
# 1. LIVE-DATEN VON DER FREIEN dRPC-API HOLEN
# 1. LIVE-DATEN VON DER OFFIZIELLEN BLOCKCHAIN-API HOLEN
# 1. LIVE-DATEN MIT EINEM BROWSER-AUSWEIS (HEADERS) HOLEN
url = "https://blockchain.info/ticker"

# Wir tun so, als wären wir ein normaler Internet-Browser
ausweis = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Wir übergeben den Ausweis beim Abrufen (headers=ausweis)
antwort = requests.get(url, headers=ausweis)
daten = antwort.json()

# Hier holen wir uns den aktuellen Euro-Preis
Bitcoin_preis = daten["EUR"]["last"]
print(f"Der aktuelle Preis von Bitcoin beträgt: {Bitcoin_preis} €")




# 2. IN CSV SPEICHERN MIT PANDAS
# 2. IN CSV SPEICHERN MIT PANDAS
neue_zeile = pd.DataFrame([[Bitcoin_preis]], columns=["Preis"])
csv_name = "bitcoin_preise.csv"

# Wir prüfen, ob die Datei schon existiert
if not os.path.isfile(csv_name):
    # Wenn NEIN: Datei neu erstellen UND die Überschrift "Preis" mitschreiben
    neue_zeile.to_csv(csv_name, index=False)
else:
    # Wenn JA: Einfach nur den neuen Preis unten anhängen (ohne neue Überschrift)
    neue_zeile.to_csv(csv_name, mode='a', header=False, index=False)

print("Der Preis wurde erfolgreich in der CSV-Datei gespeichert!")


# 3. IN SQL-DATENBANK SPEICHERN
verbindung = sqlite3.connect("krypto.db")
cursor = verbindung.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS bitcoin (preis REAL)")
cursor.execute("INSERT INTO bitcoin (preis) VALUES (?)", [Bitcoin_preis])
verbindung.commit()
print("Der Preis wurde erfolgreich in der SQL-Datenbank gespeichert!")

# 4. MACHINE LEARNING KI TRAINIEREN
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([56000, 56500, 57000, 57800, Bitcoin_preis])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

vorhersage = model.predict(X_test)

print("\n--- KI ERGEBNIS ---")
print("Echter Preis des Test-Werts:", y_test)
print("Vorhersage der KI für diesen Wert:", vorhersage)
