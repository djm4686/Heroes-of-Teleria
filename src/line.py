class Line:
    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2
        self.slope = (self.p1[1] - self.p2[1])/(self.p1[0]-self.p2[0])
        self.b = -((self.p1[0] * self.slope) - self.p1[1])
    def isPointGreaterThan(self, point):
        if point[1] < (point[0] * self.slope) + self.b:
            return True
        else:
            return False
    def isPointLessThan(self, point):
        if point[1] > (point[0] * self.slope) + self.b:
            return True
        else:
            return False
