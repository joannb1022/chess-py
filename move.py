class Move:
    
    def __init__(self, piece, s_col, s_row, t_col, t_row):
        self.piece = piece
        self.start_pos = (s_row, s_col)
        self.end_pos = (t_row, t_col)