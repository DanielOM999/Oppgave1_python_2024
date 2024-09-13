# Importerer Alle funksjonene Fra PIL Image, piexif og os
from PIL import Image
import piexif
import os

def removeEXIF():
    # Lager en liste av all EXIF dataen i bildet
    data = list(image.getdata())

    # Lager et nytt identisk bilde uten EXIF data
    image2 = Image.new(image.mode, image.size)

    # Fjerner all EXIF dataen fra bildet
    image2.putdata(data)

    # Lagrer det nye bildet
    image2.save(os.path.join(os.path.dirname(__file__), 'MainAfter.png'))

    print("REMOVED EXIF")

def addEXIF(data):
    # Lager et EXIF dictionary med et enkelt felt kalt banana
    exif_dict = {
        "0th": {
            piexif.ImageIFD.Make: data
        }
    }

    # Konverterer EXIF dictionary til byte-format
    exif_bytes = piexif.dump(exif_dict)

    # Lagrer bildet med den nye EXIF dataen
    image.save(os.path.join(os.path.dirname(__file__), 'MainAfter.png'), exif=exif_bytes)

    print("Added EXIF")

def readEXIF():
    # Leser EXIF dataen fra bildet
    exifData = image._getexif()
    print('exifData = ' + str(exifData))



while True:
    # Åpner filen fra en spesiel path
    image = Image.open(os.path.join(os.path.dirname(__file__), 'MainAfter.png'))

    # Ber brukeren om å lese, legge til eller fjerne EXIF data
    user = input("Wanna 'READ' 'WRITE' or 'REMOVE' EXIF data:\n")

    # Runner funksjonen for å lese EXIF data hvis brukeren velger 'read'
    if (user.lower() == "read"):
        readEXIF()

    # Runner funksjonen for å skrive EXIF data hvis brukeren velger 'write'
    elif (user.lower() == "write"):
        data = input("Enter Data: ")
        addEXIF(data)

    # Runner funksjonen for å fjerne EXIF data hvis brukeren velger 'remove'
    elif (user.lower() == "remove"):
        removeEXIF()

    # stopper programet hvis ingen av alternativene er sanne
    else:
        break