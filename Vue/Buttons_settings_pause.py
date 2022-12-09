import pygame
from pygame.locals import *

class Button_Menu_paused():
    def __init__(self, screen, x, y, text):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = 50
        self.height = 30
        self.button_rect = Rect(self.x, self.y, self.width, self.height)
        self.text = text
        self.font = pygame.font.SysFont('Constantia', 30) #cambriacambriamath , arialblack,calibri, bahnschrift
        self.clicked = False
        self.text_original = (0, 0, 0)
        self.text_click = (255, 255, 255) 
        self.text_base = self.text_original
        self.text_hover = (165, 42, 42)
      


    #affichage des bouton 
    def draw(self):
        # Créer la police
        text_img = self.font.render(self.text, True, self.text_base)
        text_len = text_img.get_width()
        self.screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 10))

    #couleur du bouton selon action souris
    def check_button(self):
        action = False
        pos = pygame.mouse.get_pos()
        mouse_action = pygame.mouse.get_pressed()

        if self.button_rect.collidepoint(pos):
            if mouse_action[0]:

                self.text_base = self.text_click
                action = True
            else:
                self.text_base = self.text_hover
        else:
            self.text_base = self.text_original

        return action
