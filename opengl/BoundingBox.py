from opengl.Rectangle import *

class BoundingBox(Rectangle):
    def __init__(self, width, height, center):
        super().__init__(width,height, False)
        self.center = center

    def containsPoint(self, p):
        return p[0] >= self.minX() and p[0] <= self.maxX() and p[1] >= self.minY() and p[1] <= self.maxY()

    def getOverlap(self, bb, separationDistance):
        x1 = bb.maxX() - self.minX() + separationDistance

        if x1>0:
            x2 = self.maxX() - bb.minX() + separationDistance
            if x2>0:
                x3 = bb.maxY() - self.minY() + separationDistance
                if x3>0:
                    x4 = self.maxY() - bb.minY() + separationDistance
                    if x4>0:
                        minx = min(x1,x2,x3,x4)
                        if minx == x1:
                            return x1*LEFT
                        elif minx == x2:
                            return x2*RIGHT
                        elif minx == x3:
                            return x3*DOWN
                        else:
                            return x4*UP
        return ZERO