import threading
import socket

class ChatServer:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.clients = []
        self.nicknames = {}

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message == '/quit':
                    self.clients.remove(client)
                    client.close()
                    nickname = self.nicknames[client]
                    self.nicknames.remove(nickname)
                    self.broadcast(f'{nickname} left the chat!'.encode('utf-8'))
                    break
                elif message.startswith('/nick'):
                    nickname = message.split()[1]
                    self.nicknames[client] = nickname
                    client.send(f'Nickname successfully changed to {nickname}'.encode('utf-8'))
                else:
                    self.broadcast(message.encode('utf-8'))
            except:
                client.close()
                self.clients.remove(client)
                nickname = self.nicknames[client]
                self.nicknames.remove(nickname)
                self.broadcast(f'{nickname} left the chat!'.encode('utf-8'))
                break

    def receive(self):
        while True:
            client, address = self.server.accept()
            print(f'Connected with {str(address)}')
            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            self.nicknames[client] = nickname
            self.clients.append(client)
            print(f'Nickname of client is {nickname}!')
            client.send('Connected to the server!'.encode('utf-8'))
            self.broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
            client.send('Type your message:'.encode('utf-8'))
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

    def start(self):
        print('Server Started!')
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        receive_thread.join()

# get host and port from command line
host = input('Enter host: ')
port = int(input('Enter port: '))

server = ChatServer(host, port)

server.start()


