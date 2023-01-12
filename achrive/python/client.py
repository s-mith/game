import socket
import threading

class ChatClient:
    def __init__(self):
        self.client = None
        self.nickname = input('Choose a nickname: ')
        self.connect()

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('utf-8'))
                else:
                    print(message)
            except:
                print('Disconnected!')
                self.client.close()
                break

    def write(self):
        while True:
            # if message starts with /connect, then connect to a new server
            user_input = input("")
            message = f'{self.nickname}: {user_input}'
            formatted_message = message.encode('utf-8')
            if user_input.startswith('/connect'):
                self.connect()
                break
            else:
                self.client.send(formatted_message)

    def connect(self):
        if self.client:
            self.client.close()
        self.host = input('Enter host: ')
        self.port = int(input('Enter port: '))
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        self.receive_thread = threading.Thread(target=self.receive)
        self.write_thread = threading.Thread(target=self.write)
        self.receive_thread.start()
        self.write_thread.start()

        

client = ChatClient()
