from .monde import Monde

# classe passerelle entre controleur et métier
class Jeu:
    def __init__(self, controleur, size_tile):
        self.width, self.height = controleur.screen.get_size()
        # plateau de jeu
        self.monde = Monde(size_tile, controleur.screen.get_size())

    def update(self):
        pass

    def check_if_construction_possible_on_grid(self, grid):
        return self.monde.check_if_construction_possible_on_grid(grid)

    def check_if_clear_possible_on_grid(self, grid):
        return self.monde.check_if_clear_possible_on_grid(grid)


    def clear(self,grid):
        if self.check_if_clear_possible_on_grid(grid):
            self.monde.add_building_on_point(grid, 'herbe')

    def add_building_on_point(self, grid_pos, path):
        self.monde.add_building_on_point(grid_pos, path)

    def init_board(self, file_name):
        return self.monde.init_board(file_name)

    def get_date(self):
        return self.date

    def get_board(self):
        return self.monde.board
