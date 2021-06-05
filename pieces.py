import itertools

class Piece:
    def __init__(self, color):
        self.color = color
        self.can_castle = True

    def get_image(self):
        """ścieżka do pliku png figury"""
        return r'pieces/{}{}.png'.format(self.color, self.__class__.__name__[0])


class Pawn(Piece):
    """Pion"""
    def __init__(self, color):
        Piece.__init__(self, color)
        self.can_move_two = True
        self.en_passant_increasing = False
        self.en_passant_decreasing = False

    def can_reach(self, s_col, s_row, t_col, t_row):
        if(abs(t_row - s_row) == 2 and self.can_move_two):
            return True

        if self.color == 'b' and t_row - s_row == 1:
            return True

        if self.color == 'w' and t_row - s_row == -1:
            return True

        return False

    def get_directions(self):
        res = []
        if self.color == 'b':
            res.append((1,0))
            if self.can_move_two:
                res.append((2,0))
        else:
            res.append((-1,0))
            if self.can_move_two:
                res.append((-2,0))
        return res

    def get_en_passant(self):
        res = []
        if self.color == 'b':
            multip = 1
        else:
            multip = -1

        if self.en_passant_decreasing:
            res.append((1*multip,-1))
        if self.en_passant_increasing:
            res.append((1*multip, 1))

        return res


class King(Piece):
    """Król"""
    def __init__(self, color):
        Piece.__init__(self, color)
        self.can_castle = True

    def can_reach(self, s_col, s_row, t_col, t_row):
        return (abs(s_col - t_col) == 1 and abs(s_row - t_row) == 1)\
             or (abs(s_col - t_col) == 1 and abs(s_row - t_row) == 0)\
             or (abs(s_col - t_col) == 0 and abs(s_row - t_row) == 1)

    def get_directions(self):
        return [(1,0), (1,1), (0, 1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]


class Queen(Piece):
    """Królowa"""
    def __init__(self, color):
        Piece.__init__(self, color)

    def can_reach(self, s_col, s_row, t_col, t_row):
        return Rook.can_reach(self, s_col, s_row, t_col, t_row) or Bishop.can_reach(self, s_col, s_row, t_col, t_row)

    def get_directions(self):
        return King.get_directions(self)


class Rook(Piece):
    """Wieża"""
    def __init__(self, color):
        Piece.__init__(self, color)
        self.can_castle = True

    def can_reach(self, s_col, s_row, t_col, t_row):
        return s_col == t_col or s_row == t_row

    def get_directions(self):
        return [(1,0), (0,1), (-1, 0), (0, -1)] #UP, RIGHT, DOWN, LEFT


class Bishop(Piece):
    """Goniec"""
    def __init__(self, color):
        Piece.__init__(self, color)

    def can_reach(self, s_col, s_row, t_col, t_row):
        return abs(s_col - t_col) == abs(s_row - t_row)

    def get_directions(self):
        return [(1,1), (-1,1), (-1, -1), (1, -1)] #UR, LR, LL, UL


class Knight(Piece):
    """Skoczek"""
    def __init__(self, color):
        Piece.__init__(self, color)

    def can_reach(self, s_col, s_row, t_col, t_row):
        return (abs(s_col - t_col) == 2 and abs(s_row - t_row) == 1) or (abs(s_col - t_col) == 1 and abs(s_row - t_row) == 2)

    @staticmethod
    def get_directions():
        return [(2,1), (1,2), (-1,2), (-2,1), (-2,-1), (-1,-2), (1,-2), (2, -1)]

    def get_image(self):
        return r'pieces/{}{}.png'.format(self.color, 'N')