import pygame

from Model import pathfinding
from .basic_action import Basic_Action

class Adding_Road(Basic_Action):

    def __init__(self, surface, chemin):
        Basic_Action.init(self, surface)
        self.can_thinking = False
        self.chemins = None


    def getChemin(self, start, end):

        if (self.carriere.controleur.check_if_construction_possible_on_grid(start)) and (self.carriere.controleur.check_if_construction_possible_on_grid(end)) :
            is_drawing_possible_on_this_grid = True
            self.chemins = self.carriere.controleur.find_path(self, start, end)

    def draw(self, chemins):
        for grid in chemins:
            pass

    def events(self, event):
        Basic_Action.events(self, event)
        chemin = self.getChemin(Basic_Action.grid_position_start, Basic_Action.grid_position_end)
        if chemin !=None:
            self.draw(self.chemin)