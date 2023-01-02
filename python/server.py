import threading
import socket

class user:
    # a user object contains the socket, the nickname and the address of the user
    def __init__(self, socket, nickname, address):
        self.socket = socket
        self.nickname = nickname
        self.address = address

    def nick(self, nickname):
        self.nickname = nickname
    
    def __str__(self):
        return f"{self.nickname} ({self.address})"



class ChatServer:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.users = {}

    def broadcast(self, message):
        for client in self.users:
            client.send(message)

    def message(self, message, clientz):
        for client in self.users:
            if client != clientz:
                client.send(message)

    def kill(self, client):
        client.close()
        # remove client from users
        nickname = self.users[client].nickname
        self.users.pop(client)
        self.broadcast(f'{nickname} left the chat!'.encode('utf-8'))

    def handle(self, client):
        """Handles a single client connection. 
        Responsible for receiving messages from the client and broadcasting them to all other clients."""
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message.startswith('/'):
                    """Handle commands here."""
                    if message == '/quit':
                        self.kill(client)
                        break
                    elif message.startswith('/connect'):
                        self.kill(client)
                        break
                    elif message.startswith('/nick'):
                        nickname = message.split()[1]
                        self.users[client].nick(nickname)
                        client.send(f'Nickname successfully changed to {nickname}'.encode('utf-8'))
                    else:
                        client.send('Invalid command!'.encode('utf-8'))
                else:
                    """Broadcast message to all clients."""
                    self.message(message.encode('utf-8'), client)
            except:
                self.kill(client)
                break

    def receive(self):
        while True:
            client, address = self.server.accept()
            print(f'Connected with {str(address)}')
            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            while nickname in [user.nickname for user in self.users.values()]:
                client.send('ERROR: name already in use'.encode('utf-8'))
                client.send('NICK'.encode('utf-8'))
                nickname = client.recv(1024).decode('utf-8')
            self.users[client] = user(client, nickname, address)
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


