from pygame import Rect
from settings import *

class Pixel(Rect):
    def __init__(self, row, column):
        super().__init__(0,0,0,0)
        self.color = None
        self.row = row
        self.column = column


    def draw(self, pos, color):
        if self.collidepoint(pos):
            self.color = color

    def clear(self, pos):
        if self.collidepoint(pos):
            self.color = None