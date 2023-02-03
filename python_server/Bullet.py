from GameObjectVolume import gameobjectvolume

class bullet(gameobjectvolume):
    def __init__(self, x, y, id, color, direction, speed, damage, owner, player_velocity, width=10, height=10):
        super().__init__(x, y, id, width, height)
        self.color = color
        
        self.velocity_x = direction[0] * speed + player_velocity[0]
        self.velocity_y = direction[1] * speed + player_velocity[1]
        self.damage = damage
        self.owner = owner
        self.lifetime = 5
        

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

    def collisions(self, objects):
        collided = []
        for object in objects:
            if object.id != self.id:
                if self.x + self.width > object.x and self.x < object.x + object.width:
                    if self.y + self.height > object.y and self.y < object.y + object.height:
                        collided.append(object)
        return collided

    def __str__(self):
        return f"bullet:{self.id}"