import socket
import threading
import pygame
import time

DELTA_TIME = 1/60

UP = pygame.K_w
DOWN = pygame.K_s
LEFT = pygame.K_a
RIGHT = pygame.K_d
FAST = pygame.K_LSHIFT


# new_keys += [keys[pygame.K_BACKQUOTE],keys[pygame.K_1],keys[pygame.K_2],keys[pygame.K_3],keys[pygame.K_4],keys[pygame.K_5],keys[pygame.K_6],keys[pygame.K_7],keys[pygame.K_8],keys[pygame.K_9],keys[pygame.K_0],keys[pygame.K_MINUS],keys[pygame.K_EQUALS],keys[pygame.K_BACKSPACE]]
# # qwerty row starting with tab ending with caps lock
# new_keys += [keys[pygame.K_TAB],keys[pygame.K_q],keys[pygame.K_w],keys[pygame.K_e],keys[pygame.K_r],keys[pygame.K_t],keys[pygame.K_y],keys[pygame.K_u],keys[pygame.K_i],keys[pygame.K_o],keys[pygame.K_p],keys[pygame.K_LEFTBRACKET],keys[pygame.K_RIGHTBRACKET],keys[pygame.K_BACKSLASH]]
# # asdf row starting with caps lock ending with enter
# new_keys += [keys[pygame.K_CAPSLOCK],keys[pygame.K_a],keys[pygame.K_s],keys[pygame.K_d],keys[pygame.K_f],keys[pygame.K_g],keys[pygame.K_h],keys[pygame.K_j],keys[pygame.K_k],keys[pygame.K_l],keys[pygame.K_SEMICOLON],keys[pygame.K_QUOTE],keys[pygame.K_RETURN]]
# # zxcv row starting with left shift ending with right shift
# new_keys += [keys[pygame.K_LSHIFT],keys[pygame.K_z],keys[pygame.K_x],keys[pygame.K_c],keys[pygame.K_v],keys[pygame.K_b],keys[pygame.K_n],keys[pygame.K_m],keys[pygame.K_COMMA],keys[pygame.K_PERIOD],keys[pygame.K_SLASH],keys[pygame.K_RSHIFT]]
# # space bar crtls alt and arrow keys
# new_keys += [keys[pygame.K_SPACE],keys[pygame.K_LCTRL],keys[pygame.K_LALT],keys[pygame.K_UP],keys[pygame.K_DOWN],keys[pygame.K_LEFT],keys[pygame.K_RIGHT]]



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
        self.killed = False


    def receive(self):
        while True:
            try:
                game_info = self.client.recv(1024).decode('utf-8')
                if game_info == 'LOGIN':
                    self.client.send(self.user.encode('utf-8'))
                    self.client.send(self.password.encode('utf-8'))
                else:
                    # game info is normally a string that has multiple rows of coma seperated values
                    try:
                        game_info = game_info.split("\n")
                        game_info = list(filter(lambda x: (False if x=="" else True), game_info))
                        game_info = list(map(lambda x : x.split(","), game_info))
                        self.players = game_info
                    except:
                        pass
            except:
                print('An error occured, Disconnected!')
                self.client.close()
                break
        self.killed = True




    def ui(self):
        last_time = time.time()
        pygame.init()
        # screen = pygame.display.set_mode((640, 480))
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        while True:
            # Process events
            screen.fill((0,0,0))
            # for player in self.players draw a rectangle using the coodinates from the indexes 2 and 3
            for player in self.players:
                x = float(player[1])
                y = float(player[2])
                color = player[3]
                pygame.draw.rect(screen, color, (x, y,30,30))


                

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    # print all the keys that are pressed
                    keys = pygame.key.get_pressed()
                    # every key on the keyboard 
                    keyboardcommands = ["KEYS:"]
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
                    
                    sendkeys = ','.join(str(key) for key in keyboardcommands)
                    self.client.send(sendkeys.encode('utf-8'))
            # Update the game state

            # Render the screen
           
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
