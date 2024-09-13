import socket, threading, queue, base64
import numpy as np

# Globale variabler
clients = []
BUFFERSIZE = 65536
messages = queue.Queue()

# Setter opp serveren
UDPServer = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServer.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFERSIZE)
UDPServer.bind(("0.0.0.0", 3000))  # Binds til alle ledige netverks iterfaces

def receive():
    while True:
        try:
            message, addr = UDPServer.recvfrom(BUFFERSIZE)  # Får framsa
            messages.put((message, addr))  # Queue-er daten til å blir prossesert
            if addr not in clients:
                clients.append(addr)  # legger til ny client hvis ikke alerede
                print(f"New client connected: {addr}")
        except Exception as e:
            print(f"Error in receiving message: {e}")
            pass

def broadcast():
    while True:
        # prosseser alle qued messages
        while not messages.empty():
            message, addr = messages.get()
            
            # sjekker hvis det er en SIGNUP_TAG
            if message.startswith(b"SIGNUP_TAG"):
                continue  # ignorer

            # sender til alle untat senderen
            for client in clients:
                if client != addr:
                    try:
                        UDPServer.sendto(message, client)
                    except Exception as e:
                        print(f"Error sending to {client}: {e}")
                        clients.remove(client)

# Starter threadsa
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)
t1.start()
t2.start()
