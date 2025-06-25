import tkinter as tk
import subprocess
import socket
import re
from client_request import Connect
import threading
import os


class HomePage:
    def __init__(self, host, port, root, username):
        self.root = root
        self.message_y = 0.15
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")  # 3440 1440
        self.root.configure(background="white")
        self.username = username
        self.page = "home"
        self.send_times = 0
        self.client = Connect(host, port)
        self.client_listener = ClientListener(host, port, root, username)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.scroll()

    def label(self, text, font=("Tahoma", 0.0145), bg="light blue", fg="blue"):
        return tk.Label(self.scrollable_frame, text=text, font=(font[0], self.ratio_x(font[1])), bg=bg, fg=fg)

    def enter(self, font=("Helvetica", 0.0145), bg="white", fg="purple", width=0.00581, show=None):
        return tk.Entry(self.scrollable_frame, font=(font[0], self.ratio_x(font[1])), bg=bg, fg=fg, width=20, show=show)

    def button(self, text, command, bg="dark blue", fg="aliceblue", width=20, height=0, font=("Verdana", 0.017)):
        return tk.Button(self.scrollable_frame, text=text, command=command, bg=bg, fg=fg, width=width, height=height,
                         font=(font[0], self.ratio_x(font[1])))

    def ratio_x(self, num):
        return int(self.screen_width * num)

    def ratio_y(self, num):
        return int(self.screen_height * num)

    def scroll(self):
        self.fixed_header = tk.Frame(self.root, bg="light blue", height=self.ratio_y(0.1))
        self.fixed_header.pack_propagate(False)
        self.canvas = tk.Canvas(self.root, bg="light blue")
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.fixed_header.pack(fill="x", side="bottom")

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollable_frame = tk.Frame(self.canvas, bg="light blue")
        self.scrollable_frame.config(width=self.screen_width, height=self.screen_height)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self._on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def scroll_update(self):
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def home(self, response="ok"):
        self.clear_screen()
        self.button(text="logout",command=self.logout, width=0, height=0).place(x=0, y=0)
        response = self.client.send(f"HOME:{self.username}:X").split(":")

        if response[0] == "NO_CONVERSATIONS":
            label = self.label("you have no conversations.")
            label.place(x=self.ratio_x(0.38), y=self.ratio_y(0.2))
            self.button("start conversation", command=self.new_con, width=0).place(x=self.ratio_x(0.39),y=self.ratio_y(0.6))

        else:
            self.label("your conversations:", font=("Tahoma", 0.02)).place(x=self.ratio_x(0.39), y=self.ratio_y(0.2))
            self.show_con_users(response)

    def logout(self):
        self.client_listener.on_closing()
        os.system("python client.py")

    # con --> conversation
    def new_con(self):
        self.page = "new_con"
        self.clear_screen()
        label = self.label("Which user do you want \nto start a conversation with?")
        label.place(x=self.ratio_x(0.39), y=self.ratio_y(0.1))
        users = self.client.send(f"GET_USERS:{self.username}:X").split("::::::::::::::")
        con_users = self.client.send(f"HOME:{self.username}:X")
        self.show_users(users, con_users)

    def show_users(self, users, con_users):
        y = 0.3
        count = 0
        for user in users:
            if user == self.username or user in con_users:
                continue
            count += 1
            response = self.client.send(f"ONLINE_USERS:{user}:X")
            if response == "TRUE":
                self.button(f"{user}: online", command=lambda u=user: self.start_con(u), width=20, height=0).place(x=self.ratio_x(0.36), y=self.ratio_y(y))
            else:
                self.button(f"{user}: offline", command=lambda u=user: self.start_con(u), width=20, height=0).place(x=self.ratio_x(0.36), y=self.ratio_y(y))
            y += 0.15
            self.scrollable_frame.config(height=self.ratio_y(y + 0.1))
            self.scroll_update()
        if count == 0:
            self.label("There are no more users.", fg="red").place(x=self.ratio_x(0.38), y=self.ratio_y(0.7))
            self.root.after(2000, self.home)

    def start_con(self, user=""):
        self.message_y = 0.15
        self.page = "chat"
        if user:
            self.talk_with = user

        self.client.send(f"START_CONVERSATION:{self.username}:{self.talk_with}")

        self.clear_screen()
        self.label(f"chat with {self.talk_with}").place(y=self.ratio_y(0.05), x=self.ratio_x(0.44))
        self.message_sender()



    def message_sender(self):
        width = self.root.winfo_width()
        self.message = tk.Entry(self.fixed_header, font=("Ariel", 50), width=width // 50)
        self.message.place(x=self.ratio_x(0.11), y=0)

        tk.Button(self.fixed_header, text="send", command=self.send_message, width=10, height=2, font=("Tahoma", 18),bg="dark red", fg="white").place(x=self.ratio_x(0.84), y=0)
        tk.Button(self.fixed_header, text="back", command=self.home, width=10, height=2, font=("Tahoma", 18), bg="blue",fg="white").place(x=0, y=0)

    def send_message(self):
        text = self.message.get()
        if not text:
            return
        text, lines = self.text_organize(text)
        if self.send_times == 0:
            tk.Button(self.scrollable_frame, text=text, font=("Tahoma", self.ratio_x(0.00872)), bg="blue", fg="white",justify="left").place(x=self.ratio_x(0.02), y=self.ratio_y(self.message_y))
            self.message_y = self.message_y + 0.07 * lines if lines == 1 else self.message_y + lines * 0.0394 + 0.07
            self.message_y = self.message_y + 0.03 if lines == 2 else self.message_y
        else:
            self.message_y = self.message_y + 0.07 * lines if lines == 1 else self.message_y + lines * 0.0394 + 0.07
            self.message_y = self.message_y + 0.03 if lines == 2 else self.message_y
            tk.Button(self.scrollable_frame, text=text, font=("Tahoma", self.ratio_x(0.00872)), bg="blue", fg="white",justify="left").place(x=self.ratio_x(0.02), y=self.ratio_y(self.message_y))
            self.send_times += 1


        self.scrollable_frame.config(height=self.ratio_y(self.message_y + 0.1))
        self.scroll_update()

        self.client.send(f"SEND_MESSAGE:{self.username}:{self.message_y}`#`{self.talk_with}`#`{text}")
        self.client.send(f"SAVE_MESSAGE:{self.username}:{self.message_y}`#`LEFT`#`{self.talk_with}`#`{text}")

        self.message.delete(0, tk.END)

    def text_organize(self, text):
        if len(text) > 30:
            text = text.split(" ")
            new_text, len_line, lines = "", 0, 1
            for word in text:
                len_line += len(word)
                if len(word) > 15:
                    count_letters = 0
                    for letter in word:
                        new_text += letter
                        if count_letters > 15:
                            new_text += "\n"
                            lines += 1
                            count_letters = 0
                        count_letters += 1
                else:
                    new_text += word + " "
                    if len_line > 20:
                        new_text += "\n"
                        lines += 1
                        len_line = 0
            return new_text, lines
        return text, 1

    def got_message(self, message_y, talk_with, text):
        if self.page == "chat":
            message_y = float(message_y)
            self.root.after(0, self.live_chat, message_y, text)

    def live_chat(self, message_y, text):
        tk.Button(self.scrollable_frame, text=text, font=("Tahoma", self.ratio_x(0.00872)), bg="red", fg="white",justify="left").place(x=self.ratio_x(0.95), y=self.ratio_y(self.message_y), anchor="ne")
        self.message_y = message_y

        self.scrollable_frame.config(height=self.ratio_y(self.message_y + 0.1))
        self.scroll_update()


    def show_con_users(self, con_users):
        y = 0.4
        for user in con_users:
            if user == self.username:
                continue
            response = self.client.send(f"ONLINE_USERS:{user}:X")
            if response == "TRUE":
                self.button(f"{user}: online", command=lambda u=user: self.offline_chat(u), width=20, height=0).place(x=self.ratio_x(0.36), y=self.ratio_y(y))
            else:
                self.button(f"{user}: offline", command=lambda u=user: self.offline_chat(u), width=20, height=0).place(x=self.ratio_x(0.36), y=self.ratio_y(y))
            y += 0.15
            self.scrollable_frame.config(height=self.ratio_y(y + 0.5))
            self.scroll_update()

        self.button("start new conversation", command=self.new_con, width=0 ,bg="red").place(x=self.ratio_x(0.362),y=self.ratio_y(y))

    def offline_chat(self, talk_with):
        self.page = "chat"
        self.clear_screen()
        self.message_y = 0.15
        self.send_times = 0

        self.label(f"chat with {talk_with}").place(y=self.ratio_y(0.05), x=self.ratio_x(0.44))
        self.talk_with = talk_with

        response = self.client.send(f"OFFLINE_CHAT:{self.username}:{talk_with}")
        response = response.split("\n\n")
        self.response_organize(response)

        self.message_sender()


    def response_organize(self, response):
        for line in response:
            if not line:
                continue
            line = line.split(" [side]")
            text, others = "".join(line[0:-1]), line[-1]
            side, message_y = others.split("[message_y]")
            if text:
                self.print_messages(text, side)
            self.message_y = float(message_y)
            self.scrollable_frame.config(height=self.ratio_y(self.message_y + 0.1))
            self.scroll_update()

    def print_messages(self, text, side):
        if side == "LEFT":
            tk.Button(self.scrollable_frame, text=text, font=("Tahoma", self.ratio_x(0.00872)), bg="blue", fg="white",justify="left").place(x=self.ratio_x(0.02), y=self.ratio_y(self.message_y))
        elif side == "RIGHT":
            tk.Button(self.scrollable_frame, text=text, font=("Tahoma", self.ratio_x(0.00872)), bg="red", fg="white",justify="left").place(x=self.ratio_x(0.95), y=self.ratio_y(self.message_y), anchor="ne")




class ClientListener:
    def __init__(self, host, port, root, username):
        self.root = root
        self.host = host
        self.port = port
        self.listener_host = self.get_ip()
        self.listener_port = 2001
        self.username = username
        self.client = Connect(host, port)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def get_ip(self):
        response = subprocess.run(["ipconfig"], capture_output=True, shell=True, text=True, encoding="utf-8", errors="ignore")
        ip = re.findall(r"192.168\.\d+\.\d+", response.stdout)
        return ip[0]

    def home(self, con_users=""):
        self.home_page = HomePage(self.host, self.port, self.root, self.username)
        self.client.send(f"ONLINE:{self.username}:{self.listener_host}")
        threading.Thread(target=self.start_listener).start()
        self.home_page.home(con_users)

    def start_listener(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.listener_host, self.listener_port))
                s.listen()
                while True:
                    conn, addr = s.accept()
                    with conn:
                        response = conn.recv(4096).decode()
                        response = self.check_request(response)
                        conn.send(response.encode())
                        if response == "offline":
                            s.close()
                            break

        except WindowsError as e:
            print("There is a run server on this ip and port!\nExiting...")
            self.on_closing()
        except Exception as e:
            print(f"Error: {e}")

    def check_request(self, response):
        mode, other = response.split(":")
        if mode == "online?":
            response = "ok"

        elif mode == "OFFLINE":
            response = "offline"

        elif mode == "GOT_MESSAGE":
            response = "got_message"
            message_y, talk_with, text = other.split("`#`")
            self.home_page.got_message(message_y, talk_with, text)

        return response

    def on_closing(self):
        response = self.client.send(f"OFFLINE:{self.username}:{self.listener_host}")
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ClientListener("192.168.10.112", 2000, root, "1")
    app.home()
    root.mainloop()