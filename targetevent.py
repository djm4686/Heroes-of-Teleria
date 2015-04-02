from battlevent import *
class TargetEvent(BattleEvent):
    def __init__(self, ide, tile, rang, color = (205, 14, 38)):
        BattleEvent.__init__(self, ide, tile, color)
        self.tile = tile
        self.range = rang
        self.tiles = self.makeTiles()
    def getTiles(self):
        return self.tiles
    def makeTiles(self):
        rang = self.range
        tiles = [self.tile]
        temptiles = [self.tile]
        currtile = self.tile
        i = 0
        while rang - i > 1:
            for t in tiles:
                for x in t.getNeighbors():
                    if x!= None:
                        m = False
                        for t2 in temptiles:
                            if t2.getID() == x.getID():
                                m = True
                        if m == False:
                            temptiles.append(x)
            
            tiles = [] + temptiles
            i = i + 1
        return tiles
    def draw(self, surface):
        for x in self.tiles:
            x.drawOutline(surface, self.color, 3)
