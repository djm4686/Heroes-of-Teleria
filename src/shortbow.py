from rangedequipment import *
class ShortBow(RangedWeapon):
    def __init__(self):
        RangedWeapon.__init__(self, "Shortbow")
        self.power = 10
    def getPower(self):
        return self.power
