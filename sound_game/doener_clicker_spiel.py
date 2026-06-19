from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Hier speichert Python deinen Döner-Spielstand
spielstand = {
    "doener": 0,           
    "doener_roboter": 0,   
    "upgrade_kosten": 10
}

@app.route('/')
def startseite():
    return render_template('index.html')

# Python bekommt Bescheid, wenn du Döner schneidest
@app.route('/klick', methods=['POST'])
def klick_verarbeiten():
    spielstand["doener"] += 1
    # Die Döner-Roboter schneiden automatisch mit
    spielstand["doener"] += spielstand["doener_roboter"]
    return jsonify(spielstand)

# Deine DEF-Funktion für den Upgrade-Kauf
@app.route('/kaufe_upgrade', methods=['POST'])
def upgrade_kaufen():
    # Prüfen, ob du genug Döner für das Upgrade hast
    if spielstand["doener"] >= spielstand["upgrade_kosten"]:
        spielstand["doener"] -= spielstand["upgrade_kosten"] 
        spielstand["doener_roboter"] += 1                     
        spielstand["upgrade_kosten"] = int(spielstand["upgrade_kosten"] * 1.5) 
        return jsonify({"erfolg": True, "spielstand": spielstand})
    
    return jsonify({"erfolg": False, "nachricht": "Nicht genug Döner!"})

if __name__ == '__main__':
    app.run(debug=True)
