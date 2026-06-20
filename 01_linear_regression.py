# ==============================================================================
# KAPITEL 1: LINEARE REGRESSION (Hauspreise vorhersagen)
# Playlist: Codebasics Machine Learning Tutorial
# ==============================================================================

# 1. Die KI-Werkzeuge importieren (laden)
from sklearn.linear_model import LinearRegression
import numpy as np

# 2. Daten vorbereiten (Größe in qm -> Preis in Euro)
# X (Features): 10 Häuser. WICHTIG: Immer in doppelten Klammern [[ ]] (2D-Array)
X = np.array([[30], [40], [50], [60], [80], [100], [120], [150], [170], [200]]) 

# y (Target): Die 10 passenden Preise. WICHTIG: X und y müssen gleich lang sein!
y = np.array([90000, 120000, 150000, 180000, 240000, 300000, 360000, 450000, 510000, 600000])

# 3. Das KI-Modell erstellen
ki_modell = LinearRegression()

# 4. DAS TRAINING (Die KI lernt den Zusammenhang zwischen qm und Preis)
ki_modell.fit(X, y)

# 5. DIE VORHERSAGE (Wir fragen die KI nach neuen Häusern mit 70, 85 und 130 qm)
haus_groesse_neu = np.array([[70], [85], [130]]) 
vorhersage = ki_modell.predict(haus_groesse_neu)

# 6. Ergebnisse mit einer Schleife ordentlich auf dem Bildschirm anzeigen
print("--- KI VORHERSAGEN ---")
for i in range(len(haus_groesse_neu)):
    groesse = haus_groesse_neu[i][0]  # Holt die reine Zahl aus den doppelten Klammern
    preis = vorhersage[i]             # Holt den passenden Preis
    print(f"Die KI schätzt den Preis für ein {groesse}qm Haus auf: {preis:.2f} Euro.")

# 7. DIE MATHEMATIK (Optional: Die gelernten Werte auslesen)
# Formel: y = m * x + b
print("\n--- MATHEMATISCHE WERTE ---")
print(f"Gelernter Quadratmeterpreis (m): {ki_modell.coef_[0]:.2f} Euro")
print(f"Theoretischer Basispreis bei 0 qm (b): {ki_modell.intercept_:.2f} Euro")
