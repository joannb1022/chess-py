import board
import gui
import tkinter
import pieces
from time import sleep
from gui import PromotionWindow, InitWindow
from gui import Checkmate, Clock

class Engine:
    def __init__(self, parent):
        self.parent = parent
        self.game = board.Board()
        self.visualiser = gui.BoardVisualiser(self.parent, self.game)
        self.turn = 'w'
        self.chosen_square = None
        self.target_square = None
        self.promotion_pieces = {'R': pieces.Rook, 'N': pieces.Knight, 'B': pieces.Bishop, 'Q': pieces.Queen}
        self.time_option = None
        self.end = False

        self.visualiser.pack()

        self.parent.protocol("WM_DELETE_WINDOW", self.end_game)


    def run(self):
        self.init_win = self.visualiser.start_game()
        self.time_option = self.init_win.chosen_time
        self.set_clocks()
        while not self.end:
            self.visualiser.draw()
            if(self.game.is_checkmate(self.turn)):
                self.visualiser.open_new_window(Checkmate, self.turn)
                self.end_game() #na razie tam jest sam exit ale moze bedzie cos jeszcze
                break
            elif self.game.is_stalemate(self.turn):
                print("DRAW")
                break
            self.make_move(self.turn)
            self.chosen_square = None
            self.clocks[self.turn].stop_clock()
            if self.turn == 'w':
                self.turn = 'b'
                self.visualiser.color = 'b'
                self.visualiser.prev_color = 'w'
            else:
                self.turn = 'w'
                self.visualiser.color = 'w'
                self.visualiser.prev_color = 'b'
            self.clocks[self.turn].start_clock()
        print("After end")

    def make_move(self, color):
        #while True:

        print("1Select square:")
        self.visualiser.parent.wait_variable(self.visualiser.wait_state)

        if self.end:
            return

        temp_square = self.visualiser.current_coordinates
        self.visualiser.set_wait_state()
        self.visualiser.set_squares_to_change([])

        temp_piece = self.game.board[temp_square[0]][temp_square[1]].piece

        while temp_piece is None or temp_piece.color != color :
            print("2Select square:")

            self.visualiser.parent.wait_variable(self.visualiser.wait_state)

            if self.end:
                return

            temp_square = self.visualiser.current_coordinates
            self.visualiser.set_wait_state()

            temp_piece = self.game.board[temp_square[0]][temp_square[1]].piece


        self.chosen_square = temp_square

        available_squares = self.game.get_moves(self.chosen_square, self.turn)
        self.visualiser.set_squares_to_change(self.visualiser.squares_to_highlight)
        self.visualiser.set_squares_to_highlight(available_squares)

        print(self.visualiser.squares_to_highlight)

        self.visualiser.draw()

        if self.end:
            return

        flag = 1
        while flag:
            print("Select target square:")

            self.visualiser.parent.wait_variable(self.visualiser.wait_state)

            if self.end:
                return

            self.target_square = self.visualiser.current_coordinates
            self.visualiser.set_wait_state()

            if self.target_square not in available_squares:
                self.chosen_square = self.target_square
                t_piece, t_color = self.game.get_piece(self.target_square)

                if t_piece is None or t_color != color:
                    self.visualiser.set_squares_to_change(self.visualiser.squares_to_highlight)
                    self.visualiser.set_squares_to_highlight([])
                else:
                    available_squares = self.game.get_moves(self.chosen_square, self.turn)
                    self.visualiser.set_squares_to_change(self.visualiser.squares_to_highlight)
                    self.visualiser.set_squares_to_highlight(available_squares)

                self.visualiser.draw()

                curr_piece = self.game.board[self.chosen_square[0]][self.chosen_square[1]].piece

                while not available_squares or curr_piece is None or curr_piece.color != color:
                    print("3Select square:")

                    self.visualiser.parent.wait_variable(self.visualiser.wait_state)

                    if self.end:
                        return

                    self.chosen_square = self.visualiser.current_coordinates
                    self.visualiser.set_wait_state()


                    curr_piece = self.game.board[self.chosen_square[0]][self.chosen_square[1]].piece
                    available_squares = self.game.get_moves(self.chosen_square, self.turn)

                    if curr_piece is not None and curr_piece.color == color:
                        self.visualiser.set_squares_to_change(self.visualiser.squares_to_highlight)
                        self.visualiser.set_squares_to_highlight(available_squares)
                        self.visualiser.draw()

                self.target_square = None
            else:
                flag = 0

            #break

        self.game.move_piece(self.chosen_square, self.target_square, True)

        last_move = self.game.move_history[-1]
        new_squares = [last_move.start_pos, last_move.end_pos]
        if last_move.en_passant:
            new_squares.append((last_move.start_pos[0], last_move.end_pos[1]))
        if last_move.castle:
            new_squares += last_move.castle
        if last_move.promotion:
            self.promotion_win = self.visualiser.open_new_window(PromotionWindow, self.turn)
            piece = self.promotion_win.chosen_piece
            promotion_piece = self.promotion_pieces[piece[1]]
            self.game.board[last_move.end_pos[0]][last_move.end_pos[1]].place_piece(promotion_piece(piece[0]))
            self.visualiser.set_squares_to_change([last_move.end_pos])
            self.visualiser.draw()

        self.visualiser.set_squares_to_change(new_squares)
        self.visualiser.set_squares_to_highlight([])



    def set_clocks(self):
        clock_white = self.visualiser.clock_white
        clock_black = self.visualiser.clock_black
        self.clocks = {'w':clock_white, 'b': clock_black}
        self.clocks['w'].set_clocks(self.time_option)
        self.clocks['b'].set_clocks(self.time_option)
        self.clocks['w'].start_clock()


    def end_game(self):
        self.end = True
        self.visualiser.wait_state.set(1)
        self.parent.after_cancel(self.visualiser.clock_white.job)
        self.parent.after_cancel(self.visualiser.clock_black.job)
        self.visualiser.clock_white.end_game = True
        self.visualiser.clock_black.end_game = True
        self.parent.destroy()
        #self.parent.quit()
        #exit()

if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Chess")
    # real_board = board.Board()
    # b = BoardVisualiser(root, real_board)
    # b.pack()

    e = Engine(root)
    e.run()

    #b.draw()

    root.mainloop()
