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
        self.button_col = (249, 231, 159)
        self.hover_col = (255, 253, 208)
        self.click_col = (9, 48, 22)
        self.text_col = (0, 0, 0)
        self.current_col = self.button_col


    #affichage des bouton 
    def draw(self):
        # Créer la police
        text_img = self.font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        pygame.draw.rect(self.screen, self.current_col, self.button_rect)
        self.screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 10))

    #couleur du bouton selon action souris
    def check_button(self):
        action = False
        pos = pygame.mouse.get_pos()
        mouse_action = pygame.mouse.get_pressed()

        if self.button_rect.collidepoint(pos):
            if mouse_action[0]:
                pygame.draw.rect(self.screen, self.click_col, self.button_rect)

                self.current_col = self.click_col
                action = True
            else:
                self.current_col = self.hover_col
        else:
            self.current_col = self.button_col

        return action
