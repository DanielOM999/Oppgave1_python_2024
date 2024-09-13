import cv2, imutils, socket, os, base64, time, threading, queue, random
import numpy as np

BUFFERSIZE = 65536
UDPClient = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClient.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFERSIZE)
UDPClient.bind(("localhost", random.randint(8000, 9000)))

vid = cv2.VideoCapture(os.path.join(os.path.dirname(__file__), 'videos/test.mp4'))
global fps, st, fram_to_count, cnt
fps,st,fram_to_count,cnt = (0,0,20,0)

name = "roa"

def receive():
        try:
            print("Hello!")
            packet, _ = UDPClient.recvfrom(BUFFERSIZE)
            data = base64.b64decode(packet, " /")
            ndata = np.fromstring(data,dtype=np.uint8)
            frame = cv2.imdecode(ndata,1)
            frame = cv2.putText(frame,"FPS:"+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
            cv2.imshow("RECIVING VIDEO", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                UDPClient.close()
                exit()
            if cnt == fram_to_count:
                try:
                    fps = round(fram_to_count/(time.time()-st))
                    st=time.time()
                    cnt=0
                except:
                    pass
            cnt+=1
        except Exception as err:
            print(err)

def transmitt():
    global fps, st, fram_to_count, cnt
    WIDTH=400
    while(vid.isOpened()):
        ret, frame = vid.read()
        if not ret:
            print("Video ended")
            exit()
        else:
            frame = imutils.resize(frame,width=WIDTH)
            encoded,buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY,80])
            message = base64.b64encode(buffer)
            UDPClient.sendto(message, ("localhost", 3000))
            frame = cv2.putText(frame,"FPS:"+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
            cv2.imshow("TRANSMITTING VIDEO", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                UDPClient.close()
                exit()
            if cnt == fram_to_count:
                try:
                    fps = round(fram_to_count/(time.time()-st))
                    st=time.time()
                    cnt=0
                except:
                    pass
        cnt+=1

t = threading.Thread(target=receive)
t2 = threading.Thread(target=transmitt)
t.daemon = True
t2.daemon = True
t.start()
t2.start()

UDPClient.sendto(f"SIGNUP_TAG:{name}".encode(), ("localhost", 3000))

while True:
    pass