# Importerer nødvendige biblioteker
import cv2, imutils, socket
import numpy as np
import time
import base64

# Definerer bufferstørrelse for dataoverføring
BUFFERSIZE = 65536
# Setter opp UDP-klientsocket
UDPCientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Øker mottaksbufferstørrelsen
UDPCientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFERSIZE)
# Henter enhetens navn
host_name = socket.gethostname()
# Definerer IP-adressen til enheten
host_ip = "10.1.120.199"
# Angir porten som brukes
port = 3000
# Melding som sendes til serveren ved conection
message = b'Hello World'

# Sender meldingen til serveren
UDPCientSocket.sendto(message, (host_ip,port))
# Variabler for FPS-beregning
fps,st,fram_to_count,cnt = (0,0,20,0)

while True:
    # Mottar datapakke fra serveren
    packet,_ = UDPCientSocket.recvfrom(BUFFERSIZE)
    # Dekoder base64-data til originalt bildeformat
    data = base64.b64decode(packet, " /")
    # Konverterer data til numpy-array for bildebehandling
    ndata = np.frombuffer(data,dtype=np.uint8)
    # Dekoder bildet fra array-format
    frame = cv2.imdecode(ndata,1)
    # Legger til FPS-tekst på bildet
    frame = cv2.putText(frame,"FPS:"+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
    # Viser det mottatte videobildet
    cv2.imshow("RECIVING VIDEO", frame)
    # Venter på tastetrykk (for å avslutte)
    key = cv2.waitKey(1) & 0xFF
    # Hvis "q" trykkes, avslutter programmet
    if key == ord("q"):
        # Lukker socketen
        UDPCientSocket.close()
        break
    # Hvis antall bilder har nådd counten
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