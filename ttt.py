DIMENSIONS = 3 # dimensions of the playing grid.

class Board(object):

    grid = [[' ' for index in range(DIMENSIONS)] for index in range(DIMENSIONS)]

    def __init__(self, grid=grid, comp='X', human='O'):
        self.comp = comp
        self.human = human
        self.grid = grid
        self.occupied = [] # store occupied positions in the grid as a tuple in this list.
        self.empty_location = ' '

    def display_board(self): # for testing only
        print '    0    1    2'
        i = 0
        for element in self.grid:
            print i, element
            i += 1

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

g =  Board()
g.display_board()
for i in range(3):
    g.move(i % 3, (i + 1) % 3)
    print 'before minimax'
    g.display_board()
    g.minimax('comp')
    print 'after minimax'
    g.display_board()
    
print 'exit', g.display_board()
