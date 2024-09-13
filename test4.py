import cv2, imutils, socket, threading, base64, queue
import numpy as np

# Global variables
clients = []
BUFFERSIZE = 65536
messages = queue.Queue()

# Setup server
UDPServer = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServer.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFERSIZE)
UDPServer.bind(("0.0.0.0", 3000))  # Bind to all available network interfaces

vid = cv2.VideoCapture(0)

def receive():
    while True:
        try:
            message, addr = UDPServer.recvfrom(1024)  # Receive initial messages
            messages.put((message, addr))  # Queue the message to be processed
            if addr not in clients:
                clients.append(addr)  # Add new client if not already in the list
                print(f"New client connected: {addr}")
        except Exception as e:
            print(f"Error in receiving message: {e}")
            pass

def broadcast():
    while True:
        # Process any queued messages from clients
        while not messages.empty():
            message, addr = messages.get()
            print(addr, message.decode())
            # Broadcast a message to all connected clients
            for client in clients:
                try:
                    if message.decode().startswith("SIGNUP_TAG"):
                        name = message.decode().split(":")[1]
                        UDPServer.sendto(f"{name} joined!".encode(), client)
                except:
                    clients.remove(client)
        
        # Stream the video feed to all clients
        while vid.isOpened():
            ret, frame = vid.read()
            if not ret:
                print("Failed to grab frame")
                break

            # Resize frame for faster transmission
            frame = imutils.resize(frame, width=400)
            encoded, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            message = base64.b64encode(buffer)
            
            # Send the encoded frame to all clients
            for client in clients:
                try:
                    UDPServer.sendto(message, client)
                except Exception as e:
                    print(f"Error sending to {client}: {e}")
                    clients.remove(client)

# Start threads
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)
t1.start()
t2.start()
