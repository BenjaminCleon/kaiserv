import pygame

class SelectionneurZone:
    OPACITY = 180

    def __init__(self, carriere):
        self.is_progress = False
        self.carriere = carriere
        self.grid_postition_to_place = None
        self.grid_to_draw = []

    def initialiser(self, surface):
        self.is_possible = True
        self.is_progress = True
        self.original_surface = surface
        self.original_surface.set_alpha(SelectionneurZone.OPACITY)
        self.image_to_draw = self.original_surface
        self.pos_without_first_click = (0,0)
        self.pos_start = None
        self.pos_end   = None

    def events(self, event):
        if self.is_progress:
            self.pos_without_first_click = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.pos_start = self.pos_without_first_click
            if self.pos_start != None :self.pos_end = self.pos_without_first_click
    
    def draw(self):
        size_of_original_image = self.original_surface.get_size()
        self.image_to_draw = pygame.transform.scale(self.original_surface, (size_of_original_image[0]*self.carriere.zoom.multiplier, size_of_original_image[1]*self.carriere.zoom.multiplier))
        self.grid_to_draw = []
        if self.pos_start is not None:
            pos_start = ((self.pos_start[0]+self.carriere.camera.scroll.x)*self.carriere.zoom.level_zoom/40, (self.pos_start[1]+self.carriere.camera.scroll.y)*self.carriere.zoom.level_zoom/40 )
            grid_position_start = self.mouse_to_grid(self.carriere.current_surface, self.carriere.camera.scroll, self.carriere.controleur.TILE_SIZE*self.carriere.zoom.multiplier, pos_start)
            grid_position_end   = self.mouse_to_grid(self.carriere.current_surface, self.carriere.camera.scroll, self.carriere.controleur.TILE_SIZE*self.carriere.zoom.multiplier, self.pos_end  )
            coordinate = self.get_square_coords_from_top_right(grid_position_start, grid_position_end)
            for i in range(coordinate[0][0], coordinate[1][0]+1):
                for j in range(coordinate[0][1], coordinate[1][1]+1):
                    self.grid_postition_to_place = grid = (round(i), round(j))
                    self.grid_to_draw.append(grid)
        else:
            grid_position = self.mouse_to_grid(self.carriere.current_surface, self.carriere.camera.scroll, self.carriere.controleur.TILE_SIZE*self.carriere.zoom.multiplier, self.pos_without_first_click)

            self.grid_postition_to_place = grid = (round(grid_position[0]), round(grid_position[1]))
            self.grid_to_draw.append(grid)

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
            
    def get_square_coords_from_top_right(self, grid_start, grid_end):
        positions = [grid_start, grid_end]
        minim = (min([x for x, y in positions]), min([y for x, y in positions]))
        maxim = (max([x for x, y in positions]), max([y for x, y in positions]))

        return minim, maxim

    def mouse_to_grid(self, surface, scroll, TILE_SIZE, pos):
        world_x = pos[0] - scroll.x - surface.get_width()/2
        world_y = pos[1] - scroll.y
        contrary_iso_y = (2*world_y-world_x)/2 
        contrary_iso_x = contrary_iso_y + world_x

        grid_x = int(contrary_iso_x//TILE_SIZE)
        grid_y = int(contrary_iso_y//TILE_SIZE)

        return grid_x, grid_y