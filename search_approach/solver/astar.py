from ..engine import *
from .base import Node, Frontier
from .heuristic_and_optimization import is_state_solvable, Heuristic

def Astar(initial_state, Heuristic, weight = 3, callback = None):
    node = Node(initial_state)
    frontier = Frontier()
    priority = Heuristic(initial_state)
    frontier.push(node, priority)
    reached = {initial_state: 0}
    
    while not frontier.is_empty():
        node = frontier.pop()

        if callback:
            grid = node.state.grid
            paths = node.get_paths(initial_state.board.positions)
            callback(grid, paths)

        if node.state.Is_Goal():
            return node
        
        for child in node.Expand():
            if not is_state_solvable(child.state): continue
            state = child.state
            cost = child.path_cost
            if state not in reached or cost < reached[state]:
                reached[state] = cost
            
                h_val = Heuristic(state)
                priority = cost + (weight * h_val)
                
                frontier.push(child, priority)

    return None