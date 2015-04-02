import button, pygame
class MultiLineTextButton(button.Button):
    def __init__(self, textLabels = [], callBack = None, cbparams = [], rect = pygame.Rect(0,0,100,50), color = (152,172,186), textColor = (0,0,0)):
        button.Button.__init__(self, textLabels[0], callBack, cbparams, rect, color, textColor)
        self.textLabels = textLabels
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, self.textColor, self.rect, 1)
        i = 0
        for x in self.textLabels:
            r = pygame.Rect(self.rect.x + 25, self.rect.y + 20 + i * 20, x.get_rect().width, x.get_rect().height)
            surface.blit(x, r)
            i = i + 1
