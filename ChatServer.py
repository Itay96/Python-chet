import threading
import socket

class Server(threading.Thread):
    def __init__(self, server_ip, server_port):
        super().__init__()
        self.connections_list = []
        self.server_ip = server_ip
        self.server_port = server_port

    def run(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((self.server_ip, self.server_port))

        server_sock.listen(5)
        print('Listening at', server_sock.getsockname())

        while True:
            client_socket, client_address = server_sock.accept()
            server_socket = ServerSocket(client_socket, client_address, self)
            server_socket.start()

            self.connections_list.append(server_socket)
            print('Connected to: ', client_socket.getpeername())

    def broadcast(self, message, client_address):
        for client in self.connections_list:
            if client.client_address != client_address:
                client.send(message)


class ServerSocket(threading.Thread):
    def __init__(self, client_socket, client_address, server):
        super().__init__()
        self.client_socket = client_socket
        self.client_address = client_address
        self.server = server

    def run(self):
        while True:
            message = self.client_socket.recv(1024).decode()

            if message:
                print(str(self.client_address) + ": " + message)
                self.server.broadcast(message, self.client_address)
            else:
                print(str(self.client_address) + " has closed the connection")
                self.client_socket.close()
                server.remove_connection(self)
                return

    def send(self, message):
        self.client_socket.sendall(message.encode())

if __name__ == '__main__':
    server = Server('10.0.0.36', 8765)
    server.start()
