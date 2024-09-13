import socket, threading

host_ip = "localhost"
port = 3000

nicname = input("Enter name:\n")

TCPclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPclient.connect((host_ip, port))

def TCPRecive():
    while True:
        try:
            message = TCPclient.recv(1024).decode("ascii")
            if message == "NICK":
                TCPclient.send(nicname.encode("ascii"))
            else:
                print(message)
        except:
            print("An error occurred!")
            TCPclient.close()
            break

def write():
    while True:
        message = f"{nicname}: {input("")}"
        TCPclient.send(message.encode("ascii"))

recive_thread = threading.Thread(target=TCPRecive)
recive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()