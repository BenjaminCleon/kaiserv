from Vue.menu_settings import *
import pygame
from pygame.locals import *

class Button_Menu():
    def __init__(self, screen, x, y, text):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = WIDTH_BUTTON
        self.height = HEIGHT_BUTTON
        self.button_rect = Rect(self.x, self.y, self.width, self.height)
        self.text = text
        self.font = pygame.font.SysFont('Constantia', 30) #cambriacambriamath , arialblack,calibri, bahnschrift
        self.clicked = False
        self.button_col = YELLOW_LIGHT
        self.hover_col = BEIGE
        self.click_col = GREEN_DARK
        self.text_col = BLACK
        self.current_col = self.button_col

    def draw(self):
        text_img = self.font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        pygame.draw.rect(self.screen, self.current_col, self.button_rect)
        self.screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 10))

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
