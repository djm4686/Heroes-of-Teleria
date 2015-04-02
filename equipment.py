class Equipment:
    def __init__(self, name, spell = None):
        self.name = name
        self.spell = spell
    def getSpell(self):
        return self.spell
    def setSpell(self, a):
        self.spell = a
    def getName(self):
        return self.name
