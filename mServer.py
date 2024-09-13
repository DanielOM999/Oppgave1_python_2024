import threading, socket

host_ip = "localhost"
port = 3000

TCPsevrer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPsevrer.bind((host_ip, port))
TCPsevrer.listen()

clients = []
nicnames = []

def TCPBrodcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            TCPBrodcast(message)
        except:
            index = client.index(client)
            clients.remove(client)
            client.close()
            nicname = nicnames[index]
            TCPBrodcast(f"{nicname} left the chat!".encode("ascii"))
            nicnames.remove(nicname)
            break

def TCPRecive():
    while True:
        client, address = TCPsevrer.accept()
        print(f"Connected with {str(address)}")

        client.send("NICK".encode("ascii"))
        nicname = client.recv(1024).decode("ascii")
        nicnames.append(nicname)
        clients.append(client)

        print(f"Clients name is: {nicname}")
        TCPBrodcast(f"{nicname} joined the chat!".encode("ascii"))
        client.send("Connected to the server!".encode("ascii"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print(f"listening at port {port}...")
TCPRecive()