import cv2, imutils, socket, os, base64, time, threading, queue
import numpy as np

messages = queue.Queue()
clients = []

BUFFERSIZE = 65536
UDPServer = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServer.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFERSIZE)
UDPServer.bind(("localhost", 3000))

# vid = cv2.VideoCapture(0)
# fps,st,fram_to_count,cnt = (0,0,20,0)

def recive():
    while True:
        try:
            message, addr = UDPServer.recvfrom(1024)
            print("hei")
            messages.put((message, addr))
        except:
            pass

def brodcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            print(addr, message)
            if addr not in clients:
                clients.append(addr)
                print(clients)
            for client in clients:
                try:
                    if message.decode().startswith("SIGNUP_TAG"):
                        name = message.decode()[message.decode().index(":")+1:]
                        UDPServer.sendto(f"{name} joined!".encode(), client)
                    else:
                        UDPServer.sendto(message, client)
                except:
                    clients.remove(client)

t1 = threading.Thread(target=recive)
t1.daemon = True
t2 = threading.Thread(target=brodcast)
t2.daemon = True

t1.start()
t2.start()

while True:
    pass
