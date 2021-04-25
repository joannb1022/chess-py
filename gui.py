import tkinter
import board
from os import listdir

class BoardVisualiser(tkinter.Frame):

    def __init__(self, parent, board, size = 64):
        self.size = size
        canvas_width = size * 8
        canvas_height = size * 8
        self.board = board
        self.parent = parent
        self.squares_to_change = [(i,j) for j in range(8) for i in range(8)]
        self.pieces = {}


        tkinter.Frame.__init__(self, parent)

        self.canvas = tkinter.Canvas(self, width = canvas_width, height = canvas_height)
        self.canvas.pack()
        #self.parent.bind('<Button>', self.highlight_piece)

        self.load_images()
        print(self.pieces)
        self.draw()


    def draw(self):
        #global pieces
        #self.pieces = []
        for el in self.squares_to_change:
            if (el[0]+el[1]) % 2 != 0:
                filler = '#a76d3e'
            else:
                filler = "#f0dfcd" 
            self.canvas.create_rectangle(el[0]*self.size, el[1]*self.size, (el[0]+1)*self.size, (el[1]+1)*self.size, fill = filler, width = 0)
        for el in self.squares_to_change:
            if self.board.get_piece(el) != (None, None):
                file_name = self.board.board[el[0]][el[1]].get_image()
                piece_image = self.pieces[file_name[7:9]]
                self.parent.piece_image = piece_image
                self.canvas.create_image((self.size*(el[1]+0.5), self.size*(el[0]+0.5)), image = piece_image)


    def load_images(self):
        pngs = listdir('pieces')
        for file_name in pngs:
            piece_image = tkinter.PhotoImage(file=f'pieces/{file_name}')
            self.pieces[file_name[:2]] = piece_image


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Chess")
    real_board = board.Board()
    b = BoardVisualiser(root, real_board)
    b.pack()

    #b.draw()
    root.mainloop()

