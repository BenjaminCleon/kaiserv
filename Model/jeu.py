from calendar import Calendar
from datetime import datetime
from .monde import Monde
from .dateKaiser import DateKaiser

BEGIN_YEAR  = -350
BEGIN_MONTH = 1
BEGIN_DAY   = 1

# classe passerelle entre controleur et métier
class Jeu:
    def __init__(self, controleur):
        self.controleur = controleur
        self.width, self.height = self.controleur.screen.get_size()
        # plateau de jeu
        self.monde = Monde(self.controleur)
        # date dans le jeu
        self.date = DateKaiser(BEGIN_YEAR,BEGIN_MONTH,BEGIN_DAY)

    def update(self):
        pass

    def check_if_construction_possible_on_grid(self, grid):
        return self.monde.check_if_construction_possible_on_grid(grid)

    def check_if_clear_possible_on_grid(self, grid):
        return self.monde.check_if_construction_possible_on_grid(grid)


    def add_building_on_point(self, grid_pos, path):
        self.monde.add_building_on_point(grid_pos, path)

    def init_board(self, file_name):
        return self.monde.init_board(file_name)

    def get_date(self):
        return self.date

    def get_board(self):
        return self.monde.board
