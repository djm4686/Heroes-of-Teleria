from armorequipment import *
class ScaleMail(Armor):
    def __init__(self):
        Armor.__init__(self, "Scalemail")
        self.ac = 10
    def getAC(self):
        return self.ac
