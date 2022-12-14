import random
from .monde import Monde
from .walker import Walker
from .ingenieur import Ingenieur
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

    def add_engeneer(self, grid_start):
        # ajout de l'ingénieur sur la postition du bâtiment d'ingénieur
        ingenieur = Ingenieur(grid_start, grid_start)
        self.walkerlist.append(ingenieur)

    def update(self):
        should_refresh = False
        for walker in self.walkerlist:
            self.update_move_walker(walker)
            if walker.name == "citizen":
                if walker.actualPosition != walker.destination and walker.chemin != False and walker.nombreDeplacement == 0:
                    if walker.chemin != None :
                        walker.actualPosition = walker.chemin[1]
                        walker.chemin.remove(walker.chemin[0])
                if walker.actualPosition == walker.destination and self.monde.board[walker.destination[0]][walker.destination[1]]["building"].name == 'panneau':
                    self.monde.board[walker.destination[0]][walker.destination[1]]["building"] = self.monde.craft_building(self.monde.information_for_each_tile['tente'])
                    should_refresh = True
            elif walker.name == "citizen_engeneer":
                walker.heal_around(self.monde)

        self.monde.update()

        self.should_refresh = should_refresh

    def update_move_walker(self, walker):
        walker.set_nbdeplacement()
        if walker.name == "citizen":
            walker.set_nextPosition ()
        elif walker.name == "citizen_engeneer":
            walker.find_new_destination(self.monde)

    def check_if_construction_possible_on_grid(self, grid):
        return self.monde.check_if_construction_possible_on_grid(grid)

    def check_if_clear_possible_on_grid(self, grid):
        return self.monde.check_if_clear_possible_on_grid(grid)


    def clear(self,grid):
        if self.check_if_clear_possible_on_grid(grid):
            building = self.monde.board[grid[0]][grid[1]]["building"]
            if building.name == "tente" or building.name == "panneau" or building.name == "engeneer":
                if building.name == "tente" or building.name == "panneau":
                    if building.__class__.__name__ == "Tente":
                        for habitation in self.monde.habitations:
                            if habitation.id == building.id:
                                self.monde.habitations.remove(habitation)
                                break
                elif building.name == "engeneer":
                    for ingenieur in self.monde.ingenieurs:
                        if ingenieur.id == building.id:
                            self.monde.ingenieurs.remove(ingenieur)
                            break

                walker_tmp = None
                for walker in self.walkerlist:
                    if walker.destination == grid:
                        walker_tmp = walker
                        break
                if walker_tmp != None: self.walkerlist.remove(walker_tmp)

            if building.name[0:5] == "route":
                pass

            self.monde.add_building_on_point(grid, 'herbe_{}'.format(random.randint(110,119)))

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
        
