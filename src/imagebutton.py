import button, pygame
class ImageButton(button.Button):
    def __init__(self, image, cb, cbp = []):
        self.font = pygame.font.Font(pygame.font.get_default_font(), 12)
        button.Button.__init__(self, textLabel = self.font.render(" ", True, (0,0,0)), callBack = cb, cbparams = cbp)
        self.image = image
        self.rect = self.image.get_rect()
    def setRect(self, rect):
        self.rect = rect
    def draw(self, surface):
        surface.blit(self.image, self.rect)
