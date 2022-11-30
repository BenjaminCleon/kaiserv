import pygame

from . import menu_settings
from .selectionneur_zone import SelectionneurZone

class Clear(SelectionneurZone):
    def __init__(self, surface, path):
        SelectionneurZone.__init__(self, surface)
        self.path = path
        self.can_thinking = False

    def events(self, event):
        SelectionneurZone.events(self, event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: self.can_thinking = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.can_thinking:
            for grid in self.grid_to_draw:
                if grid[0] >= 0 and grid[1] >= 0 and len(self.carriere.informations_tiles) > grid[0] and len(self.carriere.informations_tiles[grid[0]]) > grid[1]:
                    self.carriere.controleur.clear(grid)

            self.is_progress = False
            self.carriere.reload_board()

    def delete(self):
        pass