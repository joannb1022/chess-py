import board

class Engine:
    def __init__(self):
        self.game = board.Board()
        self.turn = 'w'
        self.chosen_square = None
        self.target_square = None
    
    def run(self):
        while True:
            self.game.print_board()
            if(self.game.is_checkmate(self.turn)):
                print(f"CHECKMATE, {self.turn} LOSES")
                break
            elif self.game.is_stalemate(self.turn):
                print("DRAW")
                break
            self.make_move(self.turn)
            self.chosen_square = None
            if self.turn == 'w':
                self.turn = 'b'
            else:
                self.turn = 'w'

    def make_move(self, color):
        while True:
            
            print("Select square:")
            temp_square = (int(input()), int(input()))
            temp_piece = self.game.board[temp_square[0]][temp_square[1]].piece

            while temp_piece is None or temp_piece.color != color:
                print("Select square:")
                temp_square = (int(input()), int(input()))
                temp_piece = self.game.board[temp_square[0]][temp_square[1]].piece


            self.chosen_square = temp_square
            
            available_squares = self.game.get_moves(self.chosen_square, self.turn)
            
            flag = 1
            while flag:
                print("Select target square:")
                self.target_square = (int(input()), int(input()))
                if self.target_square not in available_squares:
                    self.chosen_square = self.target_square
                    available_squares = self.game.get_moves(self.chosen_square, self.turn)
                    
                    curr_piece = self.game.board[self.chosen_square[0]][self.chosen_square[1]].piece

                    while not available_squares or curr_piece is None or curr_piece.color != color:
                        print("Select square:")
                        self.chosen_square = (int(input()), int(input()))
                        curr_piece = self.game.board[self.chosen_square[0]][self.chosen_square[1]].piece
                        available_squares = self.game.get_moves(self.chosen_square, self.turn)

                    self.target_square = None
                else:
                    flag = 0

            break

        self.game.move_piece(self.chosen_square, self.target_square, True)



if __name__ == "__main__":
    e = Engine()
    e.run()