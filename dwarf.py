from race import *
from modifyercontainer import *
class Dwarf(Race):
    def __init__(self):
        Race.__init__(self, "Dwarf")
        self.mods = ModifyerContainer(5,3,5,3,4)
    def getModifyers(self):
        return self.mods
