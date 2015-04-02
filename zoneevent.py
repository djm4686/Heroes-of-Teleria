from battlevent import *
class ZoneEvent(BattleEvent):
    def __init__(self, ide, tiles):
        BattleEvent.__init__(self, ide, tiles, (14, 38, 205))
        self.tiles = tiles
    def draw(self, surface):
        for x in self.tiles:
            x.drawOutline(surface, self.color, 3)
