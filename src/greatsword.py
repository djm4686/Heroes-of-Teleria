from meleeequipment import *
class GreatSword(MeleeWeapon):
    def __init__(self):
        MeleeWeapon.__init__(self, "Greatsword")
        self.power = 14
    def getPower(self):
        return self.power
