import os
from flask import Flask, render_template, request, redirect, url_for

# Initialisierung der Flask-Applikation
app = Flask(__name__)

# In-Memory-Datenbank: Eine Liste aus JSON-ähnlichen Objekten (Dictionaries)
# Diese Struktur dient als temporärer Datenspeicher für die Code-Snippets
snippets = [
    {
        "id": 1,
        "title": "Flask App Grundgerüst",
        "language": "Python",
        "code": "from flask import Flask\napp = Flask(__name__)\n\nif __name__ == '__main__':\n    app.run(debug=True)"
    },
    {
        "id": 2,
        "title": "Tailwind Zentrieren",
        "language": "HTML/CSS",
        "code": "<div class='flex items-center justify-center min-h-screen'>\n  <!-- Inhalt -->\n</div>"
    }
]

# Route für die Startseite (Index)
# Ruft alle vorhandenen Snippets ab und übergibt sie an das HTML-Template
@app.route('/')
def index():
    # render_template sucht die Datei im Unterordner 'templates'
    return render_template('index.html', snippets=snippets)

# Route zur Verarbeitung neuer Snippets via HTTP POST-Methode
# Nimmt die Formulardaten entgegen und validiert diese vor dem Speichern
@app.route('/add', methods=['POST'])
def add_snippet():
    # Extrahieren der Formulardaten über die entsprechenden Input-Namen
    title = request.form.get('title')
    language = request.form.get('language')
    code = request.form.get('code')

    # Validierung: Nur speichern, wenn die Pflichtfelder befüllt sind
    if title and code:
        # Dynamische Generierung einer fortlaufenden ID basierend auf der Listenlänge
        new_id = len(snippets) + 1

        # Hinzufügen des neuen Snippet-Objekts zur Liste
        snippets.append({
            "id": new_id,
            "title": title,
            "language": language,
            "code": code
        })

    # Nach erfolgreichem Speichern erfolgt ein Redirect zurück auf die Startseite
    return redirect(url_for('index'))

# Hauptprogramm: Startet den lokalen Entwicklungsserver
if __name__ == '__main__':
    # debug=True aktiviert automatische Code-Reloads und den interaktiven Debugger
    app.run(debug=True)
