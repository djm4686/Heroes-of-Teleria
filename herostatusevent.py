from battlevent import *
class HeroStatusEvent(BattleEvent):
    def __init__(self, ide, tile, color = (14, 38, 205)):
        BattleEvent.__init__(self, ide, tile, color)
        self.tile = tile
    def draw(self, surface):
        self.tile.drawShaded(surface, self.color)
