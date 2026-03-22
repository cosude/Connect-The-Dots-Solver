from ..engine import *
class Node:
    def __init__(self, state, parent=None, move=None, path_cost = 0):
        self.state = state   
        self.parent = parent 
        self.move = move     
        self.path_cost = path_cost
        self.depth = 0 if parent is None else parent.depth + 1

    def __repr__(self):
        return f"Node(depth={self.depth}, move={self.move})"
        
    def Expand(self):
        state = self.state
        for move in Generate_Moves(state):
            newstate = transition(state,move)
            cost = self.path_cost + 1
            yield Node(state=newstate, parent=self, move = move, path_cost=cost)
            
    def get_paths(self, start_positions):
        paths = {}
        for i, (start_pos, end_pos) in enumerate(start_positions):
            color_char = chr(ord('a') + i)
            paths[color_char] = [start_pos]

        curr = self
        while curr:
            if curr.move:
                idx = curr.move.index
                pos = curr.move.new_pos
                color_char = chr(ord('a') + idx)

                paths[color_char].insert(1, pos)
            curr = curr.parent

        for i, (start_pos, end_pos) in enumerate(start_positions):
            char = chr(ord('a') + i)
            tip = paths[char][-1] 
            
            dist = abs(tip[0]-end_pos[0]) + abs(tip[1]-end_pos[1])
            if dist == 1:
                if self.state.board.grid[end_pos[0]][end_pos[1]].lower() == char:
                    paths[char].append(end_pos)
                    
        return paths

import heapq

class Frontier:
    def __init__(self):
        self.elements = []
        self.count = 0

    def is_empty(self):
        return not self.elements

    def push(self, item, priority=0):
        heapq.heappush(self.elements, (priority, self.count, item))
        self.count += 1

    def pop(self):
        return heapq.heappop(self.elements)[2]
    
class StackFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def is_empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.is_empty():
            raise Exception("Empty frontier")
        else:
            return self.frontier.pop()