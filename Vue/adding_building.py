import pygame

from .selectionneur_zone import SelectionneurZone

class Adding_Building(SelectionneurZone):
    def __init__(self, surface, path):
        SelectionneurZone.__init__(self, surface)
        self.path = path
        self.can_thinking = False

    def events(self, event):
        SelectionneurZone.events(self, event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: self.can_thinking = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.can_thinking:
            for grid in self.grid_to_draw:
                if grid[0] >= 0 and grid[1] >= 0 and len(self.carriere.informations_tiles) > grid[0] and len(self.carriere.informations_tiles[grid[0]]) > grid[1] and \
                    self.carriere.controleur.check_if_construction_possible_on_grid(grid):
                        self.carriere.controleur.add_building_on_point(grid, self.carriere.dictionnaire_reverse_by_path[self.path])
                        print(self.carriere.controleur.find_path((39,20),grid))

            self.is_progress = False
            self.carriere.reload_board()

    def draw(self):
        SelectionneurZone.draw(self)
        if self.is_progress:
            for grid in self.grid_to_draw:
                if grid[0] >= 0 and grid[1] >= 0 and len(self.carriere.informations_tiles) > grid[0] and len(self.carriere.informations_tiles[grid[0]]) > grid[1]:
                    is_construction_possible_on_this_grid = self.carriere.controleur.check_if_construction_possible_on_grid(grid)
                    if is_construction_possible_on_this_grid :color = (0, 255, 0)
                    else : color = (255,0,0)
                    iso_for_validation = [(x*self.carriere.zoom.multiplier+self.carriere.current_surface.get_width()/2 + self.carriere.camera.scroll.x,
                                        y*self.carriere.zoom.multiplier+ self.carriere.camera.scroll.y) for x,y in self.carriere.informations_tiles[grid[0]][grid[1]]["iso"]]
                    pygame.draw.polygon(self.carriere.controleur.screen, color, iso_for_validation, 3)
