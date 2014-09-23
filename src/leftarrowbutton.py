import imagebutton, pygame
class LeftArrowButton(imagebutton.ImageButton):
    def __init__(self, cb, cbp = []):
        self.bgimage = pygame.image.load("images/buttonRound_blue.png")
        imagebutton.ImageButton.__init__(self, self.bgimage, cb, cbp)
        self.arrow = pygame.image.load("images/arrowBlue_left.png")
    def draw(self, surface):
        arect = self.arrow.get_rect()
        arect.center = self.rect.center
        arect.y = arect.y - 2
        arect.x = arect.x - 1
        surface.blit(self.bgimage, self.rect)
        surface.blit(self.arrow, arect)
        
