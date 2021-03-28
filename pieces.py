import itertools

class Piece:
    def __init__(self, color):
        self.color = color
        #self.position = (None, None) 



class Pawn(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.can_move_two = True
        

    def can_reach(self, s_col, s_row, t_col, t_row):
        if(abs(t_row - s_row) == 2 and self.can_move_two):
            return True

        if self.color == 'b' and t_row - s_row == 1:
            return True

        if self.color == 'w' and t_row - s_row == -1:
            return True

        return False

    def get_available_squares(self, row, col):
        """"""

    def draw(self):
        return 'p'

class King(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)

    def can_reach(self, s_col, s_row, t_col, t_row):
        return (abs(s_col - t_col) == 1 and abs(s_row - t_row) == 1)\
             or (abs(s_col - t_col) == 1 and abs(s_row - t_row) == 0)\
             or (abs(s_col - t_col) == 0 and abs(s_row - t_row) == 1)

    def get_available_squares(self, col, row):
        res = []
        
        if col - 1 > -1:
            if row - 1 > -1:
                res.append((col-1, row-1))
            if row + 1 < 8:
                res.append((col-1, row+1))
        
            res.append((col-1, row))

        if col+1 < 8:
            if row - 1 > -1:
                res.append((col+1, row-1))
            if row + 1 < 8:
                res.append((col+1, row+1))

            res.append((col+1, row))

        if row - 1 > -1:
            res.append((col, row-1))
        if row + 1 < 8:
            res.append((col, row+1))

        return res

    def draw(self):
        return 'k'

class Queen(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)

    def can_reach(self, s_col, s_row, t_col, t_row):
        return Rook.can_reach(self, s_col, s_row, t_col, t_row) or Bishop.can_reach(self, s_col, s_row, t_col, t_row)

    def get_available_squares(self, col, row):
        return Rook.get_available_squares(self, col, row) + Bishop.get_available_squares(self, col, row)

    def draw(self):
        return 'q'


class Rook(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)

    def can_reach(self, s_col, s_row, t_col, t_row):
        return s_col == t_col or s_row == t_row

    def get_available_squares(self, col, row):
        res = []

        for i in range(8):
            if i != col:
                res.append((i, row))
            if i != row:
                res.append((col, i))

        return res

    def draw(self):
        return 'r'

class Bishop(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)

    def can_reach(self, s_col, s_row, t_col, t_row):
        return abs(s_col - t_col) == abs(s_row - t_row)

    def get_available_squares(self, col, row):
        res = []

        for i in range(1, 8):
            if col - i > -1 and row - i > -1:
                res.append((col-i, row-i))
            if col + i < 8 and row - i > -1:
                res.append((col+i, row-i))
            if col - i > -1 and row + i < 8:
                res.append((col-i, row+i))
            if col + i < 8 and row + i < 8:
                res.append((col+i, row+i))

        return res

    def draw(self):
        return 'b'

class Knight(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)

    def can_reach(self, s_col, s_row, t_col, t_row):
        return (abs(s_col - t_col) == 2 and abs(s_row - t_row) == 1) or (abs(s_col - t_col) == 1 and abs(s_row - t_row) == 2)


    def get_available_squares(self, col, row):
        res = []

        if col - 1 > -1:

            if row - 2 > -1:
                res.append((col-1, row-2))
            if row + 2 < 8:
                res.append((col-1, row+2))

            if col - 2 > -1:
                if row - 1 > -1:
                    res.append((col-2, row-1))
                if row + 1 < 8:
                    res.append((col-2, row+1))

        if col + 1 < 8:

            if row - 2 > -1:
                res.append((col+1, row-2))
            if row + 2 < 8:
                res.append((col+1, row+2))

            if col + 2 < 8:
                if row - 1 > -1:
                    res.append((col+2, row-1))
                if row + 1 < 8:
                    res.append((col+2, row+1))

        return res

    def draw(self):
        return 's'

if __name__ == '__main__':
    q = Queen('b')
    kn = Knight('b')
    k = King('b')
    print(q.can_reach(0,0,6,1))
    #print(q.get_available_squares(0, 0))
    #print(kn.get_available_squares(0,7))
    print(k.get_available_squares(7,7))