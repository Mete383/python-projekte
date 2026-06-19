from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Hier speichert Python deinen Spielstand
spielstand = {
    "beats": 0,
    "auto_clicker": 0,
    "upgrade_kosten": 10
}

@app.route('/')
def startseite():
    return render_template('index.html')

# Python bekommt Bescheid, wenn du klickst
@app.route('/klick', methods=['POST'])
def klick_verarbeiten():
    spielstand["beats"] += 1
    # Wenn du automatische Klicker hast, zählen wir die hier dazu
    spielstand["beats"] += spielstand["auto_clicker"]
    return jsonify(spielstand)

# Deine neue DEF-Funktion für den Upgrade-Kauf!
@app.route('/kaufe_upgrade', methods=['POST'])
def upgrade_kaufen():
    # Prüfen, ob du genug Beats für das Upgrade hast
    if spielstand["beats"] >= spielstand["upgrade_kosten"]:
        spielstand["beats"] -= spielstand["upgrade_kosten"] # Beats abziehen
        spielstand["auto_clicker"] += 1                     # Einen Auto-Klicker hinzufügen
        spielstand["upgrade_kosten"] = int(spielstand["upgrade_kosten"] * 1.5) # Upgrade teurer machen
        return jsonify({"erfolg": True, "spielstand": spielstand})
    
    return jsonify({"erfolg": False, "nachricht": "Nicht genug Beats!"})

if __name__ == '__main__':
    app.run(debug=True)
