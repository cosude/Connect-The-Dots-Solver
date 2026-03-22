from .move import Move

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def Generate_Moves(state):
    board = state.board
    best_moves = None
    min_options = 5 

    for idx, (start, end) in enumerate(board.positions):
        if start == end:
            continue
            
        i, j = start
        current_char = board.grid[i][j]
        end_char = current_char.upper()
        
        current_pair_moves = []
        for di, dj in DIRECTIONS:
            ni, nj = i + di, j + dj
            
            if 0 <= ni < board.row and 0 <= nj < board.col: 
                target_cell = board.grid[ni][nj]
                
                if target_cell == "" or target_cell == end_char: 
                    dist = abs(ni - end[0]) + abs(nj - end[1])
                    current_pair_moves.append((dist, Move(index=idx, new_pos=(ni, nj))))

        num_options = len(current_pair_moves)
        if num_options == 0: 
            return []

        if num_options < min_options:
            min_options = num_options 
            
            current_pair_moves.sort(key=lambda x: x[0])
            best_moves = [m[1] for m in current_pair_moves]
            
            if min_options == 1:
                return best_moves

    return best_moves or []