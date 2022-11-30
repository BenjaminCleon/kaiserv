
# classe permettant de gérer la logique géométrique du monde
from .building import Building

class Monde:
    def __init__(self, tile_size, screen_size):
        self.board = []
        self.width, self.height = screen_size
        self.tile_size = tile_size
        self.information_for_each_tile = self.get_information_for_each_tile()

    # pour chaque case, nous donnons le rectangle permettant de placer une tile à l'avenir
    def grid_to_board(self, num_lig, num_col, name):
        rect = [
            (num_lig * self.tile_size                            , num_col * self.tile_size            ),
            (num_lig * self.tile_size + self.tile_size, num_col * self.tile_size            ),
            (num_lig * self.tile_size + self.tile_size, num_col * self.tile_size + self.tile_size),
            (num_lig * self.tile_size                            , num_col * self.tile_size + self.tile_size),
        ]

        # pour le passage en vue isométrique
        iso = [self.to_iso(x,y) for x, y in rect]

        minx = min([x for x, y in iso])
        miny = min([y for x, y in iso])

        # retour de la fonction par des informations sur la tuile
        information_building = self.information_for_each_tile[name]
        sortie = {
            "grid": [num_lig, num_col],
            "cart_rect": rect,
            "iso": iso,
            "position_rendu": [minx, miny],
            "building": self.craft_building(information_building)
        }

        return sortie
    
    # passe les coordonnées en isométrique
    def to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y)/2
        return iso_x, iso_y

    # initialise l'entiéreté du plateau
    def init_board(self, file_name):
        for num_lig in range(len(file_name)):
            self.board.append([])
            for num_col in range(len(file_name[num_lig])):
                tile_board = self.grid_to_board(num_lig, num_col, file_name[num_lig][num_col])
                self.board[num_lig].append(tile_board)

    def get_information_for_each_tile(self):
        dictionnaire = {
            'herbe'                         : ['herbe'                         , False, True , True , 1],
            'arbre'                         : ['arbre'                         , True , False, False, 1],
            'eau'                           : ['eau'                           , False, False, False, 1],
            'eau_haut'                      : ['eau_haut'                      , False, False, False, 1],
            'eau_bas'                       : ['eau_bas'                       , False, False, False, 1],
            'eau_droite'                    : ['eau_droite'                    , False, False, False, 1],
            'eau_gauche'                    : ['eau_gauche'                    , False, False, False, 1],
            'eau_coin_haut_gauche'          : ['eau_coin_haut_gauche'          , False, False, False, 1],
            'eau_coin_haut_droite'          : ['eau_coin_haut_droite'          , False, False, False, 1],
            'eau_coin_bas_droite'           : ['eau_coin_bas_droite'           , False, False, False, 1],
            'eau_coin_bas_gauche'           : ['eau_coin_bas_gauche'           , False, False, False, 1],
            'eau_coin_bas_droite_interieur' : ['eau_coin_bas_droite_interieur' , False, False, False, 1],
            'eau_coin_bas_gauche_interieur' : ['eau_coin_bas_gauche_interieur' , False, False, False, 1],
            'eau_coin_haut_gauche_interieur': ['eau_coin_haut_gauche_interieur', False, False, False, 1],
            'eau_coin_haut_droite_interieur': ['eau_coin_haut_droite_interieur', False, False, False, 1]
        }

        return dictionnaire

    def define_matrix_for_path_finding(self):
        return [[self.board[i][j]["building"].get_canbewalkthrough_into_integer() for j in range(0, len(self.board[0]))] for i in range(0,len(self.board)) ]
            
    def check_if_construction_possible_on_grid(self,grid):
        return self.board[grid[0]][grid[1]]["building"].can_constructible_over

    def check_if_clear_possible_on_grid(self,grid):
        return self.board[grid[0]][grid[1]]["building"].can_constructible_over

    def craft_building(self, infos_building):
        return Building(infos_building[0], infos_building[1], infos_building[2], infos_building[3], infos_building[4])

    def add_building_on_point(self, grid_pos, name):
        infos_building = self.information_for_each_tile[name]
        self.board[grid_pos[0]][grid_pos[1]]["building"] = self.craft_building(infos_building)