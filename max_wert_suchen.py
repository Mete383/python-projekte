highscores = [150, 320, 90, 410, 280]

# Wir starten mit der ersten Zahl als Rekord
hoechster_wert = highscores[0] 

for score in highscores:
    # WENN der aktuelle 'score' GRÖSSER ist als unser bisheriger 'hoechster_wert'...
    if score > hoechster_wert:
     
        # ...DANN wird der aktuelle 'score' unser neuer 'hoechster_wert'!
        hoechster_wert = score

print("Mein absoluter Highscore ist:", hoechster_wert)
