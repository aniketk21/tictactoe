DIMENSIONS = 3 # dimensions of the playing grid.

class Board(object):

    grid = [[' ' for index in range(DIMENSIONS)] for index in range(DIMENSIONS)]

    def __init__(self, grid=grid, comp='X', human='O'):
        self.comp = comp
        self.human = human
        self.grid = grid
        self.occupied = [] # store occupied positions in the grid as a tuple in this list.

    def display_board(self): # for testing only
        for element in self.grid:
            print element

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

    def minimax(self, player): # to be implemented

    def play_turn(self, x, y, player):
        if player == 'comp':
            self.grid[x][y] = self.comp
            self.occupied.append((x, y))
        else:
            self.grid[x][y] = self.human
            self.occupied.append((x, y))
        return self

    def draw(self): # match is a draw
        for element in self.grid:
            if element == 'X' or element == 'O':
                continue
            else:
                return False
        return True

b =  Board()
b.display_board()
b.play_turn(1, 1,' comp')
b.display_board()
print b.grid
print b.occupied
