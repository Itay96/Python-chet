import threading
import socket

class Send(threading.Thread):
    def __init__(self, client_socket, client_username):
        super().__init__()
        self.client_socket = client_socket
        self.client_username = client_username

    def run(self):
        while True:
            message = input()

            if message == 'EXIT':
                message = "CHAT V3.0 EXIT\r\n" + "Username: " + self.client_username + "\r\n"
                self.client_socket.sendall(message.encode())
                break

            else:
                message_length = str(len(message)) + "\r\n"
                message = "CHAT V3.0 TEXT\r\n" + "Username: "+ self.client_username + "\r\n" + "Char : " + message_length + message + "\r\n"
                self.client_socket.sendall(message.encode())

        print('Goodbye')
        self.client_socket.close()


class Receive(threading.Thread):
    def __init__(self, client_socket, client_username):
        super().__init__()
        self.client_socket = client_socket
        self.client_username = client_username

    def run(self):
        while True:
            message = self.client_socket.recv(1024)
            if message:
                print(message.decode())
            else:
                print('Connection lost')
                self.client_socket.close()

class Client:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        username = input('Username: ')
        self.client_socket.connect((self.server_address, self.server_port))
        print("Connected to " + self.server_address + ", " + str(self.server_port))

        send = Send(self.client_socket, username)
        receive = Receive(self.client_socket, username)

        send.start()
        receive.start()

        self.client_socket.sendall(("CHAT V3.0 JOIN\r\n" + "Username: " + username + "\r\n").encode())
        print("\rType 'EXIT' to leave the chat. \n")
        

if __name__ == '__main__':
    client = Client('10.0.0.36', 8765)
    client.start()
