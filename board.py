import pieces
from square import Square


class Board:
    def __init__(self):
        self.board = [[Square() for j in range(8)] for i in range(8)]


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
        piece = self.board[s_row][s_col].remove_piece()
        self.board[t_row][t_col].place_piece(piece)

    def print_board(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j].piece is None:
                    print("o", " ", end = "")
                else:
                    print(self.board[i][j].piece.draw(), " ", end = "")
            print('\n')


if __name__ == '__main__':
    b = Board()
    b.place_pieces()
    b.print_board()
    b.move_piece(0,0, 4, 5)
    b.print_board()