from UIContainer import *
class VerticalUIContainer(UIContainer):
    def __init__(self, width, height, (x,y) = (0,0)):
        UIContainer.__init__(self, width, height, (x, y))
        self.childContainers = []
        self.childheight = 0
    def addChild(self, child):
        child.setOrigin((self.rect.x, self.rect.y + self.childheight))
        self.childheight = self.childheight + child.getHeight()
        self.childContainers.append(child)
    def draw(self, surface):
        for x in self.childContainers:
            x.draw(surface)
