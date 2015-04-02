from race import *
from modifyercontainer import *
class Halfling(Race):
    def __init__(self):
        Race.__init__(self, "Halfling")
        self.mods = ModifyerContainer(3,6,3,4,4)
    def getModifyers(self):
        return self.mods
