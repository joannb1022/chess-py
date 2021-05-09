import board
import gui
import tkinter
from time import sleep

class Engine:
    def __init__(self, parent):
        self.game = board.Board()
        self.visualiser = gui.BoardVisualiser(parent, self.game)
        self.turn = 'w'
        self.chosen_square = None
        self.target_square = None

        self.visualiser.pack()

    def run(self):
        while True:
            self.game.print_board()
            self.visualiser.draw(self.turn)

            if(self.game.is_checkmate(self.turn)):
                print(f"CHECKMATE, {self.turn} LOSES")
                break
            elif self.game.is_stalemate(self.turn):
                print("DRAW")
                break
            self.make_move(self.turn)
            self.visualiser.promotion_window('w')
            self.chosen_square = None
            if self.turn == 'w':
                self.turn = 'b'
            else:
                self.turn = 'w'

    def make_move(self, color):
        while True:

            print("Select square:")
            temp_square = (int(input()), int(input()))

            #temp_square = self.visualiser.current_coordinates


            temp_piece = self.game.board[temp_square[0]][temp_square[1]].piece

            while temp_piece is None or temp_piece.color != color:
                print("Select square:")

                temp_square = (int(input()), int(input()))

                temp_piece = self.game.board[temp_square[0]][temp_square[1]].piece


            self.chosen_square = temp_square

            available_squares = self.game.get_moves(self.chosen_square, self.turn)
            self.visualiser.set_squares_to_highlight(available_squares)

            print(self.visualiser.squares_to_highlight)

            self.visualiser.draw(self.turn)

            flag = 1
            while flag:
                print("Select target square:")

                self.target_square = (int(input()), int(input()))

                if self.target_square not in available_squares:
                    self.chosen_square = self.target_square
                    available_squares = self.game.get_moves(self.chosen_square, self.turn)
                    self.visualiser.set_squares_to_highlight(available_squares)
                    self.visualiser.draw(self.turn)

                    curr_piece = self.game.board[self.chosen_square[0]][self.chosen_square[1]].piece

                    while not available_squares or curr_piece is None or curr_piece.color != color:
                        print("Select square:")

                        self.chosen_square = (int(input()), int(input()))

                        curr_piece = self.game.board[self.chosen_square[0]][self.chosen_square[1]].piece
                        available_squares = self.game.get_moves(self.chosen_square, self.turn)
                        self.visualiser.set_squares_to_highlight(available_squares)
                        self.visualiser.draw(self.turn)

                    self.target_square = None
                else:
                    flag = 0

            break

        self.game.move_piece(self.chosen_square, self.target_square, True)

        last_move = self.game.move_history[-1]
        new_squares = [last_move.start_pos, last_move.end_pos]
        # if last_move.en_passant:
        #     new_squares.append((last_move.start_pos[0], last_move.end_pos[1]))
        # if last_move.castle:
        #     new_squares += last_move.castle
        #if last_move.promotion:
            #promotion_piece = self.visualiser.
        self.visualiser.set_squares_to_change(new_squares)
        self.visualiser.set_squares_to_highlight([])



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
