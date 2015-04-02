from meleeequipment import *
class Pike(MeleeWeapon):
    def __init__(self):
        MeleeWeapon.__init__(self, "Pike")
        self.power = 11
    def getPower(self):
        return self.power
