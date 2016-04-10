from Tkinter import Tk, Button
from tkFont import Font
from copy import deepcopy

DIMENSIONS = 3 # dimensions of the playing grid.

class Board(object):

    def __init__(self, other=None):
        self.comp = 'X'
        self.human = 'O'
        self.grid = [[' ' for index in range(DIMENSIONS)] for index in range(DIMENSIONS)]
        self.occupied = [] # store occupied positions in the grid as a tuple in this list.
        self.empty_location = ' '
        if other:
            self.__dict__ = deepcopy(other.__dict__) # for recursive calls.

    def display_board(self): # for testing only
        print '    0    1    2'
        i = 0
        for element in self.grid:
            print i, element
            i += 1

    def won(self):
        for col in range(DIMENSIONS): # check vertical
            status = []
            for row in range(DIMENSIONS):
                if self.grid[row][col] == self.human:
                    status.append((row, col))
            if len(status) == DIMENSIONS:
                return status
        for row in range(DIMENSIONS): # check horizontal
            status = []
            for col in range(DIMENSIONS):
                if self.grid[row][col] == self.human:
                    status.append((row, col))
            if len(status) == DIMENSIONS:
                return status
        status = []
        for index in range(DIMENSIONS): # check main diagonal
            if self.grid[index][index] == self.human:
                status.append((index, index))
        if len(status) == DIMENSIONS:
            return status
        status = []
        for row in range(DIMENSIONS): # check opposite diagonal
            col = DIMENSIONS - row - 1
            if self.grid[row][col] == self.human:
                status.append((row, col))
        if len(status) == DIMENSIONS:
            return status
        return None # default case
        
    def __minimax(self, current_player):
        if self.won():
            if current_player:
                return (-1, None)
            else:
                return (1, None)
        elif self.draw():
            return (0, None)
        elif current_player:
            best_score = (-2, None)
            for row in range(DIMENSIONS):
                for col in range(DIMENSIONS):
                    if self.grid[row][col] == self.empty_location:
                        score = self.play_turn(row, col).__minimax(not current_player)[0]
                        if score > best_score[0]:
                            best_score = (score, (row, col))
            return best_score
        else:
            best_score = (2, None)
            for row in range(DIMENSIONS):
                for col in range(DIMENSIONS):
                    if self.grid[row][col] == self.empty_location:
                        score = self.play_turn(row, col).__minimax(not current_player)[0]
                        if score < best_score[0]:
                            best_score = (score, (row, col))
            return best_score

    def best_score(self):
        return self.__minimax(True)[1]

    def play_turn(self, row, col):
        board = Board(self)
        board.grid[row][col] = board.comp
        (board.comp, board.human) = (board.human, board.comp)
        return board

    def draw(self): # match is a draw
        for row in range(DIMENSIONS):
            for col in range(DIMENSIONS):
                if self.grid[row][col] == self.empty_location:
                    return False
        return True

class GUI():

    def __init__(self):
        self.app = Tk()
        self.app.title('Tic Tac Toe')
        self.app.resizable(width=False, height=False)
        self.board = Board()
        self.play_area = self.board.grid
        self.font = Font(family="Helvetica", size=32)
        self.buttons = {}
        for row in range(DIMENSIONS):
            for col in range(DIMENSIONS):
	        handler = lambda x=row,y=col: self.move(x, y)
	        button = Button(self.app, command=handler, font=self.font, width=3, height=2)
	        button.grid(row=col, column=row)
                self.buttons[row, col] = button
        handler = lambda: self.reset()
        button = Button(self.app, text='Reset', command=handler)
        button.grid(row=DIMENSIONS+1, column=0, columnspan=DIMENSIONS, sticky="WE")
        self.update()

    def reset(self):
        self.board = Board()
        self.update()

    def move(self, row, col):
        self.app.config(cursor="watch")
        self.app.update()
        self.board = self.board.play_turn(row, col)
        self.update()
        move = self.board.best_score()
        if move:
            self.board = self.board.play_turn(move[0], move[1])
            self.update()
        self.app.config(cursor="")

    def update(self):
        for row in range(DIMENSIONS):
            for col in range(DIMENSIONS):
                text = self.board.grid[row][col]
                self.buttons[row, col]['text'] = text
                self.buttons[row, col]['disabledforeground'] = 'black'
                if text == self.board.empty_location:
                    self.buttons[row, col]['state'] = 'normal'
                else:
                    self.buttons[row, col]['state'] = 'disabled'
        status = self.board.won()
        if status:
            for (row, col) in status:
                self.buttons[row, col]['disabledforeground'] = 'red'
            for row,col in self.buttons:
                self.buttons[row,col]['state'] = 'disabled'
            for row in range(DIMENSIONS):
                for col in range(DIMENSIONS):
                    self.buttons[row,col].update()

    def mainloop(self):
        self.app.mainloop()

if __name__ == '__main__':
    GUI().mainloop()
