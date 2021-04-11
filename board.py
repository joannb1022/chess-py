import pieces
import move
from square import Square
from enum import Enum

class Checked_by(Enum):
    NONE = 0
    ONE = 1
    KNIGHT = 2
    TWO = 3



class Board:
    def __init__(self):
        self.board = [[Square() for j in range(8)] for i in range(8)]
        self.black_king = (0,4)
        self.white_king = (7,4)
        self.move_history = []
        self.en_passant = []
        # self.black_king_in_check = Checked_by.NONE
        # self.white_king_in_check = Checked_by.NONE
        self.king_in_check = {'w': Checked_by.NONE, 'b': Checked_by.NONE}
        self.attackers = []

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


        curr_move = move.Move(piece, s_col, s_row, t_col, t_row, self.board[t_row][t_col].piece)

        self.board[t_row][t_col].place_piece(piece)

        self.move_history.append(curr_move)


    def get_squares_in_between(self, pos1, pos2):
        res = []

        if pos1[0] == pos2[0]:
            i, j = min(pos1[1], pos2[1])+1, max(pos1[1], pos2[1])
            while i != j:
                res.append((pos1[0], i))
                i+=1

        elif pos1[1] == pos2[1]:
            i, j = min(pos1[0], pos2[0])+1, max(pos1[0], pos2[0])
            while i != j:
                res.append((i, pos1[1]))
                i+=1

        elif abs(pos1[0] - pos2[0]) == abs(pos1[1] - pos2[1]):
            if pos1[0] > pos2[0]:
                pos1, pos2 = pos2, pos1

            if pos1[1] < pos2[1]:
                curr = (pos1[0]+1, pos1[1]+1)

                while curr[1] < pos2[1]:
                    res.append(curr)
                    curr = (curr[0]+1, curr[1]+1)
            else:
                curr = (pos1[0]+1, pos1[1]-1)
                while curr[1] > pos2[1]:
                    res.append(curr)
                    curr = (curr[0]+1, curr[1]-1)
        return res


    def print_board(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j].piece is None:
                    print("oo", ' ', end = "")
                else:
                    print(self.board[i][j].piece.draw(), " ", end = "")
            print('\n')


    def get_legal_moves(self, col, row):
        piece = self.board[row][col].piece

        res = []

        if isinstance(piece, pieces.Pawn):
            if piece.color == 'b':
                multip = 1
            else:
                multip = -1

            if self.board[multip+row][col].is_empty() and not self.discovers_check((multip, 0), col, row):
                res.append((row+multip,col))
                if multip%7 == 6 or multip%7 == 1 and self.board[2*multip+row][col].is_empty() and not self.discovers_check((multip*2, 0), col, row):
                    res.append((row+multip*2, col))


            if col-1 > -1:
                curr_square = self.board[multip+row][col-1]
                if not curr_square.is_empty() and curr_square.piece.color != piece.color and not self.discovers_check((multip, -1), col, row):
                    res.append((multip+row, col-1))


            if col+1 < 8:
                curr_square = self.board[multip+row][col+1]
                if not curr_square.is_empty() and curr_square.piece.color != piece.color and not self.discovers_check((multip, 1), col, row):
                    res.append((multip+row, col+1))

            en_passant = piece.get_en_passant()

            for el in en_passant:
                res.append(el)


        directions = piece.get_directions()


        if isinstance(piece, pieces.King):
            for el in directions:

                if row+el[0] > -1 and row+el[0] < 8 and col+el[1] > -1 and col+el[1] < 8:
                    curr_square = self.board[row+el[0]][col+el[1]]
                    if (curr_square.is_empty() or curr_square.piece.color != piece.color) and not self.discovers_check(el, col, row):
                        res.append((el[0]+row, el[1]+col))

        elif isinstance(piece, pieces.Knight):
            for el in directions:

                if row+el[0] > -1 and row+el[0] < 8 and col+el[1] > -1 and col+el[1] < 8:
                    curr_square = self.board[row+el[0]][col+el[1]]
                    if (curr_square.is_empty() or curr_square.piece.color != piece.color) and not self.discovers_check(el, col, row):
                        res.append((row+el[0], col+el[1]))
        else:
            for el in directions:
                i = row+el[0]
                j = col+el[1]

                if i > -1 and i < 8 and j > -1 and j < 8 and not self.discovers_check(el, col, row):

                    while i > -1 and i < 8 and j > -1 and j < 8 and self.board[i][j].is_empty():
                        res.append((i,j))
                        i += el[0]
                        j += el[1]

                    if i > -1 and i < 8 and j > -1 and j < 8 and self.board[i][j].piece.color != piece.color:
                        res.append((i,j))

        return res


    def is_in_check(self, color, res = None, pos = None, pawn_kill = True):

        if pos is None:
            if color == 'b':
                pos = self.black_king
            else:
                pos = self.white_king

        for i in range(pos[0]+1, 8):
            curr_square = self.board[i][pos[1]]

            if not curr_square.is_empty():
                if curr_square.piece.color == color:
                    break
                elif isinstance(curr_square.piece, pieces.Queen) or isinstance(curr_square.piece, pieces.Rook):
                    if res is not None:
                        res.append((i, pos[1]))
                    else:
                        return True
                elif isinstance(curr_square.piece, pieces.Pawn) and color == 'b' and curr_square.piece.color == 'w' and not pawn_kill and (i == pos[0]+1 or (i == 6 and i == pos[0]+2)):
                    if res is not None:
                        res.append((i, pos[1]))
                    else:
                        return True
                break

        for i in range(pos[0]-1, -1, -1):
            curr_square = self.board[i][pos[1]]

            if not curr_square.is_empty():
                if curr_square.piece.color == color:
                    break
                elif (not pawn_kill and i == pos[0] - 1 and color == "w" and curr_square.piece.color == "b") or isinstance(curr_square.piece, pieces.Queen) or isinstance(curr_square.piece, pieces.Rook):
                    if res is not None:
                        res.append((i, pos[1]))
                    else:
                        return True
                elif isinstance(curr_square.piece, pieces.Pawn) and color == 'w' and curr_square.piece.color == 'b' and not pawn_kill and (i == pos[0]-1 or (i == 1 and i == pos[0]-2)):
                    if res is not None:
                        res.append((i, pos[1]))
                    else:
                        return True
                
                break

        for i in range(pos[1]+1, 8):
            curr_square = self.board[pos[0]][i]

            if not curr_square.is_empty():
                if curr_square.piece.color == color:
                    break
                elif  isinstance(curr_square.piece, pieces.Queen) or isinstance(curr_square.piece, pieces.Rook):
                    if res is not None:
                        res.append((pos[0], i))
                    else:
                        return True
                break

        for i in range(pos[1]-1, -1, -1):
            curr_square = self.board[pos[0]][i]

            if not curr_square.is_empty():
                if self.board[pos[0]][i].piece.color == color:
                    break
                elif isinstance(self.board[pos[0]][i].piece, pieces.Queen) or isinstance(self.board[pos[0]][i].piece, pieces.Rook):
                    if res is not None:
                        res.append((pos[0], i))
                    else:
                        return True
                break


            #DIAGONAL

        j = 1
        while pos[0]-j > -1 and pos[1]+j < 8:
            curr_square = self.board[pos[0]-j][pos[1]+j]

            if not curr_square.is_empty():
                if curr_square.piece.color == color:
                    break
                elif j == 1 and color == 'w' and pawn_kill and isinstance(curr_square.piece, pieces.Pawn) or (isinstance(curr_square.piece, pieces.Bishop) or isinstance(curr_square.piece, pieces.Queen)):
                    if res is not None:
                        res.append((pos[0]-j, pos[1]+j))
                    else:
                        return True
                break#####
            j+=1

        j = 1
        while pos[0]+j < 8 and pos[1]+j < 8:
            curr_square = self.board[pos[0]+j][pos[1]+j]

            if not curr_square.is_empty():
                if curr_square.piece.color == color:
                    break
                elif j == 1 and color == 'b' and pawn_kill and isinstance(curr_square.piece, pieces.Pawn) or (isinstance(curr_square.piece, pieces.Bishop) or isinstance(curr_square.piece, pieces.Queen)):
                    if res is not None:
                        res.append((pos[0]+j, pos[1]+j))
                    else:
                        return True
                break#####
            j+=1

        j = 1
        while pos[0]+j < 8 and pos[1]-j > -1:
            curr_square = self.board[pos[0]+j][pos[1]-j]

            if not curr_square.is_empty():
                if curr_square.piece.color == color:
                    break
                elif j == 1 and color == 'b' and pawn_kill and isinstance(curr_square.piece, pieces.Pawn) or (isinstance(curr_square.piece, pieces.Bishop) or isinstance(curr_square.piece, pieces.Queen)):
                    if res is not None:
                        res.append((pos[0]+j, pos[1]-j))
                    else:
                        return True
                break#####
            j+=1

        j = 1
        while pos[0]-j > -1 and pos[1]-j > -1:
            curr_square = self.board[pos[0]-j][pos[1]-j]

            if not curr_square.is_empty():
                if curr_square.piece.color == color:
                    break
                elif j == 1 and color == 'w' and pawn_kill and isinstance(curr_square.piece, pieces.Pawn) or (isinstance(curr_square.piece, pieces.Bishop) or isinstance(curr_square.piece, pieces.Queen)):
                    if res is not None:
                        res.append((pos[0]-j, pos[1]-j))
                    else:
                        return True
                break#####
            j+=1

        possible_knights = pieces.Knight.get_directions()

        for el in possible_knights:
            if pos[0] + el[0] > -1 and pos[0] + el[0] < 8 and pos[1] + el[1] > -1 and pos[1] + el[1] < 8 \
                and isinstance(self.board[pos[0]+el[0]][pos[1]+el[1]].piece, pieces.Knight) and self.board[pos[0]+el[0]][pos[1]+el[1]].piece.color != color:
                if res is not None:
                    res.append((pos[0]+el[0], pos[1]+el[1]))
                else:
                    return True

        if res is not None and len(res) > 0:
            return True

        return False



    def discovers_check(self, dir, col, row):

        color = self.board[row][col].piece.color

        self.move_piece(col, row, col+dir[1], row+dir[0])
        is_check = self.is_in_check(color)

        # print(self.white_king)

        self.reverse_move()

        # print(self.white_king)

        return is_check


    def is_checkmate(self, color):
        #attackers = [] #figury atakujace krola (max 2)

        if color == 'w':
            pos = self.white_king
        else:
            pos = self.black_king

        """

        czesc 1:
        jesli krol jest w szachu, sprawdzamy, czy moze sie ruszyc
        jesli tak -> zawracamy false, nie ma mata
        jesli nie i jesli szachowany jest przez dwie figury (len(attackers)==2) -> zwracamy true, jest mat

        """

        if self.is_in_check(color, res = self.attackers):
            #king_moves = self.get_legal_moves(pos[1], pos[0])

            if self.get_legal_moves(pos[1], pos[0]):
               return False

            if len(self.attackers) == 2:
                self.king_in_check[color] = Checked_by.TWO
                print("dwie atakuja")
                return True

            else:
                if color == 'w':
                    color2 = 'b'
                else:
                    color2 = 'w'

                """
                czesc 2:
                sprawdzamy, czy mozemy zbic figury, ktore atakuja figury, ktore szachuja krola
                nalezy sprawdzic, czy po zbiciu figury szachujacej nie ma szacha
                jesli istenieje bicie ratujace szacha -> zwracamy true
                jesli nie ma takiego bicia, ktore ratuje krola, a figura szachujaca jest konik -> zwracamy prawde, krol jest w szachu

                """
                #figury atakujace figury, ktore szachuja krola
                attackers2 = []

                #figura atakujaca krola
                opponent_piece = self.attackers[0]
                #sprawdzamy, jakie figury atakuja opponent_piece
                self.is_in_check(color2, res = attackers2, pos = opponent_piece)
                # print(attackers2)

                if isinstance(self.board[opponent_piece[0]][opponent_piece[1]].piece, pieces.Knight):
                    self.king_in_check[color] = Checked_by.KNIGHT
                else:
                    self.king_in_check[color] = Checked_by.ONE

                for el in attackers2:

                    #dla kazdej figury z attackers2 nalezy sprawdzic, czy kiedy zabijemy nia opponent_piece, nie bedzie nadal szacha
                    direction = (opponent_piece[0]-el[0], opponent_piece[1]-el[1])
                    if not self.discovers_check(direction, el[1], el[0]):
                        return False

                if isinstance(self.board[opponent_piece[0]][opponent_piece[1]].piece, pieces.Knight):
                    return True

                """
                czesc 3:
                sprawdzamy pola pomiedzy figura atakujaca a krolem
                jesli jest mozliwe zasloniecie krola i po tym ruchu nie ma szacha -> false, krol nie jest w macie
                """

                squares_under_check = self.get_squares_in_between(opponent_piece, pos)

                for el in squares_under_check:
                    #print(el)

                    #figury mogące zablokować szacha poprzez zaslonienie krola
                    attackers3 = []
                    ha = self.is_in_check(color2, attackers3, el, pawn_kill = False)
                    #print(attackers3)

                    if self.is_in_check(color2, attackers3, el, pawn_kill = False):
                        #print(el)
                        #print(attackers3)
                        for piece in attackers3:
                            direction = (el[0]-piece[0], el[1]-piece[1])

                            if not self.discovers_check(direction, piece[1], piece[0]):
                                print("Piece: ", piece, "in dir", direction)
                                return False

                return True  #chyba?

        return False #bo jesli nie ma szacha, to na pewno nie ma mata

    def get_moves_in_check(self, pos):
        piece = self.board[pos[0]][pos[1]].piece

        res = []

        if self.king_in_check[piece.color] == Checked_by.TWO:
            if not isinstance(piece, pieces.King):
                return res
            else:
                return self.get_legal_moves(pos[1], pos[0])

        legal_moves = self.get_legal_moves(pos[1], pos[0])

        if self.king_in_check[piece.color] == Checked_by.KNIGHT:
            if isinstance(piece, pieces.King):
                return self.get_legal_moves(pos[1], pos[0])
            else:
                if pos in legal_moves: #####
                    return pos
            
        elif self.king_in_check[piece.color] == Checked_by.ONE:
            if isinstance(piece, pieces.King):
                return self.get_legal_moves(pos[1], pos[0])
            
            if piece.color == 'w':
                squares_in_check = self.get_squares_in_between(self.white_king, self.attackers[0])
            else:
                squares_in_check = self.get_squares_in_between(self.black_king, self.attackers[0])

            for el in legal_moves:
                if el in squares_in_check:
                    res.append(el)

        return res



    def reverse_move(self):

        hist = self.move_history[-1]

        self.move_piece(hist.end_pos[1], hist.end_pos[0], hist.start_pos[1], hist.start_pos[0])
        self.board[hist.end_pos[0]][hist.end_pos[1]].place_piece(hist.taken_piece)
        self.move_history.pop()


if __name__ == '__main__':
    b = Board()
    b.place_pieces()

    # b.board[6][4].remove_piece()
    # b.move_piece(3,0, 4, 6)
    # b.move_piece(2,0,0,2)
    # b.move_piece(0,6, 3,7)
    # b.move_piece(1,6, 5,7)
    # b.move_piece(2,6, 6,7)
    # #b.board[7][3].remove_piece()
    # b.board[7][5].remove_piece()

    b.move_piece(3,0, 4,1)
    b.board[6][4].remove_piece()
    b.is_checkmate('w')
    print("Moves: ", b.get_moves_in_check((7,3)))
    print(b.king_in_check['w'])

    b.print_board()
    print(b.is_checkmate('w'))
