__author__ = 'Admin'

import time
import pygame

class Cloud:
    def __init__(self, image, pos, z):
        self.image = image
        self.x, self.y = pos
        self.z = z
        self.lastTime = time.clock()
        self.image = pygame.transform.smoothscale(self.image, (self.image.get_rect().width / z, self.image.get_rect().height / z))
    def update(self):
        currtime = time.clock()
        if currtime - self.lastTime > .2:
            self.x += .1 * self.z**2
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))