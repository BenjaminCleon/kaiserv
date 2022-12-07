
# classe permettant de gérer la logique géométrique du monde
from .building import Building
import math

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
    def init_board(self, file_names):
        file_names = self.manage_for_water(file_names)

        for num_lig in range(len(file_names)):
            self.board.append([])
            for num_col in range(len(file_names[num_lig])):
                tile_board = self.grid_to_board(num_lig, num_col, file_names[num_lig][num_col])
                self.board[num_lig].append(tile_board)

    def manage_for_water(self, file_names):
        file_names_return = []
        for num_lig  in range(len(file_names)):
            file_names_return.append([])
            for num_col in range(len(file_names[num_lig])):
                if file_names[num_lig][num_col] == "eau":
                    binary_traitement = []
                    for coord in [(-1,0),(0,1),(1,0),(0,-1)]:
                        #admettons que nous avons sommes avec i = 8 et j = 7, nous etudierons pour déterminer les routes les cases
                        #                     file_names[7][7]
                        # file_names[8][6] file_names[8][7] file_names[8][8]
                        #                     file_names[9][7]
                        #
                        if (num_lig+coord[0])>=0 and (num_lig+coord[0])<len(file_names) and (num_col+coord[1])>=0 and (num_col+coord[1])<len(file_names[num_lig]) and file_names[num_lig+coord[0]][num_col+coord[1]] == 'eau':
                            binary_traitement.append(1)
                        else:
                            binary_traitement.append(0)

                    sum = 0
                    for binary_value, i in zip(binary_traitement, range(3,-1, -1)):
                        sum = int(sum + binary_value*math.pow(2, i))
                    
                    match sum:
                        case 15: file_names_return[num_lig].append("eau") # (-1,0),(0,1),(1,0),(0,-1)
                        case 14: file_names_return[num_lig].append("eau") # (-1,0),(0,1),(1,0)
                        case 13: file_names_return[num_lig].append("eau") # (-1,0),(0,1),(0,-1)
                        case 12: file_names_return[num_lig].append("eau") # (-1,0),(0,1)
                        case 11: file_names_return[num_lig].append("eau") # (-1,0)(1,0),(0,-1)
                        case 10: file_names_return[num_lig].append("eau_isole_verticale") # (-1,0),(1,0)
                        case  9: file_names_return[num_lig].append("eau") # (-1,0),(0,-1)
                        case  8: file_names_return[num_lig].append("eau_fin_haut") # (-1,0)
                        case  7: file_names_return[num_lig].append("eau") # (0,1),(1,0),(0,-1)
                        case  6: file_names_return[num_lig].append("eau") # (0,1),(1,0)
                        case  5: file_names_return[num_lig].append("eau_isole_horizontale") # (0,1),(0,-1)
                        case  4: file_names_return[num_lig].append("eau_fin_droite") # (0,1)
                        case  3: file_names_return[num_lig].append("eau") # (1,0),(0,-1)
                        case  2: file_names_return[num_lig].append("eau_fin_bas") # (1,0)
                        case  1: file_names_return[num_lig].append("eau_fin_gauche") # (0,-1)
                        case  0: file_names_return[num_lig].append("eau_isole")
                else:
                    file_names_return[num_lig].append("herbe")

        return file_names_return
                


    def get_information_for_each_tile(self):
        dictionnaire = {
            'herbe'                                  : ['herbe'                                 , False, True , True , 1],
            'panneau'                                : ['panneau'                               , False, True , True , 1],
            'tente'                                  : ['tente'                                 , True , False, False, 1],
            'arbre'                                  : ['arbre'                                 , True , False, False, 1],
            'eau'                                    : ['eau'                                   , False, False, False, 1],
            'eau_haut'                               : ['eau_haut'                              , False, False, False, 1],
            'eau_bas'                                : ['eau_bas'                               , False, False, False, 1],
            'eau_droite'                             : ['eau_droite'                            , False, False, False, 1],
            'eau_gauche'                             : ['eau_gauche'                            , False, False, False, 1],
            'eau_coin_haut_gauche'                   : ['eau_coin_haut_gauche'                  , False, False, False, 1],
            'eau_coin_haut_droite'                   : ['eau_coin_haut_droite'                  , False, False, False, 1],
            'eau_coin_bas_droite'                    : ['eau_coin_bas_droite'                   , False, False, False, 1],
            'eau_coin_bas_gauche'                    : ['eau_coin_bas_gauche'                   , False, False, False, 1],
            'eau_coin_bas_droite_interieur'          : ['eau_coin_bas_droite_interieur'         , False, False, False, 1],
            'eau_coin_bas_gauche_interieur'          : ['eau_coin_bas_gauche_interieur'         , False, False, False, 1],
            'eau_coin_haut_gauche_interieur'         : ['eau_coin_haut_gauche_interieur'        , False, False, False, 1],
            'eau_coin_haut_droite_interieur'         : ['eau_coin_haut_droite_interieur'        , False, False, False, 1],
            'eau_isole'                              : ['eau_isole'                             , False, False, False, 1],
            'eau_isole_horizontale'                  : ['eau_isole_horizontale'                 , False, False, False, 1],
            'eau_isole_verticale'                    : ['eau_isole_verticale'                   , False, False, False, 1],
            'eau_fin_gauche'                         : ['eau_fin_gauche'                        , False, False, False, 1],
            'eau_fin_droite'                         : ['eau_fin_droite'                        , False, False, False, 1],
            'eau_fin_bas'                            : ['eau_fin_bas'                           , False, False, False, 1],
            'eau_fin_haut'                           : ['eau_fin_haut'                          , False, False, False, 1],
            'route droite'                           : ['route droite'                          , False,  True,  True, 1],
            'route verticale'                        : ['route verticale'                       , False,  True,  True, 1],
            'route droitebis'                        : ['route droitebis'                       , False,  True,  True, 1],
            'route horizontale'                      : ['route horizontale'                     , False,  True,  True, 1],
            'virage vers le bas'                     : ['virage vers le bas'                    , False,  True,  True, 1],
            'Virage gauche vers droite'              : ['Virage gauche vers droite'             , False,  True,  True, 1],
            'Virage gauche vers droite vers le haut' : ['Virage gauche vers droite vers le haut', False,  True,  True, 1],
            'Debut de route'                         : ['Debut de route'                        , False,  True,  True, 1],
            'Debut de routebis'                      : ['Debut de routebis'                     , False,  True,  True, 1],
            'Fin de route'                           : ['Fin de route'                          , False,  True,  True, 1],
            'Fin de routebis'                        : ['Fin de routebis'                       , False,  True,  True, 1],
            'Fin de routebis2'                       : ['Fin de routebis2'                      , False,  True,  True, 1],
            'Début intersection deux voix'           : ['Début intersection deux voix'          , False,  True,  True, 1],
            'Debut intersection deux voixbis'        : ['Debut intersection deux voixbis'       , False,  True,  True, 1],
            'Intersection'                           : ['Intersection'                          , False,  True,  True, 1],
            'Intersectionbis'                        : ['Intersectionbis'                       , False,  True,  True, 1],
            'Carrefour'                              : ['Carrefour'                             , False,  True,  True, 1]
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