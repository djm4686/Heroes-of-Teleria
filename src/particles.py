import math, time, pygame, random
from pygame.locals import *
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def addVector(self, v):
        self.x = self.x + v.x
        self.y = self.y + v.y
    def getVectorMag(self):
        return math.sqroot(self.x**2 + self.y**2)
    def getVectorX(self):
        return self.x
    def getVectorY(self):
        return self.y
class SmokeParticleManager:
    def __init__(self, x, y):
        self.particles = []
        self.lastUpdate = time.clock()
        self.x = x
        self.y = y
        self.images = [pygame.image.load("images/particle_red.png"),
                       pygame.image.load("images/particle_blue.png")]
    def createSmokeEffect(self):
        currtime = time.clock()
        while len(self.particles) < 200 and currtime - self.lastUpdate > .1:
            self.addParticle(SmokeParticleEffect(random.choice(self.images), (random.randrange(self.x - 10,self.x),random.randrange(self.y - 10, self.y)), Vector(0,0), Vector(0, -1), 3))
            self.lastUpdate = currtime
    def addParticle(self, p):
        self.particles.append(p)
    def update(self):
        for x in range(len(self.particles)):
            try:
                self.particles[x].update()
                if self.particles[x].done == True:
                    self.particles.pop(x)
                    x = x-1
                    
            except IndexError:
                break
        self.createSmokeEffect()
    def draw(self, surface):
        for x in self.particles:
            x.draw(surface)
class ExplosionParticle:
    def __init__(self, image, origin):
        pass
class SmokeParticleEffect:
    def __init__(self, image, origin, velocity, acceleration, ttl):
        self.image = image
        self.origin = origin
        self.currCoords = origin
        self.velocity = velocity
        self.acceleration = acceleration
        self.ttl = ttl
        self.rect = pygame.Rect(self.origin, (self.image.get_rect().width, self.image.get_rect().height))
        self.lastUpdate = time.clock()
        self.firstUpdate = time.clock()
        self.done = False
    def update(self):
        currupdate = time.clock()
        if self.lastUpdate == None:
            self.lastUpdate = currupdate
        if currupdate - self.lastUpdate > .02:
            x = self.currCoords[0]
            y = self.currCoords[1]
            x = (math.sin(currupdate*random.randrange(1,5))*random.randrange(0,4)) + self.currCoords[0]
            y = y - 1
            self.currCoords = (x,y)
            
            self.rect.x = x
            self.rect.y = y
            self.lastUpdate = currupdate
##            x = self.currCoords[0] + self.velocity.getVectorX()
##            y = self.currCoords[1] + self.velocity.getVectorY()
##            self.currCoords = (x,y)
##            self.velocity.addVector(self.acceleration)
##            self.rect.x = self.currCoords[0]
##            self.rect.y = self.currCoords[1]
            
        if currupdate - self.firstUpdate > self.ttl:
            self.done = True
    def draw(self, surface):
        surface.blit(self.image, self.rect)
if __name__ == "__main__":
    p = ParticleManager(300,300)
    p2 = ParticleManager(400,300)
    p.createSmokeEffect()
    pygame.init()
    s = pygame.display.set_mode((800,600))
    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
        pygame.display.update()
        s.fill((0,0,0))
        p.update()
        p2.update()
        p.draw(s)
        p2.draw(s)
