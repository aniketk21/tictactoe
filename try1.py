from Tkinter import Tk, Button
from tkFont import Font
from copy import deepcopy

DIMENSIONS = 3 # dimensions of the playing grid.

class Board(object):

    grid = [[' ' for index in range(DIMENSIONS)] for index in range(DIMENSIONS)]


    def __init__(self, grid=grid, comp='X', human='O'):
        self.comp = comp
        self.human = human
        self.grid = grid
        self.occupied = [] # store occupied positions in the grid as a tuple in this list.
        self.empty_location = ' '
	#for col in (DIMENSIONS):
	#	for row in (DIMENSIONS):
	#		self.grid[row][col] = self.empty_location
    #def display_board(self): # for testing only
       # print '    0    1    2'
      #  i = 0
       # for element in self.grid:
        #    print i, element
        #    i += 1

    def won(self, player):
        if player == 'comp':
            for row in range(DIMENSIONS): # check horizontal
                status = []
                for col in range(DIMENSIONS):
                    if self.grid[row][col] == self.comp:
                        status.append((row, col))
                if len(status) == DIMENSIONS:
                    return status
            for col in range(DIMENSIONS): # check vertical
                status = []
                for row in range(DIMENSIONS):
                    if self.grid[row][col] == self.comp:
                        status.append((row, col))
                if len(status) == DIMENSIONS:
                    return status
            for index in range(DIMENSIONS): # check main diagonal
                status = []
                if self.grid[index][index] == self.comp:
                    status.append((index, index))
                if len(status) == DIMENSIONS:
                    return status
            for row in range(DIMENSIONS): # check opposite diagonal
                status = []
                col = DIMENSIONS - row - 1
                if self.grid[row][col] == self.comp:
                    status.append((row, col))
                if len(status) == DIMENSIONS:
                    return status
            return None # default case

        if player == 'human':
            for row in range(DIMENSIONS): # check horizontal
                status = []
                for col in range(DIMENSIONS):
                    if self.grid[row][col] == self.human:
                        status.append((row, col))
                if len(status) == DIMENSIONS:
                    return status
            for col in range(DIMENSIONS): # check vertical
                status = []
                for row in range(DIMENSIONS):
                    if self.grid[row][col] == self.human:
                        status.append((row, col))
                if len(status) == DIMENSIONS:
                    return status
            for index in range(DIMENSIONS): # check main diagonal
                status = []
                if self.grid[index][index] == self.human:
                    status.append((index, index))
                if len(status) == DIMENSIONS:
                    return status
            for row in range(DIMENSIONS): # check opposite diagonal
                status = []
                col = DIMENSIONS - row - 1
                if self.grid[row][col] == self.human:
                    status.append((row, col))
                if len(status) == DIMENSIONS:
                    return status
            return None # default case
        
    def minimax(self, player):
        if self.won(player):
            if player == 'comp':
                return (1, None)
            else:
                return (-1, None)
        elif self.draw():
            return (0, None)
        elif player == 'human':
            best_score = (-2, None)
            for row in range(DIMENSIONS):
                for col in range(DIMENSIONS):
                    if self.grid[row][col] == self.empty_location:
                        score = self.play_turn(row, col, 'comp').minimax(not 'comp')[0]
                        if score > best_score[0]:
                            best_score = (score, (row, col))
            return best_score
        else:
            best_score = (2, None)
            for row in range(DIMENSIONS):
                for col in range(DIMENSIONS):
                    if self.grid[row][col] == self.empty_location:
                        score = self.play_turn(row, col, 'comp').minimax(not 'human')[0]
                        if score < best_score[0]:
                            best_score = (score, (row, col))
            return best_score

    def best_score(self):
    	    return self.minimax(True)[1]

    def play_turn(self, row, col, player):
        if player == 'comp':
            self.grid[row][col] = self.comp
            self.occupied.append((row, col))
        else:
            self.grid[row][col] = self.human
            self.occupied.append((row, col))
        return self

    def draw(self): # match is a draw
        for element in self.grid:
            if element == 'X' or element == 'O':
                continue
            else:
                return False
        return True

#g =  Board()
#g.display_board()
#for i in range(3):
   # g.move(i % 3, (i + 1) % 3)
 #   print 'before minimax'
  #  g.display_board()
   # g.minimax('comp')
    #print 'after minimax'
    #g.display_board()
    
#print 'exit', g.display_board()


class GUI():

  def __init__(self):
    self.app = Tk()
    self.app.title('TicTacToe')
    self.app.resizable(width=False, height=False)
    self.board = Board()
    self.font = Font(family="Helvetica", size=32)
    self.buttons = {}
    for row in range(DIMENSIONS):
        for col in range(DIMENSIONS):
	    handler = lambda x=row,y=col: self.move(x,y)
	    button = Button(self.app, command=handler, font=self.font, width=2, height=1)
	    button.grid(row=col, column=row)
            self.buttons[row,col] = button
    handler = lambda: self.reset()
    button = Button(self.app, text='reset', command=handler)
    button.grid(row=DIMENSIONS+1, column=0, columnspan=DIMENSIONS, sticky="WE")
    self.update()

  def reset(self):
    self.board = Board()
    self.update()

  def move(self,row,col):
    self.app.config(cursor="watch")
    self.app.update()
    self.board = self.board.move(row,col)
    self.update()
    move = self.board.best_score()
    if move: 
      self.board = self.board.move(*move)
      self.update()
    self.app.config(cursor="")

  def update(self):
   for row in range(DIMENSIONS):
     for col in range(DIMENSIONS):
      text = self.grid[row][col]
      self.buttons[row,col]['text'] = text
      self.buttons[row,col]['disabledforeground'] = 'black'
      if text==self.board.empty_location:
        self.buttons[row,col]['state'] = 'normal'
      else:
        self.buttons[row,col]['state'] = 'disabled'
   status = self.board.won()
   if status:
      for row,col in status:
        self.buttons[row,col]['disabledforeground'] = 'red'
      for row,col in self.buttons:
        self.buttons[row,col]['state'] = 'disabled'
      for row in range(DIMENSIONS):
        for col in range(DIMENSIONS):
         self.buttons[row,col].update()

  def mainloop(self):
    self.app.mainloop()

if __name__ == '__main__':
  GUI().mainloop()
