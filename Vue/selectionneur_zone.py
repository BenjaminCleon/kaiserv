import pygame
from .basic_action import Basic_Action


class SelectionneurZone(Basic_Action):
    OPACITY = 180
    
    def __init__(self, carriere):
        Basic_Action.__init__(self, carriere)
        self.grid_postition_to_place = None
        self.grid_to_draw = []

    def initialiser(self, surface):
        Basic_Action.initialiser(self)
        self.original_surface = surface
        self.original_surface.set_alpha(SelectionneurZone.OPACITY)
        self.image_to_draw = self.original_surface

    def draw(self):
        size_of_original_image = self.original_surface.get_size()
        self.image_to_draw = pygame.transform.scale(self.original_surface, (size_of_original_image[0]*self.carriere.zoom.multiplier, size_of_original_image[1]*self.carriere.zoom.multiplier))
        self.grid_to_draw = []
        if self.pos_start is not None:
            for i in range(self.coordinate[0][0], self.coordinate[1][0]+1):
                for j in range(self.coordinate[0][1], self.coordinate[1][1]+1):
                    self.grid_postition_to_place = grid = (round(i), round(j))
                    self.grid_to_draw.append(grid)
        else:
            self.grid_position_without_first_click = self.mouse_to_grid(self.carriere.current_surface, self.carriere.camera.scroll, self.carriere.controleur.TILE_SIZE*self.carriere.zoom.multiplier, self.pos_without_first_click)

            self.grid_to_draw.append(self.grid_position_without_first_click)
        for grid in self.grid_to_draw:
            self.draw_for_an_image(grid)

    def draw_for_an_image(self, grid):
        if grid[0] >= 0 and grid[1] >= 0 and len(self.carriere.informations_tiles) > grid[0] and len(self.carriere.informations_tiles[grid[0]]) > grid[1]:
            position = self.carriere.informations_tiles[grid[0]][grid[1]]["position_rendu"]
            position = (
                ((position[0]*self.carriere.zoom.multiplier + self.carriere.current_surface.get_width()/2 + self.carriere.camera.scroll.x)),
                ((position[1]*self.carriere.zoom.multiplier - (self.image_to_draw.get_height() - self.carriere.controleur.TILE_SIZE*self.carriere.zoom.multiplier )+ self.carriere.camera.scroll.y))
            )

            self.carriere.controleur.screen.blit(self.image_to_draw, position)