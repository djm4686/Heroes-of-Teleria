__author__ = 'Admin'
import pygame, time

pygame.init()
s = pygame.display.set_mode((800,600))
i = pygame.image.load("images/medium_grey_particle.png")
width = 20
height = 20
while True:
    il = pygame.transform.smoothscale(i, (width, height))
    s.fill((255,255,255))
    s.blit(il, il.get_rect())
    width += 1
    height += 1
    pygame.display.update()
    time.sleep(1)