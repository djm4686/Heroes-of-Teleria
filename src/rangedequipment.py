from equipment import *
class RangedWeapon(Equipment):
    def __init__(self, name, rang = 4):
        Equipment.__init__(self, name)
        self.range = rang
    def getRange(self):
        return self.range
