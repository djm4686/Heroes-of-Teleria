from UIContainer import *
class HorizontalFlexUIContainer(UIContainer):
    def __init__(self):
        UIContainer.__init__(self,0,0,(0,0))
    def addChild(self, child):
        self.width = self.width + child.getWidth()
        self.child.setOrigin((self.x + self.width, self.y))
        self.surface = pygame.transform.scale(self.surface, (self.width, self.height))
        
pygame.init()    
f = FlexUIContainer()
f.addChild(UIContainer(200,200))
