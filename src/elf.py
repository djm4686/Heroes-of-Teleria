from race import *
from modifyercontainer import*
class Elf(Race):
    def __init__(self):
        Race.__init__(self, "Elf")
        self.mods = ModifyerContainer(2,5,3,5,5)
    def getModifyers(self):
        return self.mods
