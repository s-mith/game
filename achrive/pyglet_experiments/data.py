game_info = """
d,0,0"""
game_info = game_info.split("\n")
print(game_info)
game_info = list(filter(lambda x: (True if x=="" else False), iterable))
print(game_info)
game_info = map(lambda x : x.split(","))
print(game_info)
self.players = game_info