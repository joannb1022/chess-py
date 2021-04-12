from board import Board

class DrawBoard():
    def __init__(self):
        self.board = Board()
        self.board.place_pieces()
        self.board.print_board()
        self.height = 512
        self.width = 512
        self.dimension = 8
        self.square_size = self.width // self.dimension






if __name__ == '__main__':
    board = DrawBoard()
