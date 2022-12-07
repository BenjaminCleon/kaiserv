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
        self.should_refresh = False

    def update(self):
        should_refresh = False
        for walker in self.walkerlist:
            self.update_move_walker(walker)
            if walker.actualPosition != walker.destination and walker.chemin != False and walker.nombreDeplacement == 0:
                if walker.chemin != None :
                    walker.actualPosition = walker.chemin[1]
                    walker.chemin.remove(walker.chemin[0])
            if walker.actualPosition == walker.destination and self.monde.board[walker.destination[0]][walker.destination[1]]["building"].name == 'panneau':
                self.monde.board[walker.destination[0]][walker.destination[1]]["building"].name = 'tente'
                self.monde.board[walker.destination[0]][walker.destination[1]]["building"].can_be_erase = self.monde.information_for_each_tile['tente'][1]
                self.monde.board[walker.destination[0]][walker.destination[1]]["building"].can_constructible_over = self.monde.information_for_each_tile['tente'][2]
                self.monde.board[walker.destination[0]][walker.destination[1]]["building"].can_be_walk_through = self.monde.information_for_each_tile['tente'][3]
                should_refresh = True

        self.should_refresh = should_refresh

    def update_move_walker(self, walker):
        walker.set_nbdeplacement()
        walker.set_nextPosition ()

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
        walker = Walker(depart,destination)
        self.walkerlist.append(walker)
        walker.chemin = short_path(numpy.array(self.monde.define_matrix_for_path_finding()),walker.actualPosition,walker.destination)
        walker.set_nextPosition()
        
