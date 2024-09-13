import cv2, socket, threading, base64, imutils, os, random, numpy as np
import time

BUFFERSIZE = 65536
host_ip = "localhost"  # client properties
port = 3000
name = "Riot"

# setter op UDP client socket
UDPCientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPCientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFERSIZE)

# Registerer client-en med serveren
UDPCientSocket.sendto(f"SIGNUP_TAG:{name}".encode(), (host_ip, port))

# setter opp variablene og setter opp kamra for camraet
global fps, st, fram_to_count, cnt
fps, st, fram_to_count, cnt = (0, 0, 20, 0)
vid = cv2.VideoCapture(os.path.join(os.path.dirname(__file__), 'videos/test.mp4'))

def receive():
    global fps, st, fram_to_count, cnt
    print("Receiving video stream...")

    while True:
        try:
            # henter pakkene
            packet, _ = UDPCientSocket.recvfrom(BUFFERSIZE)
            
            # hånterer failed pakker
            if len(packet) < 100:
                print("Skipping control message.")
                continue
            
            # decoder dataen og converterer tilbake til bilde format
            data = base64.b64decode(packet)
            npdata = np.frombuffer(data, dtype=np.uint8)
            frame = cv2.imdecode(npdata, 1)
            
            # viser framen med FPS count
            frame = cv2.putText(frame, "FPS:" + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imshow("Receiving Video", frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break  # Exit hvis 'q' is pressed

            # FPS kalkulering
            if cnt == fram_to_count:
                try:
                    fps = round(fram_to_count / (time.time() - st))
                    st = time.time()
                    cnt = 0
                except:
                    pass
            cnt += 1
        except Exception as e:
            print(f"Error receiving frame: {e}")
            break

    cv2.destroyAllWindows()
    UDPCientSocket.close()

def send():
    while vid.isOpened():
        # henter data fra kamra og sjekker hvis den ikke failer
        ret, frame = vid.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        # compresser
        frame = imutils.resize(frame, width=400)
        encoded, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        message = base64.b64encode(buffer)
        
        # sender dataen
        try:
            UDPCientSocket.sendto(message, (host_ip, port))
        except Exception as e:
            print(f"Error sending frame: {e}")
            break
        
        # hviser enkelt hva som blir sendt
        cv2.imshow("TRANSMITTING VIDEO", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            UDPCientSocket.close()
            break

        time.sleep(0.03)  # kontrolerer framerate-en

# starter threadsa
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=send)
t1.start()
t2.start()
