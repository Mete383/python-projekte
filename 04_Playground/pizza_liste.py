player = "Mete"
einkaufsliste = []

while True:
    antwort = input("Magst du Pizza? (ja/nein): ")

    if antwort == "ja":
        print("Dann schreibe ich dir alles was du für eine Pizza brauchst!")
        einkaufsliste.append("Salami")
        einkaufsliste.append("Teig")
        einkaufsliste.append("Tomatensauce")
        break
    elif antwort == "nein":
        print("Okey, dann nächstes Mal.")
        break
    else:
        print("Bitte tippe nur 'ja' oder 'nein' ein!")

print("Hier ist deine Einkaufsliste für Pizza:")
print(einkaufsliste)
