class Walker:
    nb_walker = 0
    def __init__(self,actualPosition,destination):
        self.ID = Walker.nb_walker+1
        Walker.nb_walker=self.ID
        self.actualPosition = actualPosition #comment récupérer la position actuelle d'un walker?
        self.destination = destination #position généralement désignée par la construction d'une maison
        self.name = "citizen" #fichier sprite du walker
        self.chemin = None

