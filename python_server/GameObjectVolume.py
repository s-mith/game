from GameObject import gameobject

class gameobjectvolume(gameobject):
    def __init__(self, x, y, id, width, height):
        super().__init__(x, y, id)
        self.width = width
        self.height = height

    def __str__(self):
        return f"gameobjectvolume:{self.id}"