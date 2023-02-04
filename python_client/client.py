import socket
import threading
import random
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
MENU = pygame.K_ESCAPE
HOST = "134.195.121.194"
PORT = 3004

COLORS = ["#FFE5CC", "#E6E6FA", "#BDBDBD", "#F4F4F4", "#B3E5FC", "#B3E5FC", "#ffffff", "#000000"]

class Button:
    def __init__ (self, x, y, w, h, color, text, text_color, action, hover_color = None, hover_text_color = None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.color_normal = color
        self.text = text
        self.text_color = text_color
        self.action = action
        self.hover_color = hover_color
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))
        font = pygame.font.SysFont('Comic Sans MS', 25)
        text = font.render(self.text, True, self.text_color)
        textRect = text.get_rect()
        textRect.center = (self.x+self.w/2,self.y+self.h/2)
        screen.blit(text, textRect)
    
    def click(self):
        self.action()

    def is_hovered(self, mousepos):
        if mousepos[0] > self.x and mousepos[0] < self.x+self.w and mousepos[1] > self.y and mousepos[1] < self.y+self.h:
            self.color = self.hover_color
            return True
        else:
            self.color = self.color_normal
            return False

class InputField:
    def __init__ (self, x, y, w, h, color, text, text_color, hover_color = None, hover_text_color = None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.color_normal = color
        self.text = text
        self.text_color = text_color
        self.hover_color = hover_color
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))
        font = pygame.font.SysFont('Comic Sans MS', 25)
        text = font.render(self.text, True, self.text_color)
        textRect = text.get_rect()
        textRect.center = (self.x+self.w/2,self.y+self.h/2)
        screen.blit(text, textRect)
    
    def write(self, char):
        self.text += char

    def backspace(self):
        self.text = self.text[:-1]

    

    def is_hovered(self, mousepos):
        if mousepos[0] > self.x and mousepos[0] < self.x+self.w and mousepos[1] > self.y and mousepos[1] < self.y+self.h:
            self.color = self.hover_color
            return True
        else:
            self.color = self.color_normal
            return False



class GameClient:
    def __init__(self):
        self.client = None
        self.host = HOST
        self.port = PORT
        self.user = ""
        self.password = ""
        self.game_info = []
        self.killed = False
        self.new_game_info = ""
        self.camera_delay = 10
        self.camera_ajustment = [0,0]
        self.reset_camera = [False, False]
        self.camera_move_speed = 0.25
        self.sendkeys = ""
        self.tile_size = 50
        self.meun_open = False
        self.do_respawn = False
        self.meun_buttons = []
        self.player_status = "1"
                           
        self.ui()        

    def collect_data(self):
        while True:
            part = self.client.recv(2500).decode('utf-8')
            if part == "LOGIN":
                return part
            if "///" in part:
                # split on first occurence of /// and return the first part
                end_of_return, start_of_new = part.split("///", 1)
                temp = self.new_game_info
                self.new_game_info = start_of_new
                
                return temp + end_of_return
            else:
                temp = "".join((self.new_game_info, part))
                self.new_game_info = temp
            # except:
            #     print('An error occured!')
            #     pass          

    def receive(self):
        while self.client != None:
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

    def kill(self):
        self.killed = True

    def close(self):
        self.client.close()
        self.client = None

    def resume(self):
        self.meun_open = False

    def respawn(self):
        self.do_respawn = True
        self.meun_open = False

    def login(self):
        self.connect()
        # start a thread that will receive data from the server
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()




    
    def ui(self):
        pygame.init()
        # screen = pygame.display.set_mode((640, 480))
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen_width, screen_height = pygame.display.get_surface().get_size()
        while self.killed == False:
            if self.client:
                buttons = [
                            {"color": (255, 255, 255), "text": "respawn", "text_color": (0, 0, 0), "action": self.respawn, "hover":(0,255,0)},
                            {"color": (255, 255, 255), "text": "resume", "text_color": (0, 0, 0), "action": self.resume, "hover":(77,77,77)},
                            {"color": (255, 255, 255), "text": "quit", "text_color": (0, 0, 0), "action": self.close, "hover":(255,0,0)},
                        ]
                for i,button in enumerate(buttons):
                    self.meun_buttons.append(Button(screen_width/2-100,screen_height/2-25+(i*80),200,50, button["color"], button["text"], button["text_color"], button["action"], button["hover"]))

                while True:
                    
                    # Process events
                    screen.fill((0,0,0))
                    # for player in self.players draw a rectangle using the coodinates from the indexes 2 and 3
                    screen_width, screen_height = pygame.display.get_surface().get_size()
                    player_x = 0
                    player_y = 0
                    name1 = ""
                    score1 = ""
                    name2 = ""
                    score2 = ""
                    name3 = ""
                    score3 = ""
                    try:
                        for gameobject in self.game_info:
                            if gameobject[0] == "world":
                                self.tile_size = int(gameobject[2])
                                # put the score in the top left corner
                                name1 = gameobject[3]
                                score1 = gameobject[4]
                                name2 = gameobject[5]
                                score2 = gameobject[6]
                                name3 = gameobject[7]
                                score3 = gameobject[8]

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
                                alive = gameobject[8]
                                # if alive == "0" everything should be transparent
                                if alive == "1":
                                    if self.player_status == "0":
                                        self.player_status = "1"
                                        self.meun_open = False 
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
                                else:
                                    # make the player transparent
                                    if name == self.user:
                                        self.meun_open = True
                                        self.player_status = "0"
                                    # pygame.draw.rect(screen, pygame.Color((255,255,255)), ((x+screen_width/2-25)+self.camera_ajustment[0],(y+screen_height/2-25)+self.camera_ajustment[1], w, h))
                                    s = pygame.Surface((w, h), pygame.SRCALPHA)   
                                    s.fill((255,255,255,155))                
                                    screen.blit(s, ((x+screen_width/2-25)+self.camera_ajustment[0],(y+screen_height/2-25)+self.camera_ajustment[1]))
                                    # draw name under the player
                                    font = pygame.font.SysFont('Comic Sans MS', 10)
                                    text = font.render(name+"[dead]", True, (0, 0, 0))
                                    text.set_alpha(155)
                                    textRect = text.get_rect()
                                    textRect.center = ((x+screen_width/2)+self.camera_ajustment[0],(y+screen_height/2+37)+self.camera_ajustment[1])
                                    screen.blit(text, textRect)


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
                        
                        if self.meun_open:
                                # make the buttons with 200 width and 50 height centered on the screen
                                # get the mouse position
                                for button in self.meun_buttons:
                                    button.is_hovered(pygame.mouse.get_pos())
                                    button.draw(screen) 
                        font = pygame.font.SysFont('Comic Sans MS', 40)
                        textsurface = font.render(name1 + ": " + score1, False, (255, 255, 255))
                        screen.blit(textsurface,(0,0))
                        if name2 != "":
                            textsurface = font.render(name2 + ": " + score2, False, (255, 255, 255))
                            screen.blit(textsurface,(0,40))
                        if name3 != "":
                            textsurface = font.render(name3 + ": " + score3, False, (255, 255, 255))
                            screen.blit(textsurface,(0,80))
                    except:
                        pass
                    if self.do_respawn:
                        self.client.send(",ACTIONS:,respawn".encode('utf-8'))
                        self.do_respawn = False
                        

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                            # print all the keys that are pressed
                            keys = pygame.key.get_pressed()
                            if keys[MENU]:
                                self.meun_open = not self.meun_open
                            if self.killed:
                                self.meun_open = True

                            if event.type == pygame.MOUSEBUTTONDOWN and self.meun_open:
                                for button in self.meun_buttons:
                                    if button.is_hovered(pygame.mouse.get_pos()):
                                        button.click()
                                

                            if not self.meun_open:
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


            else:
                
                selected = None
                button = Button(screen_width/2-100, screen_height/2+100, 200, 50, (255, 255, 255), "Login", (0, 0, 0), self.login, (0, 255, 0), (0, 0, 0))
                Escape = Button(screen_width/2-100, screen_height/2+200, 200, 50, (255, 255, 255), "Exit", (0, 0, 0), self.kill, (0, 255, 0), (0, 0, 0))
                
                userFeild =  InputField(screen_width/2-100, screen_height/2-100, 200, 50, (255, 255, 255), "Username", (0, 0, 0),(255, 255, 255))
                passwordFeild =  InputField(screen_width/2-100, screen_height/2, 200, 50,  (255, 255, 255), "Password", (0, 0, 0),(255, 255, 255))
                while not self.client and not self.killed:
                    # center the button as if it were going to have 2 buttons above it
                    screen.fill((0,200,0))
                    mouse_pos = pygame.mouse.get_pos()
                    
                    button.draw(screen)
                    
                    Escape.draw(screen)
                    
                    userFeild.draw(screen)
                    
                    passwordFeild.draw(screen)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            if button.is_hovered(mouse_pos):
                                self.user = userFeild.text
                                self.password = passwordFeild.text
                                if self.user == "Username":
                                    nouns = [
                                            'people',
                                            'history',
                                            'way',
                                            'art',
                                            'world',
                                            'information',
                                            'map',
                                            'two',
                                            'family',
                                            'government',
                                            'health',
                                            'system',
                                            'computer',
                                            'meat',
                                            'year',
                                            'thanks',
                                            'music',
                                            'person',
                                            'reading',
                                            'method',
                                            'data',
                                            'food',
                                            'understanding',
                                            'theory',
                                            'law',
                                            'bird',
                                            'literature',
                                            'problem',]
                                    
                                    self.user = random.choice(nouns) + str(random.randint(0, 1000))
                                button.click()
                            elif userFeild.is_hovered(mouse_pos):
                                selected = userFeild
                            elif passwordFeild.is_hovered(mouse_pos):
                                selected = passwordFeild  
                            elif Escape.is_hovered(mouse_pos):
                                Escape.click() 
                        if event.type == pygame.KEYDOWN:
                            # if the key is backspace and the user is typing in a feild
                            if event.key == pygame.K_BACKSPACE and selected != None:
                                selected.backspace()
                            # if the key is tab switch the selected feild
                            elif event.key == pygame.K_TAB:
                                if selected == userFeild:
                                    selected = passwordFeild
                                else:
                                    selected = userFeild
                            # if the key any other key and the user is typing in a feild
                            elif selected != None:
                                selected.write(event.unicode)
                            self.user = userFeild.text
                            self.password = passwordFeild.text

                    pygame.display.flip()
        print("killed")
        pygame.quit()
        print("killed")
        # kill the program
        exit()
        print("killed")

            



    def connect(self):
        if self.client:
            self.client.close()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

client = GameClient()