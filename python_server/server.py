import threading
import socket
import random
import time
from World import world

PORT = 3004
HOST = 'localhost'

DELTA_TIME = 1/60
global count
count = 0


        

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
                    gameobjects = self.world.gameobjects_near(player.x, player.y, 1800, 1000)
                    # subtract player x and y from gameobjects
                    colors = ["#ff0000", "#00ff00", "#0000ff", "#ffff00", "#00ffff", "#ff00ff", "#ffffff", "#000000"]
                    
                    finalGameObjects = ""
                    world = self.world.__str__().split(":")
                    top_players = self.world.top_players()
                    
                    final_top_players = []
                    for playerv in top_players:
                        final_top_players.append([playerv.username, playerv.score])
                        
                    if len(final_top_players) < 3:
                        for i in range(3 - len(final_top_players)):
                            final_top_players.append(["", ""])

                    
                    finalGameObjects += f"{world[0]},{world[1]},{self.world.tile_size},{final_top_players[0][0]},{final_top_players[0][1]},{final_top_players[1][0]},{final_top_players[1][1]},{final_top_players[2][0]},{final_top_players[2][1]}\n"
                    
                    for gameobject in gameobjects:
                        info = gameobject.__str__().split(":")
                        if info[0] == "player":
                            color_id = colors.index(gameobject.color)
                            x = gameobject.x - player.x
                            y = gameobject.y - player.y
                            alive = int(gameobject.alive)
                            finalGameObjects += f"{info[0]},{info[1]},{x},{y},{gameobject.width},{gameobject.height},{color_id},{gameobject.health},{alive}\n"
                        elif info[0] == "bullet":
                            color_id = colors.index(gameobject.color)
                            x = gameobject.x - player.x
                            y = gameobject.y - player.y
                            finalGameObjects += f"{info[0]},{info[1]},{x},{y},{gameobject.width},{gameobject.height},{color_id}\n"
                        elif info[0] == "tile":
                            color_id = colors.index(gameobject.color)
                            x = gameobject.x - player.x
                            y = gameobject.y - player.y
                            finalGameObjects += f"{info[0]},{info[1]},{x},{y},{color_id}\n"


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
        self.world.remove_player(socket)
        

    def handle(self, socket):
        """Handles a single socket connection. 
        Responsible for receiving messages from the socket and broadcasting them to all other sockets."""
        while True:
            playerkeys = None
            try:
                rawinput = socket.recv(1024).decode('utf-8')
                playerinput = rawinput.split(",")
                # get rid of empty strings
                playerinput = list(filter(lambda x: x != "", playerinput))
                # starts with KEYS
                # print(playerinput)
                if self.world.players[socket].alive:
                    if playerinput[0] == "KEYS:":
                        self.users[socket].keys = playerinput[1:]
                        if "FIRE" in playerinput[1:]:
                            self.world.players[socket].orientation = [float(playerinput[playerinput.index("FIRE")+1]),  float(playerinput[playerinput.index("FIRE")+2])]
                    elif playerinput[0] == "ORIENTATION:":
                        self.world.players[socket].orientation = [float(playerinput[1]),  float(playerinput[2])]
                if playerinput[0] == "ACTIONS:":
                    if playerinput[1] == "respawn":
                        # randomize spawn location
                        
                        world_width = ((self.world.tile_width/2) * self.world.tile_size) - self.world.tile_size
                        world_height = ((self.world.tile_height/2) * self.world.tile_size) - self.world.tile_size
                        self.world.players[socket].respawn(random.randint(-world_width, world_width), random.randint(-world_height, world_height))


                    
                    
            except:
                print(f"killed {self.world.players[socket].username}")
                self.kill(socket)
                break
            
            

    def update_thread(self):
        while True:
            for socket in self.users:
                playerkeys = self.users[socket].keys
                self.world.players[socket].commands(playerkeys)
                if "FIRE" in playerkeys and self.world.players[socket].can_fire():
                    self.world.create_bullet(self.world.players[socket].x+self.world.players[socket].width/2, self.world.players[socket].y+self.world.players[socket].height/2, 0, "#000000", self.world.players[socket].orientation, 40, 10,  socket)

            
            self.world.check_bullets()
            
            self.world.check_deaths()

                
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
            world_width = ((self.world.tile_width/2) * self.world.tile_size) - self.world.tile_size
            world_height = ((self.world.tile_height/2) * self.world.tile_size) - self.world.tile_size
            self.world.make_player(socket, random.randint(-world_width, world_width), random.randint(-world_height, world_height), socket, username, password)
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