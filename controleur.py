import pygame

from file_reader import set_tile_size
from Model.jeu import Jeu
from Vue.IHM   import IHM

class Controleur:
    def __init__(self):
        # démarrage de pygame
        pygame.init()

        # variable locale
        self.playing = False
        running = True

        # initialisation des valeurs de paramètre
        self.TILE_SIZE = set_tile_size("./settings.txt")

        # initialisation des attributs
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.clock  = pygame.time.Clock()

        self.metier = None
        self.ihm    = IHM(self)

        self.grid_width = self.grid_height = 0

        # boucle du menu
        self.ihm.menu.display_main()
        while running:
            # boucle du jeu
            self.ihm.events()
            self.ihm.menu.events()
            self.ihm.menu.draw()
            self.clock.tick(60)
            while self.playing:
                self.clock.tick(60)
                self.ihm.events()
                #self.metier.update()
                self.ihm.update()
                self.ihm.draw()

        pygame.exit()

    def play(self):
        self.playing = True

    def check_if_construction_possible_on_grid(self, grid):
        return self.metier.check_if_construction_possible_on_grid(grid)

    def add_building_on_point(self, grid_pos, name):
        self.metier.add_building_on_point(grid_pos, name)

    def clear(self, grid_pos, name):
        self.metier.clear(grid_pos, name)

    def get_board(self):
        return self.metier.get_board()

    def create_new_game(self):
        self.metier = Jeu(self, self.TILE_SIZE)
    
    def find_path(self,spawn,grid):
        return astar(self.metier.monde.define_matrix_for_path_finding(),spawn,grid)

Controleur()
