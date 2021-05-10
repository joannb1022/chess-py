import tkinter
import board
from os import listdir
import os
from time import sleep
from time import strftime

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
        self.color = 'w'
        self.prev_color = 'w'

        self.new_window = None
        self.wait_state = tkinter.IntVar()

        tkinter.Frame.__init__(self, parent)

        self.canvas = tkinter.Canvas(self, width = canvas_width, height = canvas_height)
        self.canvas.pack()
        self.parent.bind('<Button>', self.get_coord)

        self.clock_white = tkinter.Label()
        self.clock_black = tkinter.Label()

        self.load_images()
        #self.draw('w')
        self.draw()
        self.show_clocks()

    def start_game(self):
        self.new = tkinter.Toplevel(self.parent)
        self.new.attributes('-topmost', True)
        self.new_window = InitWindow(self.new)
        return self.new_window

    def draw(self):
        # print(len(self.squares_to_change))

        # if self.color != self.prev_color:
        #     self.squares_to_change = []
        #     for i in range(8):
        #         for j in range(8):
        #             self.squares_to_change.append((i,j))

        # for el in self.squares_to_change:
        #     self.canvas.delete(f'{el[0]}{el[1]}')
        #     self.canvas.delete(f'{7-el[0]}{7-el[1]}')
        # for el in self.squares_to_highlight:
        #     self.canvas.delete(f'{el[0]}{el[1]}')
        #     self.canvas.delete(f'{7-el[0]}{7-el[1]}')


        self.squares_to_change = []
        for i in range(8):
            for j in range(8):
                self.squares_to_change.append((i,j))

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

    def show_clocks(self):
        hour = strftime("%H")
        minute = strftime("%M")
        second = strftime("%S")
        self.clock_black.config(text = hour + ":" + minute + ":" + second )
        self.clock_black.after(1000, self.show_clocks)
        self.clock_black.pack(side = tkinter.RIGHT)

        self.clock_white.config(text = hour + ":" + minute + ":" + second)
        self.clock_white.after(1000, self.show_clocks)
        self.clock_white.pack(side = tkinter.RIGHT)

    def start_clock():
        print("ehj")

    def stop_clock():
        print("rgr")

    def show_checkmate(self, color):
        self.new = tkinter.Toplevel(self.parent)
        self.new_window = Checkmate(self.new, color)
        self.parent.destroy()

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


    def load_buttons(self):
        self.buttons = [] #nie wiem czy dawac to self, bo bez tego tez zadziala chyba to nie jest nam potrzebne potem
        for i, piece in enumerate(self.pieces):
            photo = self.images[piece]
            b = tkinter.Button(self.parent, height = self.size, width = self.size, image = photo, command = lambda i=i: self.button_press(i))
            b.image = photo
            b.pack(side = tkinter.LEFT)
            self.buttons.append(b)

    def button_press(self, i):
        #0 wieza, 1 konik, 2 goniec, 3 krolowa
        self.chosen_piece = self.pieces[i]
        self.parent.destroy()


    def load_images(self):
        for file_name in self.pieces:
            base_folder = os.path.dirname(__file__)
            image_path = os.path.join(base_folder, f'pieces/{file_name}.png')
            piece_image = tkinter.PhotoImage(file=image_path)
            self.images[file_name] = piece_image


class InitWindow():
    def __init__(self, parent):
        # tkinter.Frame.__init__(self, parent)

        self.parent = parent
        self.size = 400
        self.parent.geometry(f'{self.size}x{self.size}')
        self.frame = tkinter.Frame(self.parent)
        self.label = tkinter.Label(self.parent, text="Hello")
        self.time_array = [1, 2, 5, 10]
        self.chosen_time = None

        self.label.pack()
        self.frame.pack()

        self.load_buttons()

        self.parent.wait_window(self.parent)

    def load_buttons(self):
        start_button = tkinter.Button(self.parent, text = 'Start', bd = '5' ,command = self.destroy_win)
        start_button.pack(side = tkinter.BOTTOM)

        for i, time in enumerate(self.time_array):
            b = tkinter.Button(self.parent,text = f'{time}', command = lambda i=i: self.choose_time(i))
            b.pack(side = tkinter.LEFT)

    def choose_time(self, i):
        self.chosen_time = self.time_array[i]

    def destroy_win(self):
        self.parent.destroy()


class Checkmate():
    def __init__(self, parent, color):

        self.parent = parent
        self.parent.geometry("450x300")

        frame = tkinter.Frame(self.parent)
        label = tkinter.Label(self.parent, text=f"CHECKMATE, {color} LOSES").place(x = 200, y = 100)

        self.parent.wait_window(self.parent)


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Chess")
    real_board = board.Board()
    b = BoardVisualiser(root, real_board)
    b.pack()

    #b.draw()
    root.mainloop()
