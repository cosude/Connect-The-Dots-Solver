from .state import State
from .board import Board

def transition(state, move):
    old_board = state.board
    idx = move.index 
    nr, nc = move.new_pos

    new_positions = list(old_board.positions)
    head, goal = new_positions[idx]

    char = old_board.grid[head[0]][head[1]]

    new_positions[idx] = ((nr, nc), goal)
    grid_as_list = list(old_board.grid)
    
    target_row = list(grid_as_list[nr])
    target_row[nc] = char.lower()
    
    grid_as_list[nr] = tuple(target_row)
    new_grid = tuple(grid_as_list)

    return State(Board(old_board.row, old_board.col, new_positions, grid=new_grid))