class BattleEvent:
    def __init__(self, ide, tiles, color):
        self.id = ide
        self.tiles = tiles
        self.color = color
    def getID(self):
        return self.id
    def draw(self, surface):
        pass
