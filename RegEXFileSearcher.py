import re, os # Importerer modulene og funksjonene til regex og os

def process_user_input(user_input):
    # Fjerner ekstra mellomrom og deretter erstatter dem med \s+ som betyr 
    # i regex et eller flere mellomrom
    user_input = re.sub(r"\s\s+" , " ", user_input)
    user_input = user_input.replace(' ', r'\s+')

    # Konverterer dereter til en rå streng for regex
    raw_uInput = rf"{user_input}"

    # Returnerer den nye strengen
    return raw_uInput

# Leser brukerens input og deretter sender den til Process user input funksjonen
user = input("Enter name you wanna search:\n")
processed_string = process_user_input(user)

# Sjekker om strengen som kommer fra process user unput funksjonen er tom
if processed_string:
    # Åpner filen EleverVG2IT.txt i mappen filen ligger i med utf-16 encoding som filen har
    with open(os.path.join(os.path.dirname(__file__), 'EleverVG2IT.txt'), 'r', encoding='utf-16') as file:
        # Leser filen linje for linje
        for line_num, line in enumerate(file, 1):
            # Søker etter det brukeren skrev inn med regex comandoene ved bruk av regex
            match = re.search(processed_string, line)
            # hvis regex finner match
            if match:
                # da printes det ut en f string som sier user inputen linjen som filen er på
                # starten på hvor den fant dataen i linjen og slutten
                print(f"Found {user} at line {line_num} and starts at {match.start()} and ends at {match.end()}")