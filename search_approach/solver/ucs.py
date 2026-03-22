from ..engine import *
from .base import Node, Frontier
from .heuristic_and_optimization import is_state_solvable

def UCS(initial_state, callback = None):
    node = Node(initial_state)
    frontier = Frontier()
    frontier.push(node, 0)
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
            state = child.state
            cost = child.path_cost
            if state not in reached or cost < reached[state]:
                reached[state] = cost
                priority = cost
                
                frontier.push(child, priority)

    return None