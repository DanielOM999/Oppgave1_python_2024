import cv2, socket, threading, base64, numpy as np
import time

BUFFERSIZE = 65536
host_ip = "localhost"  # Update this with the server's IP
port = 3000
name = "Riot"

# Setup client socket
UDPCientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPCientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFERSIZE)

# Register client with the server
UDPCientSocket.sendto(f"SIGNUP_TAG:{name}".encode(), (host_ip, port))

global fps, st, fram_to_count, cnt
fps, st, fram_to_count, cnt = (0, 0, 20, 0)

def receive():
    global fps, st, fram_to_count, cnt
    print("Receiving video stream...")
    
    while True:
        try:
            packet, _ = UDPCientSocket.recvfrom(BUFFERSIZE)
            data = base64.b64decode(packet, " /")
            npdata = np.frombuffer(data, dtype=np.uint8)
            frame = cv2.imdecode(npdata, 1)
            
            # Display the frame with FPS count
            frame = cv2.putText(frame, "FPS:" + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imshow("Receiving Video", frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break  # Exit if 'q' is pressed

            # FPS calculation
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

# Start the thread to receive the video stream
t1 = threading.Thread(target=receive)
t1.start()
