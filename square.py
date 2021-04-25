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
        if self.piece is None:
            return True
        return False
        #return self.piece

    def get_piece(self):
        return self.piece

    def get_image(self):
        if self.piece:
            return self.piece.get_image()
        return None
    
