from .board import Board

class State:
    def __init__(self, board):
        self.board = board
        self.grid = board.grid
        
    def Is_Goal(self):
        for start, end in self.board.positions:
            if self.board.grid[start[0]][start[1]] != self.board.grid[end[0]][end[1]]:
                return False
        return True
    
    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return self.board.grid == other.board.grid

    def __hash__(self):
        return hash(self.board.grid)