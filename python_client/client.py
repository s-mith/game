import socket
import threading
import pygame
import time
import math

DELTA_TIME = 1/60

UP = pygame.K_w
DOWN = pygame.K_s
LEFT = pygame.K_a
RIGHT = pygame.K_d
FAST = pygame.K_LSHIFT
FIRE = pygame.K_SPACE

COLORS = ["#FFE5CC", "#E6E6FA", "#BDBDBD", "#F4F4F4", "#B3E5FC", "#B3E5FC", "#ffffff", "#000000"]

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
        self.game_info = []
        self.killed = False
        self.new_game_info = ""
        self.camera_delay = 10
        self.camera_ajustment = [0,0]
        self.reset_camera = [False, False]
        self.camera_move_speed = 0.25
        self.sendkeys = ""
        self.tile_size = 50
        self.connect()        

    def collect_data(self):
        while True:
            # try:
            part = self.client.recv(2500).decode('utf-8')
            if part == "LOGIN":
                return part
            if "///" in part:
                end_of_return, start_of_new = part.split("///")
                old_game_info, self.new_game_info = self.new_game_info, start_of_new
                temp = "".join((old_game_info,end_of_return))
                
                if "///" in "".join((old_game_info,end_of_return)):
                    pass
                else:
                    return "".join((old_game_info,end_of_return))
            else:
                temp = "".join((self.new_game_info, part))
                self.new_game_info = temp
            # except:
            #     print('An error occured!')
            #     pass          

    def receive(self):
        while True:
            game_info = ""
            game_info = self.collect_data()

            if game_info == 'LOGIN':
                self.client.send(self.user.encode('utf-8'))
                self.client.send(self.password.encode('utf-8'))
            else:
                # game info is normally a string that has multiple rows of coma seperated values
                try:
                    game_info = game_info.split("\n")
                    game_info = list(filter(lambda x : x != '', game_info))
                    game_info = list(map(lambda x : x.split(","), game_info))
                    self.game_info = game_info
                except:
                    pass

    def ui(self):
        pygame.init()
        # screen = pygame.display.set_mode((640, 480))
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        while True:
            
            # Process events
            # screen.fill((0,0,0))
            # for player in self.players draw a rectangle using the coodinates from the indexes 2 and 3
            screen_width, screen_height = pygame.display.get_surface().get_size()
            player_x = 0
            player_y = 0

            for gameobject in self.game_info:
                if gameobject[0] == "world":
                    self.tile_size = int(gameobject[2])
                if gameobject[0] == "player":
                    name = gameobject[1]
                    x = float(gameobject[2])
                    y = float(gameobject[3])
                    if name == self.user:
                        player_x = x
                        player_y = y
                    w = int(gameobject[4])
                    h = int(gameobject[5])
                    color = gameobject[6]
                    health = gameobject[7]
                    pygame.draw.rect(screen, pygame.Color(COLORS[int(color)]), ((x+screen_width/2-25)+self.camera_ajustment[0],(y+screen_height/2-25)+self.camera_ajustment[1], w, h))
                    # draw name under the player
                    font = pygame.font.SysFont('Comic Sans MS', 25)
                    text = font.render(name, True, (0, 0, 0))
                    textRect = text.get_rect()
                    textRect.center = ((x+screen_width/2)+self.camera_ajustment[0],(y+screen_height/2+37)+self.camera_ajustment[1])
                    screen.blit(text, textRect)
                    # draw health bar
                    # draw a white rectangle above the player
                    
                    pygame.draw.rect(screen, pygame.Color(COLORS[6]), (((x+screen_width/2-25)+self.camera_ajustment[0])-w*.25 ,((y+screen_height/2-25)+self.camera_ajustment[1]-13), w*1.5, 10))
                    pygame.draw.rect(screen, pygame.Color("#ff0000"), (((x+screen_width/2-25)+self.camera_ajustment[0])-w*.25,((y+screen_height/2-25)+self.camera_ajustment[1]-13), (w*(int(health)/100))*1.5, 10))


                    # draw a red rectangle above the player
                elif gameobject[0] == "bullet":
                    x = float(gameobject[2])
                    y = float(gameobject[3])
                    w = int(gameobject[4])
                    h = int(gameobject[5])
                    color = gameobject[6]
                    pygame.draw.rect(screen, pygame.Color(COLORS[int(color)]), ((x+screen_width/2-25)+self.camera_ajustment[0],(y+screen_height/2-25)+self.camera_ajustment[1], w, h))
                elif gameobject[0] == "tile":
                    x = float(gameobject[2])
                    y = float(gameobject[3])
                    color = gameobject[4]
                    pygame.draw.rect(screen, pygame.Color(COLORS[int(color)]), ((x+screen_width/2-25)+self.camera_ajustment[0],(y+screen_height/2-25)+self.camera_ajustment[1], self.tile_size, self.tile_size))
            


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    # print all the keys that are pressed
                    keys = pygame.key.get_pressed()
                    # every key on the keyboard 
                    keyboardcommands = [",KEYS:"]
                    if keys[UP]:
                        keyboardcommands.append("UP")
                    if keys[DOWN]:
                        keyboardcommands.append("DOWN")
                    if keys[LEFT]:
                        keyboardcommands.append("LEFT")
                    if keys[RIGHT]:
                        keyboardcommands.append("RIGHT")
                    if keys[FAST]:
                        keyboardcommands.append("FAST")
                    if keys[FIRE]:
                        keyboardcommands.append("FIRE")
                        mousepos = pygame.mouse.get_pos()
                        # figure out the direction of the mouse relative to the in the form of a space on a unit circle
                        player_location = ((player_x+screen_width/2-25)+self.camera_ajustment[0]+25,(player_y+screen_height/2-25)+self.camera_ajustment[1]+25)
                        mouse_direction = (mousepos[0]-player_location[0], mousepos[1]-player_location[1])
                        if mouse_direction[0] == 0 and mouse_direction[1] == 0:
                            mouse_direction = (0, 0)
                        else:
                            mouse_direction = (mouse_direction[0]/math.sqrt(mouse_direction[0]**2+mouse_direction[1]**2), mouse_direction[1]/math.sqrt(mouse_direction[0]**2+mouse_direction[1]**2))
                        keyboardcommands.append(str(mouse_direction[0]))
                        keyboardcommands.append(str(mouse_direction[1]))

                    sendkeys = ','.join(str(key) for key in keyboardcommands)
                    self.sendkeys = sendkeys
                    self.client.send(sendkeys.encode('utf-8'))
                elif event.type == pygame.MOUSEMOTION:
                    keyboardcommands = [",ORIENTATION:"]
                    mousepos = pygame.mouse.get_pos()
                    # figure out the direction of the mouse relative to the in the form of a space on a unit circle
                    player_location = ((player_x+screen_width/2-25)+self.camera_ajustment[0]+25,(player_y+screen_height/2-25)+self.camera_ajustment[1]+25)
                    mouse_direction = (mousepos[0]-player_location[0], mousepos[1]-player_location[1])
                    # mouse_direction = (mouse_direction[0]/math.sqrt(mouse_direction[0]**2+mouse_direction[1]**2), mouse_direction[1]/math.sqrt(mouse_direction[0]**2+mouse_direction[1]**2))
                    # fix the divide by zero error
                    if mouse_direction[0] == 0 and mouse_direction[1] == 0:
                        mouse_direction = (0, 0)
                    else:
                        mouse_direction = (mouse_direction[0]/math.sqrt(mouse_direction[0]**2+mouse_direction[1]**2), mouse_direction[1]/math.sqrt(mouse_direction[0]**2+mouse_direction[1]**2))

                    keyboardcommands.append(str(mouse_direction[0]))
                    keyboardcommands.append(str(mouse_direction[1]))
                    
                    sendkeys = ','.join(str(key) for key in keyboardcommands)
                    self.sendkeys = sendkeys
                    self.client.send(sendkeys.encode('utf-8'))

            self.reset_camera = [True, True]
            if "UP" in self.sendkeys:
                if self.camera_ajustment[1] > -self.camera_delay:
                    self.camera_ajustment[1] -= self.camera_move_speed
                self.reset_camera[1] = False
            if "DOWN" in self.sendkeys:
                if self.camera_ajustment[1] < self.camera_delay:
                    self.camera_ajustment[1] += self.camera_move_speed
                self.reset_camera[1] = False
            if "LEFT" in self.sendkeys:
                if self.camera_ajustment[0] > -self.camera_delay:
                    self.camera_ajustment[0] -= self.camera_move_speed
                self.reset_camera[0] = False
            if "RIGHT" in self.sendkeys:
                if self.camera_ajustment[0] < self.camera_delay:
                    self.camera_ajustment[0] += self.camera_move_speed
                self.reset_camera[0] = False
            if "FAST" in self.sendkeys:
                self.camera_delay = 15
            else:
                self.camera_delay = 10
            
            if self.reset_camera[0]:
                if self.camera_ajustment[0] > 0:
                    self.camera_ajustment[0] -= self.camera_move_speed
                elif self.camera_ajustment[0] < 0:
                    self.camera_ajustment[0] += self.camera_move_speed
            if self.reset_camera[1]:
                if self.camera_ajustment[1] > 0:
                    self.camera_ajustment[1] -= self.camera_move_speed
                elif self.camera_ajustment[1] < 0:
                    self.camera_ajustment[1] += self.camera_move_speed
                
            pygame.display.flip()
            if self.killed:
                pygame.quit()
                break
        input("Press enter to exit")
        
    def connect(self):
        if self.client:
            self.client.close()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        self.receive_thread = threading.Thread(target=self.receive)
        self.UI_thread = threading.Thread(target=self.ui)
        self.receive_thread.start()
        self.UI_thread.start()

client = GameClient()