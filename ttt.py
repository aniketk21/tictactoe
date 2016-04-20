'''
    Tic Tac Toe game, written in Python.
    Copyright (C) 2016   Aniket Kulkarni    kaniket21@gmail.com
    Copyright (C) 2016   Rohan Patil        rohanrahulpatil89@gmail.com
    Copyright (C) 2016   Sumedh Kale        sumedh_kale@yahoo.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import random
from copy import deepcopy

try:
    from Tkinter import Tk, Button
    from tkFont import Font
except:
    print '------------------------------------------------'
    print 'Tkinter package is not installed on your system'
    print 'and is required.'
    print 'Install it using: sudo apt-get install python-tk'
    print '------------------------------------------------'

DIMENSIONS = 3 # dimensions of the playing grid.

class Board(object):

    def __init__(self, other=None):
        '''
        grid: 2D array of size (DIMENSIONS * DIMENSIONS)
        '''
        self.comp = 'X'
        self.human = 'O'
        self.grid = [[' ' for index in range(DIMENSIONS)] for index in range(DIMENSIONS)]
        # store occupied positions in the grid as a tuple in this list.
        self.occupied = []
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
        '''
        inputs: None

        This function checks if the human is winning in any row, column or any
        of the two diagonals. If such a combination of locations is found, it
        is returned as a list of 3 tuples.

        returns: `status`, a list of tuples of locations in the grid.
        '''
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

    def won_easy(self):
        '''
        input: None

        This function checks if the comp is winning in any row, column or any
        of the two diagonals. If such a combination of locations is found, it
        is returned as a list of 3 tuples. This function is used only for the
        easy level.

        returns: `status`, a list of tuples of locations in the grid.
        '''
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
        '''
        input: `current_player`, the player who's playing currently. This
               parameter is either True or False.

        This is the minimax function for the undefeatable level.
        If the current player is winning, -1 is returned. Else, +1 is returned.
        If the match is a draw, 0 is returned.
        Else, this function is called recursively depending on the current
        player on all the empty locations.

        returns: a tuple, (score, location)
        '''
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
        '''
        input: None

        This function initiates the call to `__minimax_hard`.
        
        returns: a tuple of (row, col), the position where `comp` will
        play next.
        '''
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
        '''
        input: None

        This function initiates the call to `__minimax_medium`.
        
        returns: a tuple of (row, col), the position where `comp` will
        play next.
        '''
        return self.__minimax_medium(True, True)[1]

    def best_score_easy(self):
        '''
        input: None

        This function appends all the empty locations to `unoccupied`
        and then returns a random location from this list.

        returns: a tuple of (row, col)
        '''
        unoccupied = []
        for row in range(DIMENSIONS):
            for col in range(DIMENSIONS):
                if self.grid[row][col] == self.empty_location:
                    unoccupied.append((row, col))
        if unoccupied:
            # return a random location from the unoccupied locations
            return random.choice(unoccupied)
        return None

    def play_turn(self, row, col):
        '''
        inputs: `row` and `col`, the location to place an 'X' or an 'O'.

        This function constructs its own `Board`. Then it places a symbol at
        `row`, `col`. Then `comp` and `human` are swapped, as it is a
        two-player game.

        returns: `board`, with a symbol placed at `row`, `col`
        '''
        board = Board(self)
        board.grid[row][col] = board.comp
        (board.comp, board.human) = (board.human, board.comp)
        return board

    def draw(self):
        '''
        input: None

        This function checks if there is no empty location on the board and
        returns True if this condition is met.

        returns: True or False, depending on whether the board is full or not.
        '''
        for row in range(DIMENSIONS):
            for col in range(DIMENSIONS):
                if self.grid[row][col] == self.empty_location:
                    return False
        return True


class GUI(object):

    def __init__(self):
        '''
        constructor of `class GUI`.
        The default level is 'EASY'.
        '''
        self.app = Tk()
        self.app.title('Tic Tac Toe')
        self.app.resizable(width=False, height=False)
        self.board = Board()
        self.font = Font(family="Helvetica", size=32)
        self.font_levels = Font(family="Times", size=14) 
        self.buttons = {}
        self.level = 'EASY'
        for row in range(DIMENSIONS):
            for col in range(DIMENSIONS):
	        handler = lambda x=row, y=col: self.move(x, y, 'EASY')
	        button_T = Button(self.app, command=handler,
                                  font=self.font, width=3,
                                  height=2, bd=3)
	        button_T.grid(row=col, column=row)
                self.buttons[row, col] = button_T
        self.which_level()
        self.update()
    
    def which_level(self):
        '''
        #FF6103: cadmiumorange
        #00CD00: green3
        #EE0000: red2
        '''
        handler_E = lambda: self.reset('EASY')
        button_E = Button(self.app, text="EASY", command=handler_E,
                          bg="#00CD00", foreground="white",
                          font=self.font_levels, bd=4)
        button_E.grid(row=DIMENSIONS+1, column=0,
                      columnspan=1, sticky="WE")

        handler_M = lambda: self.reset('MEDIUM')        
        button_M = Button(self.app, text="MEDIUM", command=handler_M,
                          bg="#FF6103", foreground="white",
                          font=self.font_levels, bd=4)
        button_M.grid(row=DIMENSIONS+1, column=1,
                      columnspan=1, sticky="WE")
        
        handler_H = lambda: self.reset('HARD')
        button_H = Button(self.app, text="HARD", command=handler_H,
                          bg="#EE0000", foreground="white",
                          font=self.font_levels, bd=4)
        button_H.grid(row=DIMENSIONS+1, column=2,
                      columnspan=1, sticky="WE")

    def reset(self, level):
        '''
        This function resets the `board` after any level is selected.
        A new instance of `Board()` is created, all the buttons are cleared
        and then new buttons are created.
        '''
        self.board = Board()
        for button in self.app.grid_slaves():
            button.grid_forget()
        self.create_buttons(level)
        self.which_level()
        self.update()

    def create_buttons(self, level):
        '''
        This functions creates buttons according to the selected level.
        '''
        for row in range(DIMENSIONS):
            for col in range(DIMENSIONS):
                if level == 'HARD':
                    handler = lambda x=row, y=col: self.move(x, y, 'HARD')
                    self.level = 'HARD'
                elif level == 'EASY':
                    handler = lambda x=row, y=col: self.move(x, y, 'EASY')
                    self.level = 'EASY'
                elif level == 'MEDIUM':
                    handler = lambda x=row, y=col: self.move(x, y, 'MEDIUM')
                    self.level = 'MEDIUM'
                button_T = Button(self.app, command=handler,
                                  font=self.font, width=3,
                                  height=2, bd=3)
                button_T.grid(row=col, column=row)
                self.buttons[row, col] = button_T

    def move(self, row, col, level):
        '''
        inputs: `row`, `col`, `level`, where the turn is to be played.

        This function calls the `best_score` of a specific level depending
        on the level selected and location on which user plays a turn.
        '''
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
        '''
        input: None

        This function updates the board.
        #FF0000: red1
        '''
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
                self.buttons[row, col]['disabledforeground'] = '#FF0000'
            for (row, col) in self.buttons:
                self.buttons[row, col]['state'] = 'disabled'
            for row in range(DIMENSIONS):
                for col in range(DIMENSIONS):
                    self.buttons[col, row].update()

    def mainloop(self):
        self.app.mainloop()

if __name__ == '__main__':
    GUI().mainloop()
