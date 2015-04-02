from targetevent import *
class MoveEvent(TargetEvent):
    def __init__(self, ide, tile, rang):
        TargetEvent.__init__(self, ide, tile, rang, color = (14,38,205))
        self.tile = tile
    def makeTiles(self):
        rang = self.range
        tiles = [self.tile]
        temptiles = [self.tile]
        currtile = self.tile
        i = 0
        while rang - i > 1:
            for t in tiles:
                for x in t.getNeighbors():
                    if x!= None and x.getGameObject() == None:
                        temptiles.append(x)
            
            tiles = [] + temptiles    
            i = i + 1
        return tiles
##    def getTiles(self, currtile = None, tiles = [], rang = None):
##        if rang == None:
##            rang = self.range
##            currtile = self.tile
##            tiles = []
##        print rang
##        if rang == 1:
##            return currtile
##        for x in self.tile.getNeighbors():
##            here = False
##            for y in tiles:
##                if x != None and x.getID() != y.getID():
##                    pass
##                else:
##                    here = True
##            if here == False:
##                t = self.getTiles(x, tiles, rang-1)
##                if isinstance(t, list):
##                    tiles = tiles + t
##                else:
##                    tiles = tiles.append(t)
##        print tiles
##        return tiles
