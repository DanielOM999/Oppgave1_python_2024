import socket
import threading
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

host_ip = "localhost"
port = 3000

nicname = input("Enter name:\n")

TCPclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPclient.connect((host_ip, port))

class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Socket Client Chat")
        self.geometry("400x500")

        self.chat_box = ctk.CTkTextbox(self, width=380, height=380)
        self.chat_box.grid(row=0, column=0, padx=10, pady=10)
        self.chat_box.configure(state="disabled")

        self.input_box = ctk.CTkEntry(self, width=300)
        self.input_box.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.send_button = ctk.CTkButton(self, text="Send", command=self.write_message)
        self.send_button.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        
        self.recive_thread = threading.Thread(target=self.TCPRecive)
        self.recive_thread.daemon = True
        self.recive_thread.start()

    def display_message(self, message):
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", message + "\n")
        self.chat_box.configure(state="disabled")
        self.chat_box.see("end")

    def TCPRecive(self):
        while True:
            try:
                message = TCPclient.recv(1024).decode("ascii")
                if message == "NICK":
                    TCPclient.send(nicname.encode("ascii"))
                else:
                    self.display_message(message)
            except:
                self.display_message("An error occurred!")
                TCPclient.close()
                break

    def write_message(self):
        message = f"{nicname}: {self.input_box.get()}"
        self.input_box.delete(0, "end")
        TCPclient.send(message.encode("ascii"))

if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()
