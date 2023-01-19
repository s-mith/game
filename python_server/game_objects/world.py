from GameObject import gameobject
from Player import player
from Tile import tile
from random import *
from Bullet import bullet
import time


class world(gameobject):
    def __init__(self, id, x=0, y=0):
        super().__init__(x, y, id)
        self.players = {}
        self.bullets = []
        self.tile_width = 200
        self.tile_height = 200
        self.tile_size = 100
        self.tile_map = []
        # create a 2d array of tiles
        colors = ["#ff0000", "#00ff00", "#0000ff", "#ffff00", "#00ffff", "#ff00ff"]
        for i in range(self.tile_width):
            self.tile_map.append([])
            for j in range(self.tile_height):
                self.tile_map[i].append(tile((i-int(self.tile_width/2))*self.tile_size, (j-int(self.tile_height/2))*self.tile_size, 0, choice(colors), self.tile_size, self.tile_size))
        # make a flat version of the tile map on one line
    
    def flat_map(self):
        return [item for sublist in self.tile_map for item in sublist]

    def all_gameobjects(self):
        return self.flat_map() + self.bullets + list(self.players.values())

    def gameobjects_near(self, x, y, range_x, range_y):
        return [obj for obj in self.all_gameobjects() if obj.x > x - range_x and obj.x < x + range_x and obj.y > y - range_y and obj.y < y + range_y]

    def make_player(self,key, x, y, id, user, password):
        self.players[key] = player(x, y, id, user, password)

    def remove_player(self, key):
        del self.players[key]

    def create_bullet(self, x, y, id, color, direction, speed, damage, owner):
        self.bullets.append(bullet(x, y, id, color, direction, speed, damage, owner, (self.players[owner].velocity_x, self.players[owner].velocity_y)))
        self.players[owner].shoot(self.bullets[-1])


    def remove_bullet(self, bullet):
        self.bullets.pop(self.bullets.index(bullet))

    def check_hit(self, obj1, obj2):
        if obj1.x < obj2.x + obj2.width and obj1.x + obj1.width > obj2.x and obj1.y < obj2.y + obj2.height and obj1.y + obj1.height > obj2.y:
            return True
        return False

    def check_bullets(self):
        for bullet in self.bullets:
            targets = bullet.collisions(self.players.values())
            for target in targets:
                if bullet.owner != target.id:
                    target.health -= bullet.damage
                    self.remove_bullet(bullet)
            
        

    def moves(self):
        time_now = time.time()
        for OBJ in self.all_gameobjects():
            if hasattr(OBJ, 'move'):
                OBJ.move()
            if type(OBJ) == bullet:
                if OBJ.birth + OBJ.lifetime < time_now:
                    self.remove_bullet(OBJ)


    def __str__(self):
        return f"world:{self.id}"