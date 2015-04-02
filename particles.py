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
        self.images = [pygame.image.load("images/medium_red_particle.png"),
                       pygame.image.load("images/medium_blue_particle.png"),
                       pygame.image.load("images/medium_grey_particle.png")]
    def createSmokeEffect(self):
        currtime = time.clock()
        while len(self.particles) < 100 and currtime - self.lastUpdate > .05:
            self.addParticle(SmokeParticleEffect(self.images[2], (self.x-10,self.y - 15), Vector(0,0), Vector(0, -1), 3))
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
        self.image = image.convert_alpha()
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height
        self.origin = origin
        self.currCoords = origin
        self.velocity = velocity
        self.acceleration = acceleration
        self.ttl = ttl
        self.rect = pygame.Rect(self.origin, (self.image.get_rect().width*5, self.image.get_rect().height*5))
        self.initialImage = self.image
        self.x = self.rect.x
        self.y = self.rect.y
        self.lastUpdate = time.clock()
        self.firstUpdate = time.clock()
        self.size = 1
        self.alpha = 255
        self.image.set_alpha(self.alpha)
        self.done = False
    def blit_alpha(self, target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width()*4, source.get_height()*4)).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)
        target.blit(temp, location)
    def update(self):
        currupdate = time.clock()
        if self.lastUpdate == None:
            self.lastUpdate = currupdate
        if currupdate - self.lastUpdate > .02:
            self.size += .02
            self.alpha = int(255 - ((currupdate - self.firstUpdate)/self.ttl) * 255)
            x = self.currCoords[0]
            y = self.currCoords[1]
            x = (math.sin(currupdate*random.randrange(1,5))*random.randrange(0,4)) + x
            y = y - 1
            self.currCoords = (x,y)
            self.image = pygame.transform.smoothscale(self.initialImage, (int(self.width * self.size), int(self.height * self.size)))
            self.image.set_alpha(self.alpha)
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
            self.alpha = 0
            self.done = True
    def draw(self, surface):
        #surface.blit(self.image, self.rect)
        self.blit_alpha(surface, self.image, (self.rect.x, self.rect.y), self.alpha)


class GalaxyParticle:

    def __init__(self, image, origin, velocity, angle, ttl, size):
        self.image = image.convert_alpha()
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height
        self.origin = origin
        self.currCoords = origin
        self.angle = angle * (2 * math.pi/360)
        self.velocity = Vector(velocity, self.angle)
        self.acceleration = Vector(0, 0)
        self.size = 1 + float(size)/10
        self.image = pygame.transform.smoothscale(self.image, (int(self.width*self.size), int(self.height*self.size)))
        self.ttl = ttl
        self.rect = pygame.Rect(self.origin, (self.image.get_rect().width*5, self.image.get_rect().height*5))
        self.initialImage = self.image
        self.x = self.rect.x
        self.y = self.rect.y
        self.lastUpdate = time.clock()
        self.firstUpdate = time.clock()
        self.size = 1
        self.alpha = 255
        self.image.set_alpha(self.alpha)
        self.done = False

    def blit_alpha(self, target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width()*4, source.get_height()*4)).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)
        target.blit(temp, location)

    def applyAccel(self, a):
        self.acceleration = a

    def update(self):
        currupdate = time.clock()
        if self.lastUpdate == None:
            self.lastUpdate = currupdate
        elif currupdate - self.lastUpdate > .2:
            self.velocity.addVector(self.acceleration)
            self.x += self.velocity.magnitudeX
            self.y += self.velocity.magnitudeY
            self.alpha = int(255 - ((currupdate - self.firstUpdate)/self.ttl) * 255)
        if currupdate - self.firstUpdate > self.ttl:
            self.done = True
    def draw(self, surface):
       self.blit_alpha(surface, self.image, (self.x, self.y), self.alpha)


class GalaxyParticleManager:

    def __init__(self, x, y, ttl, particleImage):
        self.ttl = ttl
        self.particles = []
        self.lastUpdate = time.clock()
        self.x = x
        self.y = y
        self.dead = False
        self.changedCenter = False
        self.startTime = time.clock()
        self.image = particleImage
    def die(self):
        self.dead = True
    def distanceFromCenter(self, p):
        x = self.x - p.x
        y = self.y - p.y
        d = math.sqrt(x**2 + y**2)
        if d > 10:
            return d
        else:
            return 10

    def angleFromCenter(self, p):
        x = self.x - p.x
        y = self.y - p.y
        if x != 0:
            return math.atan2(y,x)
        else:
            return .01
    def changeCenter(self, x, y):
        self.x = x
        self.y = y
        self.changedCenter = True
    def createGalaxyEffect(self):
        currtime = time.clock()
        while len(self.particles) < 20 and currtime - self.lastUpdate > .05:
            self.particles.append(GalaxyParticle(image = self.image, origin = (self.x+random.randrange(-20,20), self.y+random.randrange(-20,20)), velocity = .01,
                                                 angle = random.randrange(0, 360), ttl = 4, size = random.randrange(0, 5)))
            self.lastUpdate = currtime
    def update(self):
        curTime = time.clock()
        for x in range(len(self.particles)):
            try:
                self.particles[x].update()
                self.particles[x].applyAccel(Vector((1/self.distanceFromCenter(self.particles[x])**2), self.angleFromCenter(self.particles[x])))
                if self.particles[x].done or self.distanceFromCenter(self.particles[x]) > 200:
                    self.particles.pop(x)
                    x -= 1

            except IndexError:
                break
        if curTime - self.startTime > self.ttl:
            self.die()
        else:
            self.createGalaxyEffect()

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)



class Vector:
    def __init__(self, mag, angle):
        self.magnitudeX = math.cos(angle) * mag
        self.magnitudeY = math.sin(angle) * mag
    def addVector(self, v):
        self.magnitudeX += v.magnitudeX
        self.magnitudeY += v.magnitudeY

if __name__ == "__main__":
    p = GalaxyParticleManager(300,300, 5)
    #p2 = GalaxyParticleManager(400,300)
    p.createGalaxyEffect()
    pygame.init()
    s = pygame.display.set_mode((800,600))
    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
            if e.type == MOUSEMOTION:
                p.changeCenter(e.pos[0], e.pos[1])

        pygame.display.update()
        s.fill((0,0,0))
        p.update()
        #p2.update()
        p.draw(s)
        #p2.draw(s)
