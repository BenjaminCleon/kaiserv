class Basic_Action:
    def __init__(self, carriere):
        self.is_progress = False
        self.carriere = carriere

    def initialiser(self):
        self.is_possible = True
        self.is_progress = True