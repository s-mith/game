from GameObject import gameobject
from Player import player
from Tile import tile
from random import *


class world(gameobject):
    def __init__(self, id, x=0, y=0):
        super().__init__(x, y, id)
        self.players = {}
        self.bullets = []
        self.width = 200
        self.height = 200
        self.tile_map = []
        # create a 2d array of tiles
        colors = ["#ff0000", "#00ff00", "#0000ff", "#ffff00", "#00ffff", "#ff00ff"]
        for i in range(self.width):
            self.tile_map.append([])
            for j in range(self.height):
                self.tile_map[i].append(tile((i-100)*100, (j-100)*100, 0, choice(colors)))
                switch = False
        # make a flat version of the tile map on one line
    
    def flat_map(self):
        return [item for sublist in self.tile_map for item in sublist]

    def all_gameobjects(self):
        return self.bullets + self.flat_map() + list(self.players.values())

    def gameobjects_near(self, x, y, range_x, range_y):
        return [obj for obj in self.all_gameobjects() if obj.x > x - range_x and obj.x < x + range_x and obj.y > y - range_y and obj.y < y + range_y]

    def make_player(self,key, x, y, id, user, password):
        self.players[key] = player(x, y, id, user, password)

    def moves(self):
        for OBJ in self.all_gameobjects():
            if hasattr(OBJ, 'move'):
                OBJ.move()

    def __str__(self):
        return "world:{self.id}"