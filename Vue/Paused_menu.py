import pygame as pg
import sys
from file_reader import reader_bmp_map
from Vue.Buttons_settings import *


class Pause_menu:

    def __init__(self, screen, controleur):
        self.controleur = controleur
        self.displayed = False
        self.screen = screen
        self.x = screen.get_width()/2 #récupère longueur
        self.y = screen.get_height()/2 #récupère hauteur
        self.font = pg.font.SysFont('Constantia', 75)
        self.font2 = pg.font.SysFont('Constantia', 50)
        self.space = 60
        self.new_game = False
        self.save = False
        self.menu_principale = False
        self.quitter = False
    

        self.new_game = Button_Menu_paused(self.screen, self.x, self.y  - (self.space), 'Nouvelle partie')
        self.save = Button_Menu_paused(self.screen, self.x, self.y  - (2*self.space), 'Sauvegarder')
        self.menu_principale = Button_Menu_paused(self.screen, self.x, self.y  - (3*self.space), 'Menu principale')
        self.quitter = Button_Menu_paused(self.screen, self.x, self.y  - (4*self.space), 'Quitter le jeu')
            

    def events(self):
        if self.displayed :
            if self.menu_principale.check_button():
                self.controleur.playing = False
                self.controleur.paused = False 

            if self.new_game.check_button():#
                self.controleur.create_new_game()
                self.controleur.metier.init_board(reader_bmp_map(2, self.controleur))
                self.controleur.ihm.init_sprite()
                self.controleur.play()
            
            if self.save.check_button():
                self.controleur.ihm.carriere.Save_game()

            if self.quitter.check_button():
                run = False
                sys.exit()


    def draw(self):
        if self.displayed :

            pg.draw.rect(self.screen, (255, 255, 255),((self.x),(self.y),200,400))
        
            self.new_game.draw()
            self.save.draw()
            self.menu_principale.draw()
            self.quitter.draw()
        