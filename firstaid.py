import spell
import particles
import pygame

class FirstAid(spell.Spell):

    def __init__(self):
        spell.Spell.__init__(self, "First Aid", 10)
        self.range = 1
        self.description = "This hero uses his First Aid skills to heal himself in battle."
    def getParticleEmitter(self, point):
        p = particles.GalaxyParticleManager(point[0], point[1], 4, pygame.image.load("images/medium_white_particle.png"))
        p.createGalaxyEffect()
        return p
    def target(self, t):
        t.heal(self.damage)
