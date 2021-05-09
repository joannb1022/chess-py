class Move:
    
    def __init__(self, piece, s_pos, t_pos, taken_piece, en_passant = False, castle = None, promotion = False):
        self.piece = piece
        self.start_pos = s_pos
        self.end_pos = t_pos
        self.taken_piece = taken_piece
        self.en_passant = en_passant
        self.castle = castle
        self.promotion = promotion