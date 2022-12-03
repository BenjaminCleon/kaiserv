class Walker:
    nb_walker = 0
    def __init__(self,ID,actualPosition,nextPosition,sprite):
        self.ID = Walker.nb_walker+1
        Walker.nb_walker=self.ID
        self.actualPosition = None #comment récupérer la position actuelle d'un walker?
        self.nextPosition = None #position généralement désignée par la construction d'une maison
        self.sprite = "assets/upscale_citizen/Citizen05_00001.png" #fichier sprite du walker

