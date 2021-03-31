import pieces
import move
from square import Square



class Board:
    def __init__(self):
        self.board = [[Square() for j in range(8)] for i in range(8)]
        self.black_king = (0,4)
        self.white_king = (7,4)
        self.move_history = []

    def place_pieces(self):
        self.board[0][0].place_piece(pieces.Rook('b'))
        self.board[0][7].place_piece(pieces.Rook('b'))
        self.board[7][0].place_piece(pieces.Rook('w'))
        self.board[7][7].place_piece(pieces.Rook('w'))

        self.board[0][1].place_piece(pieces.Knight('b'))
        self.board[0][6].place_piece(pieces.Knight('b'))
        self.board[7][1].place_piece(pieces.Knight('w'))
        self.board[7][6].place_piece(pieces.Knight('w'))

        self.board[0][2].place_piece(pieces.Bishop('b'))
        self.board[0][5].place_piece(pieces.Bishop('b'))
        self.board[7][2].place_piece(pieces.Bishop('w'))
        self.board[7][5].place_piece(pieces.Bishop('w'))

        self.board[0][3].place_piece(pieces.Queen('b'))
        self.board[7][3].place_piece(pieces.Queen('w'))

        self.board[0][4].place_piece(pieces.King('b'))
        self.board[7][4].place_piece(pieces.King('w'))

        for i in range(8):
            self.board[1][i].place_piece(pieces.Pawn('b'))
            self.board[6][i].place_piece(pieces.Pawn('w'))


    def move_piece(self, s_col, s_row, t_col, t_row):

        s_square = self.board[s_row][s_col]

        if isinstance(s_square.piece, pieces.King):
            if s_square.piece.color == 'b':
                self.black_king = (t_row, t_col)
            else:
                self.white_king = (t_row, t_col)

        piece = s_square.remove_piece()
        self.board[t_row][t_col].place_piece(piece)

    def print_board(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j].piece is None:
                    print("o", " ", end = "")
                else:
                    print(self.board[i][j].piece.draw(), " ", end = "")
            print('\n')


    def get_legal_moves(self, col, row):
        piece = self.board[row][col].piece

        res = []
        directions = piece.get_directions()

        if isinstance(piece, pieces.Pawn):
            


        elif isinstance(piece, pieces.King):
            for el in directions:
                curr_square = self.board[row+el[0]][col+el[1]]
                if row+el[0] > -1 and row+el[0] < 8 and col+el[1] > -1 and col+el[1] < 8 \
                      and (curr_square.is_empty() or curr_square.piece.color != piece.color) and not self.discovers_check(el, col, row):
                      res.append((el[0]+row, el[1]+col))

        elif isinstance(piece, pieces.Knight):
            for el in directions:
                curr_square = self.board[row+el[0]][col+el[1]]
                if row+el[0] > -1 and row+el[0] < 8 and col+el[1] > -1 and col+el[1] < 8 \
                    and (curr_square.is_empty() or curr_square.piece.color != piece.color) and not self.discovers_check(el, col, row):
                    res.append((row+el[0], col+el[1]))
        else:
            for el in directions:
                if not self.discovers_check(el, col, row):
                    
                    i = row+el[0]
                    j = col+el[1]
                    
                    while i > -1 and i < 8 and j > -1 and j < 8 and self.board[i][j].is_empty():
                        res.append((i,j))
                        i += el[0]
                        j += el[1]
                    
                    if i > -1 and i < 8 and j > -1 and j < 8 and self.board[i][j].piece.color != piece.color:
                        res.append((i,j))

        return res


    def is_in_check(self, color):
        if color == 'b':
            pos = self.black_king
        else:
            pos = self.white_king

        for i in range(pos[0]+1, 8):
            if self.board[i][pos[1]].piece.color == color:
                break
            elif isinstance(self.board[i][pos[1]].piece, pieces.Queen) or isinstance(self.board[i][pos[1]].piece, pieces.Rook):
                return True
            
        for i in range(pos[0]-1, -1, -1):
            if self.board[i][pos[1]].piece.color == color:
                break
            elif isinstance(self.board[i][pos[1]].piece, pieces.Queen) or isinstance(self.board[i][pos[1]].piece, pieces.Rook):
                return True
            
        for i in range(pos[1]+1, 8):
            if self.board[pos[0]][i].piece.color == color:
                break
            elif isinstance(self.board[pos[0]][i].piece, pieces.Queen) or isinstance(self.board[pos[0]][i].piece, pieces.Rook):
                return True

        for i in range(pos[1]-1, -1, -1):
            if self.board[pos[0]][i].piece.color == color:
                break
            elif isinstance(self.board[pos[0]][i].piece, pieces.Queen) or isinstance(self.board[pos[0]][i].piece, pieces.Rook):
                return True
                    
            
            #DIAGONAL

        j = 1
        while pos[0]-j > -1 and pos[1]+j < 8:
            if self.board[pos[0]-j][pos[1]+j].piece.color == color:
                break
            elif j == 1 and color == 'w' and isinstance(self.board[pos[0]-1][pos[1]+1].piece, pieces.Pawn):
                return True
            elif isinstance(self.board[pos[0]-j][pos[1]+j].piece, pieces.Bishop) or isinstance(self.board[pos[0]-j][pos[1]+j].piece, pieces.Queen):
                return True
        j = 1
        while pos[0]+j < 8 and pos[1]+j < 8:
            if self.board[pos[0]+j][pos[1]+j].piece.color == color:
                break
            elif j == 1 and color == 'b' and isinstance(self.board[pos[0]+1][pos[1]+1].piece, pieces.Pawn):
                return True
            elif isinstance(self.board[pos[0]-j][pos[1]+j].piece, pieces.Bishop) or isinstance(self.board[pos[0]-j][pos[1]+j].piece, pieces.Queen):
                return True
        j = 1
        while pos[0]+j < 8 and pos[1]-j > -1:
            if self.board[pos[0]+j][pos[1]-j].piece.color == color:
                break
            elif j == 1 and color == 'b' and isinstance(self.board[pos[0]+1][pos[1]-1].piece, pieces.Pawn):
                return True
            elif isinstance(self.board[pos[0]-j][pos[1]-j].piece, pieces.Bishop) or isinstance(self.board[pos[0]-j][pos[1]-j].piece, pieces.Queen):
                return True
            
        j = 1
        while pos[0]-j > -1 and pos[1]-j > -1:
            if self.board[pos[0]-j][pos[1]-j].piece.color == color:
                break
            elif j == 1 and color == 'w' and isinstance(self.board[pos[0]-1][pos[1]-1].piece, pieces.Pawn):
                return True
            elif isinstance(self.board[pos[0]-j][pos[1]-j].piece, pieces.Bishop) or isinstance(self.board[pos[0]-j][pos[1]-j].piece, pieces.Queen):
                return True


        possible_knights = pieces.Knight.get_directions()

        for el in possible_knights:
            if pos[0] + el[0] > -1 and pos[0] + el[0] < 8 and pos[1] + el[1] > -1 and pos[1] + el[1] < 8 \
                and isinstance(self.board[el[0]][el[1]].piece, pieces.Knight) and self.board[el[0]][el[1]].piece.color != color:
                return True

        return False
        


    def discovers_check(self, dir, col, row):
        
        color = self.board[row][col].piece.color

        self.move_piece(col, row, col+dir[1], row+dir[0])
        is_check = self.is_in_check(color)
        self.move_piece(col, row, col+dir[1], row+dir[0])

        return is_check


if __name__ == '__main__':
    b = Board()
    b.place_pieces()
    b.print_board()
    b.move_piece(0,0, 4, 5)
    b.print_board()