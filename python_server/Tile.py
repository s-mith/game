from GameObjectVolume import gameobjectvolume

class tile(gameobjectvolume):
    def __init__(self, x, y, id, color, size, is_wall = False, is_solid = False, is_visible = False, is_explored = False, is_walkable = True):
        super().__init__(x, y, id, size, size)
        self.color = color
        self.is_wall = is_wall
        self.is_solid = is_solid
        self.is_visible = is_visible
        self.is_explored = is_explored
        self.is_walkable = is_walkable

    def __str__(self):
        return f"tile:{self.id}"