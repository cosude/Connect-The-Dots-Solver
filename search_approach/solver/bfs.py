from ..engine import *
from .base import Node, Frontier
from .heuristic_and_optimization import is_state_solvable

def BFS(initial_state, callback=None):
    start_node = Node(initial_state, parent=None, move=None)
    frontier = Frontier()
    frontier.push(start_node)
    reached = {initial_state: 0}

    while not frontier.is_empty():
        node = frontier.pop()

        if callback:
            callback(node)

        if node.state.Is_Goal():
            return node
        
        for child in node.Expand():
            if child.state.Is_Goal():
                return child
            elif child.state not in reached:
                reached[child.state] = 0
                frontier.push(child)
    return None