import threading
import socket
import random
import time
import pygame
from player import player


DELTA_TIME = 1/60


        

class user:
    def __init__(self, socket, username, password, address):
        self.socket = socket
        self.address = address
        self.player = player(username, password)
        self.keys = ["0","0","0","0"]


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
            positions = positions + f"\n{self.users[client].player.username},{self.users[client].player.x},{self.users[client].player.y},{self.users[client].player.color}"
        for client in self.users:
            client.send(positions.encode('utf-8'))

    def kill(self, client):
        client.close()
        self.users.pop(client)
        

    def handle(self, client):
        """Handles a single client connection. 
        Responsible for receiving messages from the client and broadcasting them to all other clients."""
        while True:
            playerkeys = None
            try:
                playerinput = client.recv(1024).decode('utf-8').split(",")
                # starts with KEYS
                if playerinput[0] == "KEYS:":
                    self.users[client].keys = playerinput[1:]
            except:
                print(f"killed {self.users[client].player.username}")
                self.kill(client)
                break
            
            

    def update_thread(self):
        while True:
            for client in self.users:
                playerkeys = self.users[client].keys
                if "DOWN" in playerkeys:
                    self.users[client].player.increase_velocity_y()
                if "UP" in playerkeys:
                    self.users[client].player.decrease_velocity_y()
                if "RIGHT" in playerkeys:
                    self.users[client].player.increase_velocity_x()
                if "LEFT" in playerkeys:
                    self.users[client].player.decrease_velocity_x()
                if "FAST" in playerkeys:
                    self.users[client].player.max_velocity = 20
                    self.users[client].player.velocity_increment = 4
                else:
                    self.users[client].player.max_velocity = 10
                    self.users[client].player.velocity_increment = 2
                self.users[client].player.move()
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




