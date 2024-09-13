# Importerer nødvendige biblioteker
import cv2, imutils, socket
import numpy as np
import time
import base64

# Definerer bufferstørrelse for dataoverføring
BUFFERSIZE = 65536
# Setter opp UDP-socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Øker mottaksbufferstørrelsen
UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFERSIZE)
# Henter enhetens navn
host_name = socket.gethostname()
# Definerer IP-adressen til enheten
host_ip = "10.1.120.199"
# Angir porten som brukes
port = 3000
# Setter opp socket-adressen
socket_address = (host_ip, port)
# Binder socketen til adressen
UDPServerSocket.bind(socket_address)
print("Listening at:",socket_address)

# Starter videokameraet (0 er standardkamera altså webcamra)
vid = cv2.VideoCapture(0)
# Variabler for FPS-beregning
fps,st,fram_to_count,cnt = (0,0,20,0)

while True:
    # Mottar meldinger fra client-en
    msg,client_addr = UDPServerSocket.recvfrom(BUFFERSIZE)
    # Skriver ut client-ens adresse
    print("Client connected from:", client_addr)
    # Setter bredde for videobilder
    WIDTH=400
    # Sjekker om videoen kan åpnes
    while(vid.isOpened()):
        # Leser et bilde fra kameraet
        _,frame = vid.read()
        # Endrer størrelse på bildet
        frame = imutils.resize(frame,width=WIDTH)
        # setter bildet som JPEG
        encoded,buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY,80])
        # encoder bildet som base64
        message = base64.b64encode(buffer)
        # Sender bilde til client-en
        UDPServerSocket.sendto(message, client_addr)
        # Legger til FPS-tekst på bildet
        frame = cv2.putText(frame,"FPS:"+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        # Viser videoen med tekst
        cv2.imshow("TRANSMITTING VIDEO", frame)
        # Venter på tastetrykk (da for å avslutte)
        key = cv2.waitKey(1) & 0xFF
        # Hvis "q" trykkes, avslutter programmet
        if key == ord("q"):
            # Lukker socketen
            UDPServerSocket.close()
            break
        # Hvis antall bilder har nådd the count
        if cnt == fram_to_count:
            try:
                # Beregner FPS
                fps = round(fram_to_count/(time.time()-st))
                # Resetter starttidspunkt
                st=time.time()
                # Resetter counten
                cnt=0
            except:
                pass
        # Øker counten
        cnt+=1