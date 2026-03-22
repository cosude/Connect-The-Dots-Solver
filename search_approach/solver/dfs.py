from ..engine import *
from .base import Node, StackFrontier
from .heuristic_and_optimization import is_state_solvable

def DFS(initial_state, callback=None):
    start_node = Node(state=initial_state, parent=None, move=None)
    
    frontier = StackFrontier()
    frontier.add(start_node)

    explored = set()

    while not frontier.is_empty():
        node = frontier.remove()

        if callback:
            callback(node)

        if node.state.Is_Goal():
            return node

        explored.add(node.state)

        for child in node.Expand():
            if child.state.Is_Goal():
                return child
            elif child.state not in explored and not frontier.contains_state(child.state):
                frontier.add(child)

    return None