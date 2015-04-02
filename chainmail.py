from armorequipment import *
class ChainMail(Armor):
    def __init__(self):
        Armor.__init__(self, "Chainmail")
        self.ac = 10
    def getAC(self):
        return self.ac
