from client_request import Connect
import tkinter as tk
from tkinter import messagebox
from client_home import ClientListener


class ClientGui:
    def __init__(self, root, client):
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.client = client
        self.root = root
        self.root.title("chat server")
        self.root.geometry(f"{self.screen_width}x{self.screen_height}") #3440 1440
        self.root.configure(background="light blue")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def label(self,text, font=("Tahoma", 50), bg="light blue", fg="blue"):
        return tk.Label(self.root, text=text, font=font, bg=bg, fg=fg)

    def enter(self, font=("Helvetica", 50), bg="white", fg="purple", width=20, show=None):
        return tk.Entry(self.root, font=font, bg=bg, fg=fg, width=width, show=show)

    def button(self, text, command, bg="dark blue", fg="aliceblue", width=15, height=0, font=("Verdana", 60)):
        return tk.Button(self.root, text=text, command=command, bg=bg, fg=fg, width=width, height=height, font=font)

    def square(self, width=500, height=500, bg="white"):
        return tk.Canvas(self.root, width=width, height=height, bg=bg)

    def ratio(self, num):
        return int(self.screen_width * num)

    def start_screen(self):
        self.clear_screen()
        self.label("==============\nchat server\n==============", font=("Helvetica", 70)).pack(pady=(int(self.screen_height * 0.048), int(self.screen_height * 0.007)))
        self.label("What would you like to do?").pack()
        self.button("register", command=self.register_screen).pack(pady=(int(self.screen_height * 0.048), int(self.screen_height * 0.007)))
        self.button("login", self.login_screen).pack(pady=(int(self.screen_height * 0.007), int(self.screen_height * 0.007)))
        self.square(width=10, height=self.screen_height).place(x=self.screen_width - self.ratio(0.05), y=0)
        self.square(width=10, height=self.screen_height).place(x=self.ratio(0.05), y=0)

    def get_host_ip(self):
        self.clear_screen()
        self.label("Host ip:", font=("Tahoma", 100)).pack(pady=int(self.screen_height * 0.2))
        self.enter_host_ip = self.enter()
        self.enter_host_ip.pack(pady=(int(self.screen_height * 0.01), int(self.screen_height * 0.1)))
        self.button(text="ok", command=self.confirm_ip, width=15).pack()

    def confirm_ip(self):
        if self.enter_host_ip.get() == "":
            self.label("Please enter ip address", fg="red").pack(pady=int(self.screen_height * 0.01))
            self.root.after(2000, self.get_host_ip)
        else:
            try:
                client = Connect()
                response = client.send("IS_HOST", host=self.enter_host_ip.get(), port=2000)
                self.client.start(self.enter_host_ip.get())
            except:
                self.label("There is no run server at this ip address", fg="red").pack(pady=int(self.screen_height * 0.01))
                self.root.after(2000, self.get_host_ip)

    def register_screen(self):
        self.clear_screen()
        self.label("Choose username and password").pack(pady=(int(self.screen_height * 0.07), self.ratio(0.003)))
        self.label("Username:", fg="black").pack(pady=(int(self.screen_height * 0.07), self.ratio(0.003)))
        self.username = self.enter()
        self.username.pack(pady=(int(self.screen_height * 0.007), int(self.screen_height * 0.014)))
        self.label("Password:", fg="black").pack(pady=(int(self.screen_height * 0.01), self.ratio(0.003)))
        self.password = self.enter(show="*")
        self.password.pack(pady=(int(self.screen_height * 0.007), int(self.screen_height * 0.035)))
        self.button("register", self.register, width=7, height=0, font=("Verdana", self.ratio(0.017441))).place(x=self.ratio(0.38), y=int(self.screen_height * 0.6))
        self.button("back", self.start_screen, width=7, height=0, font=("Verdana", self.ratio(0.017441))).place(x=self.ratio(0.507), y=int(self.screen_height * 0.6))

    def register(self):
        if not self.username.get():
            self.label("Please enter username!", fg="red", font=("Tahoma", 35)).place(x=self.ratio(0.43),y=int(self.screen_height * 0.493))
            self.root.after(2000, self.register_screen)
        elif not self.password.get():
            self.label("Please enter password!", fg="red", font=("Tahoma", 35)).place(x=self.ratio(0.43),y=int(self.screen_height * 0.493))
            self.root.after(2000, self.register_screen)
        elif "`#`" in self.username.get() or ":" in self.username.get():
            self.label("Invalid username", fg="red", font=("Tahoma", 35)).place(x=self.ratio(0.43),y=int(self.screen_height * 0.493))




        else:
            self.client.register(self.username.get(), self.password.get())

    def login_screen(self):
        self.clear_screen()
        self.label("Enter your username and password").pack(
            pady=(int(self.screen_height * 0.07), int(self.screen_height * 0.007)))
        self.label("Username:", fg="black").pack(pady=(int(self.screen_height * 0.07), int(self.screen_height * 0.007)))
        self.username = self.enter()
        self.username.pack(pady=(int(self.screen_height * 0.007), int(self.screen_height * 0.014)))
        self.label("Password:", fg="black").pack(pady=(int(self.screen_height * 0.01), int(self.screen_height * 0.007)))
        self.password = self.enter(show="*")
        self.password.pack(pady=(int(self.screen_height * 0.007), int(self.screen_height * 0.035)))
        self.button("login", self.login, width=7, height=0, font=("Verdana", self.ratio(0.017441))).place(x=self.ratio(0.38), y=int(self.screen_height * 0.6))
        self.button("back", self.start_screen, width=7, height=0, font=("Verdana", self.ratio(0.017441))).place(x=self.ratio(0.507), y=int(self.screen_height * 0.6))

    def login(self):
        if not self.username.get():
            self.label("Please enter username!", fg="red", font=("Tahoma", 35)).place(x=self.ratio(0.43),y=int(self.screen_height * 0.493))
            self.root.after(2000, self.login_screen)
        elif not self.password.get():
            self.label("Please enter password!", fg="red", font=("Tahoma", 35)).place(x=self.ratio(0.43),y=int(self.screen_height * 0.493))
            self.root.after(2000, self.login_screen)
        else:
            self.client.login(self.username.get(), self.password.get())


class Client:
    def __init__(self, root):
        self.root = root
        self.gui = ClientGui(root, self)
        self.gui.get_host_ip()

    def start(self, host):
        self.client = Connect(host, 2000)
        self.host = host
        self.gui.start_screen()

    def register(self, username, password):
        response = self.client.send(f"REGISTER:{username}:{password}")
        if response == "SUCCESS":
            messagebox.showinfo("Registration completed!", f"Registration is complete. You are now redirected to the login page")
            self.gui.login_screen()
        else:
            messagebox.showerror("Registration failed!", response)
            self.gui.register_screen()


    def login(self, username, password):
        response = self.client.send(f"LOGIN:{username}:{password}")
        if response == "SUCCESS":
            self.home(username)
        else:
            messagebox.showerror("Login failed!", response)
            self.gui.login_screen()

    def home(self, username):
        self.home_page = ClientListener(self.host, 2000, self.root, username)
        response = self.client.send(f"HOME:{username}:X")
        response = response.split(":")
        if response == "NO_CONVERSATIONS":
            self.home_page.home()
        else:
            self.home_page.home(response)



if __name__ == '__main__':
    root = tk.Tk()
    client = Client(root)
    root.mainloop()


