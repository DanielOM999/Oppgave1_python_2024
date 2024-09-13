import threading, socket, base64, queue
import numpy as np

host_ip = "localhost"
tcp_port = 3000
udp_port = 3001

TCPServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPServer.bind((host_ip, tcp_port))
TCPServer.listen()

clients = []
nicknames = []

UDPServer = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServer.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
UDPServer.bind(("localhost", udp_port))

udp_clients = []
udp_messages = queue.Queue()

def TCPBroadcast(message):
    for client in clients:
        client.send(message)

def handle_tcp_client(client):
    while True:
        try:
            message = client.recv(1024)
            TCPBroadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            TCPBroadcast(f"{nickname} left the chat!".encode("ascii"))
            nicknames.remove(nickname)
            break

def TCPReceive():
    while True:
        client, address = TCPServer.accept()
        print(f"Connected with {str(address)}")

        client.send("NICK".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)

        print(f"Client's name is: {nickname}")
        TCPBroadcast(f"{nickname} joined the chat!".encode("ascii"))
        client.send("Connected to the server!".encode("ascii"))

        thread = threading.Thread(target=handle_tcp_client, args=(client,))
        thread.start()

def receive_udp():
    while True:
        try:
            message, addr = UDPServer.recvfrom(65536)
            udp_messages.put((message, addr))
            if addr not in udp_clients:
                udp_clients.append(addr)
                print(f"New UDP client connected: {addr}")
        except Exception as e:
            print(f"Error in receiving UDP message: {e}")
            pass

def broadcast_udp():
    while True:
        while not udp_messages.empty():
            message, addr = udp_messages.get()
            if message.startswith(b"SIGNUP_TAG"):
                continue

            for client in udp_clients:
                if client != addr:
                    try:
                        UDPServer.sendto(message, client)
                    except Exception as e:
                        print(f"Error sending to {client}: {e}")
                        udp_clients.remove(client)

tcp_thread = threading.Thread(target=TCPReceive)
udp_receive_thread = threading.Thread(target=receive_udp)
udp_broadcast_thread = threading.Thread(target=broadcast_udp)

tcp_thread.start()
udp_receive_thread.start()
udp_broadcast_thread.start()

print(f"TCP listening at port {tcp_port} and UDP at port {udp_port}...")
