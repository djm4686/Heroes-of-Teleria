from isometrictile import *
import time
import math
class IsoBoard:
    def __init__(self, rows, cols, size = 64, json = None):
        self.tiles = []
        self.rows = rows
        self.cols = cols
        self.size = size
        self.lastTime = time.clock()
        self.totalTiles = 0
        self.animationEquation = None
        self.selectedTile = None
        if not json:
            self.generateBoard()
            self.setNeighbors()
    def add_zone(self):
        pass
    def getTileByID(self, id):
        for x in range(len(self.tiles)):
            for y in range(len(self.tiles[x])):
                if self.tiles[x][y].getID() == id:
                    return (x, y)
    def clear_zones(self):
        pass
    def getZone2(self):
        returns = []
        for x in self.tiles:
            for y in x:
                if y.getZone() == 2:
                    returns.append(y)
        return returns
    def getNeighborTiles(self, tile, r):
        if r == 1:
            return [tile]
        tiles = [tile]
        neighbors = tile.getNeighbors()
        for t in neighbors:
            if t != None:
                tiles += self.getNeighborTiles(t, r-1)
        tiles = list(set(tiles))
        return tiles
    def collidepoint(self, point):
        for row in self.tiles[-1::-1]:
            for tile in row[-1::-1]:
                if tile.collidepoint(point):
                    return tile
    def setNewCoords(self, coordDifference):
        self.x += coordDifference[0]
        self.y += coordDifference[1]
        for x in self.tiles:
            for y in x:
                y.x = y.x + coordDifference[0]
                y.y = y.y + coordDifference[1]
                y.reMakePoints()
    def setDirection(self, hero, point):
        tile = hero.getTile()
        x,y = point
        cx,cy = tile.getCenter()
        if x > cx and y < cy:
            hero.setDirection(1)
        if x < cx and y < cy:
            hero.setDirection(4)
        if x > cx and y > cy:
            hero.setDirection(2)
        if x < cx and y > cy:
            hero.setDirection(3)
    def getZone1(self):
        returns = []
        for x in self.tiles:
            for y in x:
                if y.getZone() == 1:
                    returns.append(y)
        return returns
    def setNeighbors(self):
        for row in range(len(self.tiles)):
            for col in range(len(self.tiles[row])):
                if row != 0:
                    self.tiles[row][col].setN1(self.tiles[row - 1][col])
                if col != len(self.tiles[row])-1:
                    self.tiles[row][col].setN2(self.tiles[row][col + 1])
                if row != len(self.tiles) -1:
                    self.tiles[row][col].setN3(self.tiles[row+1][col])
                if col != 0:
                    self.tiles[row][col].setN4(self.tiles[row][col-1])
    def getTileIndeces(self, tile):
        for row in range(len(self.tiles)):
            for col in range(len(self.tiles[row])):
                if self.tiles[row][col].getID() == tile.getID():
                    return (col, row)
    def generateJSON(self):
        jsons = ["'rows': {}, 'cols': {}".format(self.rows, self.cols)]
        for x in self.tiles:
            for tile in x:
                jsons.append(tile.generateJSON())
        return jsons
    @staticmethod
    def createTileListFromJSON(row, col, jsons):
        tiles = []
        i = 0
        j = -1
        for json in jsons:
            if i == 0 or i > col:
                tiles.append([])
                i = 1
                j += 1
            tiles[j].append(IsometricTile.makeFromJSON(json))
            i += 1
        return tiles
    @staticmethod
    def createFromJSON(jsons):
        row, col = jsons[0]["rows"], jsons[0]["cols"]
        tiles = IsoBoard.createTileListFromJSON(row, col, jsons[1::])
        newBoard = IsoBoard(row, col, json=True)
        newBoard.x = 400
        newBoard.y = 100
        newBoard.tiles = tiles
        newBoard.setNeighbors()
        return newBoard

    def addRow(self):
        self.rows += 1
        self.tiles.append([])
        for column in range(self.cols):
            self.tiles[-1].append(IsometricTile(self.totalTiles,
                                                self.x + (self.size * .5 * column) - ((self.rows-1) * self.size * .5),
                                                self.y + ((self.rows - 1) * self.size * .5 * .5) + (.5 * column * self.size * .5),
                                                size = self.size,
                                                height = 1,
                                                xindex = column,
                                                yindex = self.rows - 1,
                                                zone = 0))
            self.totalTiles += 1
        self.setNeighbors()
    def addColumn(self):
        self.cols += 1
        for row in range(self.rows):
            self.tiles[row].append(IsometricTile(self.totalTiles,
                                                self.x + (self.size * .5 * (self.cols-1) - (row * self.size * .5)),
                                                self.y + (row * self.size * .5 * .5) + (.5 * (self.cols-1) * self.size * .5),
                                                size = self.size,
                                                height = 1,
                                                xindex = self.cols-1,
                                                yindex = row,
                                                zone = 0))
            self.totalTiles += 1
        self.setNeighbors()
    @staticmethod
    def createBaseBoard():
        return IsoBoard(10, 10)

    def generateBoard(self, xcoord = 400, ycoord = 100):
        self.x = xcoord
        self.y = ycoord
        self.setStartCoords((xcoord, ycoord))
    def setStartCoords(self, coord):
        xcoord = coord[0]
        ycoord = coord[1]
        j = 0
        for row in range(self.rows):
            self.tiles.append([])
            for column in range(self.cols):
                #h = (self.cols - column - row)
                #if h < 1:
                #    h = 1
                h = 1
                if row > (self.rows-1) / 2:
                    self.tiles[row].append(IsometricTile(j, xcoord + (self.size * .5 * column) - (row * self.size * .5), ycoord + (row * self.size * .5 * .5) + (.5 * column * self.size * .5), size = self.size, height = h, xindex=column, yindex=row, zone = 2))
                else:
                    self.tiles[row].append(IsometricTile(j, xcoord + (self.size * .5 * column) - (row * self.size * .5), ycoord + (row * self.size * .5 * .5) + (.5 * column * self.size * .5), size = self.size, xindex=column, yindex=row, height = h))
                j += 1
        self.totalTiles = j
    def drawHeroes(self, surface):
        for row in self.tiles:
            for tile in row:
                tile.drawHero(surface)
    def centerCamera(self, tile):
        pass

    def selectTile(self, tile):
        self.selectedTile = tile

    def drawTiles(self, surface):
        if self.animationEquation:
            pass
        for row in self.tiles:
            for tile in row:
                tile.drawTile(surface)
        if self.selectedTile:
            self.selectedTile.drawOutline(surface, (255,0,0), 3)
        
