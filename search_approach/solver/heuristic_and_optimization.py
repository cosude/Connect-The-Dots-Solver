from itertools import combinations

def is_reachable(grid, start, goal, rows, cols):
    """Fast BFS to check if a path exists through empty cells."""
    queue = [start]
    visited = {start}
    while queue:
        r, c = queue.pop(0)
        if (r, c) == goal: return True
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if (nr, nc) not in visited and (grid[nr][nc] == "" or (nr, nc) == goal):
                    visited.add((nr, nc))
                    queue.append((nr, nc))
    return False

def is_state_solvable(state):
    """Checks if every unfinished pair still has a physical path."""
    for idx, (head, goal) in enumerate(state.board.positions):
        if head == goal: continue
        if not is_reachable(state.board.grid, head, goal, state.board.row, state.board.col):
            return False
    return True

def Manhattan(pointA, pointB):
    return abs(pointA[0] - pointB[0]) + abs(pointA[1] - pointB[1])

def Rectangular_Cost_ver1(pairA, pairB):
    cost = 0
    width_cost = 0
    length_cost = 0
    A_mini = min(pairA[0][0], pairA[1][0])
    A_maxi = max(pairA[0][0], pairA[1][0])
    A_minj = min(pairA[0][1], pairA[1][1])
    A_maxj = max(pairA[0][1], pairA[1][1])
    A_width = A_maxi-A_mini
    A_length = A_maxj - A_minj
    B_mini = min(pairB[0][0], pairB[1][0])
    B_maxi = max(pairB[0][0], pairB[1][0])
    B_minj = min(pairB[0][1], pairB[1][1])
    B_maxj = max(pairB[0][1], pairB[1][1])
    B_width = B_maxi-B_mini
    B_length = B_maxj - B_minj
    if not ((A_mini <= B_mini and A_maxi >= B_maxi and A_minj <= B_minj and A_maxj >= B_maxj) or 
            (A_mini >= B_mini and A_maxi <= B_maxi and A_minj >= B_minj and A_maxj <= B_maxj)):
        if A_width != B_width:
            width_cost = abs(A_width - B_width)
        if A_length != B_length:
            length_cost = abs(A_length-B_length)
    cost = min(width_cost, length_cost)
    return cost
def Rectangular_Cost_ver2(pairA, pairB):
    A_r1, A_c1 = pairA[0]
    A_r2, A_c2 = pairA[1]
    B_r1, B_c1 = pairB[0]
    B_r2, B_c2 = pairB[1]
    A_min_r, A_max_r = min(A_r1, A_r2), max(A_r1, A_r2)
    A_min_c, A_max_c = min(A_c1, A_c2), max(A_c1, A_c2)
    B_min_r, B_max_r = min(B_r1, B_r2), max(B_r1, B_r2)
    B_min_c, B_max_c = min(B_c1, B_c2), max(B_c1, B_c2)

    overlap_r = max(0, min(A_max_r, B_max_r) - max(A_min_r, B_min_r) + 1)
    overlap_c = max(0, min(A_max_c, B_max_c) - max(A_min_c, B_min_c) + 1)
    
    overlap_area = overlap_r * overlap_c
    return overlap_area

def Heuristic(state):
    heuristic_value = 0
    for start, end in state.board.positions:
        heuristic_value+=Manhattan(start, end)
    
    for pairA, pairB in combinations(state.board.positions, 2):
        heuristic_value+=Rectangular_Cost_ver1(pairA, pairB)
    return heuristic_value