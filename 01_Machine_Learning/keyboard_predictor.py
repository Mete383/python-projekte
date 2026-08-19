import sqlite3
import random
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

DB_NAME = "Tastatur.db"

# Globale Variablen, damit alle Funktionen darauf zugreifen können
ZUSTAENDE = ("Wie neu", "Gut", "Mittel", "Schlecht")
MARKEN = ("Logitech", "Razer", "Corsair", "SteelSeries", "HyperX", "Asus", "MSI")
LAYOUTS = ("QWERTZ", "QWERTY", "AZERTY", "DVORAK")
NUTZUNGEN = ("Bluetooth", "Kabelgebunden")

def SQL_Datenbank_erstellen():
    with sqlite3.connect(DB_NAME) as verbindung:
        cursor = verbindung.cursor()
        # Tabelle mit ALLEN Features erstellen, die wir später brauchen
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tastaturen (
                id INTEGER PRIMARY KEY, 
                marke TEXT, 
                modell TEXT, 
                layout TEXT, 
                zustand TEXT, 
                nutzung TEXT, 
                preis REAL
            )
        """)
        cursor.execute("DELETE FROM tastaturen") # Alte Daten löschen

def generiere_1000_Tastatur_daten():
    tastatur_liste = []
    
    with sqlite3.connect(DB_NAME) as verbindung:
        cursor = verbindung.cursor()

        for i in range(1000):
            m = random.choice(MARKEN)
            z = random.choice(ZUSTAENDE)
            l = random.choice(LAYOUTS)
            n = random.choice(NUTZUNGEN)
            modell = f"Modell {random.randint(1, 3)}" # Wichtig für den OneHotEncoder

            # Basispreis-Logik
            if m == "Logitech": basispreis = 100
            elif m == "Razer": basispreis = 150
            elif m == "Corsair": basispreis = 120
            elif m == "SteelSeries": basispreis = 130
            elif m == "HyperX": basispreis = 110
            elif m == "Asus": basispreis = 140
            else: basispreis = 125
                
            if z == "Wie neu": basispreis += 50
            elif z == "Gut": basispreis += 20
            elif z == "Mittel": basispreis -= 20
            elif z == "Schlecht": basispreis -= 50
                
            if l == "QWERTZ": basispreis += 10
            elif l == "QWERTY": basispreis += 5
            elif l == "AZERTY": basispreis -= 5
            else: basispreis -= 10
                
            if n == "Bluetooth": basispreis += 20

            # Realistische Preisabweichung
            endpreis = max(15, basispreis + random.randint(-15, 15))
            
            tastatur_liste.append((m, modell, l, z, n, round(endpreis, 2)))
                            
        cursor.executemany("""
            INSERT INTO tastaturen (marke, modell, layout, zustand, nutzung, preis) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, tastatur_liste)
        print(f"📊 Daten-Generator: Erfolgreich {len(tastatur_liste)} Tastaturen erzeugt!")

def daten_laden_von_db() -> pd.DataFrame:
    try:
        with sqlite3.connect(DB_NAME) as verbindung:
            sql_befehl = "SELECT marke, modell, layout, zustand, nutzung, preis FROM tastaturen"
            return pd.read_sql_query(sql_befehl, verbindung)
    except Exception as e:
        print(f"❌ Fehler beim Laden der Daten: {e}")
        return pd.DataFrame()

def pipeline_trainieren_und_speichern(df: pd.DataFrame):
    if df.empty:
        print("❌ Keine Daten zum Trainieren vorhanden.")
        return

    # Features (X) und Zielwert (y) festlegen (alles kleingeschrieben)
    X = df[['marke', 'modell', 'layout', 'zustand', 'nutzung']]
    y = df['preis']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    übersetzer_maschine = ColumnTransformer(
        transformers=[
            ('onehot', OneHotEncoder(handle_unknown='ignore'), ['marke', 'modell', 'layout', 'zustand', 'nutzung'])
        ],
        remainder='passthrough'
    )

    fließband = Pipeline(steps=[
        ('übersetzer', übersetzer_maschine),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    fließband.fit(X_train, y_train)

    y_pred = fließband.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"📊 Mean Absolute Error (MAE) auf Testdaten: {mae:.2f} €")

    joblib.dump(fließband, "tastatur_pipeline.pkl")
    print("💾 Fließband erfolgreich gespeichert als 'tastatur_pipeline.pkl'")        

    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel('Tatsächliche Preise')
    plt.ylabel('Vorhergesagte Preise')
    plt.title('Leistungsüberprüfung des Tastatur-Fließbands')
    plt.show()

def sichere_eingabe(aufforderung, erlaubte_liste):
    while True:
        eingabe = input(aufforderung).strip()
        if eingabe in erlaubte_liste:
            return eingabe
        else:
            print(f"❌ Ungültige Eingabe. Bitte wählen Sie aus: {', '.join(erlaubte_liste)}")

def zeige_merkmal_wichtigkeit():
    # 1. Zuerst laden wir das Fließband
    pipeline = joblib.load("tastatur_pipeline.pkl")

    # 2. Dann holen wir die Bausteine heraus
    uebersetzer = pipeline.named_steps['übersetzer']
    ki_gehirn = pipeline.named_steps['regressor']

    # 3. JETZT können wir die Spaltennamen und Wichtigkeiten auslesen
    spalten_namen = uebersetzer.get_feature_names_out()
    wichtigkeiten = ki_gehirn.feature_importances_

    # 4. In eine schöne Tabelle packen und sortieren
    wichtigkeits_df = pd.DataFrame({
        'Merkmal': spalten_namen,
        'Wichtigkeit (%)': wichtigkeiten * 100
    }).sort_values(by='Wichtigkeit (%)', ascending=False)
    
    print("\n" + "=" * 50)
    print("📊 RELEVANZ-ANALYSE: WORAUF ACHTET DIE KI AM MEISTEN?")
    print("=" * 50)
    print(wichtigkeits_df.head(8).to_string(index=False))
    print("=" * 50)

if __name__ == "__main__":
    print("🚀 Starte automatisierte Profi-Pipeline...")
    print("=" * 50)
    
    # 1. Daten generieren und Modell trainieren
    SQL_Datenbank_erstellen()
    generiere_1000_Tastatur_daten()
    meine_daten = daten_laden_von_db()
    pipeline_trainieren_und_speichern(meine_daten)
    
    # 2. Relevanz-Analyse deiner selbst geschriebenen Funktion anzeigen
    zeige_merkmal_wichtigkeit()
    
    # 3. Das soeben gespeicherte Fließband direkt laden
    modell_gehirn = joblib.load("tastatur_pipeline.pkl")
    
    # --- AB HIER STARTET DIE ENDLOSSCHLEIFE ---
    while True:
        print("\n" + "=" * 50)
        print("🔮 INTERAKTIVE PREISVORHERSAGE")
        print("=" * 50)
        
        # Inputs über das Terminal abfragen (Deine sicheren Abfragen)
        eingabe_marke = sichere_eingabe("Welche Marke? (z.B. Razer, Logitech, Corsair): ", MARKEN)
        eingabe_modell = sichere_eingabe("Welches Modell? (z.B. Modell 1, Modell 2, Modell 3): ", [f"Modell {i}" for i in range(1, 4)])
        eingabe_layout = sichere_eingabe("Welches Layout? (z.B. QWERTZ, QWERTY): ", LAYOUTS)
        eingabe_zustand = sichere_eingabe("Welcher Zustand? (z.B. Wie neu, Gut, Mittel, Schlecht): ", ZUSTAENDE)
        eingabe_nutzung = sichere_eingabe("Welche Nutzung? (z.B. Bluetooth, Kabelgebunden): ", NUTZUNGEN)

        # Inputs in exakt dieselbe Dataframe-Struktur pressen
        neue_tastatur_df = pd.DataFrame([{
            'marke': eingabe_marke,
            'modell': eingabe_modell,
            'layout': eingabe_layout,
            'zustand': eingabe_zustand,
            'nutzung': eingabe_nutzung
        }])
        
        # Preis schätzen lassen
        geschätzter_preis = float(modell_gehirn.predict(neue_tastatur_df)[0])
        
        print("-" * 50)
        print(f"💰 Der geschätzte Preis für diese Tastatur beträgt: {geschätzter_preis:.2f} €")
        print("=" * 50)
        
        # Repariertes Ende: Abfrage für eine weitere Runde oder Beenden
        nochmal = input("\nMöchtest du eine weitere Tastatur schätzen lassen? (ja/nein): ").strip().lower()
        if nochmal != 'ja':
            print("\n👋 Programm beendet. Bis zum nächsten Mal!")
            break
