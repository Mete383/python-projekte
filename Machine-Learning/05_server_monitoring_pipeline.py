import requests
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from sklearn.tree import DecisionTreeClassifier

# ====================================================================
# STEP 1: API (Echte Live-Außentemperatur für Böblingen holen)
# ====================================================================
url = "https://open-meteo.com"

antwort = requests.get(url)
daten = antwort.json()

aussentemperatur = daten["current"]["temperature_2m"]
print(f"Aktuelle Außentemperatur am Serverstandort: {aussentemperatur} °C")

# ====================================================================
# STEP 2: PANDAS (Temperatur-Entwicklung im Serverraum prüfen)
# ====================================================================
raum_temps = [21.5, 22.0, 22.8, 23.5, aussentemperatur]
daten_woerterbuch = {"Temperatur": raum_temps}
tabelle = pd.DataFrame(daten_woerterbuch)

tabelle["Temp_Aenderung"] = tabelle["Temperatur"].pct_change()
tabelle["Temp_Aenderung"] = tabelle["Temp_Aenderung"].fillna(0) 
print("\n--- PANDAS DATENABGLEICH ---")
print(tabelle)

# ====================================================================
# STEP 3: SQL (System-Logs in die Datenbank schreiben)
# ====================================================================
verbindung = sqlite3.connect("Temperatur.db")
cursor = verbindung.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS server_logs (temp REAL, aenderung REAL)")

letzte_aenderung = tabelle["Temp_Aenderung"].values[-1]

cursor.execute("INSERT INTO server_logs VALUES (?, ?)", [aussentemperatur, letzte_aenderung])
verbindung.commit()
print("\n[SQL]: Die Server-Logdaten wurden erfolgreich gespeichert!")

# ====================================================================
# STEP 4: NUMPY (Server-Auslastung analysieren)
# ====================================================================
cpu_auslastung = np.array([45, 55, 85, 90, 60])

auslastung_schnitt = np.mean(cpu_auslastung)
cpu_schwankung = np.std(cpu_auslastung)

print("\n--- NUMPY HARDWARE-ANALYSE ---")
print("Durchschnittliche CPU-Auslastung:", auslastung_schnitt)
print("Schwankung der CPU-Auslastung:", cpu_schwankung)

# ====================================================================
# STEP 5: MACHINE LEARNING (Entscheidungsbaum für Alarmstufe)
# ====================================================================
model = DecisionTreeClassifier()

# Trainingsdaten: [Temperatur_hoch, CPU_hoch]
X_train = np.array([[1, 1], [1, 0], [0, 1], [0, 0]])
y_train = np.array([1, 0, 1, 0])  # 1 = ALARM 🚨, 0 = Alles OK ✅

# Der aktuelle Zustand des Systems wird geprüft
aktueller_zustand = [1 if aussentemperatur > 23 else 0, 1 if cpu_auslastung[-1] > 80 else 0]

model.fit(X_train, y_train)
prediction = model.predict([aktueller_zustand])
print("System-Status der KI (1 = ALARM 🚨, 0 = Alles OK ✅):", prediction)

# ====================================================================
# STEP 6: MATPLOTLIB (System-Diagramm zeichnen)
# ====================================================================
X_stunden = np.arange(1, len(cpu_auslastung) + 1)

plt.plot(X_stunden, cpu_auslastung)
plt.title("Server CPU-Auslastung Report")
plt.xlabel("Stunden")
plt.ylabel("Auslastung in %")

chart_dateiname = "server_report.png"
plt.savefig(chart_dateiname)
plt.close()

# ====================================================================
# STEP 7: SMTPLIB (Notfall-Mail vorbereiten & senden)
# ====================================================================
msg = MIMEMultipart()
msg["From"] = "deine_mail@gmail.com"
msg["To"] = "deine_mail@gmail.com"
msg["Subject"] = f"IT-REPORT: System-Status-Alarmstufe ist {prediction}"

with open(chart_dateiname, "rb") as f:
    bild_daten = f.read()

msg.attach(MIMEImage(bild_daten))

# Hier ist die korrigierte Server-Adresse ohne "://"
server = smtplib.SMTP("://gmail.com", 587)
server.starttls()
server.login("deine_mail@gmail.com", "dein_passwort")

server.sendmail(msg["From"], msg["To"], msg.as_string())
server.quit()

print("\n[MEISTERSTÜCK ERFOLGREICH]: Der Server-Wächter-Report wurde komplett generiert und versendet!")
