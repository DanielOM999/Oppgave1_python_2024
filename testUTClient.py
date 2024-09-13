import socket, threading, cv2, base64, imutils, os, numpy as np
import time
import customtkinter as ctk
from PIL import Image, ImageTk

host_ip = "localhost"
tcp_port = 3000
udp_port = 3001
BUFFERSIZE = 65536

nickname = input("Enter your name:\n")

TCPClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPClient.connect((host_ip, tcp_port))

UDPClient = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClient.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFERSIZE)

video_streaming = False
fps, st, frame_to_count, cnt = (0, 0, 20, 0)
vid = cv2.VideoCapture(os.path.join(os.path.dirname(__file__), 'videos/test.mp4'))  # Webcam input (0 for default)

def send_udp_video():
    global video_streaming
    while video_streaming:
        ret, frame = vid.read()
        if not ret:
            print("Failed to grab frame")
            break

        frame = imutils.resize(frame, width=400)
        encoded, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        message = base64.b64encode(buffer).decode('ascii')
        enName = base64.b64encode(nickname.encode()).decode('ascii')

        combined_message = f"{enName}|{message}"

        try:
            UDPClient.sendto(combined_message.encode('ascii'), (host_ip, udp_port))
        except Exception as e:
            print(f"Error sending frame: {e}")
            break

        cv2.imshow("Transmitting Video", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            video_streaming = False
            break

        time.sleep(0.03)
    UDPClient.sendto(b"END", (host_ip, udp_port))
    print("Video streaming stopped.")

def receive_udp_video(self):
    global fps, st, frame_to_count, cnt
    while True:
        try:
            packet_data, _ = UDPClient.recvfrom(BUFFERSIZE)
            if packet_data == b"END":
                print("Video stream ended.")
                self.after(0, self.remove_image)
            combined_message = packet_data.decode('ascii')
            enName, message = combined_message.split('|')

            name = base64.b64decode(enName).decode('ascii')
            print(name)
            
            data = base64.b64decode(message)
            npdata = np.frombuffer(data, dtype=np.uint8)
            frame = cv2.imdecode(npdata, 1)
            frame = cv2.putText(frame, "FPS:" + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            # cv2.imshow("Receiving Video", frame)
            self.after(0, self.display_image, frame)
            
            if cnt == frame_to_count:
                fps = round(frame_to_count / (time.time() - st))
                st = time.time()
                cnt = 0
            cnt += 1

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            continue

class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Socket Client Chat")
        self.geometry("400x520")

        self.chat_box = ctk.CTkTextbox(self, width=380, height=380)
        self.chat_box.grid(row=0, column=0, padx=10, pady=10)
        self.chat_box.configure(state="disabled")

        self.input_box = ctk.CTkEntry(self, width=300)
        self.input_box.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.send_button = ctk.CTkButton(self, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.toggle_video_button = ctk.CTkButton(self, text="Toggle Video", command=self.toggle_video)
        self.toggle_video_button.grid(row=2, column=0, padx=10, pady=10)

        self.image_label = ctk.CTkLabel(self, image=None, text="", width=400, height=225)
        self.image_label.grid(row=0, column=3, padx=10, pady=10)

        self.recive_thread = threading.Thread(target=self.TCPReceive)
        self.recive_thread.daemon = True
        self.recive_thread.start()

        self.udp_receive_thread = threading.Thread(target=receive_udp_video, args=(self,))
        self.udp_receive_thread.daemon = True
        self.udp_receive_thread.start()


    def display_message(self, message):
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", message + "\n")
        self.chat_box.configure(state="disabled")
        self.chat_box.see("end")
    
    def display_image(self, frame):
        self.geometry("850x520")
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(frame_rgb)
        image_ctk = ctk.CTkImage(dark_image=image_pil, size=(400, 225))
        self.image_label.configure(image=image_ctk)
        self.image_label.image = image_ctk
    
    def remove_image(self):
        self.geometry("400x520")
        self.image_label.configure(image=None)
        self.image_label.image = None

    def TCPReceive(self):
        while True:
            try:
                message = TCPClient.recv(1024).decode("ascii")
                if message == "NICK":
                    TCPClient.send(nickname.encode("ascii"))
                else:
                    self.display_message(message)
            except:
                self.display_message("An error occurred!")
                TCPClient.close()
                break

    def send_message(self):
        message = f"{nickname}: {self.input_box.get()}"
        self.input_box.delete(0, "end")
        TCPClient.send(message.encode("ascii"))

    def toggle_video(self):
        global video_streaming
        video_streaming = not video_streaming
        if video_streaming:
            self.video_thread = threading.Thread(target=send_udp_video)
            self.video_thread.start()

if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()
