import socket
import threading
import pygame
import time

DELTA_TIME = 1/20

class GameClient:
    def __init__(self):
        self.client = None
        self.user = input('username: ')
        self.password = input('password: ')
        try:
            self.host, self.port = input("server address: ").split(':')
            self.port = int(self.port)
        except ValueError:
            print("Error: invalid server address")
            return
        self.connect()
        self.players = []


    def receive(self):
        while True:
            try:
                game_info = self.client.recv(1024).decode('utf-8')
                if game_info == 'LOGIN':
                    self.client.send(self.user.encode('utf-8'))
                    self.client.send(self.password.encode('utf-8'))
                else:
                    # game info is normally a string that has multiple rows of coma seperated values
                    game_info = game_info.split("\n")
                    game_info = filter(lambda x: x=="", iterable)
                    game_info = map(lambda x : x.split(","))
                    self.players = game_info
            except:
                print('An error occured!')
                self.client.close()
                break




    def UI(self):
        last_time = time.time()
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        while True:
            # Process events

            # for player in self.players draw a rectangle using the coodinates from the indexes 2 and 3
            for player in self.players:
                

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif last_time + DELTA_TIME*1000 > time.time():
                    # print all the keys that are pressed
                    keys = pygame.key.get_pressed()
                    # turn keys into a string seperated by commas
                    keys = ','.join(str(key) for key in keys)
                    self.client.send(keys.encode('utf-8'))

            # Update the game state

            # Render the screen
            pygame.display.flip()
    

            

    def connect(self):
        if self.client:
            self.client.close()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        self.receive_thread = threading.Thread(target=self.receive)
        self.UI_thread = threading.Thread(target=self.UI)
        self.receive_thread.start()
        self.UI_thread.start()

        

client = GameClient()
