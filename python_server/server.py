import threading
import socket
import random
import time

import sys
sys.path.insert(0, 'game_objects')
from World import world

PORT = 3004
HOST = '127.0.0.1'

DELTA_TIME = 1/60


        

class user:
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address
        self.keys = []

    def __str__(self):
        return f"({self.address})"




class Server:
    def __init__(self):
        self.host, self.port = HOST, PORT
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.users = {}
        self.world = world(0)
        self.start()


    def update(self):
        """Sends the current state of the world to all clients."""
        try:
            for socket in self.users:
                try:
                    # get gameobjects within 2000 from player
                    player = self.world.players[socket]
                    gameobjects = self.world.gameobjects_near(player.x, player.y, 1100, 700)
                    # subtract player x and y from gameobjects
                    colors = ["#ff0000", "#00ff00", "#0000ff", "#ffff00", "#00ffff", "#ff00ff", "#ffffff"]
                    
                    finalGameObjects = ""
                    for gameobject in gameobjects:
                        color_id = colors.index(gameobject.color)
                        x = gameobject.x - player.x
                        y = gameobject.y - player.y
                        finalGameObjects += f"{x},{y},{gameobject.width},{gameobject.height},{color_id}\n"

                    # remove player and append to the end
                    
                    # format x, y, w, h, c seperated by colons
                    
                    
                    # make gameobjects into a string
                    # remove last newline
                    finalGameObjects = finalGameObjects[:-1]
                    finalGameObjects += "///"
                    # send to client
                    
                    finalGameObjectChunks = [finalGameObjects[i:i+2500] for i in range(0, len(finalGameObjects), 2500)]
                    for chunk in finalGameObjectChunks:
                        socket.send(chunk.encode('utf-8'))
                    
                except:
                    pass
        except:
            pass

    def kill(self, socket):
        socket.close()
        self.users.pop(socket)
        self.world.players.pop(socket)
        

    def handle(self, socket):
        """Handles a single socket connection. 
        Responsible for receiving messages from the socket and broadcasting them to all other sockets."""
        while True:
            playerkeys = None
            try:
                playerinput = socket.recv(1024).decode('utf-8').split(",")
                # starts with KEYS
                if playerinput[0] == "KEYS:":
                    self.users[socket].keys = playerinput[1:]
            except:
                print(f"killed {self.world.players[socket].username}")
                self.kill(socket)
                break
            
            

    def update_thread(self):
        while True:
            for socket in self.users:
                playerkeys = self.users[socket].keys
                self.world.players[socket].commands(playerkeys)
            self.world.moves()
            self.update()
            time.sleep(DELTA_TIME)

    def receive(self):
        while True:
            socket, address = self.server.accept()
            socket.send('LOGIN'.encode('utf-8'))

            username = socket.recv(1024).decode('utf-8')
            password = socket.recv(1024).decode('utf-8')

            self.users[socket] = user(socket, address)
            self.world.make_player(socket, 0, 0, 1, username, password)
            print(f"{username} connected from {address}!")
            thread = threading.Thread(target=self.handle, args=(socket,))
            thread.start()

    def start(self):
        print('Server Started!')
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        update_thread = threading.Thread(target=self.update_thread)
        update_thread.start()
        receive_thread.join()



server = Server()
