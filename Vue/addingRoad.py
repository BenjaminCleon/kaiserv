import pygame
import math

from .basic_action import Basic_Action

class Adding_Road(Basic_Action):

    def __init__(self, surface):
        Basic_Action.__init__(self, surface)
        self.can_thinking = False
        self.chemins = None


    def getChemin(self, start, end):
        if start[0] >= 0 and start[1] >= 0 and len(self.carriere.informations_tiles) > start[0] and len(self.carriere.informations_tiles[start[0]]) > start[1] and \
           end  [0] >= 0 and end  [1] >= 0 and len(self.carriere.informations_tiles) > end  [0] and len(self.carriere.informations_tiles[end  [0]]) > end  [1] and \
                self.carriere.controleur.check_if_construction_possible_on_grid(start) and self.carriere.controleur.check_if_construction_possible_on_grid(end):
            self.chemins = self.carriere.controleur.find_path(start, end)

        if type(self.chemins) == bool or self.chemins == None:
            self.chemins = []
            self.chemins.append(start)

    def draw(self):
        size_of_original_image = self.original_surface.get_size()
        self.image_to_draw = pygame.transform.scale(self.original_surface, (size_of_original_image[0]*self.carriere.zoom.multiplier, size_of_original_image[1]*self.carriere.zoom.multiplier))

        if self.grid_position_start != None and self.grid_position_end != None:
            self.getChemin(self.grid_position_start, self.grid_position_end)
            for grid in self.chemins:
                self.draw_for_an_image(grid)
        else:
            self.grid_position_without_first_click = self.mouse_to_grid(self.carriere.current_surface, self.carriere.camera.scroll, self.carriere.controleur.TILE_SIZE * self.carriere.zoom.multiplier, self.pos_without_first_click)
            self.draw_for_an_image(self.grid_position_without_first_click)

    def events(self, event):
        n=1
        #n <= len(self.chemins)
        Basic_Action.events(self, event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: self.can_thinking = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.can_thinking:

            file_names = [[self.carriere.informations_tiles[i][j]["building"].name for j in
                          range(0, len(self.carriere.informations_tiles[i]))] for i in
                          range(0, len(self.carriere.informations_tiles))]
            for grid in self.chemins:
                file_names[grid[0]][grid[1]] = "route"

            for num_lig in range(0, len(file_names)):
                for num_col in range(0, len(file_names)):
                    if file_names[num_lig][num_col][0:5] == "route":
                        coords = [(-1,0),(0,1),(1,0),(0,-1)]
                        binary_array = []
                        for coord in coords:
                            if (num_lig+coord[0]) >= 0 and (num_lig+coord[0]) < len(file_names)    and \
                               (num_col+coord[1] >= 0) and (num_col+coord[1] < len(file_names[num_lig])) and \
                                file_names[num_lig+coord[0]][num_col+coord[1]][0:5] == "route":
                                binary_array.append(1)
                            else:
                                binary_array.append(0)

                        sum = 0
                        for binary_value, i in zip(binary_array, range(3,-1, -1)):
                            sum = int(sum + binary_value*math.pow(2, i))

                        tile = "route droite"
                        match sum:
                            case  0: pass
                            case  1: tile = "route Debut de route"
                            case  2: tile = "route Debut de routebis"
                            case  3: tile = "route virage vers le bas"
                            case  4: tile = "route Fin de route"
                            case  5: tile = "route droite"
                            case  6: tile = "route Virage gauche vers droite"
                            case  7: tile = "route Début intersection deux voix"
                            case  8: tile = "route Fin de routebis"
                            case  9: tile = "route Virage gauche vers droite vers le haut"
                            case 10: tile = "route verticale"
                            case 11: tile = "route Intersectionbis"
                            case 12: tile = "route Virage gauche vers le bas"
                            case 13: tile = "route Intersection"
                            case 14: tile = "route Debut intersection deux voixbis"
                            case 15: tile = "route Carrefour"

                        self.carriere.controleur.add_building_on_point((num_lig,num_col), tile)

            self.is_progress = False
            self.carriere.reload_board()