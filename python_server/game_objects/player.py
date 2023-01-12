import random

def magic_hex_color():
    temp = [random.randint(123,255), random.randint(123,255), random.randint(123,255)]
    deaden = random.randint(1,2)
    if deaden == 1:
        temp[random.randint(0,2)] = 0
    if deaden == 2:
        # choose a value that isn't already 0 and make it 0
        list = []
        for i in range(3):
            if temp[i] != 0:
                list.append(i)
        temp[list[random.randint(0,len(list)-1)]] = 0
    # cast temp to tuple
    temp = tuple(temp)
    return '#%02x%02x%02x' % temp


class player:
    def __init__(self, user, password):
        self.x = 0
        self.y = 0
        self.color = magic_hex_color()
        self.health = 100
        self.alive = True
        self.max_velocity = 10
        self.velocity_increment = 2
        self.velocity_x = 0
        self.velocity_y = 0
        self.friction = 0.75
        self.username = user
        self.password = password
        self.keys = ""

        
    def increase_velocity_x(self):
        if self.velocity_x < self.max_velocity:
            self.velocity_x += self.velocity_increment
    
    def decrease_velocity_x(self):
        if self.velocity_x > -self.max_velocity:
            self.velocity_x -= self.velocity_increment

    def increase_velocity_y(self):
        if self.velocity_y < self.max_velocity:
            self.velocity_y += self.velocity_increment

    def decrease_velocity_y(self):
        if self.velocity_y > -self.max_velocity:
            self.velocity_y -= self.velocity_increment

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_x *= self.friction
        self.velocity_y *= self.friction
        if abs(self.velocity_x) <= 0.1:
            self.velocity_x = 0
        if abs(self.velocity_y) <= 0.1:
            self.velocity_y = 0