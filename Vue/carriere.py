import pygame
import pickle

from .menu_button import Button_Menu
from .camera import Camera
from .zoom import Zoom
from .utils import draw_text

class Carriere:
    def __init__(self, controleur):
        self.controleur = controleur
        self.width, self.height = self.controleur.screen.get_size()

        # camera pour se déplacer dans le monde
        self.camera = Camera(self.width, self.height)
        # path selon tile
        self.dictionnaire = self.get_tile()
        self.dictionnaire_reverse_by_path = self.get_dictionnary_by_path()
        # surface sur lesquels notre map de base s'affiche
        self.basic_surface = None
        self.current_surface = None
        self.basic_surface_size = None
        # informations sur les tuiles
        self.informations_tiles = None
        # zoom sur la carte
        self.zoom = Zoom()
        self.zoom.update(0)

        self.buttontestsave = Button_Menu(self.controleur.screen, 0, 0, "Enregistrer")

    def draw_main_components(self):
        self.controleur.screen.fill((0, 0, 0))
        if self.zoom.should_scale:
            self.current_surface = pygame.transform.scale(self.basic_surface,(self.basic_surface_size[0]*self.zoom.multiplier, self.basic_surface_size[1]*self.zoom.multiplier) )
            self.zoom.should_scale = False
        
        self.controleur.screen.blit(self.current_surface, (self.camera.scroll.x, self.camera.scroll.y))
        self.buttontestsave.draw()

    def events(self, event):
        if event.type == pygame.MOUSEWHEEL:
                self.zoom.update(event.y)
        if self.buttontestsave.check_button():
            self.Save_game()

    def Save_game(self):
        object = self.controleur.metier
        filename = "test.sav"
        filehandler = open(filename, 'wb') 
        pickle.dump(object, filehandler)

    def reload_board(self):
        self.informations_tiles = self.controleur.get_board()
        self.basic_surface_size = (self.controleur.TILE_SIZE*self.controleur.grid_width*2,
                                   self.controleur.TILE_SIZE*self.controleur.grid_height*2+self.controleur.TILE_SIZE)
        self.basic_surface = pygame.Surface(self.basic_surface_size)
        self.current_surface = self.basic_surface
        self.informations_tiles = self.controleur.get_board()
        for num_lig in range(len(self.informations_tiles)):
            for num_col in range(len(self.informations_tiles[num_lig])):
                name = self.informations_tiles[num_lig][num_col]["building"].name
                image = self.dictionnaire[name] if name != None else None
                position = self.informations_tiles[num_lig][num_col]["position_rendu"]
                self.basic_surface.blit(image, (position[0] + self.basic_surface.get_width()/2,
                                                position[1] -(image.get_height() - self.controleur.TILE_SIZE)))
        
        self.current_surface = pygame.transform.scale(self.basic_surface,(self.basic_surface_size[0]*self.zoom.multiplier, self.basic_surface_size[1]*self.zoom.multiplier) )

    def update(self):
        self.camera.update()

    # initialise chaque sprite à afficher 
    def init_sprite(self):
        self.reload_board()

    
    # permet de récupérer le chemin d'une image
    def get_tile(self):
        dictionnaire = {
            'herbe'               : pygame.image.load("assets/upscale_land/Land1a_00115.png").convert_alpha(),
            'arbre'               : pygame.image.load("assets/upscale_land/Land1a_00049.png").convert_alpha(),
            'eau'                 : pygame.image.load("assets/upscale_land/Land1a_00120.png").convert_alpha(),
            'eau_haut'            : pygame.image.load("assets/upscale_land/Land1a_00136.png").convert_alpha(),
            'eau_bas'             : pygame.image.load("assets/upscale_land/Land1a_00128.png").convert_alpha(),
            'eau_droite'          : pygame.image.load("assets/upscale_land/Land1a_00140.png").convert_alpha(),
            'eau_gauche'          : pygame.image.load("assets/upscale_land/Land1a_00132.png").convert_alpha(),
            'eau_coin_haut_gauche': pygame.image.load("assets/upscale_land/Land1a_00150.png").convert_alpha(),
            'eau_coin_haut_droite': pygame.image.load("assets/upscale_land/Land1a_00152.png").convert_alpha(),
            'eau_coin_bas_droite' : pygame.image.load("assets/upscale_land/Land1a_00156.png").convert_alpha(),
            'eau_coin_bas_gauche' : pygame.image.load("assets/upscale_land/Land1a_00146.png").convert_alpha(),
            'eau_coin_bas_droite_interieur' : pygame.image.load("assets/upscale_land/Land1a_00173.png").convert_alpha(),
            'eau_coin_bas_gauche_interieur' : pygame.image.load("assets/upscale_land/Land1a_00170.png").convert_alpha(),
            'eau_coin_haut_gauche_interieur': pygame.image.load("assets/upscale_land/Land1a_00171.png").convert_alpha(),
            'eau_coin_haut_droite_interieur': pygame.image.load('assets/upscale_land/Land1a_00172.png').convert_alpha(),
            'panneau'                       : pygame.image.load("assets/upscale_house/Housng1a_00045.png").convert_alpha()
        }
        return dictionnaire

    def get_dictionnary_by_path(self):
        dictionnaire = {
            "assets/upscale_land/Land1a_00115.png": 'herbe'                         ,
            "assets/upscale_house/Housng1a_00045.png": "panneau"                    ,
            "assets/upscale_land/Land1a_00049.png": 'arbre'                         ,
            "assets/upscale_land/Land1a_00120.png": 'eau'                           ,
            "assets/upscale_land/Land1a_00136.png": 'eau_haut'                      ,
            "assets/upscale_land/Land1a_00128.png": 'eau_bas'                       ,
            "assets/upscale_land/Land1a_00140.png": 'eau_droite'                    ,
            "assets/upscale_land/Land1a_00132.png": 'eau_gauche'                    ,
            "assets/upscale_land/Land1a_00150.png": 'eau_coin_haut_gauche'          ,
            "assets/upscale_land/Land1a_00152.png": 'eau_coin_haut_droite'          ,
            "assets/upscale_land/Land1a_00156.png": 'eau_coin_bas_droite'           ,
            "assets/upscale_land/Land1a_00146.png": 'eau_coin_bas_gauche'           ,
            "assets/upscale_land/Land1a_00173.png": 'eau_coin_bas_droite_interieur' ,
            "assets/upscale_land/Land1a_00170.png": 'eau_coin_bas_gauche_interieur' ,
            "assets/upscale_land/Land1a_00171.png": 'eau_coin_haut_gauche_interieur',
            'assets/upscale_land/Land1a_00172.png': 'eau_coin_haut_droite_interieur'
        }
        return dictionnaire

