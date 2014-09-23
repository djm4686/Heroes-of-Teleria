from rangedequipment import *
class LongBow(RangedWeapon):
    def __init__(self):
        RangedWeapon.__init__(self, "Longbow")
        self.power = 10
    def getPower(self):
        return self.power
