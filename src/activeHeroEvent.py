from battlevent import *
class activeHeroEvent(BattleEvent):
    def __init__(self, ide, tile):
        BattleEvent.__init__(self, ide, tile, (14, 133, 205))
        self.tile = tile
    def draw(self, surface):
        self.tile.drawShaded(surface, self.color)
