import socket
import threading

class ChatClient:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.nickname = input('Choose a nickname: ')

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('utf-8'))
                elif message.startswith('/nick'):
                    self.nickname = message.split()[1]
                    print(f'Your nickname has been changed to {self.nickname}')
                else:
                    print(message)
            except:
                print('An error occurred!')
                self.client.close()
                break

    def write(self):
        while True:
            message = f'{self.nickname}: {input("")}'
            self.client.send(message.encode('utf-8'))

    def start(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        write_thread = threading.Thread(target=self.write)
        write_thread.start()

client = ChatClient("localhost", 2007)
client.start()