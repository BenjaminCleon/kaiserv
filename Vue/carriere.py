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
        self.draw_walker()
        self.buttontestsave.draw()

    def draw_walker(self):
        walkers_infos = self.controleur.get_walker_infos()
        if walkers_infos != None:
            for walker in walkers_infos:
                if walker.destination != walker.actualPosition:
                    coef = walker.nombreDeplacement / walker.nb_deplacement_max
                    image = self.dictionnaire[walker.name]
                    image = pygame.transform.scale(image, (image.get_width()*self.zoom.multiplier, image.get_height()*self.zoom.multiplier))
                    positionActuelle = self.informations_tiles[walker.actualPosition[0]][walker.actualPosition[1]]["position_rendu"]
                    positionSuivante = self.informations_tiles[walker.nextPosition  [0]][walker.nextPosition  [1]]["position_rendu"]
                    positionFinale   = (positionActuelle[0]+(positionSuivante[0] - positionActuelle[0])*coef, positionActuelle[1]+(positionSuivante[1] - positionActuelle[1])*coef)
                    positionFinale = (
                        ((positionFinale[0]*self.zoom.multiplier + self.current_surface.get_width()/2 + self.camera.scroll.x)),
                        ((positionFinale[1]*self.zoom.multiplier - (image.get_height() - self.controleur.TILE_SIZE*self.zoom.multiplier )+ self.camera.scroll.y))
                    )

                    self.controleur.screen.blit(image, positionFinale)

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
            'herbe'                         : pygame.image.load("assets/upscale_land/Land1a_00115.png").convert_alpha(),
            'arbre'                         : pygame.image.load("assets/upscale_land/Land1a_00049.png").convert_alpha(),
            'eau'                           : pygame.image.load("assets/upscale_sea/Land1a_00120.png").convert_alpha(),
            'eau_haut'                      : pygame.image.load("assets/upscale_sea/Land1a_00136.png").convert_alpha(),
            'eau_bas'                       : pygame.image.load("assets/upscale_sea/Land1a_00128.png").convert_alpha(),
            'eau_droite'                    : pygame.image.load("assets/upscale_sea/Land1a_00140.png").convert_alpha(),
            'eau_gauche'                    : pygame.image.load("assets/upscale_sea/Land1a_00132.png").convert_alpha(),
            'eau_coin_haut_gauche'          : pygame.image.load("assets/upscale_sea/Land1a_00148.png").convert_alpha(),
            'eau_coin_haut_droite'          : pygame.image.load("assets/upscale_sea/Land1a_00152.png").convert_alpha(),
            'eau_coin_bas_droite'           : pygame.image.load("assets/upscale_sea/Land1a_00156.png").convert_alpha(),
            'eau_coin_bas_gauche'           : pygame.image.load("assets/upscale_sea/Land1a_00144.png").convert_alpha(),
            'eau_coin_bas_droite_interieur' : pygame.image.load("assets/upscale_sea/Land1a_00173.png").convert_alpha(),
            'eau_coin_bas_gauche_interieur' : pygame.image.load("assets/upscale_sea/Land1a_00170.png").convert_alpha(),
            'eau_coin_haut_gauche_interieur': pygame.image.load("assets/upscale_sea/Land1a_00171.png").convert_alpha(),
            'eau_coin_haut_droite_interieur': pygame.image.load('assets/upscale_sea/Land1a_00172.png').convert_alpha(),
            
            'eau_isole'                     : pygame.image.load('assets/upscale_sea/Land1a_00199.png' ).convert_alpha(),
            'eau_fin_gauche'                : pygame.image.load('assets/upscale_sea/Land1a_00164.png' ).convert_alpha(),
            'eau_fin_droite'                : pygame.image.load('assets/upscale_sea/Land1a_00166.png' ).convert_alpha(),
            'eau_fin_haut'                  : pygame.image.load('assets/upscale_sea/Land1a_00167.png' ).convert_alpha(),
            'eau_fin_bas'                   : pygame.image.load('assets/upscale_sea/Land1a_00165.png' ).convert_alpha(),
            'eau_isole_verticale'           : pygame.image.load('assets/upscale_sea/Land1a_00160.png'  ).convert_alpha(),
            'eau_isole_horizontale'         : pygame.image.load('assets/upscale_sea/Land1a_00162.png'  ).convert_alpha(),
            'panneau'                       : pygame.image.load("assets/upscale_house/Housng1a_00045.png").convert_alpha(),
            'citizen'                       : pygame.image.load("assets/upscale_citizen/Citizen05_00001.png").convert_alpha(),
            'tente'                         : pygame.image.load("assets/upscale_house/Housng1a_00002.png").convert_alpha(),
            'route droite'                  : pygame.image.load('assets/upscale_road/Land2a_00093.png').convert_alpha(),
            'route verticale'               : pygame.image.load('assets/upscale_road/Land2a_00094.png').convert_alpha(),
            'route droitebis'               : pygame.image.load('assets/upscale_road/Land2a_00095.png').convert_alpha(),
            'route horizontale'             : pygame.image.load('assets/upscale_road/Land2a_00096.png').convert_alpha(),
            'virage vers le bas'            : pygame.image.load('assets/upscale_road/Land2a_00097.png').convert_alpha(),
            'Virage gauche vers droite'     : pygame.image.load('assets/upscale_road/Land2a_00098.png').convert_alpha(),
            'Virage gauche vers le bas'     : pygame.image.load('assets/upscale_road/Land2a_00099.png').convert_alpha(),
            'Virage gauche vers droite vers le haut': pygame.image.load('assets/upscale_road/Land2a_00100.png').convert_alpha(),
            'Debut de route'   : pygame.image.load('assets/upscale_road/Land2a_00101.png').convert_alpha(),
            'Debut de routebis': pygame.image.load('assets/upscale_road/Land2a_00102.png').convert_alpha(),
            'Fin de route'     : pygame.image.load('assets/upscale_road/Land2a_00103.png').convert_alpha(),
            'Fin de routebis'  : pygame.image.load('assets/upscale_road/Land2a_00104.png').convert_alpha(),
            'Fin de routebis2' : pygame.image.load('assets/upscale_road/Land2a_00105.png').convert_alpha(),
            'Début intersection deux voix'   : pygame.image.load('assets/upscale_road/Land2a_00106.png').convert_alpha(),
            'Debut intersection deux voixbis': pygame.image.load('assets/upscale_road/Land2a_00107.png').convert_alpha(),
            'Intersection'   : pygame.image.load('assets/upscale_road/Land2a_00108.png').convert_alpha(),
            'Intersectionbis': pygame.image.load('assets/upscale_road/Land2a_00109.png').convert_alpha(),
            'Carrefour'      : pygame.image.load('assets/upscale_road/Land2a_00110.png').convert_alpha()
        }
        return dictionnaire

    def get_dictionnary_by_path(self):
        dictionnaire = {
            "assets/upscale_land/Land1a_00115.png": 'herbe'                         ,
            "assets/upscale_house/Housng1a_00045.png": "panneau"                    ,
            "assets/upscale_sea/Land1a_00049.png": 'arbre'                         ,
            "assets/upscale_sea/Land1a_00120.png": 'eau'                           ,
            "assets/upscale_sea/Land1a_00136.png": 'eau_haut'                      ,
            "assets/upscale_sea/Land1a_00128.png": 'eau_bas'                       ,
            "assets/upscale_sea/Land1a_00140.png": 'eau_droite'                    ,
            "assets/upscale_sea/Land1a_00132.png": 'eau_gauche'                    ,
            "assets/upscale_sea/Land1a_00150.png": 'eau_coin_haut_gauche'          ,
            "assets/upscale_sea/Land1a_00152.png": 'eau_coin_haut_droite'          ,
            "assets/upscale_sea/Land1a_00156.png": 'eau_coin_bas_droite'           ,
            "assets/upscale_sea/Land1a_00146.png": 'eau_coin_bas_gauche'           ,
            "assets/upscale_sea/Land1a_00173.png": 'eau_coin_bas_droite_interieur' ,
            "assets/upscale_sea/Land1a_00170.png": 'eau_coin_bas_gauche_interieur' ,
            "assets/upscale_sea/Land1a_00171.png": 'eau_coin_haut_gauche_interieur',
            'assets/upscale_sea/Land1a_00172.png': 'eau_coin_haut_droite_interieur',
            'assets/upscale_sea/Land1a_00164.png' : 'eau_fin_gauche',
            'assets/upscale_sea/Land1a_00160.png': 'eau_isole_verticale',
            'assets/upscale_sea/Land1a_00162.png': 'eau_isole_horizontale',
            'assets/upscale_sea/Land1a_00199.png': 'eau_isole',
            "assets/upscale_house/Housng1a_00002.png": 'tente',
            "assets/upscale_road/Land2a_00093.png" : 'route droite',
            "assets/upscale_road/Land2a_00094.png" : 'route verticale',
            "assets/upscale_road/Land2a_00095.png" : 'route droitebis',
            "assets/upscale_road/Land2a_00096.png" : 'route horizontale',
            "assets/upscale_road/Land2a_00097.png" : 'virage vers le bas',
            "assets/upscale_road/Land2a_00098.png" : 'Virage gauche vers droite',
            "assets/upscale_road/Land2a_00099.png" : 'Virage gauche vers le bas',
            "assets/upscale_road/Land2a_00100.png" : 'Virage gauche vers droite vers le haut',
            "assets/upscale_road/Land2a_00101.png" : 'Debut de route',
            "assets/upscale_road/Land2a_00102.png" : 'Debut de routebis',
            "assets/upscale_road/Land2a_00103.png" : 'Fin de route',
            "assets/upscale_road/Land2a_00104.png" : 'Fin de routebis',
            "assets/upscale_road/Land2a_00105.png" : 'Fin de routebis2',
            "assets/upscale_road/Land2a_00106.png" : 'Début intersection deux voix',
            "assets/upscale_road/Land2a_00107.png" : 'Debut intersection deux voixbis',
            "assets/upscale_road/Land2a_00108.png" : 'Intersection',
            "assets/upscale_road/Land2a_00109.png" : 'Intersectionbis',
            "assets/upscale_road/Land2a_00110.png" : 'Carrefour'
        }
        return dictionnaire

