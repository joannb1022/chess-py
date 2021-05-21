class Move:
    
    def __init__(self, piece, s_pos, t_pos, taken_piece = None, en_passant = False, castle = None, promotion = False):
        self.piece = piece
        self.start_pos = s_pos
        self.end_pos = t_pos
        self.taken_piece = taken_piece
        self.en_passant = en_passant
        self.castle = castle
        self.promotion = promotion

    def to_string(self):
        takes = 'x' if self.taken_piece is not None else ''
        return f'{self.piece.__class__.__name__[0]}{self.start_pos[1]+1}{chr(self.start_pos[0]+95)}{takes}{self.end_pos[1]+1}{chr(self.end_pos[0]+95)}'