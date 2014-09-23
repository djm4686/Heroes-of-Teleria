from armorequipment import *
class PlateMail(Armor):
    def __init__(self):
        Armor.__init__(self, "Platemail")
        self.ac = 10
    def getAC(self):
        return self.ac
