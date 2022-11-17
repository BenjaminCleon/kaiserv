import os
from tkinter import Y
import pygame

class Button_HUD:
    def __init__(self, screen, x, y, name):
        self.position_top_left = (x,y)
        self.image_hover = None
        self.image_click = None
        self.who_is_visible = ""
        self.screen = screen
        self.name = name
        self.init_picture()
        self.rect = pygame.Rect( x,y, 41*self.screen.get_width()/1920,28*self.screen.get_height()/1080)

    def init_picture(self):
        image_click = f"./assets/hud/{self.name}_click.png"
        image_hover = f"./assets/hud/{self.name}_hover.png"

        if os.path.exists(image_click) and os.path.exists(image_hover):
            self.image_click = pygame.image.load(image_click).convert_alpha()
            self.image_hover = pygame.image.load(image_hover).convert_alpha()

    def draw(self):
        if self.who_is_visible == "image_hover" and self.image_hover != None:
            self.screen.blit(self.image_hover, self.position_top_left)
        elif self.who_is_visible == "image_click" and self.image_click != None:
            self.screen.blit(self.image_click, self.position_top_left)