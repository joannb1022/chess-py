import tkinter
import board
from os import listdir
import os
from time import sleep

class BoardVisualiser(tkinter.Frame):

    def __init__(self, parent, board, size = 64):
        self.size = size
        canvas_width = size * 8
        canvas_height = size * 8
        self.board = board
        self.parent = parent
        self.squares_to_change = [(i,j) for j in range(8) for i in range(8)]
        self.squares_to_highlight = []
        self.pieces = {}
        self.current_coordinates = (None, None)
        self.clicked = False
        self.new_window = None
        self.color = 'w'
        self.prev_color = 'w'
        self.wait_state = tkinter.IntVar()

        tkinter.Frame.__init__(self, parent)

        self.canvas = tkinter.Canvas(self, width = canvas_width, height = canvas_height)
        self.canvas.pack()
        self.parent.bind('<Button>', self.get_coord)

        self.load_images()
        print(self.pieces)
        #self.draw('w')
        self.draw()

    def test(self, event):
        print('test')

    def draw(self):
        print(len(self.squares_to_change))

        # if self.color != self.prev_color:
        #     self.squares_to_change = []
        #     for i in range(8):
        #         for j in range(8):
        #             self.squares_to_change.append((i,j))
        
        self.squares_to_change = []
        for i in range(8):
            for j in range(8):
                self.squares_to_change.append((i,j))

        for el in self.squares_to_change:
            self.canvas.delete(f'{el[0]}{el[1]}')
            self.canvas.delete(f'{7-el[0]}{7-el[1]}')
        for el in self.squares_to_highlight:
            self.canvas.delete(f'{el[0]}{el[1]}')
            self.canvas.delete(f'{7-el[0]}{7-el[1]}')

        #print(self.canvas.find_all())
        self.canvas.delete("all")
        #sleep(0.5)

        for el in self.squares_to_change:
            if (el[0]+el[1]) % 2 != 0:
                filler = '#a76d3e'
            else:
                filler = "#f0dfcd"
            if self.color == 'w':
                self.canvas.create_rectangle(el[1]*self.size, el[0]*self.size, (el[1]+1)*self.size, (el[0]+1)*self.size, fill = filler, width = 0, tag = f'{el[0]}{el[1]}')
            else:
                self.canvas.create_rectangle((7-el[1])*self.size, (7-el[0])*self.size, (7-el[1]+1)*self.size, (7-el[0]+1)*self.size, fill = filler, width = 0, tag = f'{7-el[0]}{7-el[1]}')


        for el in self.squares_to_change:
            if self.board.get_piece(el) != (None, None):
                
                file_name = self.board.board[el[0]][el[1]].get_image()
                piece_image = self.pieces[file_name[7:9]]

                if self.color == 'w':
                    self.canvas.create_image((self.size*(el[1]+0.5), self.size*(el[0]+0.5)), image = piece_image, tag = f'{el[0]}{el[1]}')
                else:
                    self.canvas.create_image((self.size*(7-el[1]+0.5), self.size*(7-el[0]+0.5)), image = piece_image, tag = f'{7-el[0]}{7-el[1]}')

        for el in self.squares_to_highlight:
            if self.board.get_piece(el) != (None, None):
                if self.color == 'w':
                    self.higlight_square(el)
                else:
                    self.higlight_square((7-el[0], 7-el[1]))
            else:
                if self.color == 'w':
                    self.canvas.create_oval((el[1]+0.4)*self.size, (el[0]+0.4)*self.size, (el[1]+0.6)*self.size, (el[0]+0.6)*self.size, fill = '#1C9005', outline = '#1C9005', tag = f'{el[0]}{el[1]}')
                else:
                    self.canvas.create_oval((7-el[1]+0.4)*self.size, (7-el[0]+0.4)*self.size, (7-el[1]+0.6)*self.size, (7-el[0]+0.6)*self.size, fill = '#1C9005', outline = '#1C9005', tag = f'{7-el[0]}{7-el[1]}')


    def higlight_square(self, square):
        self.canvas.create_polygon(square[1]*self.size, square[0]*self.size, square[1]*self.size, square[0]*self.size+16, square[1]*self.size+16, square[0]*self.size, fill = '#1C9005', tag = f'{square[0]}{square[1]}')
        self.canvas.create_polygon((square[1]+1)*self.size-16, square[0]*self.size, (square[1]+1)*self.size, square[0]*self.size, (square[1]+1)*self.size, square[0]*self.size+16, fill = '#1C9005', tag = f'{square[0]}{square[1]}')
        self.canvas.create_polygon((square[1]+1)*self.size-16, (square[0]+1)*self.size, (square[1]+1)*self.size, (square[0]+1)*self.size, (square[1]+1)*self.size, (square[0]+1)*self.size-16, fill = '#1C9005', tag = f'{square[0]}{square[1]}')
        self.canvas.create_polygon(square[1]*self.size, (square[0]+1)*self.size-16, square[1]*self.size, (square[0]+1)*self.size, square[1]*self.size+16, (square[0]+1)*self.size, fill = '#1C9005', tag = f'{square[0]}{square[1]}')

    def load_images(self):
        pngs = listdir('pieces')
        for file_name in pngs:
            piece_image = tkinter.PhotoImage(file=f'pieces/{file_name}')
            self.pieces[file_name[:2]] = piece_image


    def set_squares_to_change(self, squares):
        self.squares_to_change = squares

    def set_squares_to_highlight(self, squares):
        self.squares_to_highlight = squares

    def get_coord(self, event):
        x, y = int(event.x/self.size), int(event.y/self.size)
        self.clicked = True
        print('visualiser:', self.clicked)
        if self.color == 'w':
            self.current_coordinates = (y,x)
        else:
            self.current_coordinates = (7-y, 7-x)
        
        print('in get_coord')
        self.wait_state.set(1)

    def promotion_window(self, color):
        self.new = tkinter.Toplevel(self.parent)
        self.new_window = PromotionWindow(self.new, color)
        return self.new_window

    def set_wait_state(self):
        self.wait_state = tkinter.IntVar()

    # def close_windows(self):
    #     self.parent.destroy()



class PromotionWindow(tkinter.Frame):
    def __init__(self, parent, color):
        # tkinter.Frame.__init__(self, parent)

        self.parent = parent
        self.parent.geometry("280x100")
        self.frame = tkinter.Frame(self.parent)
        self.size = 64
        self.images = {}
        self.pieces = [f'{color}R', f'{color}N', f'{color}B', f'{color}Q']
        self.label = tkinter.Label(self.parent, text="Choose piece")
        self.label.pack()
        self.frame.pack()
        self.chosen_piece = None

        self.load_images()
        self.load_buttons()
        self.parent.wait_window(self.parent)

        # self.canvas = tkinter.Canvas(self, width = 4*self.size, height = self.size)
        # self.canvas.pack()
        # self.post_images()
        # self.parent.bind('<Button>', self.get_piece)

    def load_buttons(self):
        self.buttons = [] #nie wiem czy dawac to self, bo bez tego tez zadziala chyba to nie jest nam potrzebne potem
        for i, piece in enumerate(self.pieces):
            photo = self.images[piece]
            b = tkinter.Button(self.parent, height = 64, width = 64, image = photo, command = lambda i=i: self.button_press(i))
            b.image = photo  #bez tego mi sie nie ladowaly (cos z tym garbage collector)
            b.pack(side = tkinter.LEFT)
            self.buttons.append(b)

    def button_press(self, i):
        #0 wieza, 1 konik, 2 goniec, 3 krolowa
        self.chosen_piece = self.pieces[i]
        self.parent.destroy()

    # def get_piece(self, event):
    #     x = int(event.x/self.size)
    #     print(x)
    #     return self.pieces[x]

    def load_images(self):
        for file_name in self.pieces:
            base_folder = os.path.dirname(__file__)
            image_path = os.path.join(base_folder, f'pieces/{file_name}.png')
            piece_image = tkinter.PhotoImage(file=image_path)
            self.images[file_name] = piece_image

    # def post_images(self):
    #     for i in range(4):
    #         print(self.images[self.pieces[i]])
    #         #self.canvas.create_image((self.size*(i+0.5), self.size*(i+0.5)), image = self.images[self.pieces[i]])
    #         self.canvas.create_rectangle(0, 0, 100, 100, fill = "red")
    #         self.canvas.create_image((0, 0), image = self.images[self.pieces[i]])



if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Chess")
    real_board = board.Board()
    b = BoardVisualiser(root, real_board)
    b.pack()

    #b.draw()
    root.mainloop()