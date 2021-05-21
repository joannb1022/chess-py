from pieces import Knight

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
        if self.castle:
            return 'O-O'

        takes = 'x' if self.taken_piece is not None else ''
        piece_symbol = 'N' if isinstance(self.piece, Knight) else self.piece.__class__.__name__[0]
        return f'{piece_symbol}{chr(self.start_pos[1]+97)}{8-self.start_pos[0]}{takes}{chr(self.end_pos[1]+97)}{8-self.end_pos[0]}'