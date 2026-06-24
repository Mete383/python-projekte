woerter_liste = ["radar", "computer", "anna", "schule", "rentner", "python"]
palindrom_liste = [] # Hier kommen die richtigen Wörter rein

for wort in woerter_liste:
    # Drehe das aktuelle Wort um
    wort_rueckwaerts = wort[::-1]
    
    # WENN das Wort vorwärts gleich rückwärts ist...
    if wort == wort_rueckwaerts:
        # ...DANN füge es der palindrom_liste hinzu!
        palindrom_liste.append(wort)

# Am Ende geben wir die gefilterte Liste aus
print("Gefundene Palindrome:", palindrom_liste)
