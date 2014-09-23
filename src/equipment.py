class Equipment:
    def __init__(self, name):
        self.name = name
        self.ability = None
    def getAbility(self):
        return self.ability
    def setAbility(self, a):
        self.ability = a
    def getName(self):
        return self.name
