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
        self.place_pieces()

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


    def move_piece(self, s_pos, t_pos, real_move = False):

        if real_move:
            for el in self.en_passant:
                piece = self.board[el[0]][el[1]].piece
                if piece is not None:
                    piece.en_passant_decreasing = False
                    piece.en_passant_increasing = False

        s_square = self.board[s_pos[0]][s_pos[1]]

        if isinstance(s_square.piece, pieces.King):
            if s_square.piece.color == 'b':
                self.black_king = (t_pos[0], t_pos[1])
            else:
                self.white_king = (t_pos[0], t_pos[1])

            if abs(s_pos[1]-t_pos[1]) == 2:
                direction = t_pos[1]-s_pos[1]/2
                if direction == -1:
                    column = 0
                else:
                    column = 7

                rook = self.board[t_pos[0]][column].remove_piece()
                self.board[t_pos[0]][t_pos[1]-direction].place_piece(rook)

        elif isinstance(s_square.piece, pieces.Pawn):
            if real_move:
                s_square.piece.en_passant_decreasing = False
                s_square.piece.en_passant_increasing = False
                s_square.piece.can_move_two = False

            if abs(t_pos[0]-s_pos[0]) == 2:
                if t_pos[1] > 0:
                    p_square = self.board[t_pos[0]][t_pos[1]-1]

                    if p_square.piece is not None and p_square.piece.color != s_square.piece.color:
                        p_square.piece.en_passant_increasing = True
                        self.en_passant.append((t_pos[0], t_pos[1]-1))

                if t_pos[1] < 7:
                    p_square = self.board[t_pos[0]][t_pos[1]+1]

                    if p_square.piece is not None and p_square.piece.color != s_square.piece.color:
                        p_square.piece.en_passant_decreasing = True
                        self.en_passant.append((t_pos[0], t_pos[1]+1))

            elif s_square.piece.en_passant_increasing and t_pos[1]-s_pos[1] == 1 and real_move:
                self.board[s_pos[0]][t_pos[1]].remove_piece()
            elif s_square.piece.en_passant_decreasing and t_pos[1]-s_pos[1] == -1 and real_move:
                self.board[s_pos[0]][t_pos[1]].remove_piece()

        piece = s_square.remove_piece()


        curr_move = move.Move(piece, s_pos, t_pos, self.board[t_pos[0]][t_pos[1]].piece)

        self.board[t_pos[0]][t_pos[1]].place_piece(piece)

        self.move_history.append(curr_move)

        if real_move:
            piece.can_castle = False


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


    def get_moves(self, pos, color):
        if self.king_in_check[color] != Checked_by.NONE:
            return self.get_moves_in_check(pos)
        return self.get_legal_moves(pos)


    def get_legal_moves(self,pos):
        piece = self.board[pos[0]][pos[1]].piece
        res = []

        if piece is None:
            return res

        if isinstance(piece, pieces.Pawn):
            if piece.color == 'b':
                multip = 1
            else:
                multip = -1


            if self.board[multip+pos[0]][pos[1]].is_empty() and not self.discovers_check((multip, 0), pos):
                res.append((pos[0]+multip,pos[1]))
                if piece.can_move_two and pos[0]%7 == 6 or pos[0]%7 == 1 and self.board[2*multip+pos[0]][pos[1]].is_empty() and not self.discovers_check((multip*2, 0), pos):
                    res.append((pos[0]+multip*2, pos[1]))


            if pos[1]-1 > -1:
                curr_square = self.board[multip+pos[0]][pos[1]-1]
                if not curr_square.is_empty() and curr_square.piece.color != piece.color and not self.discovers_check((multip, -1), pos):
                    res.append((multip+pos[0], pos[1]-1))


            if pos[1]+1 < 8:
                curr_square = self.board[multip+pos[0]][pos[1]+1]
                if not curr_square.is_empty() and curr_square.piece.color != piece.color and not self.discovers_check((multip, 1), pos):
                    res.append((multip+pos[0], pos[1]+1))

            en_passant = piece.get_en_passant()


            for el in en_passant:
                if not self.discovers_check(el, pos):
                    res.append((pos[0]+el[0], pos[1]+el[1]))



        elif isinstance(piece, pieces.King):
            directions = piece.get_directions()
            for el in directions:

                if pos[0]+el[0] > -1 and pos[0]+el[0] < 8 and pos[1]+el[1] > -1 and pos[1]+el[1] < 8:
                    curr_square = self.board[pos[0]+el[0]][pos[1]+el[1]]

                    if (curr_square.is_empty() or curr_square.piece.color != piece.color) and not self.discovers_check(el, pos):

                        res.append((el[0]+pos[0], el[1]+pos[1]))

            if self.check_castling(pos, 1):
               res.append((pos[0], pos[1]+2))
            if self.check_castling(pos, -1):
               res.append((pos[0], pos[1]-2))


        elif isinstance(piece, pieces.Knight):
            directions = piece.get_directions()
            for el in directions:

                if pos[0]+el[0] > -1 and pos[0]+el[0] < 8 and pos[1]+el[1] > -1 and pos[1]+el[1] < 8:

                    curr_square = self.board[pos[0]+el[0]][pos[1]+el[1]]

                    if (curr_square.is_empty() or curr_square.piece.color != piece.color) and not self.discovers_check(el, pos):

                        res.append((pos[0]+el[0], pos[1]+el[1]))

        else:
            directions = piece.get_directions()
            for el in directions:
                i = pos[0]+el[0]

                j = pos[1]+el[1]

                if i > -1 and i < 8 and j > -1 and j < 8 and not self.discovers_check(el,pos):


                    while i > -1 and i < 8 and j > -1 and j < 8 and self.board[i][j].is_empty():
                        res.append((i,j))
                        i += el[0]
                        j += el[1]

                    if i > -1 and i < 8 and j > -1 and j < 8 and self.board[i][j].piece.color != piece.color:
                        res.append((i,j))

        return res

    def check_castling(self, king_pos, direction):

        king = self.board[king_pos[0]][king_pos[1]].piece

        if not king.can_castle or self.king_in_check[king.color] != Checked_by.NONE:
            return False

        if direction == 1:
            column = 7
        else:
            column = 0

        if not self.board[king_pos[0]][column].piece.can_castle:
            return False

        squares_in_between = self.get_squares_in_between(king_pos, (king_pos[0], column))

        for el in squares_in_between:
            if self.board[el[0]][el[1]].piece is not None:
                return False

        return not self.is_in_check(king.color, pos = (king_pos[0], king_pos[1]+direction)) and not self.is_in_check(king.color, pos = (king_pos[0], king_pos[1]+2*direction))



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
                elif isinstance(curr_square.piece, pieces.Queen) or isinstance(curr_square.piece, pieces.Rook): ######
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

    def get_piece(self, pos):
        piece = self.board[pos[0]][pos[1]].get_piece()
        if piece is None:
            return None, None
        return piece, piece.color


    def discovers_check(self, dir,pos):
        color = self.board[pos[0]][pos[1]].piece.color

        self.move_piece(pos, (pos[0]+dir[0], pos[1]+dir[1]))
        is_check = self.is_in_check(color)

        # print(self.white_king)

        self.reverse_move()

        # print(self.white_king)

        return is_check


    def is_checkmate(self, color):

        #czyszczenie tablicy figur atakujących króla w przypadku wykonania ruchu przez gracza
        self.attackers = []

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
            #king_moves = self.get_legal_moves(pos)

            if self.get_legal_moves(pos):
               return False

            if len(self.attackers) == 2:
                self.king_in_check[color] = Checked_by.TWO
                print(self.attackers)
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
                    if not self.discovers_check(direction, el):
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
                    #ha = self.is_in_check(color2, attackers3, el, pawn_kill = False)
                    #print(attackers3)

                    if self.is_in_check(color2, attackers3, el, pawn_kill = False):
                        #print(el)
                        print(attackers3)
                        for piece in attackers3:
                            direction = (el[0]-piece[0], el[1]-piece[1])

                            if not self.discovers_check(direction, piece):
                                print("Piece: ", piece, "in dir", direction)
                                return False

                return True  #chyba?

        return False #bo jesli nie ma szacha, to na pewno nie ma mata

    def get_moves_in_check(self, pos):
        piece = self.board[pos[0]][pos[1]].piece

        res = []
        if piece is None:
            return res

        if self.king_in_check[piece.color] == Checked_by.TWO:
            if not isinstance(piece, pieces.King):
                return res
            else:
                return self.get_legal_moves(pos)

        legal_moves = self.get_legal_moves(pos)

        if self.king_in_check[piece.color] == Checked_by.KNIGHT:
            if isinstance(piece, pieces.King):
                return self.get_legal_moves(pos)
            else:
                if pos in legal_moves: #####
                    return pos

        elif self.king_in_check[piece.color] == Checked_by.ONE:
            if isinstance(piece, pieces.King):
                return self.get_legal_moves(pos)

            if piece.color == 'w':
                squares_in_check = self.get_squares_in_between(self.white_king, self.attackers[0])
            else:
                squares_in_check = self.get_squares_in_between(self.black_king, self.attackers[0])

            for el in legal_moves:
                if el in squares_in_check:
                    res.append(el)

        return res


    def is_stalemate(self, color):
        if not self.king_in_check[color] == Checked_by.NONE:
            return False
        
        for i in range(8):
            for j in range(8):
                if self.board[i][j].piece is not None and self.board[i][j].piece.color == color and self.get_legal_moves((i,j)):
                    return False
        return True

    def reverse_move(self):

        hist = self.move_history[-1]

        self.move_piece(hist.end_pos, hist.start_pos)
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

    b.move_piece((0,3), (1,4))
    b.move_piece((6,4), (3,4), True)

    b.move_piece((1,3), (3,3), True)


    #b.move_piece((3,4), (2,3))
    #b.move_piece((7,3), (3,3), True)

    print(b.get_legal_moves((3,4)))

    b.print_board()
    #print(b.is_checkmate('w'))
    #print(b.check_castling((7,4), 1))
