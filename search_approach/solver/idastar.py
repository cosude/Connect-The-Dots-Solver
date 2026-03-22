from ..engine import *
from .base import Node, Frontier
from .heuristic_and_optimization import is_state_solvable

def IDAstar(initial_state, Heuristic, weight=3.0, callback=None):
    threshold = Heuristic(initial_state)
    root = Node(initial_state)
    while True:
        result, min_exceeded = search(root, threshold, Heuristic, weight, callback)
        
        if result is not None:
            return result
        
        if min_exceeded == float('inf'):
            return None
    
        threshold = min_exceeded
        

def search(node, threshold, Heuristic, weight, callback):
    if callback:
        grid = node.state.grid
        paths = node.get_paths(node.state.board.positions)
        callback(grid, paths)
    
    h_val = Heuristic(node.state)
    f_val = node.path_cost + (weight * h_val)
    
    if f_val > threshold:
        return None, f_val
    
    if node.state.Is_Goal():
        return node, threshold
    
    min_exceeded = float('inf')
    
    for child in node.Expand():
        if not is_state_solvable(child.state): continue

        res, t = search(child, threshold, Heuristic, weight, callback)
        
        if res is not None:
            return res, threshold
        
        if t < min_exceeded:
            min_exceeded = t
            
    return None, min_exceeded