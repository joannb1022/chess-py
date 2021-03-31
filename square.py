class Square:
    def __init__(self):
        self.piece = None

    def place_piece(self, piece):
        self.piece = piece

    def remove_piece(self):
        temp = self.piece
        self.piece = None
        return temp

    def is_empty(self):
        return self.piece
