import threading
import socket
import random
import time

DELTA_TIME = 1/20

class player:
    def __init__(self, user, password):
        self.x = 0
        self.y = 0
        self.health = 100
        self.alive = True
        self.max_velocity = 5
        self.velocity_x = 0
        self.velocity_y = 0
        self.friction = 0.5
        self.username = user
        self.password = password
        self.keys = ""
        
    def increase_velocity_x(self):
        if self.velocity_x < self.max_velocity:
            self.velocity_x += 1
    
    def decrease_velocity_x(self):
        if self.velocity_x > -self.max_velocity:
            self.velocity_x -= 1

    def increase_velocity_y(self):
        if self.velocity_y < self.max_velocity:
            self.velocity_y += 1

    def decrease_velocity_y(self):
        if self.velocity_y > -self.max_velocity:
            self.velocity_y -= 1

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_x *= self.friction
        self.velocity_y *= self.friction
        if velocity_x <= 0.1:
            self.velocity_x = 0
        if velocity_y <= 0.1:
            self.velocity_y = 0
        

class user:
    def __init__(self, socket, username, password, address):
        self.socket = socket
        self.address = address
        self.player = player(username, password)


    def __str__(self):
        return f"({self.address})"




class ChatServer:
    def __init__(self, saved_players):
        self.host = input('Enter host: ')
        self.port = int(input('Enter port: '))
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.users = {}
        self.saved_players = saved_players
        self.start()

    def update(self):
        positions = ""
        for client in self.users:
            positions = positions + f"\n {self.users[client].player.username},{self.users[client].player.x},{self.users[client].player.y}"
        for client in self.users:
            client.send(positions.encode('utf-8'))

    def kill(self, client):
        client.close()
        self.users.pop(client)
        

    def handle(self, client):
        """Handles a single client connection. 
        Responsible for receiving messages from the client and broadcasting them to all other clients."""
        while True:
            try:
                json_player_commands = client.recv(1024).decode('utf-8')
                
            except:
                self.kill(client)
                break

    def update_thread(self):
        while True:
            self.update()
            time.sleep(DELTA_TIME)

    def receive(self):
        while True:
            client, address = self.server.accept()
            client.send('LOGIN'.encode('utf-8'))

            username = client.recv(1024).decode('utf-8')
            password = client.recv(1024).decode('utf-8')

            self.users[client] = user(client, username, password, address)
            print(username)
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

    def start(self):
        print('Server Started!')
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        update_thread = threading.Thread(target=self.update_thread)
        update_thread.start()
        receive_thread.join()

# get host and port from command line


# open the file with the saved players
with open('saved_players.txt', 'r') as file:
    saved_players = file.readlines()



server = ChatServer(saved_players)




