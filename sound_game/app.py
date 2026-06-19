from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# 1. Deine Berechnungs-Funktion (Dein Backend-Gehirn)
def berechne_sparzeit(startkapital, sparrate, zielsumme):
    aktuelles_geld = startkapital
    monate = 0
    
    while aktuelles_geld < zielsumme:
        aktuelles_geld = aktuelles_geld + sparrate
        monate = monate + 1
        
        if monate % 12 == 0:
            aktuelles_geld = aktuelles_geld * 1.02
    
    return monate           


@app.route('/')
def startseite():
    return render_template('index.html')


# 2. Der Startknopf für die Webseite (Nimmt die Daten entgegen)
@app.route('/berechne', methods=['POST'])
def daten_verarbeiten():
    daten = request.json
    start = int(daten["startkapital"])
    rate = int(daten["sparrate"])
    ziel = int(daten["zielsumme"])
    
    # Hier wird deine Funktion aufgerufen
    ergebnis = berechne_sparzeit(start, rate, ziel)
    
    return jsonify({"monate": ergebnis})


if __name__ == '__main__':
    app.run(debug=True)
