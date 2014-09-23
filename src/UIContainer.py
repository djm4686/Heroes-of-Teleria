import pygame
class UIContainer(pygame.Rect):
    def __init__(self, width, height, (x,y) = (0,0)):
        pygame.Rect.__init__(self, x, y, width, height)
        self.height = height
        self.width = width
        self.surface = pygame.Surface((width, height))
        self.childwidth = 0
        self.childheight = 0
        self.children = []
    def getHeight(self):
        return self.height
    def addChild(self, child):
        child.setOrigin((self.rect.x, self.rect.y))
        self.childwidth = self.childwidth + child.getHeight()
        self.childheight = self.childheight + child.getHeight()
        self.childContainers.append(child)
    def getWidth(self):
        return self.width
    def setOrigin((x,y)):
        self.rect.x = x
        self.rect.y = y
    def draw(self, surface):
        surface.blit(self.surface, self)
        for x in self.children:
            x.draw(self)
