__author__ = 'dmadden'
import moveevent
import random
import math

class AIBehavior:


    def __init__(self, party):
        self.PLAYERID = 2
        self.party = party

    def checkTileID(self, tiles, id):
        for x in tiles:
            if x != None and x.getID() == id:
                return True
        else:
            return False
    def processTurn(self, board, hero, hasMoved, hasAttacked):
        return self.determineCommand(board, hero, hasMoved, hasAttacked)
    def determineCommand(self, board, hero, hasMoved, hasAttacked):
        if hasMoved and hasAttacked:
            return "End", None
        elif hasAttacked != True:
            tile = self.checkForAdjacentEnemy(hero)
            if tile != None:
                return "MeleeAttack", tile
            if tile == None and not hasMoved:
                return "Move", self.AIMove(board, hero)
            elif hasMoved:
                return "End", None
        elif hasMoved != True:
            return "End", None


    def AIProcessMove(self, board, hero):
        moveTile = self.AIMove(board, hero)
        if moveTile:
            hero.setTile(moveTile)
            x, y = board.getTileByID(moveTile.getID())
            moveTile.setGameObject(hero)
            board.tiles[x][y] = moveTile
        return board
    def AIAttack(self, board, hero):
        tile = self.checkForAdjacentEnemy(hero)
        if tile:
            defender = tile.getGameObject()
            hero.meleeAttack(defender)
            tile.setGameObject(defender)
            x, y = board.getTileByID(tile.getID())
            board.tiles[x][y] = tile
        return board

    def getTargets(self, board, hero):
        self.heuristic = lambda current, dest: math.sqrt(abs(current.getCenter()[1] - dest.getCenter()[1])**2 + abs(current.getCenter()[0] - dest.getCenter()[0])**2)/60
        dests = []
        for x in board.tiles:
            for y in x:
                if y.getGameObject() != None and not self.checkTileID(self.party.getHeroes(), y.getGameObject().getID()) and not y.getGameObject().isDead():
                    y.dist = self.heuristic(hero.tile, y)
                    dests.append(y)
        return dests
    def checkForAdjacentEnemy(self, hero):
        for x in hero.getTile().getNeighbors():
            if x != None and x.getGameObject() != None and not self.checkTileID(self.party.getHeroes(), x.getGameObject().getID()) and not x.getGameObject().isDead():
                return x
        return None


    def AIMove(self, board, hero):
        tiles = moveevent.MoveEvent(200, hero.getTile(), hero.getMovementRange()).makeTiles()
        dests = self.getTargets(board, hero)
        dest = sorted(dests, key=lambda y: y.dist)[0]
        self.heuristic = lambda current: math.sqrt(abs(current.getCenter()[1] - dest.getCenter()[1])**2 + abs(current.getCenter()[0] - dest.getCenter()[0])**2)/60
        start = hero.getTile()
        start.last = None
        closedSet = []
        openSet = [start]
        start.gscore = 0

        while len(openSet) > 0:
            current = sorted(openSet, key=lambda x: self.heuristic(x))[0]
            if self.checkTileID(dest.getNeighbors(), current.getID()) or current.getID() == dest.getID():
                return self.reconstructPath(current, tiles)
            closedSet.append(openSet.pop(0))
            for neighbor in current.getNeighbors():
                if neighbor == None or self.checkTileID(closedSet, neighbor.getID()) or neighbor.getGameObject() != None:
                    continue
                tentgscore = current.gscore + 1

                if not self.checkTileID(openSet, neighbor.getID()):
                    #print "FOUND ONE!!!"
                    neighbor.gscore = tentgscore
                    neighbor.last = current
                    neighbor.fscore = neighbor.gscore + self.heuristic(neighbor)
                    if not self.checkTileID(closedSet, neighbor.getID()):
                        openSet.append(neighbor)
        return False



    def reconstructPath(self, current, tiles):
        total_path = [current]
        if current in tiles:
                return current
        while current.last is not None:
            current = current.last
            if current in tiles:
                return current






