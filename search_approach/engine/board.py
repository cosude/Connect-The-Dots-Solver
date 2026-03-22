class Board:
    def __init__(self, row, col, positions, grid=None):
        self.row = row
        self.col = col
        self.positions = positions
        
        if grid is not None:
            self.grid = tuple(tuple(row) for row in grid)
        else:
            temp_grid = [["" for _ in range(col)] for _ in range(row)]
            char_code = ord('a')

            for group in positions:
                char = chr(char_code)
                start_r, start_c = group[0]
                end_r, end_c = group[1]
                
                temp_grid[start_r][start_c] = char # start dot letter is lowercase 
                temp_grid[end_r][end_c] = char.upper() #end dot letter is uppercase
                char_code += 1
            
            self.grid = tuple(tuple(row) for row in temp_grid)

    def __str__(self):
        return "\n".join(" ".join(cell or "." for cell in row) for row in self.grid)