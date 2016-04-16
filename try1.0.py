from Tkinter import Tk, Button
from tkFont import Font
from copy import deepcopy
import random

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

    def won_easy(self): # won function for easy level.
        for col in range(DIMENSIONS): # check vertical
            status = []
            for row in range(DIMENSIONS):
                if self.grid[row][col] == self.comp:
                    status.append((row, col))
            if len(status) == DIMENSIONS:
                return status
        for row in range(DIMENSIONS): # check horizontal
            status = []
            for col in range(DIMENSIONS):
                if self.grid[row][col] == self.comp:
                    status.append((row, col))
            if len(status) == DIMENSIONS:
                return status
        status = []
        for index in range(DIMENSIONS): # check main diagonal
            if self.grid[index][index] == self.comp:
                status.append((index, index))
        if len(status) == DIMENSIONS:
            return status
        status = []
        for row in range(DIMENSIONS): # check opposite diagonal
            col = DIMENSIONS - row - 1
            if self.grid[row][col] == self.comp:
                status.append((row, col))
        if len(status) == DIMENSIONS:
            return status
        return None # default case
        
    def __minimax_hard(self, current_player):
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
                        score = self.play_turn(row, col).__minimax_hard(not current_player)[0]
                        if score > best_score[0]:
                            best_score = (score, (row, col))
            return best_score
        else:
            best_score = (2, None)
            for row in range(DIMENSIONS):
                for col in range(DIMENSIONS):
                    if self.grid[row][col] == self.empty_location:
                        score = self.play_turn(row, col).__minimax_hard(not current_player)[0]
                        if score < best_score[0]:
                            best_score = (score, (row, col))
            return best_score

    def best_score_hard(self):
        return self.__minimax_hard(True)[1]

    def __minimax_medium(self, current_player, k):
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
                        score = self.play_turn(row, col).__minimax_medium(not current_player, not k)[0]
                        if score > best_score[0]:
                            best_score = (score, (row, col))
            return best_score
        else:
            best_score = (2, None)
            for row in range(DIMENSIONS):
                for col in range(DIMENSIONS):
                    	if self.grid[row][col] == self.empty_location:
				if k == False:
                       			score = self.play_turn(row, col).__minimax_medium(not current_player, k)[0]
                        		if score < best_score[0]:
                            			best_score = (score, (row, col))
				else:
					score = self.play_turn(row, col).__minimax_medium(not current_player, k)[0]
                        		if score > best_score[0]:
                            			best_score = (score, (row, col))
            return best_score

    def best_score_medium(self):
        return self.__minimax_medium(True, True)[1]

    def best_score_easy(self):
        unoccupied = []
        for row in range(DIMENSIONS):
            for col in range(DIMENSIONS):
                if self.grid[row][col] == self.empty_location:
                    unoccupied.append((row, col))
        if unoccupied:
            return random.choice(unoccupied) # return a random location from the unoccupied locations
        return None

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
        self.font = Font(family="Helvetica", size=32)
        self.font1 = Font(family="Times", size = 14) 
        self.buttons = {}
        self.level = 'EASY'
        for row in range(DIMENSIONS):
            for col in range(DIMENSIONS):
	        handler = lambda x=row,y=col: self.move(x, y, 'EASY')
	        button_T = Button(self.app, command=handler, font=self.font, width=3, height=2, bd = 3)
	        button_T.grid(row=col, column=row)
                self.buttons[row, col] = button_T
        
        self.which_level()
        self.update()
    
    def which_level(self):
        handler_E = lambda: self.reset('EASY')
        button_E = Button(self.app, text='EASY', command=handler_E, bg = "cyan", foreground="green", font = self.font1, bd = 4)
        button_E.grid(row=DIMENSIONS+1, column=0, columnspan=1, sticky="WE")

        handler_M = lambda: self.reset('MEDIUM')        
        button_M = Button(self.app, text='MEDIUM', command=handler_M, bg = "cyan", foreground = "blue", font = self.font1, bd = 4)
        button_M.grid(row=DIMENSIONS+1, column=1, columnspan=1, sticky="WE")
        
        handler_H = lambda: self.reset('HARD')
        button_H = Button(self.app, text='HARD', command=handler_H, bg = "cyan", foreground = "red", font = self.font1, bd = 4)
        button_H.grid(row=DIMENSIONS+1, column=2, columnspan=1, sticky="WE")

    def reset(self, level):
        self.board = Board()
        for button in self.app.grid_slaves():
            button.grid_forget()
        self.wh(level)
        self.which_level()
        self.update()

    def wh(self, level):
        for row in range(DIMENSIONS):
            for col in range(DIMENSIONS):
                if level == 'HARD':
                    handler = lambda x=row,y=col: self.move(x, y, 'HARD')
                    self.level = 'HARD'
                elif level == 'EASY':
                    handler = lambda x=row,y=col: self.move(x, y, 'EASY')
                    self.level = 'EASY'
                elif level == 'MEDIUM':
                    handler = lambda x=row,y=col: self.move(x, y, 'MEDIUM')
                    self.level = 'MEDIUM'
                button_T = Button(self.app, command=handler, font=self.font, width=3, height=2, bd = 3)
                button_T.grid(row=col, column=row)
                self.buttons[row, col] = button_T

    def move(self, row, col, level):
        self.app.config(cursor="watch")
        self.app.update()
        self.board = self.board.play_turn(row, col)
        self.update()
        if level == 'HARD':
            move = self.board.best_score_hard()
        elif level == 'EASY':
            move = self.board.best_score_easy()
        elif level == 'MEDIUM':
            move = self.board.best_score_medium()
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
        if self.level == 'EASY':
            status = self.board.won_easy()
            if not status:
                status = self.board.won()
        if status:
            for (row, col) in status:
                self.buttons[row, col]['disabledforeground'] = 'red'
            for (row, col) in self.buttons:
                self.buttons[row, col]['state'] = 'disabled'
            for row in range(DIMENSIONS):
                for col in range(DIMENSIONS):
                    self.buttons[col, row].update()

    def mainloop(self):
        self.app.mainloop()

if __name__ == '__main__':
    GUI().mainloop()
