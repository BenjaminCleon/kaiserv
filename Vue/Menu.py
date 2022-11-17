""" Menu screen"""
from Vue.menu_button import *
from Vue.menu_settings import *
import pygame as pg
import sys

class Menu():

    def __init__(self, screen, controleur):
        self.controleur = controleur
        self.displayed = True
        self.screen = screen
        self.font = pg.font.SysFont('Constantia', 75)
        self.font2 = pg.font.SysFont('Constantia', 50)
        self.current = "Main"
        self.background = pg.transform.scale(background_of_menu, screen.get_size())
        self.mid_width = (self.screen.get_width() // 2) - (WIDTH_BUTTON // 2)
        self.mid_height = (self.screen.get_height() // 2) - (1.5 * HEIGHT_BUTTON)
        self.start = False
        self.load = False
        self.save = False
        self.volume = 100
        self.pause = False
        #  next lines is for song
        pg.mixer.music.load(music_menu)
        #pg.mixer.music.play(-1)
        self.volume = pg.mixer.music.get_volume()

    def display_main(self):
        if self.displayed:

            # buttons
            self.Start_new_career = Button_Menu(self.screen, self.mid_width, self.mid_height - GAP, 'Start new career')
            self.Load_Saved_Game = Button_Menu(self.screen, self.mid_width, self.mid_height, 'Load Saved Game')
            self.Options         = Button_Menu(self.screen, self.mid_width, self.mid_height + GAP, 'Options')
            self.Creators        = Button_Menu(self.screen, self.mid_width, self.mid_height + (2 * GAP), 'Creators')
            self.Exit            = Button_Menu(self.screen, self.mid_width, self.mid_height + (3 * GAP), 'Exit')
            
    def events(self):
        if self.Start_new_career.check_button():
            self.controleur.play()

        if self.Load_Saved_Game.check_button():
            print("loaaaaddddddddddd")
            """self.load = True
            run = False"""

        if self.Exit.check_button():
            run = False
            sys.exit()

        if self.Options.check_button():
            self.current = "Options"
            self.display_settings()
            run = False

        if self.Creators.check_button():
            self.current = "Creators"
            self.display_creators()
            run = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                sys.exit()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.font.render(" KaiserV ", True, RED,(249, 231, 159)),
                         (self.mid_width + 5, self.mid_height - (2.5 * GAP)))

        self.Start_new_career.draw()
        self.Load_Saved_Game.draw()
        self.Creators.draw()
        self.Options.draw()
        self.Exit.draw()
        pg.display.flip()

    def display_settings(self):
        if self.displayed:

            pg.display.set_caption(' KaiserV ')

            # buttons
            Exit        = Button_Menu(self.screen, self.mid_width, self.mid_height + (5*GAP), 'Exit')
            Volume_up   = Button_Menu(self.screen, self.mid_width + (3.5 * GAP), self.mid_height + GAP, '+ Volume Up')
            Volume_down = Button_Menu(self.screen, self.mid_width - (3*GAP), self.mid_height + GAP, '- Volume Down')
            Return      = Button_Menu(self.screen, self.mid_width, self.mid_height - GAP * 2, 'Return')

            run = True
            while run:
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.font.render("Settings", True, RED,(249, 231, 159)), (self.mid_width +30, self.mid_height - GAP*3.25))

                Exit.draw()
                Volume_up.draw()
                Volume_down.draw()
                Return.draw()

                if Volume_down.check_button():
                    if self.volume > 0.0:
                        self.volume -= 0.1
                        pg.mixer.music.set_volume(self.volume)

                if Volume_up.check_button():
                    if self.volume < 1.0:
                        self.volume += 0.1
                        pg.mixer.music.set_volume(self.volume)

                if Return.check_button():
                    run = False
                    self.current = "Main"
                    self.display_main()

                if Exit.check_button():
                    run = False
                    sys.exit()

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        run = False
                        pg.quit()

                pg.display.flip()

    def display_creators(self):
        if self.displayed:

            #pg.display.set_caption(' keaserV ')
            Return = Button_Menu(self.screen, self.mid_width, self.mid_height - GAP * 2, 'Return')

            run = True
            while run:
                self.screen.fill((255, 255, 255))
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.font.render("Awa", True, GREEN_DARK ,(255, 255, 255)),
                                 (self.mid_width*0.95, self.mid_height - 40))
                self.screen.blit(self.font.render("Benjamin", True, GREEN_DARK,(255, 255, 255)),
                                 (self.mid_width * 0.95, self.mid_height + 35))
                self.screen.blit(self.font.render("Steven", True, GREEN_DARK,(255, 255, 255)),
                                 (self.mid_width * 0.95, self.mid_height + (GAP+35)))
                self.screen.blit(self.font.render("Yasmine", True, GREEN_DARK,(255, 255, 255)),
                                 (self.mid_width * 0.95, self.mid_height + GAP * 2 +35))
                self.screen.blit(self.font.render("Youssef", True, GREEN_DARK,(255, 255, 255)),
                                 (self.mid_width * 0.95, self.mid_height + GAP * 3 + 35))
                Return.draw()

                if Return.check_button():
                    run = False
                    self.current = "Main"
                    self.display_main()

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        run = False
                        sys.exit()

                pg.display.update()