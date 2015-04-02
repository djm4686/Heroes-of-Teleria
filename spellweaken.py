__author__ = 'Admin'
import spell
import spelleffectlowerbaseattack
import particles
import pygame
class Weaken(spell.Spell):
    def __init__(self):
        spell.Spell.__init__(self, "Weaken", 0, [spelleffectlowerbaseattack.LowerBaseAttack(-10)])
        self.description = "Weakens an enemy Hero within 1 tile. Causes the target to do reduced damage on attacks."
    def getParticleEmitter(self, point):
        p = particles.GalaxyParticleManager(point[0], point[1], 4, pygame.image.load("images/medium_red_particle.png"))
        p.createGalaxyEffect()
        return p
    def target(self, t):
        t.addSpellEffect(self.effects[0])

