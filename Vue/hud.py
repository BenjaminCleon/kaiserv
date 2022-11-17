import pygame as pg

from .bouton_hud import Button_HUD
from .adding_building import Adding_Building
from .clear import Clear

class HUD:
    def __init__(self, screen, carriere):
        self.screen   = screen
        self.carriere = carriere
        self.longueur = self.screen.get_width() 
        self.hauteur = self.screen.get_height()
        self.action = None

        #dimension image
        REFERENCE_SIZE_X = 1920
        REFERENCE_SIZE_Y = 1080

        # ecart entre chaque action de l'hud de droite 
        HORIZONTAL_GAP = self.longueur*0.026
        VERTICAL_GAP   = self.hauteur *0.034

        #chargement de l'image
        self.hud_right = pg.image.load("./assets/hud/hud_right.png").convert_alpha()
        size_hud_right = (self.hud_right.get_width()*self.longueur/REFERENCE_SIZE_X, self.hud_right.get_height()*self.hauteur/REFERENCE_SIZE_Y)
        self.hud_right = pg.transform.scale(self.hud_right, size_hud_right)

        self.hud_top = pg.image.load("./assets/hud/hud_top.png").convert_alpha()
        size_hud_top = (self.hud_top.get_width()*self.longueur/REFERENCE_SIZE_X, self.hud_top.get_height()*self.hauteur/REFERENCE_SIZE_Y)
        self.hud_top =  pg.transform.scale(self.hud_top, size_hud_top)

        actions = ["build", "clear", "test_clear" "road", "water", "", "", "", "", ""]
        self.button_hud_right = {}
        for i in range(3):
            for j in range(3):
                self.button_hud_right[actions[i*3+j]] = Button_HUD(self.screen,
                                                                   self.screen.get_width()*0.923+j*HORIZONTAL_GAP,
                                                                   self.screen.get_height()*0.279+i*VERTICAL_GAP ,
                                                                   actions[i*3+j])

    def events(self, event):
        pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        if self.action is not None:
            self.action.events(event)
            if self.action.is_progress == False: self.action = None
        
        for button in self.button_hud_right:
            if self.button_hud_right[button].rect.collidepoint(pos):
                # affichage
                self.button_hud_right[button].who_is_visible = "image_hover"
                if mouse_action[0]:
                    self.button_hud_right[button].who_is_visible = "image_click"
                    #interaction 
                    match button:
                        case "build":
                            if self.action == None: self.action = Adding_Building(self.carriere, "assets/upscale_land/Land1a_00049.png")
                            if not self.action.is_progress:
                                self.action.is_progress = True
                                image = pg.image.load("assets/upscale_land/Land1a_00049.png")
                                self.action.initialiser(image)
                        case "clear":
                            print("clear is working !")
                            if self.action == None: self.action = Clear(self.carriere, "assets/upscale_land/red_image.png")
                            if not self.action.is_progress:
                                self.action.is_progress = True
                                image = pg.image.load("assets/upscale_land/red_image.png")
                                self.action.initialiser(image)
                            print("dod s!t ")
                        case "road":
                            pass
                        case "water":
                            pass
            else:
                self.button_hud_right[button].who_is_visible = ""

    def draw(self):
        self.screen.blit(self.hud_right, (self.longueur*0.917, self.hauteur*0.0235))
        self.screen.blit(self.hud_top, (0, 0))
        
        if self.action != None: self.action.draw()

        for button in self.button_hud_right:
            self.button_hud_right[button].draw()

