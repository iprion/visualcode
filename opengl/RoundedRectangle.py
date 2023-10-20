from opengl.Rectangle import *


class RoundedRectangle(Rectangle):
    def __init__(self, width, height, cornerRound, dashed=False):
        super().__init__(width, height, dashed)
        self.cornerRound = cornerRound