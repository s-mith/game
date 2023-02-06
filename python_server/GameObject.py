import time
import uuid

class gameobject:
    def __init__(self, x, y, id):
        self.birth = time.time()
        self.x = x
        self.y = y
        self.id = id
        self.uuid = uuid.uuid4()
        
    def __str__(self):
        return f"gameobject:{self.id}"
