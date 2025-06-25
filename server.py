import socket
import subprocess
import re
import sys
import signal
from client_request import Connect
from database import Database

class StartServer:
    def __init__(self):
        self.host = self.get_ip()
        self.port = 2000
        self.db = Database()
        self.online_clients = {}
        self.client = Connect()
        self.run = True

    def get_ip(self):
        response = subprocess.run(["ipconfig"], capture_output=True, shell=True, text=True)
        ip = re.findall(r"192.168\.\d+\.\d+", response.stdout)
        return ip[0]

    def start(self):
        print(f"Starting server on {self.host}:{self.port}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            while self.run:
                try:
                    conn, addr = s.accept()
                    with conn:
                        response = conn.recv(4096).decode()
                        response = self.client_manager(response)
                        conn.send(response.encode())
                except Exception as e:
                    pass
            print("closing connection")
            s.close()

    def client_manager(self, response):
        mode, username, others = response.split(":", 2)

        if mode == "IS_HOST":
            response = "OK"

        elif mode == "REGISTER":
            password = others
            response = self.register(username, password)

        elif mode == "LOGIN":
            password = others
            response = self.login(username, password)

        elif mode == "HOME":
            response = self.home(username)

        elif mode == "GET_USERS":
            response = self.get_users()

        elif mode == "ONLINE":
            self.online_clients[username] = others
            print(f"{username}: {others} is online")

        elif mode == "ONLINE_USERS":
            response = self.check_online_users(username)

        elif mode == "OFFLINE":
            response = self.offline(username, others)
            print(f"{username}: {others} is offline")

        elif mode == "START_CONVERSATION":
            self.start_conversation(username, others)

        elif mode == "SEND_MESSAGE":
            message_y, talk_with, text = others.split("`#`")
            self.send_message(talk_with, text, message_y)

        elif mode == "SAVE_MESSAGE":
            message_y, side, talk_with, text = others.split("`#`")
            self.save_chat(message_y, side, talk_with, text, username)

        elif mode == "OFFLINE_CHAT":
            response = self.offline_chat(username, others)

        return response


    def register(self, username, password):
        check = self.db.check_username(username)
        if not check:
            self.db.add(username, password)
            return "SUCCESS"
        else:
            return "username already registered"

    def login(self, username, password):
        try:
            check = self.db.check_username(username)
            if check:
                if self.db.check_password(username, password):
                    return "SUCCESS"
                else:
                    return "incorrect password"
            else:
                return "invalid username"
        except Exception as e:
            return f"ERROR: {e}"

    def home(self, username):
        id = self.db.get_id(username)
        self.db.create_table(f"user{id[0]}", "username", "conversation")
        result = self.db.get_content(f"user{id[0]}")
        response = "ERROR"
        if not result:
            response = "NO_CONVERSATIONS"
        else:
            response = [user for _, user, _ in result]
            response = ":".join(response)
        return response

    def get_users(self):
        response = self.db.get_content("users")
        users = [user for _, user, _ in response]
        users = "::::::::::::::".join(users)
        return users

    def send_message(self, talk_with, text, message_y):
        print(talk_with, "got a message")
        client_ip = self.online_clients[talk_with]
        response = self.client.send(f"GOT_MESSAGE:{message_y}`#`{talk_with}`#`{text}", host=client_ip, port=2001)
        return response

    def check_online_users(self, username):
        if username in self.online_clients:
            response = "TRUE"
        else:
            response = "FALSE"
        return response

    def offline(self, username, ip):
        try:
            del self.online_clients[username]
            response = "DELETED"
            client_response = self.client.send(f"OFFLINE:{username}", host=ip, port=2001)
        except:
            pass
            response = "ERROR"
        return response

    def start_conversation(self, username, talk_with):
        sender_id = self.db.get_id(username)[0]
        receiver_id = self.db.get_id(talk_with)[0]
        check = self.db.check_username(talk_with, table=f"user{sender_id}")
        if not check:
            self.db.add(talk_with, "", column1="username", column2="conversation", table=f"user{sender_id}")
            self.db.create_table(f"user{receiver_id}", "username", "conversation")
            self.db.add(username, "", column1="username", column2="conversation", table=f"user{receiver_id}")


    def save_chat(self,message_y , side, talk_with, text, username):
        user_id = self.db.get_id(username)[0]
        receiver_id = self.db.get_id(talk_with)[0]
        sender_text = f"{text} [side]LEFT[message_y]{message_y}\n\n"
        receiver_text = f"{text} [side]RIGHT[message_y]{message_y}\n\n"
        self.db.update(f"user{user_id}", talk_with, sender_text)
        self.db.update(f"user{receiver_id}", username, receiver_text)



    def offline_chat(self, username, talk_with):
        user_id = self.db.get_id(username)[0]
        response = self.db.get_content(f"user{user_id}")
        for id, user, text in response:
            if user == talk_with:
                response = text
        return response

if __name__ == '__main__':
    server = StartServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("Keyboard interrupt detected, stopping server.")
    except Exception as e:
        print("Error running server:", e)
    finally:
        server.run = False
        print("Server stopped")