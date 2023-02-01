from GameObject import gameobject

class player(gameobject):
    def __init__(self, x, y, id, user, password, color="#ffffff", width=50, height=50):
        super().__init__(x, y, id)
        self.color = color
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
        self.width = width
        self.height = height

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

    def commands(self, commands):
        if "DOWN" in commands:
            self.increase_velocity_y()
        if "UP" in commands:
            self.decrease_velocity_y()
        if "RIGHT" in commands:
            self.increase_velocity_x()
        if "LEFT" in commands:
            self.decrease_velocity_x()
        if "FAST" in commands:
            self.max_velocity = 20
            self.velocity_increment = 4
        else:
            self.max_velocity = 10
            self.velocity_increment = 2

    def __str__(self):
        return "player:{self.username}"

