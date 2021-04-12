class Move:
    
    def __init__(self, piece, s_pos, t_pos, taken_piece):
        self.piece = piece
        self.start_pos = s_pos
        self.end_pos = t_pos
        self.taken_piece = taken_piece