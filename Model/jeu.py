from .monde import Monde
from .walker import Walker
from .pathfinding import short_path
import numpy

# classe passerelle entre controleur et métier
class Jeu:
    def __init__(self, controleur, size_tile):
        self.width, self.height = controleur.screen.get_size()
        # plateau de jeu
        self.monde = Monde(size_tile, controleur.screen.get_size())
        self.walkerlist = []

    def update(self):
        for walker in self.walkerlist:
            if walker.actualPosition != walker.destination and walker.chemin != False:
                if walker.chemin != None :
                    walker.actualPosition = walker.chemin[1]
                    walker.chemin.remove(walker.chemin[0])
                else:
                    walker.chemin = short_path(numpy.array(self.monde.define_matrix_for_path_finding()),walker.actualPosition,walker.destination)

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

    def walker_creation(self,depart,destination):
        self.walkerlist.append(Walker(depart,destination))
