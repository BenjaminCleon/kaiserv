
import pygame

class Zoom:

    def __init__(self):
        self.level_zoom = 40
        self.multiplier = self.level_zoom/100
        self.should_scale = False

    def update(self, diff):
        self.level_zoom += diff
        self.multiplier = self.level_zoom/100
        self.should_scale = True
