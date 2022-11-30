class Building:
    def __init__(self, name, can_be_erase, can_constructible_over, can_be_walk_through, square_size):
        self.name                   = name
        self.can_be_erase           = can_be_erase 
        self.can_constructible_over = can_constructible_over
        self.can_be_walk_through    = can_be_walk_through
        self.square_size            = square_size

    def get_canbewalkthrough_into_integer(self):
        return 1 if self.can_be_walk_through else 0