import socket
class Connect:
    def __init__(self, host="", port=""):
        self.host = host
        self.port = port

    def send(self, data, host="", port=0):
        self.host = host if host else self.host
        self.port = port if port else self.port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.send(data.encode())
            response = s.recv(4096).decode()
        return response