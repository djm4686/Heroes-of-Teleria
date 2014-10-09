class Spell:
    def __init__(self, name, damage, effects = []):
        self.type = "spell"
        self.name = name
        self.effects = effects
        self.damage = damage
        self.aoe = 1
        self.range = 1
        self.currentExp = 0
        self.reqExp = 100
        self.friendlyFire = False
        self.description = "Placeholder"
    def getCurrentExp(self):
        return self.currentExp
    def getDescription(self):
        return self.description
    def getFriendlyFire(self):
        return self.friendlyFire
    def getReqExp(self):
        return self.reqExp
    def getRange(self):
        return self.range
    def getAoe(self):
        return self.aoe
    def getTarget(self):
        return self.target
    def setTarget(self, tile):
        self.target = tile
    def getName(self):
        return self.name
    def getEffects(self):
        return self.effects
    def getDamage(self):
        return self.damage
    def getType(self):
        return self.type
