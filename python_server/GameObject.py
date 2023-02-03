import time

class gameobject:
    def __init__(self, x, y, id):
        self.birth = time.time()
        self.x = x
        self.y = y
        self.id = id
        
    def __str__(self):
        return f"gameobject:{self.id}"
