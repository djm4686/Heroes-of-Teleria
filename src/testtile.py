import pygame
from pygame.locals import *
from isoboard import *
pygame.init()
s = pygame.display.set_mode((800,600))
s.fill((255,255,255))
tileboard =  IsoBoard(20,20)
tileboard.draw(s)
while True:
    for event in pygame.event.get():
        if event.type == MOUSEMOTION:
            if tileboard.collidepoint(event.pos) :
                
        if event.type == QUIT:
            pygame.quit()
    pygame.display.update()
