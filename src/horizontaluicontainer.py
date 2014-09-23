from UIContainer import *
class HorizontalUIContainer(UIContainer):
    def __init__(self, width, height, (x,y) = (0,0)):
        UIContainer.__init__(self, width, height, (x, y))
        self.childContainers = []
        self.childwidth = 0
    def addChild(self, child):
        child.setOrigin((self.rect.x + self.childwidth, self.rect.y))
        self.childwidth = self.childwidth + child.getWidth()
        self.childContainers.append(child)
    def draw(self, surface):
        for x in self.childContainers:
            x.draw(surface)
