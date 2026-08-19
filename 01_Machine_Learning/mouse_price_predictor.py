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

# Name der lokalen SQLite-Datenbankdatei
DB_NAME = "Maus.db"

# Globale Variablen: Festgelegte Kategorien für die Datengenerierung und Benutzereingabe
ZUSTAENDE = ("Wie neu", "Gut", "Mittel", "Schlecht")
MARKEN = ("Logitech", "Razer", "Corsair", "SteelSeries", "Glorious", "Asus", "MSI")
DPI_STUFEN = ("8000 DPI", "16000 DPI", "26000 DPI")
NUTZUNGEN = ("Kabellos", "Kabelgebunden")

def SQL_Datenbank_erstellen():
    """Erstellt die SQLite-Datenbank und die Tabelle, falls sie noch nicht existieren."""
    with sqlite3.connect(DB_NAME) as verbindung:
        cursor = verbindung.cursor()
        # Tabelle für die Mausdaten mit den entsprechenden Spalten anlegen
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS maeuse (
                id INTEGER PRIMARY KEY, 
                marke TEXT, 
                modell TEXT, 
                dpi TEXT, 
                zustand TEXT, 
                nutzung TEXT, 
                preis REAL
            )
        """)
        # Vorherige Einträge löschen, um bei jedem Start mit frischen Daten zu arbeiten
        cursor.execute("DELETE FROM maeuse")

def generiere_1000_Maus_daten():
    """Generiert 1000 zufällige Maus-Datensätze basierend auf vordefinierten Logiken."""
    maus_liste = []
    
    with sqlite3.connect(DB_NAME) as verbindung:
        cursor = verbindung.cursor()

        for i in range(1000):
            # Zufällige Auswahl der Eigenschaften
            m = random.choice(MARKEN)
            z = random.choice(ZUSTAENDE)
            d = random.choice(DPI_STUFEN)
            n = random.choice(NUTZUNGEN)
            modell = f"Modell {random.randint(1, 3)}"

            # Basispreis-Logik: Bestimmt den Startpreis je nach Marke
            if m == "Logitech": basispreis = 70
            elif m == "Razer": basispreis = 90
            elif m == "Corsair": basispreis = 65
            elif m == "SteelSeries": basispreis = 60
            elif m == "Glorious": basispreis = 80
            elif m == "Asus": basispreis = 75
            else: basispreis = 55
                
            # Preisanpassung basierend auf dem Zustand
            if z == "Wie neu": basispreis += 30
            elif z == "Gut": basispreis += 15
            elif z == "Mittel": basispreis -= 10
            elif z == "Schlecht": basispreis -= 30
                
            # Preisanpassung basierend auf den DPI
            if d == "26000 DPI": basispreis += 25
            elif d == "16000 DPI": basispreis += 10
            else: basispreis += 0
                
            # Aufpreis für kabellose Mäuse
            if n == "Kabellos": basispreis += 30

            # Realistische Preisabweichung einbauen (+/- 10 Euro) und Mindestpreis von 10 Euro sichern
            endpreis = max(10, basispreis + random.randint(-10, 10))
            maus_liste.append((m, modell, d, z, n, round(endpreis, 2)))
                            
        # Effizientes Einfügen aller 1000 Datensätze in die SQL-Datenbank
        cursor.executemany("""
            INSERT INTO maeuse (marke, modell, dpi, zustand, nutzung, preis) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, maus_liste)
        print(f"📊 Daten-Generator: Erfolgreich {len(maus_liste)} Mäuse erzeugt!")

def daten_laden_von_db() -> pd.DataFrame:
    """Lädt die erzeugten Daten aus der SQL-Datenbank in ein Pandas DataFrame."""
    try:
        with sqlite3.connect(DB_NAME) as verbindung:
            sql_befehl = "SELECT marke, modell, dpi, zustand, nutzung, preis FROM maeuse"
            # Wandelt das SQL-Ergebnis direkt in eine tabellarische Pandas-Struktur um
            return pd.read_sql_query(sql_befehl, verbindung)
    except Exception as e:
        print(f"❌ Fehler beim Laden der Daten: {e}")
        return pd.DataFrame()

def pipeline_trainieren_und_speichern(df: pd.DataFrame):
    """Bereitet die Daten vor, trainiert das ML-Modell, wertet es aus und speichert es."""
    if df.empty:
        print("❌ Keine Daten zum Trainieren vorhanden.")
        return

    # Aufteilung in Features (X - Eigenschaften) und Target (y - Zielwert/Preis)
    X = df[['marke', 'modell', 'dpi', 'zustand', 'nutzung']]
    y = df['preis']

    # Aufteilung in Trainingsdaten (80%) und Testdaten (20%)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # ColumnTransformer: Konvertiert Textkategorien (Strings) mittels OneHotEncoder in Zahlen (0 und 1)
    übersetzer_maschine = ColumnTransformer(
        transformers=[
            ('onehot', OneHotEncoder(handle_unknown='ignore'), ['marke', 'modell', 'dpi', 'zustand', 'nutzung'])
        ],
        remainder='passthrough'
    )

    # Machine Learning Pipeline: Verknüpft die Datenvorbereitung und das KI-Modell (RandomForest)
    fließband = Pipeline(steps=[
        ('übersetzer', übersetzer_maschine),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    # KI-Modell mit den Trainingsdaten trainieren
    fließband.fit(X_train, y_train)

    # Vorhersagen auf den unbekannten Testdaten generieren
    y_pred = fließband.predict(X_test)
    # Berechnen des durchschnittlichen Fehlers (MAE)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"📊 Mean Absolute Error (MAE) auf Testdaten: {mae:.2f} €")

    # Speichert die gesamte Pipeline (inkl. Vorbereitung & Modell) als Datei ab
    joblib.dump(fließband, "maus_pipeline.pkl")
    print("💾 Fließband erfolgreich gespeichert als 'maus_pipeline.pkl'")        

    # Erstellt ein Scatter-Plot-Diagramm zur Visualisierung der Vorhersagegenauigkeit
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2) # Optimale Linie
    plt.xlabel('Tatsächliche Preise')
    plt.ylabel('Vorhergesagte Preise')
    plt.title('Leistungsüberprüfung des Maus-Fließbands')
    plt.show()

def sichere_eingabe(aufforderung, erlaubte_liste):
    """Validiert die Benutzereingabe im Terminal, um Tippfehler abzufangen."""
    while True:
        eingabe = input(aufforderung).strip()
        if eingabe in erlaubte_liste:
            return eingabe
        else:
            print(f"❌ Ungültige Eingabe. Bitte wählen Sie aus: {', '.join(erlaubte_liste)}")

def zeige_merkmal_wichtigkeit():
    """Analysiert und gibt aus, welche Eigenschaften (Features) den größten Einfluss auf den Preis haben."""
    # Geladenes Modell analysieren
    pipeline = joblib.load("maus_pipeline.pkl")
    uebersetzer = pipeline.named_steps['übersetzer']
    ki_gehirn = pipeline.named_steps['regressor']

    # Namen der transformierten Spalten und deren Gewichtung auslesen
    spalten_namen = uebersetzer.get_feature_names_out()
    wichtigkeiten = ki_gehirn.feature_importances_

    # In einer übersichtlichen Tabelle abspeichern und sortieren
    wichtigkeits_df = pd.DataFrame({
        'Merkmal': spalten_namen,
        'Wichtigkeit (%)': wichtigkeiten * 100
    }).sort_values(by='Wichtigkeit (%)', ascending=False)
    
    print("\n" + "=" * 50)
    print("📊 RELEVANZ-ANALYSE: WORAUF ACHTET DIE KI AM MEISTEN?")
    print("=" * 50)
    print(wichtigkeits_df.head(8).to_string(index=False)) # Top 8 Merkmale anzeigen
    print("=" * 50)

# Hauptprogramm (wird nur ausgeführt, wenn diese Datei direkt gestartet wird)
if __name__ == "__main__":
    print("🚀 Starte automatisierte Maus-Pipeline...")
    print("=" * 50)
    
    # 1. Pipeline-Schritte: Datenbank anlegen, Daten füttern, auslesen und KI trainieren
    SQL_Datenbank_erstellen()
    generiere_1000_Maus_daten()
    meine_daten = daten_laden_von_db()
    pipeline_trainieren_und_speichern(meine_daten)
    
    # 2. Wichtigkeitsanalyse der Features ausgeben
    zeige_merkmal_wichtigkeit()
    
    # 3. Das soeben gespeicherte Fließband direkt für interaktive Vorhersagen laden
    modell_gehirn = joblib.load("maus_pipeline.pkl")
    
    # --- INTERAKTIVE SCHLEIFE ---
    while True:
        print("\n" + "=" * 50)
        print("🔮 INTERAKTIVE MAUS-PREISVORHERSAGE")
        print("=" * 50)
        
        # Inputs über das Terminal abfragen
        eingabe_marke = sichere_eingabe("Welche Marke? (z.B. Logitech, Razer, Corsair): ", MARKEN)
        eingabe_modell = sichere_eingabe("Welches Modell? (z.B. Modell 1, Modell 2, Modell 3): ", [f"Modell {i}" for i in range(1, 4)])
        eingabe_dpi = sichere_eingabe("Wie viel DPI? (8000 DPI, 16000 DPI, 26000 DPI): ", DPI_STUFEN)
        eingabe_zustand = sichere_eingabe("Welcher Zustand? (Wie neu, Gut, Mittel, Schlecht): ", ZUSTAENDE)
        eingabe_nutzung = sichere_eingabe("Welche Nutzung? (Kabellos, Kabelgebunden): ", NUTZUNGEN)

        # Inputs in exakt dieselbe Dataframe-Struktur bringen wie beim Training
        neue_maus_df = pd.DataFrame([{
            'marke': eingabe_marke,
            'modell': eingabe_modell,
            'dpi': eingabe_dpi,
            'zustand': eingabe_zustand,
            'nutzung': eingabe_nutzung
        }])
        
        # Preis schätzen lassen
        geschätzter_preis = float(modell_gehirn.predict(neue_maus_df)[0])
        
        print("-" * 50)
        print(f"💰 Der geschätzte Preis für diese Maus beträgt: {geschätzter_preis:.2f} €")
        print("=" * 50)
        
        # Abfrage für eine weitere Runde oder Beenden
        nochmal = input("\nMöchtest du eine weitere Maus schätzen lassen? (ja/nein): ").strip().lower()
        if nochmal != 'ja':
            print("\n👋 Programm beendet. Bis zum nächsten Mal!")
            break
