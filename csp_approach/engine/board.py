class Board:
    def __init__(self, row, col, positions, grid=None):
        self.row = row
        self.col = col
        self.positions = positions
        self.end_dot_map = {}
        for idx, (p1, p2) in enumerate(positions):
            color = chr(ord('a') + idx)
            self.end_dot_map[p1] = color
            self.end_dot_map[p2] = color
        self.neighbors_cache = {}
        for r in range(row):
            for c in range(col):
                neighbors = []
                for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nr, nc = r+dr, c+dc
                    if 0<=nr<row and 0<=nc<col:
                        neighbors.append((nr,nc))
                self.neighbors_cache[(r,c)] = neighbors

        if grid is not None:
            self.grid = [list(row) for row in grid]
        else:
            self.grid = [["" for _ in range(col)] for _ in range(row)]
            for (r1,c1),(r2,c2) in positions:
                color = self.end_dot_map[(r1,c1)]
                self.grid[r1][c1] = color
                self.grid[r2][c2] = color.upper()

    def get_mutable_grid(self):
        return [row[:] for row in self.grid]

