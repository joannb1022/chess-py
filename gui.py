import tkinter
import board
from os import listdir
import os
from time import sleep
from time import strftime
import pieces


class BoardVisualiser(tkinter.Frame):
    """narzędzie do wizualizacji szachownicy"""

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
        self.show_game = [False]
        self.new_window = None
        self.wait_state = tkinter.IntVar()
        self.clock_white = None
        self.clock_black = None

        tkinter.Frame.__init__(self, parent)
        self.frame = tkinter.Frame(parent)
        self.frame.pack(side = tkinter.LEFT)
        self.canvas = tkinter.Canvas(self.frame, width = canvas_width, height = canvas_height)
        self.background = tkinter.Canvas(self.parent, width = 300, height = canvas_height, bg = '#212121')
        self.parent.geometry(f"{canvas_width+300}x{canvas_height}")
        self.canvas.pack()
        self.background.place(x = canvas_width, y = 0)
        self.scores = Score(self.parent)
        self.move_history = Moves(self.parent)
        self.parent.bind('<Button>', self.get_coord)
        self.parent.resizable(False, False)
        self.load_images()
        self.draw()

    def start_game(self):
        """uruchomienie okna do wyboru formatu czasowego gry"""

        self.new = tkinter.Toplevel(self.parent)
        self.new.attributes('-topmost', True)
        self.new_window = InitWindow(self.new)
        return self.new_window

    def draw(self):
        """funkcja wywołana po pacie"""

        self.squares_to_change = []
        for i in range(8):
            for j in range(8):
                self.squares_to_change.append((i,j))

        self.canvas.delete("all")
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
        """podświetlanie pola na szachownicy"""

        self.canvas.create_polygon(square[1]*self.size, square[0]*self.size, square[1]*self.size, square[0]*self.size+16, square[1]*self.size+16, square[0]*self.size, fill = '#1C9005', tag = f'{square[0]}{square[1]}')
        self.canvas.create_polygon((square[1]+1)*self.size-16, square[0]*self.size, (square[1]+1)*self.size, square[0]*self.size, (square[1]+1)*self.size, square[0]*self.size+16, fill = '#1C9005', tag = f'{square[0]}{square[1]}')
        self.canvas.create_polygon((square[1]+1)*self.size-16, (square[0]+1)*self.size, (square[1]+1)*self.size, (square[0]+1)*self.size, (square[1]+1)*self.size, (square[0]+1)*self.size-16, fill = '#1C9005', tag = f'{square[0]}{square[1]}')
        self.canvas.create_polygon(square[1]*self.size, (square[0]+1)*self.size-16, square[1]*self.size, (square[0]+1)*self.size, square[1]*self.size+16, (square[0]+1)*self.size, fill = '#1C9005', tag = f'{square[0]}{square[1]}')

    def load_images(self):
        """ładowanie zdjęć figur"""

        pngs = listdir('pieces')
        for file_name in pngs:
            piece_image = tkinter.PhotoImage(file=f'pieces/{file_name}')
            self.pieces[file_name[:2]] = piece_image

    def set_squares_to_change(self, squares):
        self.squares_to_change = squares

    def set_squares_to_highlight(self, squares):
        self.squares_to_highlight = squares

    def get_coord(self, event):
        """zwraca koordynaty klikniętego pola"""

        x, y = int(event.x/self.size), int(event.y/self.size)
        if x < 0 or y < 0 or x > 7 or y > 7:
            return
        self.clicked = True

        if self.color == 'w':
            self.current_coordinates = (y,x)
        else:
            self.current_coordinates = (7-y, 7-x)
        self.wait_state.set(1)

    def set_wait_state(self):
        self.wait_state = tkinter.IntVar()

    def open_new_window(self, _class, review = None, color = None, text = None):
        self.new = tkinter.Toplevel(self.parent)
        new_window = _class(self.new, review, color, text)
        return new_window

    def set_clocks(self, players):
        self.clock_white = Clock(self.parent, 'w', players['w'])
        self.clock_black = Clock(self.parent, 'b', players['b'])
        return self.clock_white, self.clock_black

    def review_game(self, history):
        """analiza przebiegu gry"""

        past_moves = []
        future_moves = []
        self.color = 'w'

        for i in range(len(history)-1, -1, -1):
            future_moves.append(history[i])

        def on_key_press(event):
            nonlocal past_moves, future_moves

            if event.keysym == 'Left' and len(past_moves) > 0:
                move = past_moves.pop()
                piece = self.board.board[move.end_pos[0]][move.end_pos[1]].remove_piece()
                self.board.board[move.start_pos[0]][move.start_pos[1]].place_piece(piece)

                if move.promotion:
                    self.board.board[move.start_pos[0]][move.start_pos[1]].place_piece(pieces.Pawn(move.piece.color))
                if move.castle:
                    self.board.move_piece(move.castle[1], move.castle[0], True)
                if move.en_passant:
                    self.board.board[move.start_pos[0]][move.end_pos[1]].place_piece(move.taken_piece)
                else:
                    self.board.board[move.end_pos[0]][move.end_pos[1]].place_piece(move.taken_piece)

                future_moves.append(move)
                self.wait_state.set(1)

            elif event.keysym == 'Right' and len(future_moves) > 0:
                move = future_moves.pop()
                self.board.move_piece(move.start_pos, move.end_pos, True)

                if move.promotion:
                    self.board.board[move.end_pos[0]][move.end_pos[1]].place_piece(move.promotion_piece)

                past_moves.append(move)
                self.wait_state.set(1)

        self.board.place_pieces()
        self.parent.bind('<KeyPress>', on_key_press)
        play_button = tkinter.Button(self.parent, text = "Play again", font=("Arial", 14), command = lambda: self.wait_state.set(2), background='#345', activebackground='#345', fg = 'white')
        play_button.place(x = 615, y = 300)
        self.draw()

        while(True):
            self.parent.wait_variable(self.wait_state)
            if self.wait_state.get() == 1:
                self.draw()
            elif self.wait_state.get() == 2:
                break

        play_button.destroy()
        self.parent.unbind('<KeyPress>')


class PromotionWindow(tkinter.Frame):
    """okienko do promocji piona"""

    def __init__(self, parent, color, text, review):
        self.parent = parent
        self.parent.geometry("280x100")
        self.frame = tkinter.Frame(self.parent)
        self.size = 64
        self.images = {}
        self.pieces = [f'{color}R', f'{color}N', f'{color}B', f'{color}Q']
        self.chosen_piece = None
        self.label = tkinter.Label(self.parent, text="Choose piece")
        self.label.pack()
        self.frame.pack()
        self.load_images()
        self.buttons = []
        self.load_buttons()
        self.parent.wait_window(self.parent)

    def load_buttons(self):
        for i, piece in enumerate(self.pieces):
            photo = self.images[piece]
            b = tkinter.Button(self.parent, height = self.size, width = self.size, image = photo, command = lambda i=i: self.button_press(i))
            b.image = photo
            b.pack(side = tkinter.LEFT)
            self.buttons.append(b)

    def button_press(self, i):
        self.chosen_piece = self.pieces[i]
        self.parent.destroy()

    def load_images(self):
        for file_name in self.pieces:
            base_folder = os.path.dirname(__file__)
            image_path = os.path.join(base_folder, f'pieces/{file_name}.png')
            piece_image = tkinter.PhotoImage(file=image_path)
            self.images[file_name] = piece_image


class InitWindow():
    """startowe okno gry"""

    def __init__(self, parent):
        self.parent = parent
        self.size = 300
        self.parent.geometry(f'{self.size}x{self.size}')
        self.frame = tkinter.Frame(self.parent)
        self.label = tkinter.Label(self.parent, text="Choose time option: ", font=("Arial",18,""))
        self.increment = tkinter.Label(self.parent, text="Choose increment: ", font=("Arial",18,""))
        self.time_array = [1, 3, 5, 10]
        self.increment_array = [0, 1, 2, 5]
        self.chosen_time = None
        self.chosen_increment = None
        self.label.place(x = 40, y = 10)
        self.increment.place(x = 40, y = 120)
        self.frame.pack()
        self.widgets()
        self.parent.wait_window(self.parent)

    def widgets(self):
        start_button = tkinter.Button(self.parent, text = 'Start',font=("Arial",18,""), bd = '5' ,command = self.destroy_win)
        start_button.place(x = 104, y = 230)

        for i, time in enumerate(self.time_array):
            b = tkinter.Button(self.parent,text = f'{time}',font=("Arial",18,""), command = lambda i=i: self.choose_time(i))
            b.place(x = 50 + i*50, y = 50)
        for i, increment in enumerate(self.increment_array):
            b = tkinter.Button(self.parent,text = f'{increment}',font=("Arial",18,""), command = lambda i=i: self.choose_increment(i))
            b.place(x = 50 + i*50, y = 160)

    def choose_time(self, i):
        self.chosen_time = self.time_array[i]

    def choose_increment(self, i):
        self.chosen_increment = self.increment_array[i]

    def destroy_win(self):
        self.parent.destroy()


class ClosingWindow():
    """okno pod koniec gry"""

    def __init__(self, parent, review, color, text):
        self.parent = parent
        self.parent.geometry("450x300")

        frame = tkinter.Frame(self.parent)
        if color == 'w':
            win_color = 'Black'
        else:
            win_color = 'White'

        if text == 'Checkmate':
            label = tkinter.Label(self.parent, font=("Arial",14), text=f"{text}, {win_color} wins").place(x = 120, y = 100)
        elif text == 'Draw':
            label = tkinter.Label(self.parent, font=("Arial",14), text=f"{text}").place(x = 195, y = 100)
        elif text == 'Time':
            label = tkinter.Label(self.parent, font=("Arial",14), text=f"{win_color} wins on time").place(x = 150, y = 100)

        play_button = tkinter.Button(self.parent, font=("Arial",14), text = "Play again", command = lambda: self.parent.destroy())
        review_button = tkinter.Button(self.parent, font=("Arial",14), text = "Review game", command = lambda rev = review: self.review_game(rev))
        play_button.place(x =  90, y = 200)
        review_button.place(x = 210, y = 200)
        self.parent.wait_window(self.parent)

    def review_game(self, review):
        review[0] = True
        self.parent.destroy()


class Clock():
    """klasa zegara"""

    def __init__(self, parent, color, player):
        self.parent = parent
        self.running = False
        self.color = color
        self.job = self.parent.after(1000, self.clock)
        self.end_game = False
        self.first_move = True
        self.player = player
        self.time_end = False
        self.minutes = tkinter.StringVar()
        self.seconds = tkinter.StringVar()
        self.minutes.set("00")
        self.seconds.set("00")
        self.player_name = tkinter.Label(self.parent, font=("Arial",11,""), text = f"Player {self.player+1}", bg = '#212121', fg = 'white')
        self.min_label = tkinter.Label(self.parent, width=3, font=("Arial",18,""), textvariable = self.minutes, bg = '#212121', fg = 'white')
        self.sec_label = tkinter.Label(self.parent, width=3, font=("Arial",18,""), textvariable = self.seconds, bg = '#212121', fg = 'white')
        self.canvas = tkinter.Canvas(self.parent, width = 15, height = 15, bg = '#212121', highlightbackground = '#212121')
        self.widgets()

    def widgets(self):
        if self.color == 'w':
            self.player_name.place(x = 634, y = 50)
            self.sec_label.place(x = 700, y = 20)
            self.min_label.place(x = 600,y = 20)
            self.canvas.place(x = 694, y = 52)
            self.canvas.create_rectangle(0, 15, 15, 0, fill = "white")
        if self.color == 'b':
            self.player_name.place(x = 634, y = 230)
            self.sec_label.place(x = 700, y = 200)
            self.min_label.place(x = 600, y = 200)
            self.canvas.place(x = 694, y = 232)
            self.canvas.create_rectangle(0, 15, 15, 0, fill = "black")

    def set_increment(self, increment):
        self.increment = increment

    def set_clocks(self, time):
        self.max_time = time
        self.minutes.set("{0:02d}".format(time))
        self.total_times = int(self.minutes.get())*60 + int(self.seconds.get())

    def clock(self):
        if self.running == True:
            mins, secs = divmod(self.total_times, 60)
            self.minutes.set("{0:02d}".format(mins))
            self.seconds.set("{0:02d}".format(secs))

            if self.end_game:
                return

            self.job = self.parent.after(1000, self.clock)
            self.parent.update()

            if self.total_times == 0:
                self.running = False
                self.time_end = True

            self.total_times -= 1

    def stop_clock(self):
        self.running = False
        if not self.first_move:
            self.total_times += self.increment + 1
        mins, secs = divmod(self.total_times, 60)
        self.first_move = False

        self.minutes.set("{0:02d}".format(mins))
        self.seconds.set("{0:02d}".format(secs))
        if not self.end_game:
            self.parent.update()

    def start_clock(self):
        self.running = True
        self.clock()

    def reset_clock(self):
        self.minutes.set("00")
        self.seconds.set("00")


class Moves():
    """wizualizacja listy wykonanych ruchów"""

    def __init__(self, parent):
        self.parent = parent
        self.len = 0
        self.frame = tkinter.Frame(self.parent)
        self.frame.place(x=570, y=80)
        self.labels = []
        self.canvas = tkinter.Canvas(self.frame, height = 100, width = 200, bg = '#393d4f', highlightbackground = '#393d4f')
        self.canvas.pack(side= tkinter.LEFT, fill = tkinter.BOTH, expand = 1)
        self.scrollbar = tkinter.Scrollbar(self.frame, orient = tkinter.VERTICAL, command = self.canvas.yview)
        self.scrollbar.pack(side=tkinter.RIGHT, fill = tkinter.Y)
        self.canvas.configure(yscrollcommand = self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda x: self.canvas.configure(scrollregion = self.canvas.bbox('all')))
        self.move_frame = tkinter.Frame(self.canvas, bg = '#393d4f')
        self.canvas.create_window((100, 0), window = self.move_frame)

    def add_move(self, history, color):
        col = 0 if color == 'w' else 1

        if self.len%2==0:
            self.labels.append(tkinter.Label(self.move_frame, width = 10, text = f'{self.len//2+1}. {history[-1].to_string()}', bg = '#393d4f', fg = 'white'))
            self.labels.append(tkinter.Label(self.move_frame, width = 10, text = '', bg = '#393d4f', fg = 'white'))
            self.labels[-2].grid(row = self.len//2, column = 0)
            self.labels[-1].grid(row = self.len//2, column = 1)
        else:
            self.labels.append(tkinter.Label(self.move_frame, width = 10, text = history[-1].to_string(), bg = '#393d4f', fg = 'white'))
            self.labels[-1].grid(row = self.len//2, column = col)   

        self.move_frame.bind("<Configure>", lambda x: self.canvas.configure(scrollregion = self.canvas.bbox('all')))
        self.len+=1

    def clean_history(self):
        for el in self.labels:
            el.destroy()
        self.labels = []
        self.len = 0


class Score:
    """wizualizacja aktualnego wyniku"""

    def __init__(self, parent):
        self.parent = parent
        self.frame = tkinter.Frame(self.parent, bg = '#212121')
        self.frame.place(x = 555, y = 410)
        self.score_label = tkinter.Label(self.frame, width = 5, font=("Arial", 18), text = 'Score', bg = '#212121', fg = 'white')
        self.score_label.grid(row = 0, column = 1)
        self.scores = [tkinter.Label(self.frame, width = 6, font=("Arial",16), text = 'Player 1\n0', bg = '#212121', fg = 'white'), tkinter.Label(self.frame, width = 6, font=("Arial",16), text = 'Player 2\n0', bg = '#212121', fg = 'white')]
        self.scores[0].grid(row = 1, column = 0)
        self.scores[1].grid(row = 1, column = 2)

    def update_scores(self, scores):
        self.scores[0].config(text = 'Player 1\n'+str(scores[0]))
        self.scores[1].config(text = 'Player 2\n'+str(scores[1]))