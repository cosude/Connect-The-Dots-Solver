from collections import deque
import copy

class CSP_Solver:
    def __init__(self, board):
        self.board = board
        self.row, self.col = board.row, board.col
        self.grid = board.get_mutable_grid()
        self.colors = [chr(ord('a') + i) for i in range(len(board.positions))]

        self.paths = {color: [] for color in self.colors}

    def solve(self, callback=None):
        grid_copy = copy.deepcopy(self.grid)
        if self.backtrack_color(grid_copy, 0, callback):
            self.grid = grid_copy
            return grid_copy, self.paths 
        return None, None

    def backtrack_color(self, grid, color_idx, callback=None):
        """Recursively extend paths color by color."""
        if color_idx >= len(self.colors):
            return True  

        color = self.colors[color_idx]
        endpoints = [pos for pos, c in self.board.end_dot_map.items() if c.lower() == color]
        start, end = endpoints
        path = [start]

        if self.extend_path(grid, path, end, color, callback):
            self.paths[color] = list(path) 
            if self.backtrack_color(grid, color_idx + 1, callback):
                return True
            self.paths[color] = []
        return False

    def extend_path(self, grid, path, target, color, callback=None):
        """Recursively try to extend the path to reach target."""
        r, c = path[-1]
        if (r, c) == target:
            return True 

        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.row and 0 <= nc < self.col:
                if grid[nr][nc] == "" or (nr, nc) == target:
                    if self.blocks_other_paths(grid, (nr, nc), color):
                        continue
                    grid[nr][nc] = color
                    path.append((nr, nc))

                    if callback:
                        display_paths = {**self.paths, color: list(path)}
                        callback(grid, display_paths)


                    if self.extend_path(grid, path, target, color):
                        return True
                    
                    path.pop()
                    if (nr, nc) != target:
                        grid[nr][nc] = ""
        return False

    def blocks_other_paths(self, grid, cell, current_color):
        """Check if coloring this cell blocks any remaining unassigned color paths."""
        r, c = cell
        for color in self.colors:
            if color == current_color:
                continue
            endpoints = [pos for pos, ch in self.board.end_dot_map.items() if ch.lower() == color]
            if not self.is_reachable(grid, endpoints[0], endpoints[1], blocked={(r,c)}):
                return True
        return False

    def is_reachable(self, grid, start, goal, blocked=set()):
        """BFS to check if a path exists from start to goal through empty cells or the color itself."""
        queue = deque([start])
        visited = set()
        while queue:
            r, c = queue.popleft()
            if (r, c) == goal:
                return True
            visited.add((r, c))
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.row and 0 <= nc < self.col:
                    if (nr, nc) in visited or (nr, nc) in blocked:
                        continue
                    val = grid[nr][nc]
                    if val == "" or val.lower() == grid[start[0]][start[1]].lower():
                        queue.append((nr, nc))
        return False